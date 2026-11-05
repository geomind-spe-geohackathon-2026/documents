# QA-225: Heating is short 2.76 MWh on every one of 365 days (1,009 MWh, unmet share 0.903 % of the 1 % limit) while the 30 MW peak boiler has spare capacity: the plant never covers the heating pipe loss

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | gemini,geomind |
| Reporter | QA-E2E-design-I |
| Found | 2026-11-05 17:35 UTC |
| Versions | backend 1.1.104, geomind 0.4.97, gemini 0.6.16 |
| Where | project QA-TEST QA-E2E-design-I 1 (f1704a61-f1b8-4b63-84d3-20bd30beaed7); run 76d19df6-485f-46ee-a182-6b03ed70ab33; results `result/b8bc0df839230959` (design/best_v1, 300 m3/h) and row a6a3aec3 (same design at 50 m3/h) |
| Fixer | hotfix-python-lead |

## Steps

1. Reference case loaded; chat asks for a plant design (see QA-171).
2. The design lead builds HeatingHeatPumpCoolingPlant, 1 doublet, backup `peak`, peak boiler 30 MW, heating supply/return pipes 1000 m, D 0.4 m, U 1.0 W/m2/K (engineer's "assumption", no source).
3. Simulate the year; read the daily coverage.

## Expected

With a 30 MW boiler and backup `peak` the plant meets the heat demand every day (demand peak 30.0 MW on 2027-01-28, otherwise far below): unmet share 0 or close to it. A loss in the network pipe is heat the plant makes, not heat the consumer misses.

## Actual

- `coverage.heating`: **short 2.76 MWh on all 365 days** (summer days with 4.5 MW demand included), 1,008.9 MWh in the year; demand 111,667.7 MWh = CSV. The boiler peaks at 29.0 MW (50 m3/h) / 16.3 MW (300 m3/h): it never limits.
- The shortfall is the same for 300 and 50 m3/h (heat_delivered 110,658.77 MWh in both), so it does not depend on the geothermal part.
- 2.76 MWh/day = 0.115 MW = the supply pipe loss: pi x 0.4 m x 1000 m x 1.0 W/m2/K x ~90 K = 0.113 MW.
- `heat_delivered` unmet share 0.00903 passes the 1 % limit by 0.1 %: an unsourced 1000 m pipe uses 90 % of the allowance; a 1.2 km pipe or U 1.2 would fail the case.
- Three numbers for the heat of one result: coverage 110,658.8, `lcoh.energy` 110,734.6 MWh/yr, compute_kpis 110,660 (rounded).

## Evidence

- `../evidence/QA-225/coverage-heating-a6a3aec3.json`: the daily heating coverage (demand, geothermal, backup, short).
- check_results of `result/b8bc0df839230959`: heat_delivered 110,658.77, heating_coverage 0.99097 (run log, 17:16:46 UTC).

## Cause

Guess: gemini's dispatch sets the boiler/heat pump duty to the consumer demand at the plant outlet, then the supply pipe loses heat, and the consumer gets demand minus loss; nothing raises the duty by the pipe loss. Secondary (geomind): the energy engineer picks a 1000 m network with no source; the case gives no network, so a pipe with losses should not be added without a Knowledge value or the user's word.

## Proposed fix

1. gemini (Sahand's OK needed; for gemini-requests.md): the dispatch covers the demand at the consumer, i.e. adds the pipe's heat loss to the duty of the last source (boiler or heat pump) when it has capacity; unmet only when capacity runs out.
2. geomind: handbook-design (ch 2.5 network losses) and the energy engineer's brief: when the case gives no network, model no pipe (or length 0) or ask; never an unsourced 1000 m.
3. One delivered-heat number per result (coverage, lcoh energy, KPI).

## Fix

## Retest
