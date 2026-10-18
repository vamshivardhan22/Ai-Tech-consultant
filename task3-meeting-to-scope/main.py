"""Meeting-to-Scope API with explicit agent handoffs and human approval boundary."""
from __future__ import annotations

import json
import os
import re
import sqlite3
from contextlib import closing
from typing import Any
from uuid import uuid4

import httpx
from anthropic import AsyncAnthropic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
KB_URL = os.getenv("KNOWLEDGE_BRAIN_URL", "http://localhost:8001")
DB_PATH = os.getenv("MEETING_DB_PATH", "/data/meetings.db")
app = FastAPI(title="AI Tech Consultant — Meeting to Scope", version="0.1.0")


def db() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


@app.on_event("startup")
async def startup() -> None:
    with closing(db()) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS baselines(
          id TEXT PRIMARY KEY, client_name TEXT NOT NULL, transcript TEXT NOT NULL,
          scope_json TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")
        con.commit()


class MeetingRequest(BaseModel):
    client_name: str = Field(min_length=1, max_length=200)
    transcript: str = Field(min_length=20, max_length=150000)
    hourly_rate: float | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, min_length=3, max_length=8)
    baseline_id: str | None = None


class MeetingOutput(BaseModel):
    baseline_id: str
    requirements: list[dict[str, Any]]
    product_fit: list[dict[str, Any]]
    tasks: list[dict[str, Any]]
    scope_of_work: dict[str, Any]
    proposal: dict[str, Any]
    approval_required: bool = True
    model: str
    warnings: list[str] = Field(default_factory=list)


class CompareRequest(BaseModel):
    baseline_id: str
    followup_transcript: str = Field(min_length=10, max_length=150000)


async def call_claude_json(system: str, prompt: str) -> Any | None:
    if not API_KEY:
        return None
    try:
        client = AsyncAnthropic(api_key=API_KEY)
        message = await client.messages.create(
            model=MODEL, max_tokens=1800, temperature=0,
            system=system + " Return valid JSON only. Do not invent transcript facts, rates, or commitments.",
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(block.text for block in message.content if getattr(block, "type", "") == "text").strip()
        text = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text, flags=re.I)
        return json.loads(text)
    except Exception:
        return None


def fallback_requirements(transcript: str) -> list[dict[str, Any]]:
    # Each extracted item retains its original sentence as traceable evidence.
    chunks = [re.sub(r"\s+", " ", x).strip(" -\t") for x in re.split(r"(?<=[.!?])\s+|\n+", transcript)]
    chunks = [x for x in chunks if len(x) >= 18]
    return [
        {"id": f"REQ-{i:03d}", "text": sentence[:500], "evidence": sentence[:700],
         "status": "needs_review", "confidence": "low", "source": "transcript"}
        for i, sentence in enumerate(chunks[:40], 1)
    ]


async def requirements_agent(transcript: str) -> tuple[list[dict[str, Any]], str]:
    result = await call_claude_json(
        "You are the requirements analyst agent. Extract only explicit or clearly implied client requirements. Attach a verbatim evidence excerpt to every item. Return {requirements:[{text,evidence,acceptance_criteria,open_questions,priority}]}",
        f"MEETING TRANSCRIPT:\n{transcript}\nExtract requirements. Keep ambiguous requests as open questions."
    )
    if isinstance(result, dict) and isinstance(result.get("requirements"), list):
        output = []
        for i, item in enumerate(result["requirements"][:40], 1):
            if not isinstance(item, dict) or not item.get("text"):
                continue
            output.append({"id": f"REQ-{i:03d}", "text": str(item["text"])[:500],
                "evidence": str(item.get("evidence", ""))[:700],
                "acceptance_criteria": item.get("acceptance_criteria", []),
                "open_questions": item.get("open_questions", []),
                "priority": item.get("priority", "unconfirmed"), "status": "needs_review"})
        if output:
            return output, MODEL
    return fallback_requirements(transcript), "deterministic-fallback"


async def knowledge_check(requirement: dict[str, Any]) -> dict[str, Any]:
    question = f"Does the product documentation describe a built-in setting or feature that could satisfy this client request? Request: {requirement['text']}"
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.post(f"{KB_URL}/v1/answers", json={"question": question, "top_k": 3})
            response.raise_for_status()
            data = response.json()
            return {"requirement_id": requirement["id"], "question": question,
                "answer": data.get("answer", ""), "citations": data.get("citations", []),
                "abstained": data.get("abstained", True),
                "recommendation": "human_check_product_fit" if not data.get("abstained", True) else "unknown_needs_clarification"}
    except Exception as exc:
        return {"requirement_id": requirement["id"], "question": question,
            "answer": "", "citations": [], "abstained": True,
            "recommendation": "knowledge_api_unavailable", "error": type(exc).__name__}


