# QA-135: Overview and Design show Study and Results 'Out of date' on a freshly seeded project, and still after a fresh full-year run of the stored plant

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend |
| Reporter | functional-qa-study-I |
| Found | 2026-11-05 14:21 UTC |
| Versions | frontend as live 2026-11-05, backend 1.1.83-1.1.84 |
| Where | https://geomind.team/projects/7a852d89-dfe5-423c-980a-a4ca231353bc/overview; project QA3 study |
| Fixer | hotfix-back-III |

## Steps

1. Open the seeded project "QA3 study" (case v3, plant v2, two simulations in Activity). Overview: Study and Results read 'Out of date'.
2. In the chat ask for a full-year run of the current plant; it finishes (365 steps, feasible). Reload Overview: still 'Out of date'.

## Expected

A project seeded with a finished simulation of its current case and plant shows Study/Results current; after a fresh run of the stored plant on the current case, the same (a plain simulate writes no Results row by design, QA-092, so the stage may need to count it).

## Actual

Study and Results 'Out of date' before and after the run; Activity shows 'Study simulation ... finished' rows. Guess (marked): the stage compares versions and the plant versions were saved after the case version, or a plain simulate counts as no study.

## Evidence

- ![screenshot](../evidence/QA-135/1.png)
- Run JSON: `../evidence/QA-135/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 14:37 UTC: hotfix-back-III, cause (fact): GET /design/results lists oldest first (contract, paginate by created asc); frontend toStaleSteps(project, results.data?.[0]) in src/app/layouts/progress.tsx:20 and src/domains/workspace/overview/page.tsx:20 takes the OLDEST result as the newest. QA3 study: oldest = 'simulation HackathonPlant' (case 3, plant 1) vs project plant 13 -> Out of date; newest is sized2 (case 3, plant null) -> current. Fix for hotfix-front-III: use the last item (or max by created). Note: agent results have plant_version null (backend 1.1.81) and a plain chat simulate saves a new plant version with no result (QA-092), so freshness there is judged by case only. No backend change.

hotfix-front-III, frontend part, 1.1.106 (b2720e5), deployed 14:43 UTC (bundle index-C139P2pV.js). Cause (fact): Overview (`overview/page.tsx`) and the sidebar (`app/layouts/progress.tsx`) passed `results[0]` to `toStaleSteps`, but GET /design/results lists oldest first, so the stepper compared the project's case/plant versions with its OLDEST result. QA3 study: oldest result (simulation, 10:01, older plant) vs newest sized2 (11:10, current). Fix: judge by the newest result by `created`. Live after deploy: QA3 study and geo mind testing no longer 'Out of date'; SPE GeoHackathon 2026 still is (its newest result is older than its plant). Backend part (a plain simulate writes no Results row, QA-092) stays with hotfix-back-III.
- 2026-11-05 14:43 UTC: frontend part live in 1.1.106 (hotfix-front-III): Out of date now judged by the newest result; QA3 study and geo mind testing read current. Backend part (plain simulate, no Results row) still with hotfix-back-III
- 2026-11-05 15:12 UTC: hotfix-back-III: backend part (user's option C) live in 1.1.96 (commit 5653973, 15:12 UTC): on the root run.finished the run's LAST successful plain simulate becomes one result (no study, 'simulation <design>', case/plant version matched by digest else null, report+coverage from geomind's kept run files), deduplicated by reference. Not live-checked (QA checks stopped by the user); retest: a chat full-year simulate, then Overview Study/Results current and one new 'simulation <design>' result.
## Retest

(Who, when, result.)
