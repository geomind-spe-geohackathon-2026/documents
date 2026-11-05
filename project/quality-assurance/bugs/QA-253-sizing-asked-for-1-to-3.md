# QA-253: Sizing asked for 1 to 3 doublets, the search covers only 1 to 2: set_ranges refuses d2.nominal_flow on the 2-doublet stored plant, the lead narrows size.doublets to max 2 without telling the user

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind,gemini |
| Reporter | QA-AI-design-I |
| Found | 2026-11-05 18:00 UTC |
| Versions | backend 1.1.109 (geomind 0.4.110, gemini 0.6.17) |
| Where | api.geomind.team; project QA-TEST QA-AI-design-I 3 (ef781ee9-4a2a-4e11-9228-f5965f372680); chat 25e27df1-fff2-434f-87b3-bdbf1917957e; run 5e847cc6-14af-4f05-a34f-5b3cb10fdb2e; design_lead 17:46:42-17:47:55 UTC |
| Fixer | hotfix-python-lead |

## Steps

1. Reference case + economics; gemini's `plants/HeatingHeatPumpCoolingPlant.json` stored as plant version 1 (2 doublets, `size.doublets` range 1-3).
2. "Size the stored plant for this case: choose the number of doublets (1 to 3) and the heat pump and boiler sizes for the lowest LCTS, keeping every hard limit."

## Expected

One `set_ranges` with `size.doublets` 1-3 (the challenge's design variable, the user's words, and the plant's own range), and the optimizer searches 1, 2 and 3 doublets.

## Actual

- 17:46:42 `set_ranges` with `size.doublets` 1-3 and `d0/d1/d2.nominal_flow` 50-300 m3/h -> refused: "unknown path 'd2.nominal_flow'; valid: size.doublets, ..., d0.nominal_flow, ..." (d2 exists only once size.doublets is 3).
- 17:47:55 the lead resends with `size.doublets` **1 to 2** (and d0/d1 only): accepted. `optimize` (40 evaluations) and `run_study compare_doublets` rank 1 vs 2 doublets only.
- The answer says "The LCTS search ... minimised over doublet count, flow, depth, heat pump, boiler and chiller capacity" and lists 1 and 2 doublets; it never says 3 doublets were left out.

The result (1 doublet, LCTS 37.97 EUR/MWh, feasible) may still be the optimum, but the user's search space was cut silently.

## Cause

Facts: gemini's set_ranges validates per-doublet paths against the plant's current module set; the lead's fix for the refusal was to shrink the range, not to drop the `d2.*` path.

## Proposed fix

- gemini (via Sahand) / geomind `tools/gemini/set_ranges`: accept a range on `dN.<path>` (or a shared `doublet.<path>`) that applies to every doublet the search creates, so 3 doublets can carry a flow range.
- geomind `prompts/design/lead.md`: never narrow a range the user or the case gave; when a path is refused, drop that path and keep the range; say in the answer what was searched.

## Fix

- 2026-11-05 18:34 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
## Retest
