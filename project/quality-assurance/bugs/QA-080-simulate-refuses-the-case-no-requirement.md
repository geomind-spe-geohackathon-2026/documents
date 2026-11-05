# QA-080: simulate refuses the case: 'no requirement on doublet gives a flow range (min and max) of d0.production_flow'; the case stores the PDF's 50-300 m3/h as two rules, so no plant can be simulated

| Field | Value |
|---|---|
| Status | open |
| Severity | blocker |
| Area | gemini |
| Reporter | functional-qa-I |
| Found | 2026-11-05 05:18 UTC |
| Versions | backend 1.1.72 (health 2026-11-05 05:16 UTC), geomind 0.4.67, gemini 0.6.7 (per coordinator's note) |
| Where | project 61134432, chat cb8b9b2d-edce-4f69-9dfb-6b015a821601, run 37950240-d44b-499d-bf8e-2f75c0baa35e, run JSON steps 255, 271, 284, 290 (design_lead simulate) |
| Fixer | |

## Steps

1. Case from the PDF (requirements: min_stable_flow min 50 and max_production_flow max 300 m3/h as two rules, as the case lead writes them).
2. Build and size a plant (size_plant works), then call simulate.

## Expected

The PDF's flow limit 50-300 m3/h per doublet is accepted by gemini's schedule (either two rules or one range), and simulate runs the 2027 year.

## Actual

simulate -> {'error': {'code': 'case_incomplete', 'path': 'requirements', 'message': "schedule: no requirement on doublet gives a flow range (over='each', when='running', min and max) of d0.production_flow; expected one, a limit has no default"}} (4 times in the run, on design/A_sized and the B family). size_plant ran, build_plant succeeded. The case holds the limits as separate rules max_production_flow (max 300) and min_stable_flow (min 50) plus doublet_count 1..3. The design lead named it ('a case-shape issue, not a plant value') but handed over: the case team did not get it, so after about 70 min the comparison has no simulation, no capacities, no energies. The same cause blocks every design in the project.
## Evidence

- ![screenshot](../evidence/QA-080/1.png)
- Run JSON: `../evidence/QA-080/run-<id>.json`

## Cause

Guess: either the case lead should store ONE doublet rule with min 50 and max 300 on production_flow (and the min_stable_flow semantics 'when running' is kept), or gemini's schedule should combine the two rules. Fix in whichever side is cheaper; then tell the design lead how to ask the case lead for a case change. Also seen in the same run: the case lead wrote O2, C2H6, C3H8 = 0 mol% into utilities.gas.composition after the user said there is no grid gas (zeros nobody gave).

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
