# QA-135: Overview and Design show Study and Results 'Out of date' on a freshly seeded project, and still after a fresh full-year run of the stored plant

| Field | Value |
|---|---|
| Status | open |
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
## Retest

(Who, when, result.)
