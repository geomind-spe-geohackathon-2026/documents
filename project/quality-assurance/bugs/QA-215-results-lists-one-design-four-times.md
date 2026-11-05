# QA-215: Results lists one design four times (two tabs with the same name 'simulation HeatingAbsorptionCoolingPlant', opt1, simulation opt1); plant version empty on 3 of 4; sensitivity study has no Results view, only raw JSON

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | backend,frontend |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 17:30 UTC |
| Versions | backend 1.1.106, frontend bundle index-CEvw1roy.js |
| Where | https://geomind.team/projects/8fcbf709-537a-40d9-ac1f-abadd1061775/design/results (project `QA-TEST QA-E2E-study-I 1`); result 7e0c79f0-3a4d-429a-bbdb-2f3ed13c53f2 "simulation opt1" (plant version 4, HeatingAbsorptionCoolingPlant, 2 doublets, 2500 m) |
| Fixer | hotfix-front-VII |

## Steps

1. Chat: simulate the plant (run 61721f4c), ask a sensitivity (run d6f8e79a), optimise (run
   4eb8e2f4; it also ran a price sensitivity `lcts_sensitivity_prices`).
2. Design > Results; Results > Compare; Design > Study > lcts_sensitivity_prices > Open record.

## Expected

One row per distinct design (or the repeats grouped), each named so the user can tell them apart
(plant version, study, time); the sensitivity shows as a table or tornado chart (the result API has
a `tornado` field).

## Actual

- Results has 4 tabs: "simulation HeatingAbsorptionCoolingPlant" twice (ed9e4c2b, feef9aa8),
  "opt1" (fa626d14), "simulation opt1" (7e0c79f0). All four are the same design: Compare shows the
  same 20.96 kt, 49.281 EUR/MWh, 23.956 MEUR, 2 doublets, 2500 m, all passed.
- `plant_version` is null on 3 of 4 rows (only 7e0c79f0 has 4), so the user cannot tell which plant
  each came from. The optimisation also wrote plant versions 3 ("baseline built by the assistant")
  and 4 ("ranged2 changed by the assistant") for the same plant: only ranges changed.
- The tab strip is wider than the panel: selecting Compare scrolls the whole Design panel sideways
  (titles cut at the left).
- Study page: lcts_sensitivity_prices has Result empty; Open record shows only the raw JSON
  (`rows[]` with 15-digit values). No Results row, `tornado` stays null. The user sees the ranking
  only in the chat.

## Evidence

- `../evidence/QA-215/1.png` (Compare: four identical rows), `../evidence/QA-215/results-first.json`.
- Study record: https://geomind.team/projects/8fcbf709-537a-40d9-ac1f-abadd1061775/design/study/fa3dcd72-7f3c-4db3-ae25-3eb4d0fee4c8/record

## Cause

Facts: QA-135 option C writes the last simulate of each run as a Results row, and the optimiser's
best is a row too; nothing deduplicates or names by plant version. Guess: the simulate row does not
carry the plant version when the agent simulates the project plant without a version.

## Proposed fix

backend: set plant_version on every result row (the version simulated); skip or link a row whose
design equals an existing row's; give a sensitivity/sample study a Results row with `tornado` /
`spread`. frontend: tab label with plant version and time; wrap or scroll only the tab strip;
render the study record of a sensitivity as a table/tornado.

## Fix

## Retest
