# QA-175: Plant issues come one stage at a time: build_plant lists 111 missing values, then each patch_plant reveals 1-4 new ones (well_diameter, chiller and cooler setpoints, injection_pump.frequency), 7 patch_plant to get a simulable plant

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | gemini,geomind |
| Reporter | QA-AI-design-I |
| Found | 2026-11-05 17:15 UTC |
| Versions | backend 1.1.102 at run start, 1.1.103 and 1.1.104 deployed during the run (geomind 0.4.98, gemini 0.6.16 then 0.6.17) |
| Where | api.geomind.team; project QA-TEST QA-AI-design-I 1 (b9ef5c9a-e030-4357-91ee-b17dabfdeaa6); chat efb95fd0-f997-4530-a314-f93baf64ef5f; run 0df89b7e-69e0-46b3-abe1-231e51d9570a; design_lead steps #5 (build_plant) and #21-#27 (patch_plant) |
| Fixer | hotfix-python-lead |

## Steps

1. As QA-174. The lead builds `HeatingHeatPumpCoolingPlant` once (`build_plant`, 16:50:58 UTC): 111 `missing_value` issues.
2. It splits all 111 paths among 4 engineers (`fill_parts`, one call, as the prompt says) and applies the 113 proposed changes in one `patch_plant` (QA-145 design: build once, patch once).

## Expected

`build_plant` lists every value the plant needs before it can simulate, so one `patch_plant` after the team gives `missing: 0` and the lead goes on to `size_plant` / `simulate` (prompt step 5).

## Actual

The plant write chain (`../evidence/QA-175/plant-writes.json`):

| UTC | Call | Changes | Result |
|---|---|---|---|
| 16:50:58 | build_plant start | - | 111 missing |
| 17:06:00 | patch_plant assembled | 113 | refused: choice values given as bare strings / lists (friction_correlation 'darcy_weisbach', segment 'below_esp', correction_factors [1, 0]) "expected an object like {'value': ...}", reported with code `missing_value` |
| 17:06:59 | patch_plant assembled | 113 | refused: unknown `params.d0.injector.segment`; `esp.head_coefficients` shape (0,) expected (6,) |
| 17:08:05 | patch_plant assembled | 110 | saved; NEW missing: `params.d0.well_diameter`, `nominal_flow`, `pump_efficiency`, `nominal_wellhead_pressure` (none were in build_plant's 111) |
| 17:08:55 | patch_plant complete | 5 | refused: changes[3] has no `value` |
| 17:09:18 | patch_plant complete | 5 | saved; NEW: `compression_chiller.temperature_setpoint` has no value (missing 1) |
| 17:09:41 | patch_plant ready | 1 | saved; NEW: `compression_cooler.temperature_setpoint` (missing 1) |
| 17:10:10 | patch_plant final_plant | 1 | saved; NEW: simulation inputs `injection_pump.frequency` expected a data column or a default (missing 1) |
| 17:11:4x | patch_plant built2, built3 ... | | still going when this was written |

7 patch_plant (3 refused) and 4 plant versions in 6 minutes, after 16 min of team work, and still no simulate; the lead hit its 30-step limit at 17:10:56 and asked the user to continue. Each discovery costs one LLM round trip of the lead at 40-60 k input tokens (5-58 s).

## Reproduced in run 2 (QA-AI-design-I, 17:31-17:41 UTC)

Run 5d0216a6-4acb-487b-a885-396a5e99366d (project QA-TEST QA-AI-design-I 2, compare loop, family C HeatingAbsorptionCoolingPlant): the same chain. build_plant 17:31:35 -> team -> patch_plant `filled` refused (bare string choice values) 17:38:26 -> `filled` saved, new missing `params.d0.well_diameter` ... 17:39:03 -> `complete`: `peak_boiler.temperature_setpoint` 17:40:29 -> `ready`: `absorption_chiller.temperature_setpoint` 17:40:38 -> `built`: invalid_binding (simulation input) 17:40:41 -> `ready2`: `absorption_cooler.fluid_out` tear stream 17:40:49 -> `ready3` missing 0 at 17:40:56. 7 patch_plant, 1 refused, 6 plant versions for one family; then the second family (B) starts the same chain at 17:42:00.

## Cause

Facts: gemini's plant check reports a stage at a time: the design-mode values of the doublet (`well_diameter`, `nominal_flow`, `pump_efficiency`, `nominal_wellhead_pressure`) only after `d0.depth` is set; schedule setpoints (`invalid_design`) only after `missing_value` is empty; simulation inputs (`invalid_binding`) only after the schedule is complete. The refusals are geomind/gemini shape checks on values the engineers returned in a free form (bare strings for choices).
Guess: `build_plant`/`patch_plant` stop at the first failing stage of gemini's validation instead of running every stage on what is known.

## Proposed fix

1. gemini (ask via Sahand, `gemini-requests.md`): the plant check returns every issue of every stage in one answer (missing parameters incl. the ones a design value will require, schedule setpoints, simulation inputs), each with its stage; or a `check(all_stages=True)` the geomind tool calls.
2. geomind `tools/gemini` patch_plant: wrap a bare scalar/string/list for a choice parameter as `{"value": x}` instead of refusing (the engineers do this every run), and report shape errors with code `invalid_input`, not `missing_value`.
3. geomind prompts `design/reservoir.md`, `design/energy.md`: show the exact change shape for a choice parameter (`{"value": "darcy_weisbach"}`) and "no coefficients: leave head/power coefficients out", not `[]`.
4. geomind `prompts/design/lead.md` step 4: after the one team patch, fill the remaining 1-4 values yourself in ONE patch_plant, never one per issue.

## Fix

- 2026-11-05 17:15 UTC: gemini part needs Sahand's OK (gemini-requests.md)
- 2026-11-05 18:09 UTC: deployed 19:01-19:03 CET: backend 1.1.112, geomind 0.4.118/0.4.119, gemini 0.6.19 (hotfix-python team)
- 2026-11-05 18:28 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
## Retest

## Retest on geomind 0.4.119 (QA-AI-design-I, 2026-11-05 18:35 UTC): improved, not one patch

Run 2b72af99-9161-4049-b192-4b12d6db9625 (project QA-TEST QA-AI-design-I 4, backend 1.1.112, the same request as run 0df89b7e, chat auto-approve). From build_plant (18:07:13) to `missing 0` (18:17:18): 5 patch_plant, 2 refused (18:13:52 `params.d0.permeability`/`thickness` are case values, not design values; 18:16:39 `injection_pump.efficiency = 0.7` without `{value}`), 3 saved. The team patch (18:14:50) left 1 missing (`compression_chiller.capacity`); the next one revealed a tear stream (`compression_cooler.fluid_out` has no first guess) that build_plant had not named. `simulate` (18:15:35) refused `injection_pump.frequency` as a parameter although patch_plant had accepted it. Before: 7-10 patch_plant per plant (runs 0df89b7e, 5d0216a6); now 5. Still open: the tear-stream stage and the parameter/control check of simulate are not in the first answer.
