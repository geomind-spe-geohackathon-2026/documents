# QA-254: patch_plant crashes with IndexError at gemini modules/values.py:70 when a parameter is uninitialized but _missing_paths() lists nothing (patching d0.nominal_flow on a filled HeatingHeatPumpCoolingPlant)

| Field | Value |
|---|---|
| Status | verified |
| Severity | blocker |
| Area | gemini |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 17:58 UTC |
| Versions | backend 1.1.109 (geomind 0.4.110, gemini 0.6.17) |
| Where | https://geomind.team/projects/0b986dd6-8f95-4383-9d15-5e589ff122c9; run bfcec811-c5ad-496e-a829-6ec44de3251c (hackathon report run II), design_lead, 17:56-17:58 UTC |
| Fixer | |

## Steps

1. build_plant `A_hp_compression` (HeatingHeatPumpCoolingPlant, 1 doublet), then one patch_plant with 113 values -> `design/A_filled` (succeeds).
2. patch_plant on `design/A_filled` with `params.d0.nominal_flow` 300 m3/h (alone, or with `pump_efficiency` 0.7 and `nominal_wellhead_pressure` 10 bar).

## Expected

The patch is saved, or a `missing_value` error naming what is missing.

## Actual

`patch_plant: internal error IndexError: list index out of range at modules/values.py:70` on every try (list form and mapping form, 1 or 3 values). The design lead cannot set the design flow; the run is stuck before any study.

## Cause

Fact: `gemini/gemini/modules/module.py:392` `_parameter_value` raises `root._missing_error(root._missing_paths())` when a parameter is not initialized. `_missing_paths()` returns an empty list here (the parameter is not listed: probably a `_waiting_params` one derived from a design value), and `_missing_error` (`values.py:70`) reads `items[0]`, so an IndexError escapes instead of a ValidationError.
Fix: when `_missing_paths()` is empty, name the parameter itself (`self.path.name`) in the error; and find why the derived parameter is uninitialized after the 113-value patch (likely the ESP window or well sections derived from nominal_flow).

## Fix

## Retest

- 2026-11-05 18:03 UTC: Manual QA-IV 18:04 UTC on gemini 0.6.19: the same patch_plant (d0.nominal_flow on design/A_filled, run bfcec811) saves design/A_flow and lists missing values (pump_efficiency, nominal_wellhead_pressure) instead of IndexError

- 2026-11-05 QA-E2E-design-I: run dca5ed1a (project QA-TEST QA-E2E-design-I 2): patch_plant B_ready 17:57:22 UTC and size_plant B_sized 18:02:08 UTC, both "internal error IndexError: list index out of range at modules/values.py:70" (d0.nominal_flow missing). The 18:02:08 call was one minute after the 18:01 UTC deploy of 0.6.19, in a run started at 17:46: either the worker still had 0.6.17, or size_plant has the same crash path. To retest on a fresh run.
