# QA-132: Simulation of the stored plant has d0 flow 341 m3/h (> 300 m3/h hard cap) on 2027-01-01 while verdict.feasible is true

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | gemini |
| Reporter | functional-qa-simulation-I |
| Found | 2026-11-05 14:18 UTC |
| Versions | backend 1.1.86-1.1.88 (run on 1.1.84), geomind 0.4.80 |
| Where | https://geomind.team/projects/ef87f914-3aaa-4f58-be60-2d54c7687511 (QA3 simulation); simulate result 11c2e401cd91606b; d0 series result-6a5e0fdfc8567e08 |
| Fixer | hotfix-python |

## Steps

1. Chat: "simulate the stored plant design for the whole year 2027 ..." (answer: verdict.feasible true, coverage 1.0, 0 failed steps).
2. Chat: "Do the hard constraints hold ...? Check each doublet's flow (50 to 300 m3/h when on) ...".

## Expected

Competition cap: 50-300 m3/h per doublet while active (PDF section 3). A simulation of a plant that exceeds it is flagged infeasible, or the controller limits the flow to 300 m3/h.

## Actual

The agent read d0.esp fluid_in.volume_flow = 341.276 m3/h on 2027-01-01 (d1 216.68 m3/h, in range). That is above the 300 m3/h cap, yet the run summary says verdict.feasible true and the constraint is not flagged. The agent could not scan the other 364 days (no series scan tool, see QA-125) and could not read brine cooling (no doublet brine_cooling series in the stored result). 84 steps, 22 needed another try. Also: the cooling supply is 25 C on days with no cooling demand (2027-01-01..06), 20 C when cold is delivered.

## Evidence

- ![screenshot](../evidence/QA-132/1.png)
- Run JSON: `../evidence/QA-132/run-<id>.json`

## Cause

Guess: the plant's flow limit is not set to 300 m3/h (plant stage), and the verdict does not check the case requirements per day.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 14:28 UTC: geomind 0.4.87 (341 m3/h was the ESP intake volume with free gas; liquid flow 300; skill names reservoir.liquid_flow), backend 1.1.89, deployed 14:27 UTC
## Retest

(Who, when, result.)
