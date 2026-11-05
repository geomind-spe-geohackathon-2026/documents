# QA-214: Results contradict: Days covered says geothermal was off on 125 days, the Running time check says each of the two doublets ran 330 d

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | gemini,frontend |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 17:30 UTC |
| Versions | backend 1.1.106, frontend bundle index-CEvw1roy.js |
| Where | https://geomind.team/projects/8fcbf709-537a-40d9-ac1f-abadd1061775/design/results (project `QA-TEST QA-E2E-study-I 1`); result 7e0c79f0-3a4d-429a-bbdb-2f3ed13c53f2 "simulation opt1" (plant version 4, HeatingAbsorptionCoolingPlant, 2 doublets, 2500 m) |
| Fixer | hotfix-front-VII |

## Steps

As QA-213; Results > "simulation opt1" (or any of the four, same design): Days covered and
Constraints.

## Expected

Both sections agree. With two doublets that each run 330 of 365 days, at least one runs on every
day unless both rest at once; the heating days with geothermal = 0 should match the days both
doublets were off.

## Actual

- Days covered, heating: "Geothermal topped up by backup: 240 days; Backup only (geothermal off):
  125 days ... geothermal was off on 125 days". In the API `coverage.heating`, geothermal > 0 on
  exactly 240 days, sum 43625.6 MWh.
- Constraints: "Running time limit, Doublet 1: 330 d (<= 330 d), margin 0 d"; same for Doublet 2;
  message "330 d against the limit 330 d" with no worst day.
- The agent (run 4eb8e2f4) repeats "running_time_limit 330/330 d".

Either the doublets ran about 240 days and the check prints the limit as the value, or they ran 330
days and in 90+ days their heat went somewhere the coverage does not count (for example the
absorption chiller drive in summer), which "geothermal off" then misstates. Both are wrong for a
judge reading the page.

## Evidence

- `../evidence/QA-214/result-7e0c79f0.json` (`coverage.heating`, `constraints` d0/d1.running_time_limit).

## Cause

Guess, unverified: the running_time_limit check returns the cap (330) as its value when the
doublet's active-day count is not read; or coverage counts only geothermal heat to the heating grid.

## Proposed fix

gemini (via Sahand's list, gemini requests need approval) or the backend's check mapping: report the
doublet's real active days as the value of running_time_limit; frontend Days covered: say
"geothermal not used for heating" when the doublets ran but fed only the chiller, and show active
days per doublet.

## Fix

## Retest
