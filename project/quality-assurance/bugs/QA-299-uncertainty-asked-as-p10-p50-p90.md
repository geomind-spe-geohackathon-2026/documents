# QA-299: Uncertainty asked as P10/P50/P90: sample_uncertainty returns only p5/p50/p95, so the agent gives P5/P95 and says P10 and P90 do not exist; values come with 15 digits

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | gemini |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 18:47 UTC |
| Versions | backend 1.1.117 (gemini 0.6.21+), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 8` (485dbcfc-63f4-474f-a2dd-b94ab85bc34f); run 8d7c09f7-3356-4e40-8c37-40fefeeacc1e |
| Fixer | hotfix-python-lead-II |

## Steps

1. Reference case + HackathonPlant. Chat: "Run an uncertainty study on the current plant: sample the gas, electricity and
   carbon prices over their ranges in the economics file and give me the P10, P50 and P90 of the cost of thermal supply."

## Expected

P10, P50 and P90 of LCTS (P10/P90 is the usual reporting band in geothermal resource and cost studies).

## Actual

The study runs right (only the three prices, 200 draws, seed 42). The answer: "gemini does not produce P10 and P90: its
Monte Carlo output carries only p5, p50 and p95 ... the 10th and 90th percentiles are not available from gemini, and I
have not computed them myself", then p5 40.84453095568741, p50 46.34714771797602, p95 51.570972388640115 EUR/MWh (15
digits, QA-099). The 200 draws are stored, so the percentiles exist in the data; the agents are (rightly) not allowed to
compute them.

## Evidence

- `../evidence/QA-248/run-8d7c09f7-retest-log.json` (economist sample_uncertainty output: summary keys mean, p5, p50,
  p95, failed).

## Cause

`gm.study.sample` summary gives fixed percentiles (p5, p50, p95); geomind's `sample_uncertainty` passes it through.

## Proposed fix

gemini: the sample summary takes `percentiles` (default [5, 10, 50, 90, 95]) or always adds p10 and p90; geomind
`sample_uncertainty` passes a `percentiles` input and the display rounds to 4 significant digits (QA-099).

## Fix

- 2026-11-05 19:12 UTC: geomind main 71d80ab (0.4.131+), gemini dev 5782a138 (0.6.27); QA-312 also needs back-lead's DatabaseWorkspace.save_plant_version

## Retest

- 2026-11-05 19:53 UTC, QA-AI-analysis-I, backend 1.1.124: project `QA-TEST QA-AI-analysis-I 8`, run
  20bd2c15-1af8-4372-a47f-a32d054f339e: still p5/p50/p95 only ("gemini cannot give P10 and P90"), but now rounded to 5
  digits (40.845 / 46.347 / 51.571 EUR/MWh). STATUS says gemini 0.6.27 (the fix) was pushed, not deployed, at 20:20 CET,
  so this is not a failed retest; to retest once gemini 0.6.27+ is live.
