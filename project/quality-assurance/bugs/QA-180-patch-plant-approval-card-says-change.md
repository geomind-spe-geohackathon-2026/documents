# QA-180: patch_plant approval card says 'Change 0 value(s)' for a patch that removes a doublet or adds a third one (modules, connections)

| Field | Value |
|---|---|
| Status | duplicate |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 17:14 UTC |
| Versions | frontend <x.y.z>, backend <x.y.z> (geomind <x.y.z>) |
| Where | <URL>; project <name/id>; chat <id>; run <id>; step <n> |
| Fixer | |

## Steps

1. 
2. 

## Expected

## Actual

## Evidence

- ![screenshot](../evidence/QA-180/1.png)
- Run JSON: `../evidence/QA-180/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 17:14 UTC: duplicate of QA-172 (evidence added)
## Retest

(Who, when, result.)


Duplicate of QA-172. Extra evidence: run 7a7ace73-e8b5-4291-9252-33fd7240be84 (project `QA-TEST QA-AI-analysis-I 1`), cards request-231 (patch removing doublet d1, saved as HackathonPlant_1d_v2) and request-249 (patch adding d2, HackathonPlant_3d) both said 'Change 0 value(s) of design/HackathonPlant_v1 ... : .' (`../evidence/QA-179/approval-cards.log`).
