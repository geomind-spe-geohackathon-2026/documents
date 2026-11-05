# QA-352: Uncertainty/sensitivity answers still end with raw 'improvement: ...' lines under 'What could improve it'

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | geomind |
| Reporter | QA-E2E-study-II |
| Found | 2026-11-05 20:44 UTC |
| Versions | backend 1.1.125 |
| Where | project `QA-TEST QA-E2E-study-II 1` (0ce04203-df3c-4259-b9bf-d7c5ebdce123); chat bb245cd8-1ff3-4bdc-b8bd-1eb88f953519; runs 00944350, daa590fc |
| Fixer | m3 |

## Steps

1. Ask for an uncertainty analysis (run 00944350) or a three-price sensitivity plus Monte Carlo (run daa590fc).
2. Read the end of the answer.

## Expected

Improvement ideas written as normal sentences (QA-300 fixed this for the comparison answer), no 'improvement:' prefix.

## Actual

Both answers end with a section 'What could improve it' with two lines that start with the raw tag 'improvement: ...'. Same cause as QA-300, other answer types.

## Evidence

- ![screenshot](../evidence/QA-352/1.png)
- Run JSON: `../evidence/QA-352/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
