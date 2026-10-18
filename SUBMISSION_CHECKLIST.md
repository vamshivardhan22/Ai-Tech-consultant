# Submission Checklist

## Deliverable completeness

- [ ] Task 1: crawl the intended support site in small batches and verify saved records.
- [ ] Task 1: verify supported answer, cited excerpt, and unknown-question escalation.
- [ ] Task 2: verify how-to, refund/cancellation, unknown answer, and feedback-streak reset.
- [ ] Task 3: record three real role-play meeting transcripts and at least one follow-up.
- [ ] Task 3: check requirement-to-evidence traceability and review estimate assumptions.
- [ ] Record any model failure, retry, or fallback instead of hiding it.

## Reproducibility

- [ ] Start from a clean checkout using docker compose up --build.
- [ ] Confirm Python tests and TypeScript type-check pass.
- [ ] Confirm the latest GitHub Actions run is green and link it in the submission notes.
- [ ] Run the evaluation cases and record actual results, model IDs, latency, and token/cost data.
- [ ] Export the real coding-tool conversation log required by the organizer.
- [ ] Record the actual tool(s) used and ask the organizer how to disclose earlier ChatGPT/GitHub-assisted scaffolding. Do not fabricate a coding-tool history.

## Security and presentation

- [ ] Verify .env is ignored and no API keys or customer personal data are committed.
- [ ] Do not expose local services publicly without authentication and authorization.
- [ ] Confirm no email-sending or client-delivery path is active.
- [ ] Record the demo using the real working app, not mocked screenshots.
- [ ] List limitations explicitly in the final submission.

**Submission gate:** do not claim “production-ready,” “100% working,” a measured accuracy score, or passing CI until those statements are backed by actual verification.
