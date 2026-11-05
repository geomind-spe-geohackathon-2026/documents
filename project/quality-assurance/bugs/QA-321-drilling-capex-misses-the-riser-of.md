# QA-321: Producer split at the ESP into riser 1,500 m + well 2,000 m is accepted and simulated as a 2,000 m producer on a 3,500 m doublet (design invalid, cost follows the simulated well)

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | gemini |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 19:21 UTC |
| Versions | backend 1.1.118 (geomind 0.4.130, gemini 0.6.26) |
| Where | project 0b986dd6-8f95-4383-9d15-5e589ff122c9, result 54b2e4f4-a6a5-4475-9fad-57d93112d504 (B_r1_best); report export of that result |
| Fixer | hotfix-python-lead-II |

## Steps

Plant B_r1_best: d0.depth 3500 m; producer split at the ESP: riser (above_esp) section_length [1500] m, well (below_esp) [2000] m; injector [3500] m. capex.drilling 1,239.13 EUR/m.

## Expected

Drilled length 1500 + 2000 + 3500 = 7,000 m: 8.67 MEUR.

## Actual

Report, Capital cost by kind: Drilling 6.815 MEUR = 5,500 m x 1,239.13. One section (1,500 m, very likely the riser) is not costed: capex 1.86 MEUR too low, annualised 0.13 MEUR/yr, LCTS about 0.97 EUR/MWh too low (29.55 instead of about 30.5).
For comparison the no-agent design (not split at the ESP, 2 doublets at 3,282 m) is costed 16.27 MEUR = 13,130 m = 2 x 2 x 3,282 m: correct.

## Cause

Guess: the drilling cost sums the well and injector section lengths of a Doublet but not the riser of a well split at the ESP (gemini costs).

## Fix

## Retest

## Update 2026-11-05 20:25 CET (from hotfix-python-lead-II)

The cost is not under-counted: the design is invalid. The producer was given as two separate paths (riser 1,500 m and well 2,000 m) that do not add up to the doublet depth of 3,500 m in one path, so gemini simulated a 2,000 m producer and costed what it simulated; adding the riser to the cost would double-count normal designs. Consequence for the report: B_r1_best (LCTS 29.55, 12/12 checks) rests on an inconsistent well and is not a valid result. Fix: gemini 0.6.30 refuses a producer whose riser and well paths differ from the depth, plus a design prompt line; deploys with QA-278 (0.6.29).
