# QA-083: gemini 'internal error' (no detail) from build_plant, patch_plant and simulate: a plant with degasser+gas_makeup+flare+atmosphere, the ESP flow window, nominal_wellhead_pressure; 17 internal errors in one run, no design stored

| Field | Value |
|---|---|
| Status | fixing |
| Severity | blocker |
| Area | gemini |
| Reporter | functional-qa-3 |
| Found | 2026-11-05 06:06 UTC |
| Versions | backend 1.1.74 (geomind 0.4.69, gemini 0.6.8); frontend 1.1.71 |
| Where | project QA2 functional-qa-3 studies (932b318c-f285-4827-aefe-c8fa3327735b), chat 510ab94f-c4f7-4019-9f75-cb40229b374e, run eb7b95df (a 'go on' after QA-081; cancelled by me after about 35 min, 5.1M tokens in) |
| Fixer | hotfix-python |

## Steps

1. Project with the competition PDF and CSVs, case built by the agents (questions answered, see QA-081), then 'go on'.
2. The design team builds the plant; open the run JSON, tool_calls with error code 'internal'.

## Expected

A built or patched plant, or a precise error naming the path (gemini's own errors name the path, e.g. missing_value).

## Actual

17 tool calls in run eb7b95df return `{'error': {'code': 'internal', 'message': '<tool>: internal error', 'path': None}}`:
- `build_plant` (process_engineer, steps 5-9) of a free plant with modules Doublet, Flare, Degasser, Atmosphere, GasMakeup, Boiler, inlet `grid_gas`; minimal repro the agent found (name `t2`): modules `flare` (Flare), `degasser` (Degasser), `atmosphere` (Atmosphere), `gas_makeup` (GasMakeup); inlet `grid_gas: gas`; connections degasser.gas_out->gas_makeup.gas_in, gas_makeup.excess_out->flare.gas_in, flare.flue_out->atmosphere.gas_in. The same file without gas_makeup and flare builds.
- `patch_plant` (well_engineer, design_lead) with `changes.params.d0.esp.{minimum_flow,maximum_flow,best_efficiency_flow}` in m3/h: any two of the three store, the third raises internal; also `params.d0.nominal_wellhead_pressure = 6 bar` and `bar(g)`; and `params.d0 {nominal_flow 300 m3/h, well_diameter 0.2 m, pump_efficiency 0.75, nominal_wellhead_pressure 6 bar}`.
- `simulate` (design_lead) of design/GEMINI2027_merged with changes d0 nominal_flow 300 m3/h, well_diameter 0.2 m, pump_efficiency 0.75, nominal_wellhead_pressure 6 bar.
The agents then loop for 35 min on workarounds (the same sentence 'the internal error is isolated...' repeated), no design is stored, 5.1M tokens burnt. The message has no path or cause, so the agent cannot fix it itself. (A real traceback must be in the worker log; gemini errors should be one of its 7 classes with a code.)

## Evidence

- ![screenshot](../evidence/QA-083/1.png)
- Run JSON (gzip): `../evidence/QA-083/run-eb7b95df.json.gz`

## Cause

Guess: an uncaught exception in gemini 0.6.8 (new in 0.6.7/0.6.8, since QA-076/QA-080 work) is caught by geomind's generic handler and turned into 'internal'; the worker log has the traceback.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
