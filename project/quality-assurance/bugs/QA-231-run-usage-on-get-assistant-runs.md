# QA-231: Run usage on GET /assistant/runs/{id} jumps down and up during a run (2.24 M -> 0.65 M -> 5.17 M input tokens within 15 min) and ends below the per-agent total (5.18 M vs 5.56 M, 0.133 vs 0.155 USD)

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | backend |
| Reporter | QA-E2E-design-I |
| Found | 2026-11-05 17:39 UTC |
| Versions | frontend <x.y.z>, backend <x.y.z> (geomind <x.y.z>) |
| Where | <URL>; project <name/id>; chat <id>; run <id>; step <n> |
| Fixer | |

## Steps

1. 
2. 

## Expected

## Actual

## Evidence

- ![screenshot](../evidence/QA-231/1.png)
- Run JSON: `../evidence/QA-231/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
