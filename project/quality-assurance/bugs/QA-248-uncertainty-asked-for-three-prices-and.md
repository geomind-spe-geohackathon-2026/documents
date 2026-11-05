# QA-248: Uncertainty asked for three prices and P10/P50/P90: sample_uncertainty samples all six declared uncertainties (also discount rate, gradient, permeability) and gives only P5/P50/P95; the agent cannot do either

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | geomind,gemini |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 17:47 UTC |
| Versions | backend 1.1.108 |
| Where | project `QA-TEST QA-E2E-study-I 1` (8fcbf709-537a-40d9-ac1f-abadd1061775); chat c0cae905-a2a8-44cf-8bec-f4899f313e8b; run fd4b7e2c (cancelled by me after 40 s), run 01222f3a-43f3-4331-aa69-0e73a3cb8eea ("please continue") |
| Fixer | hotfix-python-lead |

## Steps

1. Chat: "Run an uncertainty study on the current plant: sample the gas, electricity and carbon
   prices over their ranges in the economics file and give me the P10, P50 and P90 of the cost of
   thermal supply." Cancel the run after 40 s (Cancel run: worked, cancelled in 13 s).
2. Chat: "Please continue the uncertainty study you started." (resume worked: 2 min 24 s, 14 steps,
   18 calls, 0.007 USD.)

## Expected

P10/P50/P90 of lcts with only the three prices varied (the user's request), or a clear one-line
offer to do exactly that.

## Actual

- `sample_uncertainty` (200 samples, seed 0) varies every uncertainty the case declares: the
  three prices plus economics.discount_rate, site.ground.gradient and site.reservoir.permeability;
  there is no `values` subset (sensitivity has one).
- It returns only mean, p5, p50, p95: "P10 and P90 do not exist in gemini's output ... I will not
  interpolate them". The user gets P5 40.65, P50 53.83, P95 68.21 EUR/MWh (15 digits each, QA-099).
- To restrict the draw the agent proposes a case change (remove three uncertainties), which would
  mark every study out of date.
- Accuracy: P50 53.83 vs the point value 49.28 EUR/MWh: the answer explains it by the triangular
  modes and the extra parameters, fair. The extra geology parameters make the spread wider than the
  question asked for.

## Evidence

- Run log: `../evidence/QA-248/run-01222f3a-log.json`.

## Cause

Fact: gemini's sample_uncertainty has no parameter subset and a fixed percentile list; the agent may
not compute numbers itself.

## Proposed fix

gemini (for Sahand's request list): `sample_uncertainty(values=[...], percentiles=[...])` like
sensitivity. Until then geomind: let the economist compute percentiles of the stored draws with one
`calculate`/`run_python` on the study's samples (a deterministic statistic of gemini's own draws,
labelled as such), and say in one line which parameters were varied.

## Fix

## Retest