async def estimator_agent(requirements: list[dict[str, Any]], fit: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], str]:
    prompt_data = {"requirements": requirements, "product_fit_checks": fit}
    result = await call_claude_json(
        "You are a software estimation agent. Estimate implementation work as ranges, identify assumptions/dependencies/risks, and do not treat unknown product-fit as confirmed. Return {tasks:[{requirement_id,title,hours_min,hours_max,rationale,dependencies,assumptions}]}",
        json.dumps(prompt_data, ensure_ascii=False)
    )
    if isinstance(result, dict) and isinstance(result.get("tasks"), list):
        clean = []
        for task in result["tasks"][:60]:
            if not isinstance(task, dict) or not task.get("title"):
                continue
            clean.append({
                "requirement_id": str(task.get("requirement_id", "")),
                "title": str(task["title"])[:300],
                "hours_min": max(1, int(task.get("hours_min", 2))),
                "hours_max": max(max(1, int(task.get("hours_min", 2))), int(task.get("hours_max", 6))),
                "rationale": str(task.get("rationale", "Model-generated estimate; requires developer review."))[:700],
                "dependencies": task.get("dependencies", []),
                "assumptions": task.get("assumptions", []),
                "estimate_status": "model_estimate_needs_human_review"
            })
        if clean:
            return clean, MODEL
    tasks = []
    for requirement in requirements:
        tasks.append({"requirement_id": requirement["id"], "title": requirement["text"][:120],
            "hours_min": 2, "hours_max": 8,
            "rationale": "Default placeholder range because no validated estimation model result was available.",
            "dependencies": [], "assumptions": ["Confirm requirement and product fit with a developer."],
            "estimate_status": "placeholder_not_quote"})
    return tasks, "deterministic-fallback"


async def proposal_agent(client_name: str, requirements: list[dict[str, Any]], tasks: list[dict[str, Any]], hourly_rate: float | None, currency: str | None) -> tuple[dict[str, Any], dict[str, Any], str]:
    data = {"client_name": client_name, "requirements": requirements, "tasks": tasks,
            "rate_provided": hourly_rate is not None and currency is not None}
    result = await call_claude_json(
        "You are a senior consultant and proposal writer. Return JSON with scope_of_work {goals,deliverables,in_scope,out_of_scope,acceptance_criteria,assumptions,open_questions} and proposal {title,summary,approach,timeline_assumptions,commercials,approval_notes}. Never invent rates, prices, dates, or guarantees.",
        json.dumps(data, ensure_ascii=False)
    )
    if isinstance(result, dict) and isinstance(result.get("scope_of_work"), dict) and isinstance(result.get("proposal"), dict):
        scope, proposal = result["scope_of_work"], result["proposal"]
        model = MODEL
    else:
        scope = {
            "goals": [r["text"] for r in requirements[:10]],
            "deliverables": [t["title"] for t in tasks],
            "in_scope": [r["text"] for r in requirements],
            "out_of_scope": ["Items not stated in the transcript or separately approved change requests."],
            "acceptance_criteria": [c for r in requirements for c in (r.get("acceptance_criteria") or [])],
            "assumptions": ["Requirements and estimates require human review."],
            "open_questions": [q for r in requirements for q in (r.get("open_questions") or [])]
        }
        total_min = sum(t["hours_min"] for t in tasks)
        total_max = sum(t["hours_max"] for t in tasks)
        commercials: dict[str, Any] = {"estimated_hours": {"min": total_min, "max": total_max},
            "price": "Rate required; no price generated."}
        if hourly_rate is not None and currency:
            commercials["indicative_price_range"] = {"min": round(total_min*hourly_rate, 2), "max": round(total_max*hourly_rate, 2), "currency": currency,
                "note": "Arithmetic estimate only; requires human approval."}
        proposal = {"title": f"Proposal: {client_name}", "summary": "Draft proposal based on the supplied meeting transcript.",
            "approach": "Confirm requirements and product fit, agree the scope, implement in reviewed increments, and validate acceptance criteria.",
            "timeline_assumptions": ["Schedule to be agreed after technical review."], "commercials": commercials,
            "approval_notes": ["Human approval required before client delivery.", "Estimates are indicative and not a binding quote."]}
        model = "deterministic-fallback"
    # Attach commercial arithmetic based on supplied rate only; never infer a rate.
    total_min = sum(t["hours_min"] for t in tasks)
    total_max = sum(t["hours_max"] for t in tasks)
    proposal.setdefault("commercials", {})
    proposal["commercials"].setdefault("estimated_hours", {"min": total_min, "max": total_max})
    if hourly_rate is None or not currency:
        proposal["commercials"]["price"] = "Rate required; no price generated."
    return scope, proposal, model


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "meeting-to-scope"}


