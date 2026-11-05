# QA-248: Uncertainty asked for three prices and P10/P50/P90: sample_uncertainty samples all six declared uncertainties (also discount rate, gradient, permeability) and gives only P5/P50/P95; the agent cannot do either

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind,gemini |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 17:47 UTC |
| Versions | backend 1.1.108 |
| Where | project `QA-TEST QA-E2E-study-I 1` (8fcbf709-537a-40d9-ac1f-abadd1061775); chat c0cae905-a2a8-44cf-8bec-f4899f313e8b; run fd4b7e2c (cancelled by me after 40 s), run 01222f3a-43f3-4331-aa69-0e73a3cb8eea ("please continue") |
| Fixer | hotfix-python-lead-II |

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

- 2026-11-05 18:09 UTC: deployed 19:01-19:03 CET: backend 1.1.112, geomind 0.4.118/0.4.119, gemini 0.6.19 (hotfix-python team)
- 2026-11-05 18:28 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
- 2026-11-05 18:53 UTC: QA-E2E-study-I: values subset verified; P10/P90 still not available
- 2026-11-05 19:13 UTC: geomind main 71d80ab (0.4.131+), gemini dev 5782a138 (0.6.27); QA-312 also needs back-lead's DatabaseWorkspace.save_plant_version
- 2026-11-05 20:44 UTC: QA-E2E-study-II 2026-11-05 21:45 Trondheim, backend 1.1.125, geomind 0.4.13x REOPENED: project QA-TEST QA-E2E-study-II 1, chat bb245cd8, run daa590fc: 'Monte Carlo on the same three prices P10/P50/P90': the agent says gemini's sample_uncertainty ignores the values restriction (two spellings and a re-run, every attempt drew all seven declared uncertainties) and asked how to proceed; final answer P10/P50/P90 = 26.795/31.708/39.427 EUR/MWh is the all-seven range (study uncertainty-v3-prices, 200 draws, seed 42). So the earlier retest (run 00944350, 'three prices drawn') probably also drew all of them. Run took 25 min 50 s, 91 steps, 0.042 USD
## Retest

- 2026-11-05 18:47 UTC, QA-AI-analysis-I, backend 1.1.117: fresh project `QA-TEST QA-AI-analysis-I 8`
  (485dbcfc-63f4-474f-a2dd-b94ab85bc34f, reference case + HackathonPlant), same chat text, run
  8d7c09f7-3356-4e40-8c37-40fefeeacc1e. The economist called `sample_uncertainty(values=[economics.energy.gas,
  economics.energy.electricity, economics.carbon.price], samples=200, seed=42)` (37 s); each draw has exactly these 3
  parameters; discount rate, gradient and permeability held at the case values; no case change proposed. LCTS p5 40.84,
  p50 46.35, p95 51.57 EUR/MWh (point value 45.10). 1 min 31 s, 0.0071 USD. Verified for the subset (the title). Still
  open, filed as QA-299: P10 and P90 are not available ("gemini's Monte Carlo output carries only p5, p50 and p95"),
  and values are given with 15 digits (QA-099).
  Log: `../evidence/QA-248/run-8d7c09f7-retest-log.json`.
- 2026-11-05 18:48 UTC: retest QA-AI-analysis-I 18:47 UTC backend 1.1.117: only the 3 prices sampled; P10/P90 gap filed as QA-299
- 2026-11-05 19:51 UTC: QA-E2E-study-II 2026-11-05 retest in QA-TEST QA-E2E-study-II 1 (geomind 0.4.130 era, deploy 36): asked 3 prices + P10/P50/P90; got P10 45.92, P50 48.83, P90 52.73 (200 draws, seed 42), one question for the missing heat range (correct)
## Retest

QA-E2E-study-I, 2026-11-05 18:53 UTC, project QA-TEST QA-E2E-study-I 3, run ce4be675-134b-439a-a1cc-7e879acd7112 ("sample only the gas, electricity and carbon prices ... P10, P50 and P90"): half passes. The subset works: `varied` lists exactly the three prices, the discount rate stays 0.05 (2 min 36 s, 25 calls, 0 cards). Still fails: "P10 and P90 are not available: gemini sample_uncertainty reports only P5, P50 and P95"; and the figures are 15 digits (53.976480849763796; QA-099). Reopened for the percentiles.
