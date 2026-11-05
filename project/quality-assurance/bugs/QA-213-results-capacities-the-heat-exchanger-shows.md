# QA-213: Results, Capacities: the heat exchanger shows 'not used in this run' while geothermal gave 43.6 GWh through it (its size is in MW/K and has no peak)

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | frontend,geomind |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 17:30 UTC |
| Versions | backend 1.1.106, frontend bundle index-CEvw1roy.js |
| Where | https://geomind.team/projects/8fcbf709-537a-40d9-ac1f-abadd1061775/design/results (project `QA-TEST QA-E2E-study-I 1`); result 7e0c79f0-3a4d-429a-bbdb-2f3ed13c53f2 "simulation opt1" (plant version 4, HeatingAbsorptionCoolingPlant, 2 doublets, 2500 m) |
| Fixer | |

## Steps

1. Project with the reference case and plant HeatingAbsorptionCoolingPlant; chat "simulate the
   current plant for 2027" and "optimise ...".
2. Open Design > Results, any of the four results, section Capacities.

## Expected

The heat exchanger shows how hard it worked (peak duty in MW, or the peak heat it moved, against
its UA or a duty rating), never "not used" while geothermal heat flows through it.

## Actual

"Heat exchanger 1.5 MW/K — not used in this run". The same page, Days covered: "Geothermal gave
39.1 % of the year's demand (43626 of 111668 MWh)": all of it passes this heat exchanger (the plant's
only brine-to-water exchanger). The API result has `capacities[heat_exchanger] = {value 1.5,
unit MW/K, peak null, share null, reason null}`; the frontend reads peak null as "not used".
QA-123 fixed the same claim in the agent's text; the page still makes it.

## Evidence

- `../evidence/QA-213/1.png` (Results page), `../evidence/QA-213/result-7e0c79f0.json` (`capacities`).

## Cause

Facts: capacities give a UA (W/K) for the heat exchanger with no peak; the card text treats a null
peak as not used. Guess: compute_kpis `capacities` has no duty reading for a HeatExchanger.

## Proposed fix

frontend (Results capacities card): a null peak with a null reason says "no peak reading", never
"not used". geomind/backend: give the heat exchanger its peak duty (MW, from the module's heat
flow column) as `peak`, with the UA as the size, so share = peak duty / design duty.

## Fix

## Retest
