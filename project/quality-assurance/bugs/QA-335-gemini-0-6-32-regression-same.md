# QA-335: gemini 0.6.32 regression: same no-agent setup gives worse results than 0.6.26 (evolve best 37.64 vs 29.55 EUR/MWh, invalid structures 19 vs 12; FullCooling and HeatingCooling now fail cooling supply 20.0032 > 20 degC)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | blocker |
| Area | gemini |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 19:51 UTC |
| Versions | good: backend 1.1.118, gemini 0.6.26 (project 8d5d21e0, 19:56-20:05 CET); bad: backend 1.1.125, gemini 0.6.32 (project 0f909768, 20:48-20:52 CET) |
| Where | good https://geomind.team/projects/8d5d21e0-ecb0-4894-9cfd-bdd61f670ac7 ; bad https://geomind.team/projects/0f909768-7749-4cca-9974-f441aaffc216 |
| Fixer | m6 |

## Steps

Scripts (Python, run on the Dell, API via admin login; they read gemini's examples from a scratchpad copy, set SRC in s1.py/s1b.py to a `git archive <ref> examples` of gemini): `.claude/notes/sessions/manual-qa-3-tools/showcase-rerun/` (s1.py = helpers, clean.py / cleanb.py = new project + case (examples/hackathon_2026/case.json with economics.json inline, demand.csv as case file) + superstructure plant + 5 candidate plants + studies, clean2.py = wait for the evolve, save structure rank 1 as a plant, then sensitivity, sample, run).
Studies: evolve on HackathonSuperstructure (prepare size, objectives lcts+co2, 192 evaluations, population 16, seed 0, polish 0); minimize on HeatingFullCoolingPlant, HeatingHeatPumpCoolingPlant, HeatingCoolingPlant, HackathonPlant, HeatingAbsorptionCoolingPlant (prepare size, lcts, 40 evaluations, seed 0).

## Expected

Same or better results than on gemini 0.6.26.

## Actual

| | 0.6.26 (8d5d21e0) | 0.6.32 (0f909768) |
|---|---|---|
| evolve best | 29.55 EUR/MWh, 8.54 kt, 15/15 (no heat pump, boiler, absorption + compression) | 37.64 EUR/MWh, 13.29 kt, 15/15 (heat pump, boiler, absorption + adsorption + compression) |
| evolve invalid structures | 12 of 192 | 19 of 192 (29 structures listed) |
| HeatingAbsorptionCoolingPlant | 28.61, 15/15 | 27.57, 15/15 (better) |
| HeatingFullCoolingPlant | 30.67, 15/15 (2 doublets, 3,265 m) | 48.72, 22.5 kt, 9 pass 1 FAIL (1 doublet, 2,500 m) |
| HeatingCoolingPlant | 38.68, 20/20 (3 doublets) | 43.37, 16.2 kt, 9 pass 1 FAIL (1 doublet, 2,500 m) |
| HackathonPlant | 32.53 | 31.49 |
| HeatingHeatPumpCoolingPlant | 33.23 | 32.61 |

The failing check in both: `cooling_consumer.cooling_supply_temperature` 20.0032 degC against the limit 20 degC at 2027-07-19 (a 3 mK round-off on the cooling peak day). Guess: since 0.6.32 a compression-chiller supply that ends 3 mK above 20 degC fails the hard rule, so the search treats designs with a compression chiller at peak as infeasible: the evolve loses its 0.6.26 best (which has a compression chiller), more structures become invalid, and the two candidates fall back to 1 doublet. Look at the chiller setpoint control / cooling supply rule tolerance between 0.6.26 and 0.6.32.

## Fix

- 2026-11-05 19:56 UTC: gemini cb3160ba 0.6.33 reverts a5f3b5f1; pending deploy
## Retest
