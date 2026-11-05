# QA-357: Depth search does not stretch the wells: minimize moves d0.depth to 2,875 m but well/riser/injector section_length stay 2,500 m (drilling costed for 10,000 m, not 11,500 m; hydraulics on 2,500 m paths, temperature from 2,875 m)

| Field | Value |
|---|---|
| Status | open |
| Severity | blocker |
| Area | gemini |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 21:16 UTC |
| Versions | backend 1.1.133 (geomind 0.4.137, gemini 0.6.34) |
| Where | project 32236adb-aa7a-4be9-83fd-40fcedc1238c (sahand test 5), run 8cef3941, minimize hp_boost_opt_lcts_v2, result 5cf8577e-853c-4201-b016-9e135bb82d99 |
| Fixer | |

## Steps

1. Design patched with d0.depth 2,500 m and well/riser/injector section_length [2500] m (run d935c2b1).
2. Ranges on d0.depth (2,000-3,500 m) and doublets; minimize on LCTS (run 8cef3941).

## Expected

Every result has wells as long as its depth: the chosen depth 2,875 m with 2 doublets drills 2 x 2 x 2,875 = 11,500 m (14.25 MEUR at 1,239 EUR/m), and the hydraulics use 2,875 m paths.

## Actual

Result 5cf8577e: depth 2,875 m, 2 doublets, LCTS 22.36 EUR/MWh, 17/17 checks; the report's capex by kind shows Drilling 12.39 MEUR = 10,000 m = 2 x 2 x 2,500 m. The search changed the depth (reservoir temperature from 2,875 m) but kept the 2,500 m section lengths (cost and well hydraulics). Capex is about 1.9 MEUR too low and the best design is not physically consistent; LCTS about 1 EUR/MWh too low at least.

## Cause

Guess: a range on d0.depth sets the reservoir depth but not the well, riser and injector section_length (QA-321 refuses a mismatch at write time, but the search does not keep them in step). Fix: section lengths follow the depth during size/search (scale the last section), or the depth range is refused while explicit section lengths are set.

## Fix

## Retest
