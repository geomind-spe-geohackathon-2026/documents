# QA-146: Chat busy list shows a line with no agent name

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend |
| Reporter | user via coordinator |
| Found | 2026-11-05 15:18 UTC |
| Versions | frontend <x.y.z>, backend <x.y.z> (geomind <x.y.z>) |
| Where | <URL>; project <name/id>; chat <id>; run <id>; step <n> |
| Fixer | hotfix-front-V |

## Steps

1. 
2. 

## Expected

## Actual

## Evidence

- ![screenshot](../evidence/QA-146/1.png)
- Run JSON: `../evidence/QA-146/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 15:20 UTC: frontend 1.1.112, commit 5ddc296, deployed; cause (guess): event agent id empty for the root run, or empty instance; no live check (rule)
## Retest

(Who, when, result.)
