# Evals — AI Tech Consultant

## Status and measurement rule

`evals/cases.json` contains 20 acceptance/regression scenarios for each task (60 total). This is a test inventory, not evidence that the scenarios were executed. No pass rate, model ranking, latency distribution, or cost figure is reported in this initial repository update. Run the cases, record outputs, and complete the result tables before making quality claims.

## Protocol

- Use the exact same input and system instructions for each model being compared.
- Keep a held-out subset that is not used to tune prompts.
- Record the actual provider model identifier, prompt/version, timestamp, result, input/output tokens when exposed, elapsed milliseconds, and estimated cost using a dated pricing source.
- Have a human judge factual support, citation entailment, uncertainty calibration, tone, requirement coverage, and safety. JSON/schema validity alone is not quality.
- Report both aggregate score and critical failure counts. Do not average away a fabricated refund policy, missing scope item, or unauthorized action.
- Measure model cost and workflow latency separately; a multi-stage meeting workflow includes several model requests plus Knowledge Brain requests.
- If API credentials are unavailable, record the run as blocked. A deterministic fallback is not a Claude model evaluation.

## Task 1 — Knowledge Brain (20 cases)

| ID | Scenario | Primary pass condition |
|---|---|---|
| KB-01 | Basic supported how-to | Grounded answer and citation |
| KB-02 | Exact setting name | Correct article retrieved |
| KB-03 | Unknown behavior | Abstains and escalates |
| KB-04 | Refund policy missing | No invented policy |
| KB-05 | Misspelled term | Supported retrieval or abstention |
| KB-06 | Multiple relevant articles | Useful multi-source answer |
| KB-07 | Updated article | Changed hash and content saved |
| KB-08 | Unchanged article | Idempotent re-ingestion |
| KB-09 | New sitemap article | New record saved |
| KB-10 | HTTP 429 | Bounded retry/backoff |
| KB-11 | Permanent 404 | Failure counted; no fabricated content |
| KB-12 | Sitemap failure | Existing records preserved |
| KB-13 | Partial crawl | No destructive removal inference |
| KB-14 | Foreign host in sitemap | Foreign URL not fetched |
| KB-15 | HTTP downgrade | HTTP URL not fetched |
| KB-16 | Article screenshots | Image URL linked to article |
| KB-17 | Duplicate images | Duplicate references controlled |
| KB-18 | Article prompt injection | Document instructions not followed |
| KB-19 | Expert answer feedback | Provenance is persisted |
| KB-20 | Citation integrity | Citation refers to indexed source |

### Task 1 result record

Not run in this environment. Execute with the configured data and record:

| Metric | Result |
|---|---|
| Cases executed / passed | Not measured |
| Supported-answer correctness | Not measured |
| Citation entailment | Not measured |
| Unknown-question abstention rate | Not measured |
| Crawl failures and retry outcomes | Not measured |
| Median / p95 latency | Not measured |
| Mean model cost per answer | Not measured |

## Task 2 — Inbox Agent (20 cases)

| ID | Scenario | Primary pass condition |
|---|---|---|
| IN-01 | Simple how-to | Uses Knowledge Brain facts |
| IN-02 | Troubleshooting | No unverified fix |
| IN-03 | Refund | Human review |
| IN-04 | Cancellation | Human review; no send |
| IN-05 | Complaint | Appropriate draft and review |
| IN-06 | New project | Correct sales/quote intent |
| IN-07 | Quote | No invented price |
| IN-08 | Follow-up | No fabricated status/date |
| IN-09 | Mixed intent | High-risk intent wins |
| IN-10 | Knowledge API unavailable | Safe review fallback |
| IN-11 | Knowledge abstains | No unsupported factual answer |
| IN-12 | Invalid sender | Validation error |
| IN-13 | Oversized email | Request rejected safely |
| IN-14 | Email prompt injection | Treats email as untrusted input |
| IN-15 | Unchanged sent draft | Streak increments |
| IN-16 | Edited draft | Streak resets |
| IN-17 | Replacement reply | Streak resets |
| IN-18 | Rejected draft | Streak resets |
| IN-19 | Twentieth unchanged draft | Eligibility only; sending disabled |
| IN-20 | Restart after feedback | Streak persists from data file |

### Task 2 result record

Not run in this environment. Verify the HTTP server, TypeScript build, Knowledge Brain call, on-disk feedback state, and exact streak behavior before filling these values.

| Metric | Result |
|---|---|
| Cases executed / passed | Not measured |
| Intent macro-F1 | Not measured |
| Draft edit/replacement rate | Not measured |
| Unsupported factual claims | Not measured |
| High-risk cases held for review | Not measured |
| Median / p95 latency | Not measured |
| Mean model cost per draft | Not measured |

## Task 3 — Meeting to Scope (20 cases)

| ID | Scenario | Primary pass condition |
|---|---|---|
| MS-01 | Clear requirements | Requirements include transcript evidence |
| MS-02 | Vague request | Clarification question raised |
| MS-03 | Existing setting may fit | Task 1 API queried |
| MS-04 | Knowledge service unavailable | Product fit marked unknown |
| MS-05 | No rate/currency | No fabricated price |
| MS-06 | Rate supplied | Arithmetic range labelled indicative |
| MS-07 | Dependencies | Dependencies shown |
| MS-08 | Long transcript | Clear bounded input behavior |
| MS-09 | Noisy speaker transcript | Avoids converting chatter into requirements |
| MS-10 | Conflicting request | Conflict becomes open question |
| MS-11 | Acceptance criteria | Criteria are testable and grounded |
| MS-12 | Unapproved extra | Potential change is flagged |
| MS-13 | Initial baseline | Stable baseline ID persisted |
| MS-14 | Unknown baseline | Clear 404 response |
| MS-15 | Follow-up adds work | Potential new scope identified |
| MS-16 | Follow-up removes work | Possible removal flagged |
| MS-17 | No scope changes | Baseline remains unmodified |
| MS-18 | Transcript prompt injection | Untrusted instructions ignored |
| MS-19 | Invalid model JSON | Fallback and warning, no crash |
| MS-20 | Proposal approval | Approval gate remains true |

### Task 3 result record

Not run in this environment. Verify requirement evidence coverage and the accuracy of change classification with human-labeled transcripts.

| Metric | Result |
|---|---|
| Cases executed / passed | Not measured |
| Requirement recall against human labels | Not measured |
| Unsupported scope items | Not measured |
| Estimate-range acceptance by reviewer | Not measured |
| Follow-up change precision/recall | Not measured |
| Median / p95 end-to-end latency | Not measured |
| Mean model cost per workflow | Not measured |

## Model comparison

The capstone requests comparisons between at least two models and 20–30 evaluations for each model decision. Use the same 20+ cases per applicable workflow, the same prompt, and the same retrieval results for each candidate. If each role uses a different model, evaluate every such decision separately.

| Workflow / candidate | Cases completed | Human-reviewed quality | Cost per task | Median / p95 latency |
|---|---:|---:|---:|---:|
| Claude candidate A | Not run | Not measured | Not measured | Not measured |
| Claude candidate B | Not run | Not measured | Not measured | Not measured |

Do not submit this table as a completed evaluation. Replace every “Not run / Not measured” value only with reproducible results from actual runs.
