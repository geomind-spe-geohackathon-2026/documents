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
| Fixer | m8 |

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

- 2026-11-05 18:33 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
- 2026-11-05 19:34 UTC: QA-E2E-design-I retest: patch size.doublets accepted but stays 1 (14 tries), size_plant ignores range 3-3; run e3c10ff9
## Retest

Retest (QA-E2E-design-I, 2026-11-05 19:30 UTC, backend 1.1.117): FAILS. Project QA-TEST QA-E2E-design-I 3, run e3c10ff9-933a-4ab4-abf5-591d4f2d63f8: "compare the kept design with 2 and 3 doublets at 300 m3/h each; keep the doublet counts exactly". The design lead patched `size.doublets` on design/hc_wellfix 14 times in 4 forms (19:16:53-19:20:52: `{"value": 3}`, `3`, `{"size": {"doublets": {"value": 3}}}`, with a range 3-3); each patch "reported success but the stored plant still shows size.doublets = 1" (lead, 19:18:00). `set_ranges` size.doublets 3 to 3 then `size_plant` "ignored the fixed range and kept 1 doublet" (19:19:32). It reached 2 and 3 doublets only by building free plants with explicit d1/d2, mixers and splitters (19:20:10 build_plant, 19:24:03 patch with `size` null). 8 min and ~25 calls for a doublet count. The comparison then ran (1/2/3 doublets feasible).
