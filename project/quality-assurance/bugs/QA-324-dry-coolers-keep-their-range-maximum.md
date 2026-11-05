# QA-324: Dry coolers keep their range maximum (20 MW rated, 11 MW peak; 40 MW and 20 MW in the no-agent design): cooler capacity is not sized or searched, about 1-4 MEUR of capex too much

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind,gemini |
| Reporter | Sahand (reviewer notes), Manual QA-IV |
| Found | 2026-11-05 19:23 UTC |
| Versions | backend 1.1.118 (geomind 0.4.130, gemini 0.6.26) |
| Where | report of result 54b2e4f4 (B_r1_best, project 0b986dd6) and result 8878eafd (no-agent, project 8d5d21e0); reviewer notes from Sahand 20:20 CET |
| Fixer | hotfix-python-lead-II |

## Expected

Cooler (dry cooler) capacities sized from the heat they reject (or searched like the chillers), as the boiler and chillers are.

## Actual

B_r1_best: compression cooler 20 MW rated, 11.04 MW peak (55 %), 2 MEUR at 0.1 EUR/W. No-agent best: absorption cooler 40 MW (peak 14.3), compression cooler 20 MW (peak 4.4): 6 MEUR, about 4 MEUR more than needed (LCTS about 2 EUR/MWh too high). The values are the range maxima of the plant files.

## Fix

- 2026-11-05 19:34 UTC: geomind main 0df5771, gemini dev e6284347 (0.6.31); pending deploy
## Retest
