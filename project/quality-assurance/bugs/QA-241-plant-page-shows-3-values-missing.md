# QA-241: Plant page shows '3 values missing' (params.control.dispatch, params.control.outages, params.backup) on the stored, simulated plant v14 that has them: the page's draft spec drops the plant-level params before /plant/flowsheet/validate

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | backend,frontend |
| Reporter | QA-E2E-design-I |
| Found | 2026-11-05 17:40 UTC |
| Versions | frontend 1.1.113, backend 1.1.108, geomind 0.4.97, gemini 0.6.16 |
| Where | https://geomind.team/projects/f1704a61-f1b8-4b63-84d3-20bd30beaed7/design/plant; plant version 14 ('Plant best_v1 optimised by the assistant', 17:16:42 UTC), made by run 76d19df6 |
| Fixer | hotfix-back-lead |

## Steps

1. Let the assistant design a plant (run 76d19df6): plant class HeatingHeatPumpCoolingPlant with `params.backup = peak`, `params.control.dispatch = least_cost`, `params.control.outages = lowest_demand`; it simulates (365 steps, feasible).
2. Open the Plant page.

## Expected

No missing values: the stored plant simulates and the server check of its spec says `{"problems": []}`.

## Actual

- The header says **v14 · 3 values missing**: `control.dispatch`, `control.outages`, `backup`; the Dispatch box below shows `least_cost` at the same time.
- The page posts its draft to `/plant/flowsheet/validate`, and the answer is `params.control.dispatch is missing; expected 'least_cost'`, `params.control.outages is missing; expected 'lowest_demand'`, `params.backup is missing; expected 'peak' or 'none'`.
- The same call with the version's stored `spec` returns `{"problems": [], "warnings": []}` (checked through the API).
- The draft is `saved.structure` (`frontend/src/domains/design/plant/use-plant-editor.ts:35`), and the version's `structure` has no `backup`, no `control` and no `size` (`structure.params` keys: the modules only).

A user who saves the plant from this page (a layout move, a module edit) saves a free plant without dispatch, outage rule, backup and doublet count: the agents' design would not simulate any more.

## Evidence

- ![plant page](../evidence/QA-241/1.png)
- `../evidence/QA-241/validate-request.json`: the page's validate call and its answer.

## Cause

`backend/src/core/gemini/plant.py:305` `free_document` keeps only `params` whose key is a module (`if key in document["modules"]`) and drops `type` and `size`; `backup` and `control` are plant-level params, not modules, so they are dropped from `structure` (fact from the code; matches the stored version). The frontend edits and validates `structure`.

## Proposed fix

1. Backend `free_document`: keep the plant-level policy params gemini requires on a free plant (`backup`, `control.*`), and carry the doublet count, or return the class spec when the plant has a class.
2. Frontend: validate and save the class `spec` of a class plant (only a free plant uses `structure`), so a save never drops class values.
3. Test: a class plant with backup/control round-trips through the page with 0 missing.

## Fix

hotfix-back-lead, backend 1.1.111, ~17:57 UTC: `core/gemini/plant.py` `free_document` adds `plant_level_params`: the plant's dispatch, outages and backup as gemini writes them on a plant without a class (`control.dispatch`, `control.outages`, `backup`). Checked: HackathonPlant round-trips with backup=peak, dispatch=least_cost, outages=lowest_demand.
- 2026-11-05 18:05 UTC: backend 1.1.111
## Retest

Recipe: Open the Plant page of a project with HackathonPlant: no "values missing" for backup/dispatch/outages; save and reload keeps them.
