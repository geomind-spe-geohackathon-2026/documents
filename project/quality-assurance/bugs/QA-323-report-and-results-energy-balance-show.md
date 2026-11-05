# QA-323: Report and results energy balance show gas bought and boiler heat but not the produced gas burned (from the degasser), so the boiler balance (40.4 GWh heat from 34.1 GWh gas bought) looks like 119 % efficiency

| Field | Value |
|---|---|
| Status | verified |
| Severity | minor |
| Area | backend,gemini |
| Reporter | Sahand (reviewer notes), Manual QA-IV |
| Found | 2026-11-05 19:23 UTC |
| Versions | backend 1.1.118 (geomind 0.4.130, gemini 0.6.26) |
| Where | report of result 54b2e4f4 (B_r1_best, project 0b986dd6) and result 8878eafd (no-agent, project 8d5d21e0); reviewer notes from Sahand 20:20 CET |
| Fixer | hotfix-back-lead-II |

## Expected

Energy balance lists the fuel burned by source: produced gas from the degasser (GWh), gas bought (GWh), flared gas; so boiler heat / fuel gives a plausible efficiency.

## Actual

Only 'Gas bought 34.06 GWh' and 'Heat from the boilers 40.42 GWh': a reader computes 119 % boiler efficiency. Hand check: 300 m3/h x 0.8 Nm3/m3 x 0.8 CH4 x 35.8 MJ/Nm3 = 1.9 MW, about 15 GWh in 330 days, enough to close the balance; the result has the data (co2.fuel_energy) but the report does not show it.

## Fix

Backend backend part 1.1.125 (energy table adds fuel burned on site and produced gas burned; includes flared gas, boiler-only needs gemini), hotfix-back-lead-II.
- 2026-11-05 19:54 UTC: backend part 1.1.125; boiler-only gas figure needs gemini
## Retest

Report energy table of a plant with produced gas: boiler no longer above 100%.

- 2026-11-05 19:58 UTC, QA-AI-analysis-I, backend 1.1.125, API only: same report (result b7af0082): Table 4.1 has "Fuel burned on site 30.49 GWh" and "Produced gas burned (fuel burned
  less gas bought) 18.77 GWh" beside "Gas bought 11.72 GWh"; the text says "The plant burns 30.49 GWh of fuel on site:
  11.72 GWh of gas bought and 18.77 GWh of gas produced with the brine." Verified.
- 2026-11-05 19:59 UTC: retest QA-AI-analysis-I 19:59 UTC: produced gas burned in table and text

QA-E2E-report-I, 2026-11-05 20:05 UTC, backend 1.1.125, https://geomind.team/projects/0e44cb05-6096-434e-95ee-56b434898015/design/report, result 'simulation HeatingAbsorptionCoolingPlant' (plant v2, case v3), page and Export PDF (21 pages, `../evidence/QA-313/retest-report-v2.pdf`): Table 4.1 Energy balance now lists 'Fuel burned on site 85.37 GWh' and 'Produced gas burned (fuel burned less gas bought) 20.18 GWh' beside gas bought 65.19 GWh and boiler heat 76.83 GWh; text: 'The plant burns 85.37 GWh of fuel on site: 65.19 GWh of gas bought and 20.18 GWh of gas produced with the brine.' Boiler heat / fuel = 76.83 / 85.37 = 0.90, the boiler's efficiency 0.9. Same in the PDF. Verified (flared gas is not listed; small).
