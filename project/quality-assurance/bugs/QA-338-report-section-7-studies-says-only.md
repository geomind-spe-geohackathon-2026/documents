# QA-338: Report: section 7 Studies says only 'This result is not a sensitivity or uncertainty study' for an optimisation result, and unmet demand prints as '2.01e-12 MWh of demand is not met'

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | backend |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 19:59 UTC |
| Versions | backend 1.1.125 |
| Where | POST /reporting/design/export (md, all parts), project `QA-TEST QA-AI-analysis-I 1` (4ce816b1-4bd1-48a5-8e77-9414c2b86301), result b7af0082-b903-4346-a084-11e01f8e2710 (page study minimize "QA-332 retest minimize") |
| Fixer | |

## Steps

1. Run a minimize study (lcts, 40 evaluations, seed 0, size first) on a plant version.
2. Export the report of its result with every part.

## Expected

QA-313's outline, item 7: "Studies (sensitivity tornado, uncertainty P10/P50/P90, optimisation/comparison; each with a
short reading)". For an optimisation result: what was searched (variables and ranges), how many trials, how many
feasible, the start value against the best (here the sized start vs 31.49 EUR/MWh), and the project's sensitivity or
uncertainty studies of the same plant, if any, or a line saying none was run. Tiny residuals shown as "all demand met".

## Actual

Section 7 in full: "The result comes from the find the best design study QA-332 retest minimize on cost of thermal
supply. This result is not a sensitivity or uncertainty study." (also the study kind's title is pasted into the sentence:
"the find the best design study"). The project holds a sensitivity (957c9714) and a sample (5d7bbf26) study of the same
plant version, not mentioned.
Section 4: "2.01e-12 MWh of demand is not met" and "1.137e-11 MWh of demand is not met" (floating-point residuals; the
checks say 0 %).

## Evidence

- `../evidence/QA-338/report-b7af0082-noimg.md` (images removed), lines 234-240 and 150-158.

## Cause

Guess: the backend report builder's studies section only handles results of sensitivity/sample studies; the optimiser's
history is not read. The unmet text prints the raw value without a threshold.

## Proposed fix

Backend report builder (`src/core/.../report` studies part): for a minimize/evolve result, a table of the searched
variables with range, start and best, trials and feasible count, and a reading line; list the project's sensitivity and
sample studies of the same plant version (or say none exists). Print unmet energy below 0.01 % of demand as "all demand
met".
