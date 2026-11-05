# QA-226: Cold delivered KPI 23,841 MWh exceeds the CSV cooling demand 23,742.5 MWh (+98 MWh) while the same result's coverage says 23,742.5; the cooling supply falls to 10.35 degC and the 20 degC supply check still passes

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | gemini |
| Reporter | QA-E2E-design-I |
| Found | 2026-11-05 17:35 UTC |
| Versions | backend 1.1.104, geomind 0.4.97, gemini 0.6.16 |
| Where | project QA-TEST QA-E2E-design-I 1 (f1704a61-f1b8-4b63-84d3-20bd30beaed7); run 76d19df6-485f-46ee-a182-6b03ed70ab33; `result/b8bc0df839230959` (design/best_v1) and Results row a6a3aec3 |
| Fixer | hotfix-python-lead |

## Steps

1. Reference case (cooling 20 degC supply / 25 degC return, CSV cooling 23,742.53 MWh/yr, peak 10.0 MW).
2. Design HeatingHeatPumpCoolingPlant with a 10 MW compression chiller, setpoint 20 degC, dry cooler 13 MW (run 76d19df6).
3. Simulate; read check_results, compute_kpis and the coverage.

## Expected

Cold delivered <= demand (23,742.5 MWh), equal to it with full coverage; the consumer supply holds 20 degC while cooling runs; a supply below 20 degC is not delivered "extra" cold.

## Actual

| Source (same design) | Cold |
|---|---|
| CSV demand | 23,742.53 MWh |
| `coverage.cooling` sum | 23,742.5 MWh (short 0) |
| check_results / KPI `cold_delivered` | **23,840.93 MWh** (+98.4, +0.41 %) |
| `lcoc.energy` | 23,758.79 MWh/yr |

- Same 23,840.93 for 300 m3/h and 50 m3/h, so it is the cooling side only.
- The chat answer (from the run): "the chiller ... cools it to a 20 degC setpoint (lowest 12.28 degC)", "consumer supply 10.35 to 25.0 degC", and the check "Cooling supply temperature 20 degC: pass". The chiller overcools to 12.28 degC, the consumer gets 10.35 degC, and that surplus is counted as delivered cold.

## Evidence

- `../evidence/QA-226/kpis-and-cooling-coverage-a6a3aec3.json`: KPIs and the daily cooling coverage of the stored row.
- Run log: check_results 17:16:46 UTC (`result/b8bc0df839230959`), cold_delivered 23840.93.

## Cause

Guess (gemini): the chiller's outlet is not held at its setpoint at part load (12.28 degC at the outlet); the cold KPI integrates m cp (T_return - T_supply) at the consumer, so an outlet below 20 degC counts more cold than the demand; the cooling supply temperature check is one-sided (a maximum) and passes a colder supply.

## Proposed fix

gemini (Sahand's OK needed; for gemini-requests.md): hold the chiller outlet at the setpoint (bypass or capacity control); cap delivered cold at the demand; make the cooling supply temperature check two-sided within a tolerance while running; one cold number per result (coverage = KPI = lcoc energy).

## Fix

- 2026-11-05 18:09 UTC: deployed 19:01-19:03 CET: backend 1.1.112, geomind 0.4.118/0.4.119, gemini 0.6.19 (hotfix-python team)
## Retest
