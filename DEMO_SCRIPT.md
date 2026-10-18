# Demo Script (4–5 minutes)

Use this as a guide, not as a claim that every feature is production-ready. Show actual results from the running app.

## 0:00–0:30 — Problem and design

“AI Tech Consultant connects three workflows: finding a grounded product answer, drafting a support email, and turning a client meeting into a scope. AI prepares work, but uncertain or customer-facing decisions stay under human review.”

Point out the three dashboard tabs and the three independent HTTP services.

## 0:30–1:30 — Task 1: Knowledge Brain

1. Open Knowledge Brain and submit the prefilled dashboard settings question.
2. Point out the answer, citations, and demo-fixture label.
3. Ask an unrelated question such as “What is the orbital plasma fermentation policy?”
4. Show the intended abstention and escalation for a low-evidence query.

Say clearly: “The initial store has demo fixtures until the public support site is ingested. Retrieval is lexical in this version; vector search and screenshot vision are planned, not implemented.”

## 1:30–2:30 — Task 2: Inbox Agent

1. Open Inbox Agent and generate a draft from the example email.
2. Show classification, knowledge result, citations, and review flag.
3. Change the email to request a refund or cancellation and submit again.
4. Point out that the service does not send mail and the autonomy endpoint remains disabled.

Say clearly: “The current integration creates drafts only. It does not connect to a real inbox.”

## 2:30–3:45 — Task 3: Meeting-to-Scope

1. Open Meeting to Scope and submit the sample meeting transcript.
2. Show requirements and transcript evidence, product-fit checks, estimate ranges, assumptions, and proposal.
3. Point out the generated baseline ID.
4. Submit the follow-up transcript and show the change-analysis result.
5. Explain that proposal and change analysis require human review; fallback estimates are placeholders, not a validated quote.

## 3:45–4:30 — Engineering and reliability

Show DESIGN.md, EVALS.md, and evals/cases.json. Explain the explicit failure boundaries: sitemap failures do not mass-delete data, unknown questions abstain, customer emails are not sent, and follow-up analysis does not overwrite the original baseline.

Show .github/workflows/ci.yml and say CI is configured. Do not claim it passed unless the GitHub Actions run is green.

## 4:30–5:00 — Honest limitations and next steps

“The next engineering priorities are executing CI on a clean checkout, running the acceptance cases, implementing full sitemap inventory reconciliation and scheduled sync, adding screenshot vision and hybrid retrieval, and connecting a real mailbox behind an authenticated review workflow.”

## Before recording

- [ ] Run docker compose up --build from a clean checkout.
- [ ] Verify all three service health endpoints and the dashboard.
- [ ] Confirm the current GitHub Actions run status.
- [ ] Run each of the three flows and save real screenshots.
- [ ] If using Claude, verify the API key is configured without showing it on screen.
- [ ] Do not present the 60 cases as passed; they are acceptance scenarios until actually run.
