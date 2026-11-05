# QA-149: evaluate_module refuses 81 % of calls: inlets [] (103x), a control sent as a parameter (39x), and a missing fluid reported as 'invalid inlet source_in; valid names: source_in'

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind,gemini |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 16:41 UTC |
| Versions | Seen on geomind 0.4.87-0.4.91 (runs of 2026-11-05); the code is unchanged in geomind 0.4.96 / gemini 0.6.16 (live, backend 1.1.99) |
| Where | 42 runs of 2026-11-05; energy_systems_engineer, process and integration engineers, design_lead |
| Fixer | |

## Steps

An engineer evaluates one module with `evaluate_module` while sizing a plant.

## Expected

Most calls succeed; a refusal names the real problem once, so the next call is right.

## Actual

377 calls, 305 refused (81 %). The clusters (tool.py 2026-11-05 evaluate_module):
- 103x `inlets = []; HeatPump needs the stream inlets source_in, sink_in ...` (also AbsorptionUnit 20x): the agent gives no stream state.
- 39x `parameters.temperature_setpoint is a control, not a parameter; give it in controls`.
- 19x `X: invalid inlet 'source_in'; valid names: source_in, sink_in: Stream.fluid: no value` and 22x `pipe: invalid inlet 'air_in'; valid names: fluid_in, air_in: ... A gas fluid needs gas_composition`: the name IS valid; the real problem (no fluid, no gas composition) is at the end, after a list that says the name is wrong.
- 8x `unknown module type` (e.g. heat_pump vs HeatPump).

## Evidence

Run logs as in QA-147; speed baseline causes 2 and 6 (documents/project/plans/speed-case-plant-baseline.md).

## Cause

- geomind (`tools/gemini/catalogue.py:99`): with `design=`/`result=` known, the tool could fill inlets from the plant or result instead of refusing (QA-143 did it only for a class the design holds once); a known control under `parameters` could be moved to `controls` with a note; module type could match ignoring case/underscores.
- gemini (`gemini/modules/callargs.py:172-174`): the message for a value error says "invalid inlet 'X'; valid names: ..." even when X is valid; it should say "inlet 'X': <the value error>" and list names only for an unknown name. Needs Sahand's OK (gemini request).

Note: since geomind 0.4.96 (QA-145) the design engineers no longer call plant tools; check on the next live run whether they still call evaluate_module and how often it is refused.

## Fix

## Retest
