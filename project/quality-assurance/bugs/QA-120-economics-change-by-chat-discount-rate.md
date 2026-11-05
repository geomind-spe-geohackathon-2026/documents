# QA-120: Economics change by chat: discount rate 8 % is sent as value 8 with no unit (earlier proposal used 0.05)

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | functional-qa-case-I |
| Found | 2026-11-05 11:14 UTC |
| Versions | backend 1.1.84 (geomind 0.4.80) |
| Where | https://geomind.team/projects/15b2f15f-46d0-4b09-a44b-0f849127c1f0 (QA3 case); chat 37fb7886-a3b0-46b3-b36f-6afb72971d14; request "I do not accept the economics ... discount rate 8 %"; Set case approval card |
| Fixer | hotfix-python |

## Steps

1. In the case chat reject the proposed economics and give own numbers (discount rate 8 %, 30 yr, 90/35 EUR/MWh, 70 EUR/t, 55/40 EUR/MWh).
2. Read the Set case approval card (not yet approved: the run is left waiting).

## Expected

"discount_rate": 0.08 (the form the first proposal used: 0.05 for 5 %) or an explicit percent unit.

## Actual

The card sends "discount_rate": {"value": 8} with no unit, next to values with units. If stored as a fraction this is 800 %. Not yet approved, so the stored result is untested. The other six values are right (30 yr, 70 EUR/t, 90, 35, 40, 55 EUR/MWh).

## Evidence

- Chat text: `../evidence/QA-120/chat-text.txt`

## Cause

Guess: the agent keeps the user's "8" and sends it without converting percent to fraction.

## Fix

hotfix-python-III, 2026-11-05, geomind 0.4.85 (tag v0.4.85), backend 1.1.88 (deploy 11:30 UTC).
Fix: `ask_economics` refuses a fraction key (`discount_rate`, `*share*`, `*fraction*`) given a
number above 1 with no unit: "8 reads as 800 %. For 8 % give 0.08" (`refuse_percents`), before
the user is asked.

## Retest

(Who, when, result.)
