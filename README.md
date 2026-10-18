# AI Tech Consultant

A capstone project with three connected workflows:

1. **Knowledge Brain (Python)** — ingest product documentation, answer with source citations, abstain when evidence is insufficient, and provide an API for the other workflows.
2. **Inbox Agent (TypeScript)** — classify customer emails, retrieve facts through the Knowledge Brain API, draft replies for human review, and record feedback.
3. **Meeting to Scope (Python)** — turn meeting transcripts into evidence-linked requirements, task estimates, a scope of work, and a proposal; compare follow-up meetings against an approved baseline.

## Status

This repository was initially empty. This README is a starting point, not a claim that the application is implemented or tested. Update the checklist only when the corresponding feature has been verified.

- [ ] Task 1: Knowledge Brain API and cited answers
- [ ] Task 1: resumable ingestion and safe sitemap reconciliation
- [ ] Task 1: screenshot/image understanding linked to articles
- [ ] Task 1: expert escalation and reviewed knowledge feedback
- [ ] Task 2: TypeScript email classification and grounded reply drafts
- [ ] Task 2: feedback ledger and 20-consecutive-unchanged-draft eligibility
- [ ] Task 3: transcript requirements with evidence references
- [ ] Task 3: scope, estimates, proposal, and follow-up change report
- [ ] Human approval gates for external/client-facing actions
- [ ] Automated tests and recorded model evaluations
- [ ] Clean setup verified from a fresh checkout

## Requirements

- Python for Tasks 1 and 3.
- TypeScript for Task 2 (the assignment allows Python instead if you cannot use TypeScript; do not mix languages within a task).
- Claude must be central to AI workflows; model choices must be evaluated rather than assumed.
- Tasks 2 and 3 must call Task 1 through its API and must not duplicate Task 1 implementation code.

## Setup

Setup and run commands will be added once the application code and dependency configuration are committed. No runnable application is included in this initial commit.

## Integrity note

Do not report tests, quality scores, latency, costs, mailbox integrations, recordings, or model comparisons unless they have actually been run or completed. Fixture-mode behavior must be labelled as such.
