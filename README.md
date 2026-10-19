# AI Tech Consultant

An AI-powered capstone prototype that connects product knowledge, customer email drafting, and meeting-to-scope generation through API-driven workflows.

## Overview

AI Tech Consultant brings three focused services together around a shared Knowledge Brain. It demonstrates how grounded product information can support customer communication and project planning, while keeping important decisions subject to human review.

## Core Features

### 1. Knowledge Brain — Python, FastAPI
- Ingests public help-center content through a capped sitemap crawler.
- Stores documents in SQLite and retrieves relevant content using lexical search.
- Returns answers with cited excerpts and supports abstention/escalation for unanswered questions.
- Stores reviewed expert answers for future use.

### 2. Inbox Agent — TypeScript, Express
- Classifies email intent and risk.
- Calls the Knowledge Brain API to ground customer reply drafts in product information.
- Tracks review status and feedback streaks.
- Email delivery is not implemented; sending remains disabled in this demo.

### 3. Meeting-to-Scope — Python, FastAPI
- Extracts requirements from client meeting transcripts.
- Checks product fit through the Knowledge Brain HTTP API.
- Produces development task lists, effort estimate ranges, and proposal drafts.
- Saves a baseline and compares follow-up requirements with the original scope.

## Architecture

```text
                         Dashboard
                             |
             +---------------+----------------+
             |               |                |
             v               v                v
       Knowledge Brain   Inbox Agent   Meeting-to-Scope
       Python/FastAPI   TypeScript/Express  Python/FastAPI
             ^               |                |
             +---------------+----------------+
                  Shared Knowledge Brain API
```

The Knowledge Brain is the shared source of product information. The Inbox Agent calls it when drafting replies, and Meeting-to-Scope calls it when checking existing product capabilities. Each service has a distinct responsibility and can be tested independently.

## Technology Stack

- **Languages:** Python, TypeScript, JavaScript
- **Backend:** FastAPI, Express, Node.js
- **Data storage:** SQLite
- **Integration:** REST APIs, HTTP
- **Frontend:** HTML, CSS, JavaScript
- **Local orchestration:** Docker Compose
- **Version control:** Git and GitHub

## Run Locally

**Requirements:** Docker and Docker Compose.

```bash
git clone https://github.com/vamshivardhan22/Ai-Tech-consultant.git
cd Ai-Tech-consultant
cp .env.example .env
# Optional: edit .env and add your Anthropic API key.
docker compose up --build
```

Open the dashboard at **http://localhost:8080**.

### Service endpoints

- Knowledge Brain API docs: http://localhost:8001/docs
- Inbox Agent health check: http://localhost:8002/health
- Meeting-to-Scope API docs: http://localhost:8003/docs

Without `ANTHROPIC_API_KEY`, some workflows use deterministic fallbacks. These fallbacks help verify service wiring but do not count as Claude model evaluations. To ingest public help-center pages, open the Knowledge Brain Swagger page and call `POST /v1/ingest`. Crawling is capped per request; start with a small batch and inspect the results.

## Engineering Principles

- **Grounded responses:** Use retrieved product documentation and expose cited excerpts.
- **Human oversight:** Keep customer communication and scope decisions reviewable.
- **Modular design:** Separate services and integrate them through explicit API boundaries.
- **Traceability:** Structure requirements, estimates, and scope changes for review.
- **Testability:** Verify components and service integration independently.

## Current Limitations

This is an initial demo scaffold, not a production-ready system. The current Knowledge Brain does not implement vector embeddings, a vector database, screenshot vision, daily scheduled synchronization, or complete removal reconciliation. A real mailbox adapter is not implemented. Model outputs and fallback estimates require human review. The frontend is a local demo interface without login or role permissions.

Sixty acceptance/regression cases are listed in `evals/cases.json`; they have not been executed as a model evaluation in this repository session. See [DESIGN.md](DESIGN.md) and [EVALS.md](EVALS.md) for design details and evaluation plans.

## Security Notes

Never commit `.env`, API keys, mailbox tokens, or customer data. Do not expose these services publicly without authentication, authorization, rate limiting, monitoring, backup/recovery, and a production CORS/CSRF review.

## Verification Checklist

- [ ] Start successfully with `docker compose up --build` from a clean checkout.
- [ ] Verify health and API responses from all three services.
- [ ] Test both an answerable and an unknown knowledge question.
- [ ] Confirm the email draft flow calls the Knowledge Brain; sending remains disabled.
- [ ] Verify feedback streak behavior and persistence across restart.
- [ ] Test meeting scope generation and follow-up comparison with human review.
- [ ] Run model evaluations with two Claude candidates and record actual quality, cost, and latency.
- [ ] Record three role-play meeting transcripts, including a follow-up.
- [ ] Complete the demo video and AI coding-tool log.

Do not mark checklist items complete until verified.

## Repository

[GitHub: vamshivardhan22/Ai-Tech-consultant](https://github.com/vamshivardhan22/Ai-Tech-consultant)
