# QA-149: evaluate_module refuses 81 % of calls: inlets [] (103x), a control sent as a parameter (39x), and a missing fluid reported as 'invalid inlet source_in; valid names: source_in'

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind,gemini |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 16:41 UTC |
| Versions | Seen on geomind 0.4.87-0.4.91 (runs of 2026-11-05); the code is unchanged in geomind 0.4.96 / gemini 0.6.16 (live, backend 1.1.99) |
| Where | 42 runs of 2026-11-05; energy_systems_engineer, process and integration engineers, design_lead |
| Fixer | hotfix-python |

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

- 2026-11-05 16:56 UTC: gemini 0.6.17 (a872275d, tag v0.6.17), backend 1.1.103 (665763d), deployed 2026-11-05: reader skips non-port inlets values; tear without first guess names the loop's offering modules (Cooler loop_pressure and flow); inlet errors say 'inlet X: <error>'. QA-149 geomind part (control in parameters) already fixed since geomind 0.4.81. Not live-retested.
## Retest

## More evidence (QA-AI-design-I, 2026-11-05 17:04-17:24 UTC, geomind 0.4.98, gemini 0.6.16/0.6.17)

Run 0df89b7e-69e0-46b3-abe1-231e51d9570a (project QA-TEST QA-AI-design-I 1): the design lead's `evaluate_module` 11 of 14 refused:

- HeatPump: `sink_in` without m_dot (2x, the second flagged "second time in a row"); `inlets = []` with design only; `cop_model 'lorenz'` with `mode 'cooling'` (Lorenz defined for heating only).
- Pipe (8x, 17:20-17:23): `controls.flow` is not a control of Pipe; `dt` given for a stateless pipe; then 5x `missing_value length, inner_diameter, roughness, elevation_change` (the lead sent the stream but no `parameters` and no `design=`), 2 of them refused as `failed_before` exact repeats.
Evidence: `../evidence/QA-211/run-0df89b7e-tool-calls.txt` (design_lead #16-#19, #42-#52).
Proposed extra: when parameters are missing and the call names no design, the error should say "give parameters, or design='design/<name>' and the module key"; the skill `evaluating-a-module` should show one Pipe example.
