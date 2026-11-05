# QA-125: Stored-result questions (peaks, active days) take 50-65 steps, 8+ run_python approvals and 20+ min; active days never counted

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | functional-qa-simulation-I |
| Found | 2026-11-05 11:18 UTC |
| Versions | backend 1.1.84 at start (1.1.86 at 11:18 UTC); geomind 0.4.80 (as announced) |
| Where | https://geomind.team/projects/ef87f914-3aaa-4f58-be60-2d54c7687511 (QA3 simulation); chat 'Chat' of 10:31 UTC; simulate result 11c2e401cd91606b; second question (peaks, active days, geothermal share) |
| Fixer | hotfix-python |

## Steps

1. Chat: "simulate the stored plant design for the whole year 2027 ..." -> answer in about 45 s, totals correct (111,667.68 MWh heat, 23,742.528 MWh cold, equal to the CSV sums x 24).
2. Chat: "What is the peak heat delivered and on which day, the peak cold and its day, how many days is the doublet active, how much heat comes from geothermal and how much from the boiler?"
3. Approve every run_python card (8 approvals so far, auto-approve off).

## Expected

The stored result already holds the series; peaks, their days and the count of non-zero days are one tool call each, answered in about a minute with no code approval.

## Actual

About 20 minutes and 50+ steps (the next question, constraints, was at 65 steps and still running). Several run_python approvals: the first code only printed types, the second summed MW as MWh (no x24), later versions fixed units. The final answer gives peaks right (30.0 MW on 2027-01-28, 10.0 MW on 2027-07-19) and geothermal 34,837.7 MWh vs boiler 76,829.96 MWh (boiler 69 %), but says "Days the doublet is active: I cannot give a count ... no tool counts the days of a stored series", although it had already run python on that series.

## Evidence

- ![screenshot](../evidence/QA-125/1.png)
- Run JSON: `../evidence/QA-125/run-<id>.json`

## Cause

Guess: no tool returns a series summary (count of non-zero steps, peak with its date, energy sum), so the agent builds it with run_python, loads inputs by stored-ref and loops over approvals.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
