# QA-129: The optimiser never searches the doublet count: set_ranges refuses size.doublets on the assistant's free plant, the agent drops it, the design stays at 1 doublet

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind,gemini |
| Reporter | Fatemeh (asked for the run review), Claude (DB read and write-up) |
| Found | 2026-11-05 14:14 UTC |
| Versions | backend 1.1.86 and later during the runs (2026-11-05 10:10 to 14:07 UTC) |
| Where | https://geomind.team/projects/cf0c3d9c-d925-4ffa-bd29-3ac8205090d3 (project geo mind testing), chat 27379f2e-0103-4ddf-a020-f0cd4deb20a6; run 32a12115-1a7d-4e89-8582-05466fad0db0 |
| Fixer | hotfix-python |

## Steps

1. The design team builds a free plant (`geothermal_heating_cooling`, modules and connections, no class type) and makes it feasible.
2. The design lead sets ranges for `optimize`, with `size.doublets` 1 to 3 (the user approved "doublets 1-3").

## Expected

The optimiser searches the doublet count with the other ranges (the brief's design variable, 1 to 3 doublets), as gemini's sample does (`size.doublets` value 2, range 1-3, on HeatingHeatPumpCoolingPlant).

## Actual

`set_ranges` (11:08:50 UTC) is refused: "unknown path 'size.doublets'; valid: ... d0.depth ... d0.nominal_flow ...". The design lead sends the ranges again without the doublets (11:08:58) and optimizes 125 trials on depth, flow and unit capacities only. The result lcts_best (12 of 12 pass) keeps 1 doublet: the electric boiler gives 21.5 % of the year's heat and lcts is 70.95 EUR/MWh, against 40.34 for gemini's sample plant with the doublet count searched. The user was not told that the doublet range was dropped.

## Evidence

- Postgres read-only: run_events of run 32a12115, set_ranges at 11:08:50 (error) and 11:08:58; optimize at 11:09:01 (`evaluations: 30`, 125 trials, best 70.95).
- Result lcts_best: https://geomind.team/projects/cf0c3d9c-d925-4ffa-bd29-3ac8205090d3/design/results/c5db89bc-2edc-44ae-85d9-df03168913bf

## Cause

Fact: a free plant has no `size.doublets`; the doublet count lives on class plants. Guess: the free plant has a single Doublet module `d0`, so its count cannot vary. Fix: build on the class (HeatingHeatPumpCoolingPlant, as IMP-023), or let a free plant carry `size.doublets`; and the agent must say so when a range the user approved is dropped.

## Fix

- 2026-11-05 14:28 UTC: gemini 0.6.15 (free plant takes size.doublets, resize joins copies) + geomind 0.4.87 skill (no silent drop, handbook ch 10/11), backend 1.1.89, deployed 14:27 UTC

Cause: `size.doublets` existed only on plant classes; a free plant refused it and the design lead dropped the range in silence. Fix: gemini 0.6.15: a plant without a class on one doublet `d0` takes a range on `size.doublets`; `resized` copies d0, joins the supplies with mixers, splits the brine with splitters and repeats d0's other connections, so `optimize` searches 1 to 3 doublets. geomind 0.4.87: designing-a-plant says so, forbids dropping an approved range in silence, and points to handbook-plant-design chapters 10 and 11 (IMP-023 rejected by the user).

## Retest
