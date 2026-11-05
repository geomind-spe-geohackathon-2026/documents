# QA-334: Explainer says 'gemini has no compression chiller module ... could not be modelled at all', but gemini models it as a HeatPump in chiller mode (reference plant HeatingHeatPumpCoolingPlant.compression_chiller)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-report-I |
| Found | 2026-11-05 19:53 UTC |
| Versions | backend 1.1.122+ (geomind 0.4.130+, gemini 0.6.26+), frontend live |
| Where | https://geomind.team/projects/a9ff33c4-6e46-4eaf-be31-5277221dd51d/assistant/chat; project QA-TEST QA-E2E-report-I 3; run fd996d09-a51d-4f0b-8c1a-a73240bfe0ab, analysis_lead steps with list_modules |
| Fixer | m3 |

## Steps

1. Ask "... why an absorption chiller instead of a compression chiller here?" (full question in
   QA-269 Steps).

## Expected

A reason from the design and the numbers, e.g. compare with the reference plant
HeatingHeatPumpCoolingPlant (heat pump heating + compression chiller), which the project
library and gemini's plant list both hold.

## Actual

"gemini has no compression chiller module. Its cooling category holds only AbsorptionUnit and
AdsorptionChiller (list_modules), so a compression chiller could not be modelled here at all -
this is a limit of the tool, not a finding about the site." The agent called
`list_modules {"category": "chiller"}` (refused, no such category), then
`list_modules {"category": "cooling"}` -> AbsorptionUnit, AdsorptionChiller, and concluded.
Fact: gemini models a compression chiller as a `HeatPump` in chiller mode, e.g.
`gemini/plants/heatingheatpumpcoolingplant.py:35` `self.compression_chiller = HeatPump()`
with a `compression_cooler`; the challenge sample has `plants/HeatingHeatPumpCoolingPlant.json`.
A judge or user reading the answer gets a wrong reason for a key design choice.

## Evidence

- Answer text: `../evidence/QA-334/answer.txt`
- Run steps (list_modules calls at lines 45 and 68): `../evidence/QA-334/run-fd996d09-steps.txt`

## Cause

Fact: `list_modules(category="cooling")` lists only modules whose category is cooling;
HeatPump sits under heating, and its chiller mode is not visible in the list. Nothing in the
prompts or Knowledge says "compression chiller = HeatPump(mode chiller)".

## Fix

Proposal (geomind, hotfix-python): (1) `list_modules` / `describe_module` show HeatPump under
cooling too, with "mode chiller = electric compression chiller"; (2) a line in
`knowledge/handbook-design.md` and the explainer prompt: compare a choice with the reference plant
families (`list_plants`), e.g. HeatingHeatPumpCoolingPlant for compression cooling, before
saying an option cannot be modelled.
- 2026-11-05 19:57 UTC: geomind main 737a7cf / 0bdafe8; pending deploy
## Retest

QA-E2E-report-I, 2026-11-05 20:16 UTC, live geomind 0.4.133+, project QA-TEST QA-E2E-report-I 5 (c60d19cd), run 4ffa1142 (20:07:58-20:14:27 UTC), question 'Why an absorption chiller instead of a compression chiller ... Could the compression option be simulated?': the answer now says 'gemini does model it - an electric (vapour-compression) chiller is a HeatPump in cooling mode, and the reference plant HeatingHeatPumpCoolingPlant holds one as compression_chiller', and gives a design reason from the result (chiller electricity 237 MWh/yr, grid 300 g/kWh, electricity 8.02 of 13.77 kt CO2). Verified. The comparison itself was not made: routing gap filed as a new bug. Text: `../evidence/QA-334/retest-answer.txt`.
