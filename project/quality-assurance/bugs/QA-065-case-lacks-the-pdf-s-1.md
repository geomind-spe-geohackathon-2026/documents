# QA-065: Case lacks the PDF's 1-3 doublets rule, yet the design lead says 'the case fixes the number of doublets at 1-3'

| Field | Value |
|---|---|
| Status | verified |
| Severity | minor |
| Area | geomind |
| Reporter | qa-func-1 |
| Found | 2026-11-05 00:11 UTC |
| Versions | backend 1.1.56 (health 2026-11-05 ~00:15 UTC) |
| Where | https://geomind.team/projects/a0947848-b958-4ee9-8927-56ec0a9cff03/design/case, tab Requirements; chat 235c60c5-da86-4f21-9257-e21a6e400697, design lead question about search ranges |
| Fixer | hotfix-python |

## Steps

1. Upload the challenge PDF and both CSVs, ask the chat to set up the case; approve the set_case cards.
2. Open Design, Case, Requirements.

## Expected

A requirement on the doublet count (quantity `count`, 1 to 3) next to the other PDF hard constraints, or the agents not claiming it is in the case.

## Actual

The case has 8 requirements (flow 50 and 300 m3/h, brine cooling 40 C, reinjection 1, 330 d, pump efficiency 0.7, supply 100 and 20 C); none bounds the number of doublets, although the quantity `count` exists. The design lead then asks: 'The case fixes the number of doublets at 1-3 (brief p.2) ... 1. size.doublets = 1 to 3 (from the case)'. The claim is false.

## Evidence

- ![screenshot](../evidence/QA-065/1.png)
- Run JSON: `../evidence/QA-065/run-<id>.json`

## Cause

Guess: the case lead did not map the PDF doublet rule to a requirement and the design lead assumed it did.

## Fix

Cause: the case lead's prompt named `count` only as 'a number of units' with no form for a doublet limit, and its checklist did not require every hard rule of the brief to become a requirement; the design lead's prompt let it name brief rules as the case's. gemini accepts `{name: doublet_count, on: doublet, quantity: count, min: 1, max: 3}` (no over/when/unit; checked). Fix: the case lead's prompt gives that form and its checklist requires every hard rule (flow, temperatures, reinjection, days, efficiency, number of doublets or units) as a requirement or named as open; the design lead says the case states a rule only when `read_case` shows the requirement by name, else hands it over as `case change needed: requirements: ...`. geomind 0.4.60 (commit 273cc1f, tag v0.4.59/v0.4.60), backend 1.1.61 (3d2aa31), deployed 2026-11-05 00:22 UTC by hotfix-python-II. Prompt change: retest by setting up the case from the challenge PDF again.
- 2026-11-05 00:23 UTC: geomind 0.4.60 (273cc1f, case lead maps doublet count to {on: doublet, quantity: count, min, max}; design lead cites only read_case requirements), backend 1.1.61 (3d2aa31), deployed 00:3x UTC
## Retest

functional-qa-I, 2026-11-05 ~00:55 UTC, backend 1.1.62, fresh project 'QA2 functional-qa-I full run' (61134432) from the PDF and CSVs: Case, Requirements now has 'Each doublet: count between 1 and 3' next to flow 50/300, brine cooling 40, reinjection 1, 330 d, pump efficiency >= 0.7, supply 100/20. Passed. (Pump efficiency is now 'at least 0.7'; the PDF says 70 %, fine.)
