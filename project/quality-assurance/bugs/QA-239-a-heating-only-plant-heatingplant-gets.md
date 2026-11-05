# QA-239: A heating-only plant (HeatingPlant) gets 13 passed, 0 failed, 2 not assessed on a case that demands cooling; it shows as the cheapest result (LCTS 26.96) instead of infeasible

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | gemini,backend |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 17:42 UTC |
| Versions | backend 1.1.108 (geomind 0.4.110, gemini 0.6.17) |
| Where | https://geomind.team/projects/4678c5c6-66fc-46dd-9d1e-358c3c5c1d24 (No-agent showcase); minimize study 0e60d87b-ec6f-4955-847c-b0cd3f79855a, result 92c67bd1-d700-44bb-b857-249c9a2c5633 |
| Fixer | hotfix-back-lead |

## Steps

1. Case with a cooling demand (hackathon case) and requirement cold_delivered (unmet share <= 1 %).
2. Run a study on HeatingPlant (no cooling unit).

## Expected

Infeasible: the cooling demand is not served (gemini's script ranking says feasible False, reason cold_delivered).

## Actual

checks: passed 13, failed 0, not_assessed 2 (`cold_delivered` and `cooling_supply_temperature`: "missing: the plant has no unit of the role 'cooling_supply'"). LCTS 26.96 EUR/MWh, the lowest of all results, so a heating-only plant looks like the best design in Results and Compare.

## Cause

Fact: a requirement on a role the plant lacks is reported as not assessed. For a demand the case states, no unit serving it means the demand is unmet (unmet share 1), so it should fail.

## Fix

hotfix-back-lead, backend 1.1.110, deployed ~17:50 UTC (backend part). Additive: every result
(list and detail) has `feasible` = no check failed and none not assessed; a ranking (Results,
Compare: frontend) leaves out the others. gemini part (a missing role on a stated demand fails)
with the python team.

Frontend part (hotfix-front-lead): frontend 1.1.123 (commit 9e72fd7, bundle index-C7R5NeXi.js) reads `feasible` (backend 1.1.110): an infeasible result is never the Compare best, never on the trade-off line, never the report default; its checks read "infeasible: does not serve every demand".
- 2026-11-05 18:54 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest

Recipe: GET /design/results?project=...: the heating-only result on a case with cooling has feasible false.
