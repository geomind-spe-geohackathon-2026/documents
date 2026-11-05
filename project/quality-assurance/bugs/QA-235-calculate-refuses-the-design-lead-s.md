# QA-235: calculate refuses the design lead's first two forms every run (bare numbers, a nested operation, {value, unit}): 87 degC reservoir temperature takes 4 calls, 2 refused, ~30 s, in both design runs

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-design-I |
| Found | 2026-11-05 17:45 UTC |
| Versions | backend 1.1.102-1.1.106 (geomind 0.4.98, gemini 0.6.16/0.6.17) |
| Where | api.geomind.team; run 0df89b7e-69e0-46b3-abe1-231e51d9570a (project QA-TEST QA-AI-design-I 1) design_lead #6-#9; run 5d0216a6-4acb-487b-a885-396a5e99366d (project QA-TEST QA-AI-design-I 2) design_lead 17:30:15-17:30:40 and 17:40:05 |
| Fixer | |

## Steps

1. A design run on the reference case; the lead computes the reservoir temperature at 2500 m for the engineers' briefs (its prompt asks for interface values).

## Expected

One `calculate` call: `12 degC + 30 K/km x 2500 m = 87 degC`.

## Actual

The same sequence in both runs (temperature 0, so it repeats every run; `../evidence/QA-235/calculate-calls.json`):

1. `operands: [12, {operation: multiply, operands: [30, 2.5]}]` -> refused: operands[0] = 12, expected an object.
2. `operands: [{case: site.ground.surface_temperature}, {operation: multiply, operands: [...]}]` -> refused: a nested operation is not an operand.
3. multiply alone -> C289b07 75 K; 4. add -> 87 degC.

Run 2 again at 17:40:05: `operands: [{value: 300, unit: m3/h}, ...]` refused (expected `number`, not `value`), then accepted with `number`. 3 of 9 calculate calls refused in the two runs, each a lead round trip at 35-53 k input tokens (2-13 s).

## Cause

Fact: geomind `tools/calculate` takes only flat operands of the reference kinds; the `{value, unit}` shape that every other tool uses is refused, and so is a nested operation. The `calculator` skill comes only with the first (failed) result.

## Proposed fix

geomind `tools/calculate`: accept a nested `{operation, operands}` operand (store each node as its own calculation, so the sources stay traceable), and accept `{value, unit}` as an alias of `{number, unit}`. Or put the two-line form in the tool's description so the first call is right. Separately: the doublet takes its reservoir temperature from the case once `d0.depth` is set, so the lead could read it from gemini instead of computing it.

## Fix

- 2026-11-05 18:53 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest
