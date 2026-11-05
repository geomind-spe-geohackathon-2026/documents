# QA-AI-analysis-I, round 3, 2026-11-05 (18:45-20:00 UTC)

Backend 1.1.117 -> 1.1.125 (geomind 0.4.130/0.4.131, gemini 0.6.26-0.6.31) during the round. API only.
New projects (kept): `QA-TEST QA-AI-analysis-I 8`-`15`.

## Retests

| Bug | Result | Evidence run | Note |
|---|---|---|---|
| QA-248 | verified | 8d7c09f7 | only the 3 prices sampled; P10/P90 gap -> QA-299 |
| QA-263 | verified | 0e4bfd2f, 486f038f | sensitivity of all six drivers, ranking = page study |
| QA-258 | verified | ac818659 | 3 min after the case change (was 15) |
| QA-259 | reopened 18:52, verified 19:55 | d87fcde1, 59cc8385 | ranges offered and written |
| QA-195 | verified | bbff4ad3 | no false user-confirmed seed |
| QA-285 | verified | page study bcf4fef1 | HackathonPlant optimum 32.535 EUR/MWh (was 41.30) |
| QA-221 | verified | 923b728e | design/v1..v6 used directly, 14 min (was 57) |
| QA-268 | verified | edaad491 | denial respected; what-if copy missing -> IMP-034 |
| QA-154 | verified | 6c88bb13 | kind change with std null accepted |
| QA-159 | verified | 676a19e1 | economist 3 calls |
| QA-155 | verified | code + 5 runs | text citation path not hit live |
| QA-179 | reopened | 1fba1e30 | analysis lead 7 min, 28 steps, 9 refusals for 4 s of gemini |
| QA-278 | reopened | 923b728e, e766608e | geomind run_study on design/vN: v1 52.8, v4 43.8; page minimize: v1 32.3, v4 39.5 (same ranges) |
| QA-299 | waits | 20bd2c15 | gemini 0.6.27 not deployed at retest |
| QA-332 | verified | study 4423e81a | minimize done in 10 s |
| QA-313 | verified | report b7af0082 (md) | structure, captions, text; gaps -> QA-338 |
| QA-323 | verified | same report | produced gas burned shown |
| QA-325 | verified | same report | checks scope stated |

## New scenarios

| Run | Request | Wall | USD | Outcome |
|---|---|---|---|---|
| 511a6821 | CO2 per MWh, grid vs produced gas | 1 min 38 s | 0.0053 | right (101.7 g/kWh; 8.02 kt grid, 4.90 kt fuel) |
| 1fba1e30 | optimise (30, seed 0) then sensitivity of the optimum | 11 min | 0.042 | right (32.535; six drivers, gradient 20.46 first), slow (QA-179) |
| 1d250804 (round 2 end) | compare baseline vs optimum | 1 min 45 s | 0.008 | right |
| 67af2520 (round 2 end) | smaller heat pump? | 2 min 14 s | 0.009 | found the optimiser gap (QA-285) |

## New bugs and ideas

QA-299 (minor, gemini, P10/P90), QA-338 (minor, backend, report studies section), IMP-034 (what-if costing).

## Open from this thread

QA-179 (minor), QA-278 (major, geomind/gemini), QA-299 (waits for deploy), QA-338 (minor).
