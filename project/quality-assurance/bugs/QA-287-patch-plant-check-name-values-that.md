# QA-287: patch_plant/check name values that the study's size step derives (d0.esp.stage_count, esp.power_coefficients, injection_pump.pressure_setpoint) as missing, one per patch; the design lead chases them for 20 min and never starts the study

| Field | Value |
|---|---|
| Status | open |
| Severity | blocker |
| Area | geomind,gemini |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 18:35 UTC |
| Versions | backend 1.1.116 (geomind 0.4.124, gemini 0.6.19) |
| Where | run bfcec811-c5ad-496e-a829-6ec44de3251c, design_lead, 18:05-18:35 UTC |
| Fixer | |

## Steps

After set_ranges on design/A_setpoints the lead checks the plant with patch_plant; each answer names ONE missing value; the lead asks an engineer for it, patches, and the next answer names the next one:
1. `params.injection_pump.pressure_setpoint` missing -> patched 20 bar (A_plant).
2. `d0.esp.power_coefficients` missing (after stage_count 60 was set) -> stage_count set back to null (A_final_plant).
3. `d0.esp.stage_count` missing -> the lead then tries to remove the whole ESP (`esp: null`, denied).

## Expected

gemini's own sample plant (examples/hackathon_2026/plants/HeatingHeatPumpCoolingPlant.json) has `esp.pump_type` 'unspecified' with no stage_count and no curves; a study with `prepare: [size]` derives them from the design flow. patch_plant's check should not ask for values the size step derives (or say "derived by size"), and should list every missing value at once.

## Actual

The lead spends about 20 minutes and 6 approval cards on the ESP and the injection pump, and no study has started 37 minutes into the run.

## Cause

Guess: the check that patch_plant runs (QA-175) treats values derived by `size` (ESP stages and curves, injection pump setpoint) as missing design values; with stage_count given, the curves become required. geomind should check against "after size" (or let the study size first); gemini could mark these as size-derived.

## Fix

## Retest
