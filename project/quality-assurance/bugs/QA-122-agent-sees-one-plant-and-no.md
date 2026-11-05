# QA-122: Agent sees one plant and no studies in QA3 report although the project shows 2 plants and 4 studies, so the explainer can compare no alternatives

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | functional-qa-report-I |
| Found | 2026-11-05 11:17 UTC |
| Versions | backend 1.1.84 (geomind 0.4.80), frontend not read |
| Where | https://geomind.team/projects/91b202b6-6236-45e7-8860-a58437d6eb98/assistant/chat; project QA3 report; run result/11c2e401cd91606b |
| Fixer | |

## Steps

1. In the chat ask: "Why did you choose this configuration, and which alternatives did you compare it with? Give the figures of each alternative from this project and explain how the geothermal heat drives the cooling."
2. Read the answer.

## Expected

The seeded stages are visible to the agents: the project Overview lists Plant version 2, Study "4 done" and the activity log shows studies economics/simulation on HackathonPlant and HeatingAbsorptionCoolingPlant. The explainer compares them with figures.

## Actual

Answer: "list_plants shows exactly one plant ... list_studies returned [] — no study exists ... no alternatives were compared". It took 117 steps (44 retried) and gave no comparison. The seeded plant HackathonPlant and the 4 studies are invisible to the agent (guess: the seed wrote project study rows that list_studies does not read, or the agent lists only plants of the chat). Stage gap, reported as the README asks.

## Evidence

- Chat text: `../evidence/QA-122/chat.txt` (the answer is after the question quoted in Steps)

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
