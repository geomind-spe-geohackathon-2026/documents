# QA-124: Verdict gives no value for brine cooling, running time and reinjection (3 of 8 requirements rest on 'gemini says feasible')

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | geomind |
| Reporter | functional-qa-report-I |
| Found | 2026-11-05 11:17 UTC |
| Versions | backend 1.1.84 (geomind 0.4.80), frontend not read |
| Where | https://geomind.team/projects/91b202b6-6236-45e7-8860-a58437d6eb98/assistant/chat; project QA3 report; run result/11c2e401cd91606b |
| Fixer | hotfix-python |

## Steps

1. Ask: "Does this design meet all the requirements of the challenge? List each requirement with its value and whether it passes."

## Expected

Each hard cap with its value: brine cooling per doublet (limit 40 K), running days (limit 330), reinjection ratio (0.99999-1.00001).

## Actual

The table has values for production flow (300 m3/h), pump efficiency 0.7, doublets 2, heat coverage 1.0 and cold coverage 1.0. For brine cooling, running time and reinjection it says "no ... output is exposed by read_result; gemini's verdict covers it". The run took 83 steps, 28 retried. The jury wants the checks shown with numbers.

## Evidence

- Chat text: `../evidence/QA-124/chat.txt` (the answer is after the question quoted in Steps)

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
