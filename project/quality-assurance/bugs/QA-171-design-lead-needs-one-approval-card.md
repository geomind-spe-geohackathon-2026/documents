# QA-171: Design lead needs one approval card and one plant version per missing setpoint: patch_plant's check reports the temperature_setpoint issues one at a time (heat pump, chiller, cooler, peak boiler), 6+ patch cards after the one full patch

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind,gemini |
| Reporter | QA-E2E-design-I |
| Found | 2026-11-05 17:13 UTC |
| Versions | frontend 1.1.113, backend 1.1.104, geomind 0.4.97, gemini 0.6.16 |
| Where | https://geomind.team/projects/f1704a61-f1b8-4b63-84d3-20bd30beaed7/assistant/chat/cd332dde-7afa-4865-8a75-d8f6d4be6354; project QA-TEST QA-E2E-design-I 1; run 76d19df6-485f-46ee-a182-6b03ed70ab33; design_lead 17:04-17:13 UTC |
| Fixer | hotfix-python-lead |

## Steps

1. Reference case, economics and demand of `gemini/examples/hackathon_2026/` loaded (case v3, nothing missing).
2. Chat: design a heating and cooling plant (1-3 doublets, 50-300 m3/h, <= 40 K, 100 / 20 degC).
3. Approve build_plant (HeatingHeatPumpCoolingPlant, 2 doublets), then every patch_plant card.

## Expected

QA-145: the engineers propose, the lead writes ONE patch_plant with every value. The check after it names every value simulate still needs, so at most one more patch is needed.

## Actual

After the full patch the lead needed **7 more patch_plant calls, each its own approval card and plant version** (v1 to v9), because each check returned exactly one new issue:

| UTC | Saves | Changes | Issue the check returned next |
|---|---|---|---|
| 17:04:41, 17:05:14 | (refused) | 99 | bare values not wrapped `{value}`; ESP coefficients of shape (0,) |
| 17:06:10 | v1 | 99 | 7 missing: friction correlations (well, riser, injector), injection_pump.pump_type |
| 17:08:22 | v2 | 7 | `heat_pump.temperature_setpoint` has no value |
| 17:09:06 | v3 | 1 | `compression_chiller.temperature_setpoint` |
| 17:09:52 | v4 | 1 | `compression_cooler.temperature_setpoint` |
| 17:10:26 | v5 | 1 | `peak_boiler.temperature_setpoint` |
| 17:11:35 | v6 | 1 | `simulation inputs = injection_pump.frequency; expected a data column or a default` |
| 17:12:00 | v7 | 2 | tear stream `compression_cooler.fluid_out` has no first guess (loop_pressure, flow) |
| 17:12:14 | v8 | 2 | missing `efficiency` (injection pump) |
| 17:12:30 | v9 | 1 | none |

Then the run hit the 30-step limit question (17:13:02, "continue with 30 more, or stop") before any simulate. Run time to a checkable plant: 21 min; 1.77 M input tokens, 0.062 USD at 17:13. The user clicks 9 approval cards for one design and gets 9 plant versions of which 8 are unsimulatable.

The setpoints follow from the case alone (100 degC heating supply, 20 degC cooling supply); none of the four engineers set them, and the handbook's design values table does not ask for them (guess: `inputs/handbook-design.md` ch 0.7).

## Evidence

- `../evidence/QA-171/approval-cards.jsonl`: the patch_plant cards the user approved (17:11-17:13).
- Run log at 17:10: `../evidence/QA-169/run-76d19df6-log-1710.json.gz` (patch_plant inputs and outputs, `issues`).

## Cause

- `geomind/geomind/tools/gemini/plants.py:314` `plant_issues`: `gm.check(plant, case)` and `rule_issues` do not list the schedule setpoints; only `run_issues` (a run of one step) finds them, and a run stops at the first `ValidationError`, so each round finds one (fact from the code path; the one-at-a-time behaviour seen in the log).
- `gemini/gemini/engine/schedule/fleet.py:64` `setpoint` raises for one unit at a time.
- The engineers' briefs (fill_parts) and the handbook name no setpoints, injection pump controls or cooler loop values.

## Proposed fix

1. gemini (needs Sahand's OK, list in gemini-requests): `gm.check` (or a schedule pre-check) lists every missing supply setpoint, every simulation input with no column or default, and every tear stream with no first guess, all at once, as `missing` issues with their paths.
2. Until then, geomind `rule_issues` in `plants.py`: enumerate every heat pump, chiller, peak boiler and cooler of the plant and add a missing issue for each `temperature_setpoint` that is None, before `run_issues`.
3. Handbook-design ch 0.7 / ch 0.3 module groups: list `temperature_setpoint` of each supply unit (= the case supply temperature), `injection_pump.frequency`, `pressure_setpoint`, `efficiency`, cooler `loop_pressure` and `flow`, so the engineers propose them in the first patch.
4. When several issues remain, the lead sends one patch with all of them (prompt rule already stated for QA-145; it held only for the first patch).

## Fix

## Retest
