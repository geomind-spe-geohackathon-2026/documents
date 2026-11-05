# QA-330: adopt_design of a design whose number equals an old plant version says 'already the project plant, nothing to save' while the project plant is another design

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-study-II |
| Found | 2026-11-05 19:40 UTC |
| Versions | backend 1.1.119-1.1.121 era (deploy 36, geomind 0.4.130) |
| Where | project `QA-TEST QA-E2E-study-II 1` (0ce04203-df3c-4259-b9bf-d7c5ebdce123); chat bb245cd8-1ff3-4bdc-b8bd-1eb88f953519; run e49bf334-fe77-4ef2-aa9c-f111f7d17200 |
| Fixer | |

## Steps

1. Seed a project with plant v1 HackathonPlant and v2 HeatingAbsorptionCoolingPlant (v2 current).
2. Ask: "Compare the current plant with the HackathonPlant heat-pump plant on LCOH, NPV and CO2. Do not change the project plant." (run 8ef524a4; answer says design/v2 is still the project plant).
3. Ask: "Use the best design from this comparison as the project plant." Approve the "Adopt design" card.

## Expected

The best design (design/v1, heat pump) becomes the project plant (a new plant version or the current marker set to it), said in the answer.

## Actual

adopt_design(design/v1) returns "design/v1 is plant version 1 already; nothing to save" and the answer says "The best design of the comparison is already the project plant". That is false: the comparison answer a minute earlier said design/v2 is still the project plant. The tool seems to compare the design number with a plant version number (design/v1 vs plant version 1), not the design with the current plant. Nothing was adopted; 5 steps, 0.003 USD.

## Evidence

- ![screenshot](../evidence/QA-330/1.png)
- Run JSON: `../evidence/QA-330/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
