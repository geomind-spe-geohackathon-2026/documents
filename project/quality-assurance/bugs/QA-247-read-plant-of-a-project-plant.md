# QA-247: read_plant of a project plant returns a plant that build_plant refuses (fluids thermal_heat: None 'extra inputs not permitted'; d1 'no module of the class'): the lead cannot rebuild the stored reference plant it just read

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind,gemini |
| Reporter | QA-AI-design-I |
| Found | 2026-11-05 17:50 UTC |
| Versions | backend 1.1.109 (geomind 0.4.110 from the local clone, gemini 0.6.17) |
| Where | api.geomind.team; project QA-TEST QA-AI-design-I 3 (ef781ee9-4a2a-4e11-9228-f5965f372680); chat 25e27df1-fff2-434f-87b3-bdbf1917957e; run 5e847cc6-14af-4f05-a34f-5b3cb10fdb2e; design_lead #2-#5 (17:45:01-17:45:51 UTC) |
| Fixer | hotfix-python-lead |

## Steps

1. Project with the reference case + economics and gemini's `plants/HeatingHeatPumpCoolingPlant.json` stored as plant version 1 (POST /plant/flowsheet), 2 doublets.
2. Chat: "Size the stored plant for this case: choose the number of doublets (1 to 3) and the heat pump and boiler sizes for the lowest LCTS, keeping every hard limit."
3. The project lead's brief says "Start from that stored plant; do not build a new plant from scratch."

## Expected

The design lead works on the stored plant (`design/v1` / `plant_version: 1`) with `set_ranges`, `size_plant`, `optimize`: no `build_plant` (QA-221, fixed in 0.4.110, whose prompt rule is in this run's system prompt).

## Actual

- #2 `read_plant {"project_plant": "HeatingHeatPumpCoolingPlant"}` returns the expanded plant: every fluid with all fields (null), and the generated modules (`d1`, `production_mixers`, `injection_splitters`, grids).
- #4 (20.6 s) `build_plant name 'start'` with the whole plant re-typed (12,886 characters): refused: `fluids.cooling_consumer: ... thermal_heat Extra inputs are not permitted` (the lead added a `thermal_heat: null` that read_plant does not have) and `d1 is no module of the class HeatingHeatPumpCoolingPlant, and a plant with type takes only its class's modules` (read_plant lists `d1`, which the class makes from `size.doublets` 2).
- #5 (14.6 s) the same build_plant again, 6,619 characters: the approval card (request-124); the tester denied it: "The project already has this plant as plant version 1. Use it as it is; do not re-type it."
Evidence: `../evidence/QA-247/read-and-build.json`.

## Cause

Facts: (1) the QA-221 rule in `prompts/design/lead.md` covers "to compare or rank plant versions"; a sizing request on one stored plant is not covered, so the lead still rebuilds. (2) `read_plant(project_plant=...)` returns the resolved form (generated modules, full fluid records), which `build_plant` does not take back: the read is not round-trippable.

## Proposed fix

- geomind `prompts/design/lead.md`: "A project plant is a stored design already: `design/v<N>`. Size, range, simulate and optimize it directly; `build_plant` only for a new family." (all requests, not only compare/rank).
- geomind `tools/gemini/read_plant`: return the plant file as stored (the spec), and the resolved modules under a separate key, so a copy is buildable; or refuse `build_plant` of a plant equal to a stored one with "use design/v<N>".
- gemini (via Sahand): `build_plant` with `type` could ignore generated modules that match `size` instead of refusing.

## Fix

## Retest
