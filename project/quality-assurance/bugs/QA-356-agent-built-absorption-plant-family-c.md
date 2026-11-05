# QA-356: Agent-built absorption plant (family C, 3 doublets at 2,500 m) fails 365 of 365 steps (brine/injection stream p = -62067 Pa; drive loop no convergence) after two repairs; gemini's sample absorption plant runs fine

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | Sahand (screenshot), Manual QA-IV |
| Found | 2026-11-05 21:13 UTC |
| Versions | backend 1.1.130 (geomind 0.4.135, gemini 0.6.34) |
| Where | project e7dd5fb1-4fb5-477e-969a-9378a3ba803f, run 86867082, result 8d0e2821-d56c-410c-8379-2c62afcb4d0b (c-direct-boiler-absorption), also 682d2b1d, 0fed388c |
| Fixer | hotfix-python-lead-II |

## Expected

An absorption-cooling design the agent builds runs like gemini's sample HeatingAbsorptionCoolingPlant (2 doublets, 3,250 m: LCTS 28.6, 15/15 on the same case).

## Actual

The agent's family C (3 doublets at 2,500 m) fails all 365 steps: 357 x out_of_range "Stream: p = -62067.2 Pa; expected p >= 0" in the brine/injection path, 8 x no_convergence at drive_mixer.fluid_out (absorption drive loop). Two repair rounds (section geometry, degasser outlet 10 bar, design flows at 1030 kg/m3, chiller 10 -> 5 MW) did not help. Results show 20 checks, 1 pass, 19 'not assessed' and 'Infeasible: does not serve every demand' (screenshot).

## Cause

Guess: the injection side of three doublets at 2,500 m is sized for one doublet (injection pump head/flow or pressure setpoint), so the reinjected stream goes below 0 Pa; and the drive loop of the absorption chiller lacks the first guess the sample gives. The design lead should start from the sample class's sized defaults (prepare: size) instead of hand values.

## Evidence

- ![screenshot](../evidence/QA-356/1.png)

## Fix

- 2026-11-05 21:35 UTC: gemini 0.6.35 (55f2ddff) + geomind 0.4.138; pending deploy
## Retest
