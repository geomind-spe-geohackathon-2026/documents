# QA-099: Economics answer prints 15-digit figures and uses a 365.25-day energy basis it never states (heat 111744 MWh vs the run's 111667.68)

| Field | Value |
|---|---|
| Status | open |
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

hotfix-python-III, 2026-11-05, geomind 0.4.83 (tag v0.4.83), backend 1.1.88 (deploy 11:30 UTC).
Fix: `compute_kpis` and `estimate_costs` give every figure to five significant digits
(`assessment.py::rounded`); the economist prompt says to state the basis once: currency and price
year (EUR 2015 for catalogue rows), each price's source as `about.sources` names it, and that
gemini scales annual figures to a 365.25-day year (`gemini.units.SECONDS_PER_YEAR`), hence the
0.07 % gap to a 365-day sum of the demand file.
- 2026-11-05 11:32 UTC: geomind 0.4.85, backend 1.1.88, deployed 11:30 UTC by hotfix-python-III
- 2026-11-05 17:25 UTC: QA-E2E-study-I: study tools (optimize, sensitivity) still give 15-digit figures in the answer; see Retest
## Retest

QA-E2E-study-I, 2026-11-05 17:23 UTC, backend 1.1.104, project `QA-TEST QA-E2E-study-I 1`, run
4eb8e2f4-e775-4e2a-b257-853eae883724 (chat: optimise the plant, then the sensitivity). Still fails
for study figures: the answer prints `lcts 49.28130562173663`, a table of trials with
49.65465823276261, 53.25282162719622, 47.377880660819805, and the sensitivity table with
42.09848103045964, 63.76249621862753, 21.664015188167898 ... The five-digit rounding covers
compute_kpis and estimate_costs but not the study tools (`optimize`/`read_study`, `sensitivity`).
The 365.25-day basis (heat 111744.16 vs 111667.68 MWh) is named, but not explained to the user.
Proposed: round in the study results the agent reads (the same `rounded`), and say the basis in one
line. Reopened.
