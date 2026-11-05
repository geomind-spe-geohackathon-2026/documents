# QA-260: patch_plant saves a class plant as a free plant without 'type' and 'size': the user's 2 doublets (build_plant size.doublets 2) become 1, and size_plant then returns doublets 1 with the range 2 to 2

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind,gemini |
| Reporter | QA-E2E-design-I |
| Found | 2026-11-05 18:04 UTC |
| Versions | backend 1.1.109, geomind 0.4.11x, gemini 0.6.17-0.6.19 (deploy at 18:01 UTC during the run) |
| Where | project QA-TEST QA-E2E-design-I 2 (72df9c82-e577-4605-8743-ffcee53c3a73); run dca5ed1a-35f5-4975-ad6e-94069b640590; design_lead 17:52-18:04 UTC |
| Fixer | hotfix-python-lead |

## Steps

1. Reference case loaded. Chat: "Design the plant for this case." Deny the first build card with "Start with 2 doublets instead of 1, and use backup peak" (QA-230 then blocked build_plant; the project lead restarted the design at 17:51).
2. Approve `build_plant` B_start: `{"type": "HeatingHeatPumpCoolingPlant", "size": {"doublets": {"value": 2}}, "params": {"backup": "peak", ...}}`.
3. Approve the patches (B_filled, B_ready_2), set_ranges, size_plant.

## Expected

The stored design keeps `type` HeatingHeatPumpCoolingPlant and `size.doublets` 2 through every patch; size_plant with `size.doublets` range 2 to 2 returns 2 doublets (or refuses).

## Actual

- `read_plant design/B_ready_2` (18:02:13): keys `kind, name, fluids, format, params, modules, connections`: **no `type`, no `size`**; modules `d0` only.
- `set_ranges` (18:03:06) answers `"size": {"doublets": {"range": {"max": 2, "min": 2}, "value": 1}}`.
- `size_plant` (18:03:25): `size.doublets` = **1** "1 doublet(s) of 14.48 MW each ... does not cover the heating peak of 30 MW", outside its own range 2-2; the lead notes "Sizing ran but chose 1 doublet (the user requires 2)".
- Round 1 (run 76d19df6, project QA-TEST QA-E2E-design-I 1): plant version 14 (best_v1) also has no `size` in `spec`; the Results row has `doublets` null.

## Evidence

Run log GET /api/v1/assistant/runs/dca5ed1a-35f5-4975-ad6e-94069b640590/log: build_plant 17:52:05, patch_plant 17:56:56 and 18:01:50, read_plant 18:02:13, set_ranges 18:03:06, size_plant 18:03:25.

## Cause

Guess: the patched design is written back as a free document (`type` and `size` dropped, as `backend/src/core/gemini/plant.py:305 free_document` does for the Plant page, QA-241), or geomind's patch writes `plant.to_dict(structure=True)`; a free plant has one doublet. size_plant then does not honour `range.min` of `size.doublets`.

## Proposed fix

1. geomind `tools/gemini/plants.py` patch_plant (and the store): keep `type` and `size` of a class plant in every saved design; test: build 2 doublets, patch a value, read_plant shows size.doublets 2.
2. gemini size_plant: never return a size outside the range of `size.doublets`; refuse with the reason instead.

## Fix

## Retest
