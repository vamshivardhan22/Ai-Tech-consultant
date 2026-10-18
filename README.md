# AI Tech Consultant

A capstone prototype with three connected workflows: product knowledge, customer email drafting, and meeting-to-scope generation.

## Run locally

Requirements: Docker and Docker Compose.

```bash
cp .env.example .env
# Optional: edit .env and add your Anthropic API key.
docker compose up --build
```

Open the dashboard at **http://localhost:8080**.

API documentation:
- Knowledge Brain: http://localhost:8001/docs
- Inbox Agent: http://localhost:8002/health
- Meeting-to-Scope: http://localhost:8003/docs

Without `ANTHROPIC_API_KEY`, some workflows use deterministic fallbacks. The fallback paths are useful for checking service wiring but do not count as Claude model evaluations. To ingest public help-center pages, use the Knowledge Brain Swagger page and send `POST /v1/ingest`. The crawler is capped per request; run a small batch first and inspect results.

## What it does

1. **Knowledge Brain (Python/FastAPI)** — SQLite document store, capped polite sitemap ingestion, lexical retrieval, cited excerpts, explicit abstention/escalation, and reviewed expert-answer storage.
2. **Inbox Agent (TypeScript/Express)** — intent/risk classification, Knowledge Brain API call, draft response, review status, and persistent feedback-streak ledger. It does not send email.
3. **Meeting-to-Scope (Python/FastAPI)** — transcript requirement extraction, product-fit lookup through Task 1's HTTP API, task estimate ranges, proposal draft, saved baseline and follow-up comparison.

## Current limitations

This is an initial demo scaffold, not a production-ready system. The current Knowledge Brain does not implement vector embeddings, a vector database, screenshot vision, daily scheduled sync, or complete removal reconciliation. The real mailbox adapter is not implemented. Model outputs and fallback estimates need human review. The frontend is a local demo interface without login or role permissions.

Sixty acceptance/regression cases are listed in `evals/cases.json`; they have not been executed as a model evaluation in this repository session. See `DESIGN.md` and `EVALS.md` for details.

## Configuration and safety

Never commit `.env`, API keys, mailbox tokens, or customer data. The local dashboard is allowed to call the APIs from `http://localhost:8080`. Do not expose these services publicly without authentication, authorization, rate limiting, monitoring, backup/recovery, and a production CORS/CSRF review.

## Verification checklist

- [ ] `docker compose up --build` completes successfully on a clean checkout.
- [ ] All three services return healthy responses.
- [ ] A supported and an unknown knowledge question are tested.
- [ ] Email draft flow calls the Knowledge Brain; send remains disabled.
- [ ] Feedback streak increments/resets and persists across restart.
- [ ] Meeting scope and follow-up comparison both require human approval.
- [ ] Model evals were run with two Claude candidates and actual quality/cost/latency were recorded.
- [ ] Three real role-play meeting transcripts were recorded, including a follow-up.
- [ ] Demo video and AI coding-tool log are complete.

Do not mark items complete until verified.
