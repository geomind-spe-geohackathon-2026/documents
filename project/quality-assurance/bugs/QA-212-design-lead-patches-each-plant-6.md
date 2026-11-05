# QA-212: Design lead patches each plant 6+ times, often one value per call (filled, ready, ok, v1, v2, v3, fix1): 13 patch_plant approval cards in 20 min; QA-145 meant one build and one patch

| Field | Value |
|---|---|
| Status | open |
| Severity | blocker |
| Area | geomind |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 17:29 UTC |
| Versions | backend 1.1.104 (geomind 0.4.98, gemini 0.6.17) |
| Where | https://geomind.team/projects/fcc641c0-0119-4182-9a72-adce5a17b3ed; run d4ab496f-4a1f-43fa-b760-0f550fda0714 (hackathon report run), design stage 17:07-17:29 UTC |
| Fixer | hotfix-python-lead |

## Steps

Design request with two configurations; the design lead asks the engineers (fill_parts), then writes the plants.

## Expected

QA-145 (geomind 0.4.96): engineers propose, the lead builds once and patches once with all the proposals, so one or two approval cards per configuration before the search.

## Actual

Per configuration the lead saved 6+ versions, many with one or two values each:
- hp_2500 -> hp_2500_filled (12 values) -> hp_2500_ready -> hp_2500_ok (1 value: chiller setpoint) -> hp_2500_v1 (1 value: cooler setpoint) -> hp_2500_v2 (1 value: injection pump frequency) -> hp_2500_v3 (2 values: cooler loop) -> hp_fix1 (3 values).
- abs_3500 the same in parallel.
13 patch_plant approval cards between 17:13 and 17:29 UTC, each one more round for the user. The values of the later patches (setpoints from the case, cooler approach, pump frequency) were known from the engineers' findings at the first patch.
The cards are in `../evidence/QA-212/cards.md`.

## Cause

Guess: the lead patches after each refusal of `check`/`simulate` (one missing value at a time) instead of reading every missing value at once (gemini's check lists them all) and patching once; or the engineers' couplings are applied one per call.

## Fix

- 2026-11-05 17:32 UTC: raised to blocker by Sahand 17:32 UTC: report run has 15 plants and no study after 30 min; lead also started a hand-sized build (hp_2500_v4)
- 2026-11-05 17:39 UTC: geomind 0.4.109, commit 03046e7, deployed (backend 1.1.107): design lead prompt goes from first filled build to one set_ranges, size_plant, one optimize per configuration; one patch per round
- 2026-11-05 17:44 UTC: QA-AI-design-I retest 17:50 UTC: 7 patch_plant per plant on the new prompt (run 5d0216a6); needs QA-175 (gemini all-stage check)
- 2026-11-05 18:09 UTC: deployed 19:01-19:03 CET: backend 1.1.112, geomind 0.4.118/0.4.119, gemini 0.6.19 (hotfix-python team)
- 2026-11-05 18:29 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
- 2026-11-05 18:33 UTC: Manual QA-IV 18:33 UTC: 113-value patch works, but 5 small follow-up patches remain for one configuration (setpoints, ESP stages, injection pressure) even with QA-175 live
- 2026-11-05 18:34 UTC: QA-AI-design-I retest on 0.4.119 (run 2b72af99): 5 patch_plant (2 refused) instead of 7-10; tear stream and simulate's control check still come later
## Retest

## Retest: not fixed (QA-AI-design-I, 2026-11-05 17:50 UTC)

Run 5d0216a6-4acb-487b-a885-396a5e99366d (project QA-TEST QA-AI-design-I 2, compare loop, chat auto-approve on). The run started 17:30 UTC on the old code, was resumed after the 17:33-17:39 UTC deploys, and from 17:38:17 UTC the design lead's system prompt is the new one (it has "Write ONCE ... ONE patch_plant", "ONE set_ranges", "all in ONE patch_plant per round": geomind 0.4.109 or later). With that prompt, family C (HeatingHeatPumpCoolingPlant -> HeatingAbsorptionCoolingPlant) still took 7 patch_plant in 2.5 min, 1 refused:

| UTC | Name | Result |
|---|---|---|
| 17:38:26 | C_direct_absorption_filled | refused: choice values as bare strings |
| 17:39:03 | C_direct_absorption_filled | saved; new missing `params.d0.well_diameter` and the doublet design values |
| 17:40:29 | C_direct_absorption_complete | new: `peak_boiler.temperature_setpoint` |
| 17:40:38 | C_direct_absorption_ready | new: `absorption_chiller.temperature_setpoint` |
| 17:40:41 | C_direct_absorption_built | new: invalid_binding (simulation input) |
| 17:40:49 | C_direct_absorption_ready2 | new: `absorption_cooler.fluid_out` tear stream |
| 17:40:56 | C_direct_absorption_ready3 | missing 0 |

The prompt cannot fix this alone: each patch is a correct "one patch per round", because gemini names the next stage's missing values only after the current stage passes (QA-175, with the table of run 0df89b7e). The fix needs gemini's check to report all stages at once, or geomind's patch_plant to run the later stages (schedule, bindings, tear streams) on the patched plant and return all their issues together. Evidence: `../evidence/QA-236/run-5d0216a6-tool-calls-partial.txt`.

## Retest 2026-11-05 18:33 UTC (Manual QA-IV), run bfcec811, geomind 0.4.119-0.4.124 (QA-175 live)

Better but not done. The lead wrote A_filled with 113 values in one patch (good), but after that: A_flow (1 value, nominal_flow, partly QA-254), A_ready (2), A_setpoints (4 setpoints), then after set_ranges A_complete (1: d0.esp.stage_count) and A_plant (1: injection_pump.pressure_setpoint). Setpoints, ESP stage count and injection pressure are all known before the first patch; they should be in it, or in one patch after one check. 7 patch/build cards for one configuration.

## Retest on geomind 0.4.119 (QA-AI-design-I, 2026-11-05 18:35 UTC): improved, not one patch

Run 2b72af99-9161-4049-b192-4b12d6db9625 (project QA-TEST QA-AI-design-I 4, backend 1.1.112, the same request as run 0df89b7e, chat auto-approve). From build_plant (18:07:13) to `missing 0` (18:17:18): 5 patch_plant, 2 refused (18:13:52 `params.d0.permeability`/`thickness` are case values, not design values; 18:16:39 `injection_pump.efficiency = 0.7` without `{value}`), 3 saved. The team patch (18:14:50) left 1 missing (`compression_chiller.capacity`); the next one revealed a tear stream (`compression_cooler.fluid_out` has no first guess) that build_plant had not named. `simulate` (18:15:35) refused `injection_pump.frequency` as a parameter although patch_plant had accepted it. Before: 7-10 patch_plant per plant (runs 0df89b7e, 5d0216a6); now 5. Still open: the tear-stream stage and the parameter/control check of simulate are not in the first answer.