@app.post("/v1/meetings/process", response_model=MeetingOutput)
async def process_meeting(request: MeetingRequest) -> MeetingOutput:
    warnings: list[str] = []
    requirements, requirements_model = await requirements_agent(request.transcript)
    if not requirements:
        warnings.append("No clear requirements could be extracted. Add transcript detail and retry.")
    # Product-fit check always calls the Knowledge Brain API; results are not treated as a verdict.
    fit: list[dict[str, Any]] = []
    for requirement in requirements[:20]:
        fit.append(await knowledge_check(requirement))
    tasks, estimator_model = await estimator_agent(requirements, fit)
    scope, proposal, proposal_model = await proposal_agent(request.client_name, requirements, tasks,
        request.hourly_rate, request.currency)
    baseline_id = request.baseline_id or str(uuid4())
    with closing(db()) as con:
        con.execute("INSERT OR REPLACE INTO baselines(id,client_name,transcript,scope_json) VALUES(?,?,?,?)",
                    (baseline_id, request.client_name, request.transcript, json.dumps(scope, ensure_ascii=False)))
        con.commit()
    if any(item["recommendation"] == "knowledge_api_unavailable" for item in fit):
        warnings.append("Knowledge Brain was unavailable for one or more product-fit checks.")
    if not API_KEY:
        warnings.append("ANTHROPIC_API_KEY is not configured; deterministic fallbacks were used. This is not a Claude model evaluation.")
    if requirements_model == "deterministic-fallback" or estimator_model == "deterministic-fallback" or proposal_model == "deterministic-fallback":
        warnings.append("One or more agent stages used a fallback. Review all generated content before use.")
    return MeetingOutput(baseline_id=baseline_id, requirements=requirements, product_fit=fit,
        tasks=tasks, scope_of_work=scope, proposal=proposal, approval_required=True,
        model=f"requirements:{requirements_model};estimator:{estimator_model};proposal:{proposal_model}",
        warnings=warnings)


@app.post("/v1/meetings/compare")
async def compare_followup(request: CompareRequest) -> dict[str, Any]:
    with closing(db()) as con:
        row = con.execute("SELECT scope_json,transcript,client_name FROM baselines WHERE id=?", (request.baseline_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Baseline not found. Process an initial meeting first.")
    baseline = json.loads(row["scope_json"])
    result = await call_claude_json(
        "You are a scope change analyst. Compare the previously approved baseline with follow-up transcript evidence. Only mark changes supported by the new transcript. Return {added:[...], changed:[...], removed:[...], unchanged:[...], potential_out_of_scope:[...], questions:[...]}.",
        json.dumps({"baseline_scope": baseline, "followup_transcript": request.followup_transcript}, ensure_ascii=False)
    )
    if not isinstance(result, dict):
        # Honest fallback: surface follow-up statements for a human, without pretending semantic diff is complete.
        sentences = [re.sub(r"\s+", " ", s).strip() for s in re.split(r"(?<=[.!?])\s+|\n+", request.followup_transcript)]
        sentences = [s for s in sentences if len(s) > 15]
        result = {"added": [], "changed": [], "removed": [], "unchanged": [],
            "potential_out_of_scope": [{"text": s, "reason": "Unclassified follow-up statement; human scope comparison required."} for s in sentences[:25]],
            "questions": ["Automated semantic comparison was unavailable; review the follow-up against the baseline manually."]}
    return {"baseline_id": request.baseline_id, "client_name": row["client_name"], "changes": result,
        "approval_required": True, "model": MODEL if API_KEY else "deterministic-fallback",
        "note": "This comparison is a draft for human review; it does not modify the stored baseline."}


@app.get("/v1/meetings/baselines")
async def list_baselines() -> dict[str, Any]:
    with closing(db()) as con:
        rows = con.execute("SELECT id,client_name,created_at FROM baselines ORDER BY created_at DESC LIMIT 100").fetchall()
    return {"baselines": [dict(row) for row in rows]}
