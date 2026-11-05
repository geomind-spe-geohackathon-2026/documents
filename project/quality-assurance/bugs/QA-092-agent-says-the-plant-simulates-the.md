# QA-092: Agent says the plant simulates the full year (6 of 8 caps), but the project Plant page (v8) still shows 6 missing values, Results 'No results', and Study 'Run the design' is blocked 'Waits for 4 values'; the agent's design never reaches the Plant tab

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | backend |
| Reporter | functional-qa-3 |
| Found | 2026-11-05 09:27 UTC |
| Versions | backend 1.1.79 (geomind 0.4.73), frontend 1.1.71 |
| Where | https://geomind.team/projects/932b318c-f285-4827-aefe-c8fa3327735b/design/plant and /design/study; project QA2 functional-qa-3 studies (932b318c-f285-4827-aefe-c8fa3327735b), chat 510ab94f-c4f7-4019-9f75-cb40229b374e; runs 753645c0 and the 08:27 UTC run |
| Fixer | hotfix-back-II |

## Steps

1. Let the design team run to a simulated plant (after QA-081/QA-083 work-arounds): the agent reports 'The plant now simulates the whole year (365 steps, 0 failed steps) and meets 6 of the 8 PDF caps'.
2. Open Design > Plant, Study and Results.

## Expected

The plant the agent simulated is the project plant: Plant page complete or saved as a version, Results shows its result, and a new 'Run the design' study can start.

## Actual

- Plant tab v6 'values missing: 7' (later v8 '6 values missing': d0.esp.minimum_flow, maximum_flow, best_efficiency_flow, control.dispatch, control.outages, backup), the doublet d0 marked 'missing values'; the modules shown are the older plant (degasser, filters), not the agent's gas-free design.
- Study > New study > Run the design 'qa3_run1' is created but blocked: 'Waits for 4 values. Fill them in on Plant' (4 here, 6/7 on the Plant page).
- Results tab: 'No results' while the chat says the year was simulated.
- Studies listed 'sized_v1', 'simple_sized', 'sized2027' have kind 'run', and only an 'Open run' link (the agent run page), no result view.
So from the UI the user cannot run, size or evolve anything on the design the agents built; every study (S1-S6) is blocked.

## Evidence

- ![screenshot](../evidence/QA-092/1.png)
- Run JSON: `../evidence/QA-092/run-<id>.json`

## Cause

Guess: agent designs live in the problem state / `design/<name>` store and are never written to the project plant (an accept step is missing or fails silently); the counts 4 / 6 / 7 come from different checks.

## Fix

hotfix-back-II, 2026-11-05 09:37 UTC. Cause (backend): `VersionRecorder` saved a plant version
only after `build_plant`. The agents changed their design with `patch_plant` (gas-free, ESP flows)
and simulated it; that design stayed in the chat's `design/<name>` store, so the Plant page kept
the older built plant (degasser, filters, missing ESP values) and Study blocked on its gaps.
Fix: backend 1.1.82 (commit 9da4bbf): a successful `patch_plant`, `merge_designs`, `set_ranges`,
`size_plant` or `optimize` saves the design it stored, and `simulate` on a stored design saves
that design, as the project's next plant version. Deployed with hotfix-python-II's batch (by
10:30 UTC). Not covered: a plain `simulate` result still writes no result row (Results 'No
results'); only recorded studies do (QA-088). The counts 4 / 6 / 7 come from the older plant.

## Retest

(Who, when, result.)
