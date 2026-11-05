# QA-238: Days covered / coverage: cold of the electric compression chiller is counted as geothermal (cooling 100 % geothermal on all 365 days although the compression chiller delivers up to 4.1 MW)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | gemini |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 17:42 UTC |
| Versions | backend 1.1.108 (geomind 0.4.110, gemini 0.6.17) |
| Where | https://geomind.team/projects/4678c5c6-66fc-46dd-9d1e-358c3c5c1d24 (No-agent showcase); result 137473a6-8f6c-4f69-b9b4-bbe5dd414092 (run of plant version 8, the best evolve structure) |
| Fixer | hotfix-python-lead |

## Steps

1. Plant with an absorption chiller (driven by brine heat) and an electric compression chiller; run the whole year.
2. Read `coverage.cooling` of the result (Days covered, Results).

## Expected

Cold from the compression chiller (electricity) counted as not geothermal (backup or its own class); only the absorption chiller's cold geothermal.

## Actual

`coverage.cooling`: geothermal 23,743 MWh, backup 0, on all 365 days 'geothermal', although `capacities` shows compression_chiller peak 4.13 MW (absorption 5.87 MW). The share of cold from geothermal is overstated.

## Cause

Guess: gemini's daily_coverage classes every cooling unit as geothermal, or classes by role, not by drive (QA-107a treated an ElectricBoiler as backup for heat; the same rule is missing for cold).

## Fix

- 2026-11-05 18:09 UTC: deployed 19:01-19:03 CET: backend 1.1.112, geomind 0.4.118/0.4.119, gemini 0.6.19 (hotfix-python team)
- 2026-11-05 18:27 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
## Retest
