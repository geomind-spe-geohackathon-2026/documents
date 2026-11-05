# QA-228: Comparison: 'heat from the geothermal side' computed as heat_delivered minus boiler_heat (34.8 GWh) while the boiler also drives the absorption chiller; the Results page shows 43.6 GWh geothermal for the same plant

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 17:38 UTC |
| Versions | backend 1.1.106 |
| Where | project `QA-TEST QA-E2E-study-I 1` (8fcbf709-537a-40d9-ac1f-abadd1061775); chat c0cae905-a2a8-44cf-8bec-f4899f313e8b; run 52383511-cdea-47d7-8f61-4a1737248856; design_lead calculate at 17:31:26 UTC |
| Fixer | |

## Steps

Chat: "Compare the two plants of this project, HackathonPlant (plant version 1) and
HeatingAbsorptionCoolingPlant, over 2027: cost of thermal supply, investment, CO2 and how much heat
the geothermal side gives. Which one should we pick?" (approve the build_plant card).

## Expected

Geothermal heat per plant from the simulation (the coverage / module heat flows), the same figure
the Results page shows.

## Actual

- Answer table: "Heat from the geothermal side: HackathonPlant 111 413.8 MWh, HeatingAbsorption-
  CoolingPlant 34 837.7 MWh".
- design_lead `calculate` 17:31:26: label "geothermal/brine-side heat = heat_delivered -
  boiler_heat", 111 667.7 - 76 830.0 = 34 837.7.
- But in HeatingAbsorptionCoolingPlant the peak boiler's hot water also drives the 10 MW absorption
  chiller (the answer itself says so), so boiler_heat is not all heating. The Results page for the
  same design (result 7e0c79f0, Days covered): "Geothermal gave 39.1 % of the year's demand (43626
  of 111668 MWh)". The answer understates geothermal by 8.8 GWh (20 %).
- For HackathonPlant, 111 413.8 MWh "from the geothermal side" includes the heat pump's
  compressor work (26 728 MWh of electricity bought): the brine gave less than that.
- The recommendation (HackathonPlant) does not change, but the figure the user asked for is wrong
  for both plants.

Speed: 7 min 40 s, 61 steps, 100 calls, 1.54 M input tokens, 0.035 USD. The split repeats work:
design_lead finishes twice (17:32:27 and 17:32:58, as design_lead and family_design_lead with the
same task), and the explainer writes the answer twice (comparison_driver 17:35:05-17:36:16, then
project_lead 17:36:16-17:36:48), then project_lead rewrites it (to 17:37:30).

## Evidence

- Run log: `../evidence/QA-228/run-52383511-log.json`; Results page coverage: `../evidence/QA-214/result-7e0c79f0.json`.

## Cause

Fact: no tool gives "geothermal heat to the users" directly to the agent; the design lead derives it
by subtraction. Guess: compute_kpis has no geothermal_heat KPI (the Results page reads coverage).

## Proposed fix

geomind: expose the coverage split (geothermal / backup / short per service, as the Results page
has it) through compute_kpis (e.g. `geothermal_heat`, `geothermal_share`) and tell the design
skill never to derive it by subtraction; for a heat pump plant, state brine heat and compressor work
apart. Task split: the comparison driver should call one design lead and let only the final writer
write (explainer once).

## Fix

## Retest
