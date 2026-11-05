# QA-302: Study record of a sensitivity (e.g. lcts_sensitivity_prices) shows only raw JSON rows with 15-digit values; show a ranked table or tornado (follow-up of QA-215)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend |
| Reporter | hotfix-front-lead (QA-215 follow-up) |
| Found | 2026-11-05 18:55 UTC |
| Versions | frontend <x.y.z>, backend <x.y.z> (geomind <x.y.z>) |
| Where | <URL>; project <name/id>; chat <id>; run <id>; step <n> |
| Fixer | hotfix-front-lead |

## Steps

1. 
2. 

## Expected

## Actual

## Evidence

- ![screenshot](../evidence/QA-302/1.png)
- Run JSON: `../evidence/QA-302/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

Fix: frontend 1.1.130 (bundle see STATUS), by front-m1: SensitivityTable ranked by swing, raw JSON collapsed. Shape read from gemini sensitivity.py, not checked on study fa3dcd72.
- 2026-11-05 19:01 UTC: frontend 1.1.130
## Retest

(Who, when, result.)
