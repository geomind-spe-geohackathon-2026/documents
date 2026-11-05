# QA-AI-analysis-I, round 2, 2026-11-05

Backend layer only (api.geomind.team, run logs). Versions moved from backend 1.1.105 to 1.1.112 (geomind up to 0.4.119,
gemini 0.6.19) during the round; deploys at ~17:45, ~18:05, ~18:25 UTC restarted live runs. Agents: deepseek v4.1 flash.
Projects (kept): `QA-TEST QA-AI-analysis-I 4` (six plant versions), `5` (no economics -> ask_economics), `6` (vague and
what-if requests), `7` (QA-205 retest); `1` and `3` reused.

## Retests

| Bug | Result | Run |
|---|---|---|
| QA-168 | verified: one `ask_economics`, approved values written, costs equal the reference (LCTS 45.102) | da297015, 4 min |
| QA-186 | verified: stale Knowledge sources dropped for changed keys (no "user" source recorded) | ce5d9ffc |
| QA-205 | verified: no trial-by-trial reading; answer on all 270 trials (no history summary) | 73ef62c4, 33 min (QA-221) |

## Showcase scenario through the agents vs gemini (no LLM)

| | Agents (run f548029f) | gemini |
|---|---|---|
| Wall time | 56 min 49 s, 0.168 USD, 7.0 M input tokens, 362 calls (54 refused) | page minimize of v1, v2, v4 in parallel: 46 s; showcase gm.Study 6 plants, 735 sims: 73 s |
| gemini compute inside the run | ~3 min (6 optimize 158 s, sizing 12 s, sensitivity 2 s, 5 draws 1 s) | |
| v1 HeatingFullCoolingPlant | 52.46 EUR/MWh, rank 6 (re-typed plant) | 32.38 (page, 0.6.19), 36.0 (showcase, 0.6.17), rank 1 |
| v2 HeatingHeatPumpCoolingPlant | 38.03, rank 1 | 38.03 / 38.0 |
| v3 HackathonPlant | 41.30 | 41.30 / 41.3 |
| v4 HeatingCoolingPlant | 44.30 | 38.16 / 41.9 |
| v5 HeatingAbsorptionCoolingPlant | 49.34 | 49.3 |
| v6 HeatingPlant | 44.62, infeasible (no cold) | 27.9, infeasible |
| Winner | v2 (wrong) | v1 |
| Sensitivity on the winner | 6 drivers, right tool, 2 s (on v2) | showcase on v1: gradient 18.3, discount 13.8, carbon 3.6, electricity 2.4, gas 1.6, permeability 1.4 |
| Monte Carlo 5 draws seed 1 | LCTS mean 41.81, p5 38.45, p95 46.74 (on v2) | showcase on v1: mean 42.1, p5 37.0, p95 51.5 |

Gap: the design lead re-types each stored plant instead of `design/v<N>` (QA-221); two re-typed plants differ from
the stored ones and come out 6-20 EUR/MWh worse, so the ranking and the winner are wrong (QA-278).

## Other scenarios

| Run | Request | Wall | Cost USD | Outcome |
|---|---|---|---|---|
| 10fe31e7 (P3) | set electricity 120, heat revenue 75, new costs | 37 min | 0.114 | right numbers (LCTS 47.914 = page study), far too slow (QA-258) |
| ce5d9ffc (P5) | discount 6 %, carbon 80, new LCTS/NPV | 15 min | 0.060 | right (47.937 = page study), slow (QA-258) |
| bf7b2f00 (P6) | "Is this plant a good investment?" | 4 min | 0.012 | good answer, but sensitivity on 2 of 6 drivers -> wrong "discount rate dominates" (QA-263) |
| e26ff474 (P6) | "LCTS with a discount rate of 8 %?" | 19 s | 0.0015 | right (50.911), reused the stored sensitivity study |
| ca876a33 (P6) | set analysis period 30 yr -> card denied | 4 min | 0.007 | guard forces a full catalogue economics question; question never answered (QA-268) |
| 1d250804 (P1) | compare baseline vs optimised (LCTS, CO2, capex, NPV, Pareto) | 1 min 45 s | 0.008 | right; `compare` cannot rank npv (noted) |
| 67af2520 (P6) | biggest cost, would a smaller heat pump lower LCTS? | 2 min 14 s | 0.009 | right, 4 simulations; found 39.21 at 5 MW < gemini's "optimum" 41.30 (QA-285) |

## Bugs filed this round

QA-221 (major), QA-258 (major), QA-259 (minor), QA-263 (major), QA-268 (major), QA-278 (major), QA-285 (major, gemini).
Retests: QA-168, QA-186, QA-205 verified.

## What works well

The analysis lead answers narrow questions fast and right (what-if from a stored study in 19 s; comparison 1.7 min;
heat-pump scan 2.2 min; costing with economics 75 s). Every gemini number the agents report matched a page study.
The slow and wrong cases all go through the project loop / design lead (re-typing stored plants, serial stages).
