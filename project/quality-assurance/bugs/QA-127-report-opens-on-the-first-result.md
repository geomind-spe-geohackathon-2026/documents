# QA-127: Report opens on the first result (sized1, 6 of 12 pass) instead of the best one (lcts_best, 12 of 12 pass)

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | frontend,backend |
| Reporter | Fatemeh, Claude (write-up) |
| Found | 2026-11-05 11:23 UTC |
| Versions | frontend as deployed 2026-11-05 ~12:50 UTC |
| Where | https://geomind.team/projects/cf0c3d9c-d925-4ffa-bd29-3ac8205090d3/design/report (project geo mind testing) |
| Fixer | hotfix-front-III |

## Steps

1. The project has two results: sized1 (6 of 12 checks pass) and lcts_best (the optimised design, 12 of 12 pass, result c5db89bc-2edc-44ae-85d9-df03168913bf).
2. Open Design > Report.

## Expected

The report opens on the best result: the feasible one, and among feasible ones the best on the study's objective (or the one the assistant names as final); the user can still pick another in Options. And its Agent log section shows the run that made that result (QA-109).

## Actual

"Draft from sized1": the report is built on the first, infeasible result. The agent log section still says "No assistant run was chosen" (QA-109, still open).

## Evidence

- Screenshots of the report on sized1: `../evidence/QA-109/1.webp`, `../evidence/QA-109/2.webp`.
- `frontend/src/domains/design/report/report-editor.tsx` line 66: `const result = params.get("result") ?? results[0]?.id ?? ""` (the first result in the list).

## Cause

Fact: the default is the list's first result, with no look at feasibility or objective. Fix: default to the newest feasible result with the best objective value (the backend can mark it, e.g. `best: true` on the results list), else the newest; same default for the run (the result's study `started_by_run_id`, QA-109). Fix both together.

## Fix

hotfix-front-III, frontend 1.1.100 (c7a17a7), QA-127 and QA-109 together: `report/defaults.ts` picks the result: design results whose checks all pass (none failed, none not assessed), the best on the objective of the newest minimize/maximize study among them, else the newest feasible, else the newest result; the run is the result's study `started_by.run` (empty when a user started the study). A `result` or `run` in the URL still wins. Checked locally against production data: 'geo mind testing' opens lcts_best (12/12, lcts 70.95 vs lcts_fixed 72.94) with run 32a12115's log; QA3 study opens sized2 with its run. Deploy 14:30 UTC.
- 2026-11-05 14:27 UTC: frontend 1.1.104 deployed 14:27 UTC, bundle index-DjTPYa7Q.js
## Retest

- 2026-11-05 14:29 UTC: live 1.1.104: geo mind testing opens lcts_best; QA3 study opens sized2; Optimise LCTS (only feasible optimisation) in SPE project
