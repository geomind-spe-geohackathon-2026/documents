# QA-323: Report and results energy balance show gas bought and boiler heat but not the produced gas burned (from the degasser), so the boiler balance (40.4 GWh heat from 34.1 GWh gas bought) looks like 119 % efficiency

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | backend,gemini |
| Reporter | Sahand (reviewer notes), Manual QA-IV |
| Found | 2026-11-05 19:23 UTC |
| Versions | backend 1.1.118 (geomind 0.4.130, gemini 0.6.26) |
| Where | report of result 54b2e4f4 (B_r1_best, project 0b986dd6) and result 8878eafd (no-agent, project 8d5d21e0); reviewer notes from Sahand 20:20 CET |
| Fixer | |

## Expected

Energy balance lists the fuel burned by source: produced gas from the degasser (GWh), gas bought (GWh), flared gas; so boiler heat / fuel gives a plausible efficiency.

## Actual

Only 'Gas bought 34.06 GWh' and 'Heat from the boilers 40.42 GWh': a reader computes 119 % boiler efficiency. Hand check: 300 m3/h x 0.8 Nm3/m3 x 0.8 CH4 x 35.8 MJ/Nm3 = 1.9 MW, about 15 GWh in 330 days, enough to close the balance; the result has the data (co2.fuel_energy) but the report does not show it.

## Fix

Backend backend part 1.1.125 (energy table adds fuel burned on site and produced gas burned; includes flared gas, boiler-only needs gemini), hotfix-back-lead-II.

## Retest

Report energy table of a plant with produced gas: boiler no longer above 100%.
