# AI Tech Consultant

AI Tech Consultant is a modular prototype that connects product knowledge, customer email drafting, and meeting-to-scope planning. Three services share a Knowledge Brain so that reply drafts and scope recommendations can use the same product information.

## Features

### Knowledge Brain
- Ingests public help-center pages through a capped sitemap crawler.
- Stores content in SQLite and retrieves relevant passages with lexical search.
- Returns answers with supporting excerpts and can indicate when the available information is insufficient.
- Stores reviewed expert answers for later use.

### Inbox Agent
- Classifies email intent and risk.
- Uses the Knowledge Brain API to ground customer reply drafts in product documentation.
- Tracks review status and feedback.
- Does not send emails in the current demo; delivery is intentionally disabled.

### Meeting-to-Scope
- Extracts requirements from meeting transcripts.
- Checks product fit using the Knowledge Brain API.
- Drafts development tasks, effort ranges, and a project proposal.
- Saves a baseline and compares follow-up requirements with the original scope.

## Architecture

```text
Dashboard
  ├── Knowledge Brain (Python / FastAPI)
  ├── Inbox Agent (TypeScript / Express)
  └── Meeting-to-Scope (Python / FastAPI)
         └── Shared Knowledge Brain API
```

## Tech stack

- Python and FastAPI
- TypeScript, Node.js, and Express
- SQLite
- HTML, CSS, and JavaScript
- REST APIs
- Docker Compose

## Run locally

Requirements: Docker and Docker Compose.

```bash
git clone https://github.com/vamshivardhan22/Ai-Tech-consultant.git
cd Ai-Tech-consultant
cp .env.example .env
docker compose up --build
```

Open the dashboard at http://localhost:8080.

API documentation and health checks are available at:

- Knowledge Brain API: http://localhost:8001/docs
- Inbox Agent health check: http://localhost:8002/health
- Meeting-to-Scope API: http://localhost:8003/docs

Some flows use deterministic fallbacks when an Anthropic API key is not configured. These keep the services testable but should not be treated as LLM evaluation results.

## Limitations

This is a prototype, not a production-ready customer communication system. The mailbox delivery adapter is not implemented, the frontend does not provide user authentication or role-based access, and generated replies, estimates, and scope changes require human review. The Knowledge Brain uses lexical retrieval rather than a vector database. Review `DESIGN.md` and `EVALS.md` for further design notes and evaluation plans.

## Security

Do not commit `.env` files, API keys, mailbox tokens, or customer data. Do not expose the services publicly without appropriate authentication, authorization, rate limiting, monitoring, backups, and a production security review.

## Skills demonstrated

Python, FastAPI, TypeScript, Express, REST API integration, SQLite, retrieval-based question answering, workflow orchestration, and human-in-the-loop review.
