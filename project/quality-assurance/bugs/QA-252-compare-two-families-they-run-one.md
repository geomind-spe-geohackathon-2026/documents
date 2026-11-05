# QA-252: Compare two families: they run one after the other (24 min) and a failed family is never retried; GEOMIND_COMPARE_CONCURRENCY and GEOMIND_COMPARE_RETRIES are unset in production and silently mean 1 and 0

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | backend,geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 17:55 UTC |
| Versions | backend 1.1.106/1.1.107 (geomind 0.4.98+, gemini 0.6.17) |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 2 (dfe5d6e1-8fdc-404f-b150-b8e7d919f2a1); chat f7b3b8fc-e5d2-453e-b524-e17e6733d0d9 (auto-approve on); run 56c8a22e-7071-4847-88d3-06c4dd56c960 |
| Fixer | hotfix-back-lead |

## Steps

1. New project, reference `case.json` + `economics.json` + `data/demand.csv` (valid, no plant). Chat auto-approve on.
2. Message: "The case is set. Design two plant families side by side and compare them on LCTS: (1) heating with a heat pump and cooling with a compression chiller, (2) heating with a heat pump and cooling with an absorption chiller. Tell me which one is better and why."
3. Answer the design lead's ranges question (request-140) with option 1 (the five ranges of hackathon-2026-assumptions).

## Expected

Coordinator -> `loop: compare` (it did, 5 s). The `ComparisonDriver` runs the two families side by side ("side by side up to the loop's concurrency"), and a family that fails gets another round with gemini's failures (as the single design loop does, up to 5 rounds), so the user gets a comparison.

## Actual

Run 17:30:37 to 17:54:13 UTC (23 min 36 s; 0.13 USD, design_lead 70 LLM calls / 3.27 M input tokens):

| Driver step | Time (UTC) | What |
|---|---|---|
| 1 | 17:30:43 | plan with the design lead (asks the ranges question, 2 min 22 s) |
| 2 | 17:33:05 | batch `["compression"]` only; 8 min 51 s; ends "built and sized, but NOT simulated" (failed) |
| 4 | 17:41:56 | batch `["absorption"]` only, after the first ended; 11 min 01 s; ends "INFEASIBLE, 365 of 365 steps fail" |
| 6 | 17:52:57 | explainer writes "Neither family has a verified design, so there is no LCTS comparison" (76 s) |
| 7 | 17:54:13 | `{"round": 1, "stop": "no_verified"}`, finish |

The families ran one after the other, and neither got a second round. The user asked for a comparison and got none; 24 min were spent.

## Evidence

- `../evidence/QA-252/56c8a22e-7071-4847-88d3-06c4dd56c960.log.json.gz`, `../evidence/QA-252/56c8a22e-7071-4847-88d3-06c4dd56c960.trace.txt`: `comparison_driver` steps and their notes `design loop: {"round": 1, "batch": ["compression"]}`, `{"round": 1, "batch": ["absorption"]}`, `{"round": 1, "stop": "no_verified"}`.
- `docker exec geomind-celery printenv`: `GEOMIND_DESIGN_CONCURRENCY=3`, no `GEOMIND_COMPARE_CONCURRENCY`, no `GEOMIND_COMPARE_RETRIES`; `backend/.env.example` has neither.

## Cause

- `geomind/agents/project/lead.py` `comparison()` passes `runtime.get("compare_concurrency")` and `"compare_retries"`; both are unset in production (`runtime.py` reads `GEOMIND_COMPARE_CONCURRENCY`, `GEOMIND_COMPARE_RETRIES`). `ComparisonDriver.batch_size` turns an unset concurrency into 1, and `after_check` an unset retries into 0: a silent default, against the rule "no default values: a missing value is an error".
- `after_check` retries only a family the reviewer `rejected`; a family whose design lead hands back no design (`failed`, as `compression` here) or an infeasible one before the check is never sent back, even with retries set.

## Proposed fix

- backend: set `GEOMIND_COMPARE_CONCURRENCY` (2 or 3, like `GEOMIND_DESIGN_CONCURRENCY=3`; mind the Dell CPU budget) and `GEOMIND_COMPARE_RETRIES` (e.g. 2) in `.env` and `.env.example` and in the compose of the worker.
- geomind `runtime.py` / `comparison.py`: a missing `compare_concurrency` or `compare_retries` raises (as other required settings do) instead of meaning 1 and 0.
- geomind `ComparisonDriver`: give a `failed` family (no design or an infeasible result) a retry round with its failures too, like `DesignDriver.routed_task`, within `retries`.
- The two families' own failures (compression sizing gives `d0.esp` flow 8 808 335 m3/s, absorption drive loop does not close) are design-team issues for QA-AI-design-I's scope; not reported here.

## Fix

hotfix-back-lead, backend 1.1.112, ~18:01 UTC: GEOMIND_COMPARE_CONCURRENCY=3, GEOMIND_COMPARE_RETRIES=1 in all four backend env files; checked in the worker (3, 1).
- 2026-11-05 18:06 UTC: backend 1.1.112
- 2026-11-05 18:34 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
## Retest

Recipe: Ask to compare two families: both design at the same time (overlapping step times), a failed family is tried once more.
