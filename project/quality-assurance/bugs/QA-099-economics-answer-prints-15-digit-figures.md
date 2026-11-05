# QA-099: Economics answer prints 15-digit figures and uses a 365.25-day energy basis it never states (heat 111744 MWh vs the run's 111667.68)

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | geomind |
| Reporter | functional-qa-report-I |
| Found | 2026-11-05 10:35 UTC |
| Versions | frontend 1.1.x (not read), backend 1.1.84 (geomind 0.4.80) |
| Where | https://geomind.team/projects/91b202b6-6236-45e7-8860-a58437d6eb98/assistant/chat; project QA3 report; first chat; result/11c2e401cd91606b, cost result-ac6f803291d37e42; scenario functional-qa-report-I-S1 |
| Fixer | hotfix-python |

## Steps

1. In "QA3 report" chat ask: "Please work out the economics of the finished study: CAPEX, annual OPEX, the cost of heat and of cooling per MWh, and the payback. Tell me where every cost figure comes from."
2. Read the answer (evidence/QA-099/chat-answer.txt).

## Expected

Figures rounded for a reader (MEUR to 2-3 decimals, EUR/MWh to 1-2). One energy basis, or the difference stated. Each unit cost with a source or a clear "assumption approved by you".

## Actual

- Every figure has 15-17 digits (e.g. CAPEX 23.955885571022524 MEUR, lcoh 48.927109216402506 EUR/MWh), so the answer is a wall of numbers.
- lcoh/lcoc use 111744.16 MWh heat and 23758.79 MWh cold, but the same answer gives heat_delivered 111667.68 MWh, which equals the CSV (4652.82 MW-days x 24). The cold basis 23758.79 differs from the CSV (989.272 x 24 = 23742.53). The ratio is 1.000685 = 365.25/365, so gemini seems to annualise to a 365.25-day year. The answer never says so.
- Unit costs (drilling 1239 EUR/m, boiler 0.06073 EUR/W, ...) are sourced only as "economics.json (project file)", not to a catalogue row or document; the answer also states price year 2015 without saying whether results are in 2015 EUR.
- Arithmetic checked and correct: capex items sum to 23.956 MEUR, opex parts to 5.134 MEUR/yr, payback 23.956/2.996 = 8.0 yr, lcoh = 0.8 x annualised cost / heat, lcoc = 0.2 x annualised cost / cold.

## Evidence

- Chat text: `../evidence/QA-099/chat-answer.txt`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
