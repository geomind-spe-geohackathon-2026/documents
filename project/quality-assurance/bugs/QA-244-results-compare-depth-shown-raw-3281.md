# QA-244: Results compare: depth shown raw (3281.9831696449164 m), Doublets '-' for the superstructure result (2 doublets), point labels overlap, 'dashed trade-off line' text but no line drawn

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | frontend,backend |
| Reporter | Sahand (screenshot), Manual QA-IV |
| Found | 2026-11-05 17:45 UTC |
| Versions | backend 1.1.109, frontend live 2026-11-05 17:42 UTC |
| Where | https://geomind.team/projects/4678c5c6-66fc-46dd-9d1e-358c3c5c1d24/design/results/compare |
| Fixer | hotfix-front-lead |

## Steps

Open Results, Compare, with 8 results (6 minimize, 1 evolve, 1 run), axes CO2 and Cost of thermal supply.

## Expected

Depth rounded (3,282 m); Doublets 2 for the superstructure result; readable point labels; the dashed trade-off line drawn when the text names it.

## Actual

- Table: Depth `3281.9831696449164 m`.
- Doublets `-` for "Superstructure search on LCTS and CO2" and its run (the result has d0 and d1; `doublets` is null in GET /design/results/{id}).
- Labels of HeatingCoolingPlant and HeatingHeatPumpCoolingPlant are drawn on top of each other.
- "The dashed line is the trade-off line." but no dashed line is visible.
- HeatingPlant (no cooling) sits as the cheapest point (see QA-239).

## Evidence

- ![screenshot](../evidence/QA-244/1.png)

## Fix

## Retest
