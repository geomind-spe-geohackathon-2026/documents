# QA-300: Comparison answer ends with three raw 'improvement: ...' lines and internal ids ('finding F84842168, recorded as result costs')

| Field | Value |
|---|---|
| Status | verified |
| Severity | minor |
| Area | geomind |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 18:50 UTC |
| Versions | backend 1.1.115+ |
| Where | project `QA-TEST QA-E2E-study-I 3` (ac687987-8bfe-452f-8013-7a4b577a3655); chat 00be49e5-9d56-4c05-8dc3-40f2a0a1d919; run b709a671-9bad-4a4d-9f2d-3913f11e977f |
| Fixer | hotfix-python-lead-II |

## Steps

Chat: "Compare the two plants of this project, HackathonPlant (plant version 1) and
HeatingAbsorptionCoolingPlant (plant version 2), over 2027: cost of thermal supply, investment, CO2
and how much heat the geothermal side gives. Do not change the project plant."

## Expected

A clean answer; follow-up ideas as next-step chips or one short "Next" list in plain words.

## Actual

The (correct, fast) answer ends with three lines that read like an internal record:
"improvement: keep the heat pump of v1 and drop the gas boiler duty of v2: ...",
"improvement: size the geothermal side of v2 up towards v1's heat share: ...",
"improvement: check whether v2's 10.7 MEUR capex advantage survives a carbon price above the case's ...".
The text also says "(finding F84842168, recorded as result `costs`)". The first improvement
("keep the heat pump of v1 and drop the gas boiler duty of v2") mixes the two plants into a third
that was never designed.

## Evidence

Run log: `../evidence/QA-300/run-b709a671-log.json` (final answer).

## Cause

Guess: the economist's or explainer's `improvements` field is pasted into the answer as
"improvement: <text>" lines.

## Proposed fix

geomind (project lead / explainer prompt): render improvements as a short "What could improve it"
list or as next-step chips; never print finding ids.

## Fix

- 2026-11-05 19:12 UTC: geomind main 71d80ab (0.4.131+), gemini dev 5782a138 (0.6.27); QA-312 also needs back-lead's DatabaseWorkspace.save_plant_version
## Retest

- 2026-11-05 19:51 UTC: QA-E2E-study-II 2026-11-05 retest in QA-TEST QA-E2E-study-II 1 (geomind 0.4.130 era, deploy 36): comparison answer has no raw 'improvement:' lines nor finding ids. NOTE: the uncertainty answer (run 00944350) still ends with two raw 'improvement:' lines
