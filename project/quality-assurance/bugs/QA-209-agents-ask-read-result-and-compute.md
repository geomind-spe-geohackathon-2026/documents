# QA-209: Agents ask read_result and compute_kpis for cost metrics (costs, lcts, annualised_cost) these tools do not have; 6 refused calls in one optimisation run

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 17:30 UTC |
| Versions | backend 1.1.104 |
| Where | project `QA-TEST QA-E2E-study-I 1` (8fcbf709-537a-40d9-ac1f-abadd1061775); run 4eb8e2f4-e775-4e2a-b257-853eae883724 |
| Fixer | hotfix-python-lead |

## Steps

Same run as QA-205 (chat: optimise the plant for lowest cost of thermal supply).

## Expected

Cost metrics come from `estimate_costs` (or the study record); the agents never send cost names
to `read_result` or `compute_kpis`.

## Actual

Refused calls (run log, UTC):

| Time | Agent | Call | Refusal |
|---|---|---|---|
| 17:08:24 | design_lead | read_result path "costs" | unknown_name: expected a module path |
| 17:10:32 | design_lead | read_result path "lcts" | unknown_name: expected a module path |
| 17:12:21 | reviewer | read_result field "window" (no path) | invalid_input: expected a path too |
| 17:12:35 | reviewer | read_result path "" field "window" | unknown_name |
| 17:12:52 | reviewer | compute_kpis names [lcts, lcoh, lcoc, capex, opex, annualised_cost, co2] | unknown_name: annualised_cost (compute_kpis has no cost names) |
| 17:14:44 | analysis_lead | read_rag "economics.json" | unknown_name: only the 3 uploaded documents are RAG files (economics is a case file) |

Each costs a round trip (10-20 s with the model); the reviewer's three refusals sit in a 154 s review.
The study metrics list (lcts, annualised_cost, co2) and the compute_kpis list overlap only in part
(co2 vs co2_emitted), which the agents mix up.

## Evidence

- Run log: `../evidence/QA-205/run-4eb8e2f4-log.json` (shared with QA-205).

## Cause

Guess: the tool descriptions do not say that read_result reads module columns only and that
compute_kpis has no costs; the reviewer skill asks to re-check costs without naming estimate_costs.

## Proposed fix

geomind tool descriptions: read_result "module columns only; costs: estimate_costs; KPIs:
compute_kpis"; compute_kpis refusal for a cost name should suggest estimate_costs; the reviewer skill
names estimate_costs for cost checks; read_rag's refusal for a case file should suggest read_case.

## Fix

- 2026-11-05 18:09 UTC: deployed 19:01-19:03 CET: backend 1.1.112, geomind 0.4.118/0.4.119, gemini 0.6.19 (hotfix-python team)
- 2026-11-05 18:28 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
## Retest

QA-E2E-study-I, 2026-11-05 18:47 UTC, run 4885075b (same optimisation request, project 3): no read_result / compute_kpis / read_rag refusal in 107 calls. Verified.
