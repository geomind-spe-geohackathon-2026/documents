# QA-203: Case requirements differ run to run on the same files: reinjection set exactly 1..1 without the Knowledge tolerance; pump-intake limits added that the doc says only if the design checks them

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-E2E-case-I |
| Found | 2026-11-05 17:22 UTC |
| Versions | frontend 1.1.113, backend 1.1.102-1.1.104 (geomind 0.4.97-0.4.99) |
| Where | geomind.team; projects QA-TEST QA-E2E-case-I 1 (case v2-v3), 2 (case v5), 3 (question only) |
| Fixer | |

## Steps

1. Same input in three projects: PDF + 2 CSVs, the same request.
2. Compare the case requirements with gemini's reference `examples/hackathon_2026/case.json` and the
   assumptions document (Requirements: tolerances).

## Expected

The same 8 requirements as the reference (plus heating/cooling supply temperature is fine), with the
reinjection tolerance 0.99999-1.00001 from the assumptions document.

## Actual

| Requirement | Reference / assumptions doc | Project 1 | Project 2 | Project 3 (question) |
|---|---|---|---|---|
| production flow | ONE `production_flow_range` 50-300 m3/h | same | TWO: `min_stable_flow` 50, `max_production_flow` 300 (QA-160) | - |
| reinjection | 0.99999-1.00001 while running | same | `reinjection_balance` **min 1, max 1** exact, no tolerance, not in the question | 0.99999-1.00001 |
| pump intake | "only if the design checks it" | none | none | added: gas fraction <= 0.1875, intake pressure >= 5 bar |
| brine cooling unit | K | K | `°C` (gemini reads it as a difference, so 40 K: no error) | - |

An exact 1..1 ratio fails on float round-off in a check; the reference uses a tolerance for that reason.

## Evidence

- `../evidence/QA-203/case-project1-v2.json`, `../evidence/QA-203/case-project2-v5.json`.
- Project 3 question text: item 16-17 (in the QA-E2E-case-I report).

## Cause

Guess: geoscientist IV (requirements) and the lead write the requirements freely each run; the
handbook's table (handbook-case 12.5) is not used as the one source; project 2's lead put only two
tolerance rows (heat/cold) in the question.

## Proposed fix

geomind case lead / geoscientist brief: copy requirements from handbook-case 12.5 table shape (names,
`over`, `when`, units) and the tolerance rows from the assumptions document, all of them; a check in
the lead's final checklist (11.2) against that table.

## Fix

## Retest
