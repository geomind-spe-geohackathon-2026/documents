# QA-217: API returns 500 under load: Postgres pool (5 + 10) runs out at 17:29 UTC; 116 failed requests in 27 s, 95 of them GET /runs/{id}/agents, which is polled ~400 times a minute and takes up to 51 s

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | backend |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 17:31 UTC |
| Versions | frontend <x.y.z>, backend <x.y.z> (geomind <x.y.z>) |
| Where | <URL>; project <name/id>; chat <id>; run <id>; step <n> |
| Fixer | |

## Steps

1. 
2. 

## Expected

## Actual

## Evidence

- ![screenshot](../evidence/QA-217/1.png)
- Run JSON: `../evidence/QA-217/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
