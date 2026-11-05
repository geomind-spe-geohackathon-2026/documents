# QA-148: patch_plant crashes with TypeError (reader.py:190) when an inlets entry is a stream state; a chiller condenser loop has no way to get a tear-stream first guess

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | gemini |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 16:40 UTC |
| Versions | Seen on geomind 0.4.87-0.4.91 (runs of 2026-11-05); the code is unchanged in geomind 0.4.96 / gemini 0.6.16 (live, backend 1.1.99) |
| Where | run c801850b (2026-11-05 15:17 UTC, the latest design run, 'sahand test 2'), agents integration_engineer and design_lead, tool patch_plant |
| Fixer | |

## Steps

1. A HeatingHeatPumpCoolingPlant with a compression chiller whose condenser loop is closed: compression_chiller.sink -> compression_cooler -> back to the chiller.
2. simulate / check refuses: `invalid_design: tear stream compression_cooler.fluid_out has no first guess; expected a module of the loop that gives one`.
3. The agent tries to give the first guess in the plant file: `patch_plant(design="design/hp_cooling_ready", changes={"inlets": {"compression_cooler.fluid_out": {"T": {"unit":"degC","value":20}, "p": {"unit":"bar","value":4}, "fluid": {"kind":"water"}}}})`.

## Expected

Either a validation error that says what an `inlets` entry may hold, or a documented way to give a tear stream its first guess; and a chiller condenser loop that simulates (the compression cooler or the chiller gives the first guess).

## Actual

`patch_plant: internal error TypeError: unhashable type: 'dict' at _utils/reader.py:190` (2x). The design lead stopped: "I could not get the design to a sized, simulated state ... Blocker (one issue, gemini's own): compression_cooler.fluid_out invalid_design". No result, no check. The run ended without a design.

## Evidence

- Run c801850b log; the design lead's final answer names the blocker (finding-0ad89294).

## Cause

Fact: `gemini/gemini/plants/_utils/reader.py` `_ends()` (line ~187-192) does `ends |= set(named) if isinstance(named, list) else {named}`; a mapping value is unhashable, so a TypeError escapes instead of a ValidationError.
Fact: `gemini/gemini/plants/_utils/loops.py:_start` raises "has no first guess" when the module of the tear gives no `_loop_start` temperature; the compression cooler apparently gives none (guess).

Two parts: (a) the reader should refuse a non-port `inlets` value with a ValidationError; (b) a closed chiller condenser loop needs a first guess from its modules. Both are in gemini: per the rules, a gemini change needs Sahand's OK (list it in gemini-requests.md).

## Fix

- 2026-11-05 16:56 UTC: gemini 0.6.17 (a872275d, tag v0.6.17), backend 1.1.103 (665763d), deployed 2026-11-05: reader skips non-port inlets values; tear without first guess names the loop's offering modules (Cooler loop_pressure and flow); inlet errors say 'inlet X: <error>'. QA-149 geomind part (control in parameters) already fixed since geomind 0.4.81. Not live-retested.
## Retest
