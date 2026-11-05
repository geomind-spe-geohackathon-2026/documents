# QA-346: A stale claim in the project state beats the corrected skill: after QA-299 the economist in an old chat still says P10/P90 do not exist, because earlier results hold 'gemini returns no P10/P90'

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-analysis-II |
| Found | 2026-11-05 20:14 UTC |
| Versions | backend 1.1.127 (geomind main HEAD, gemini 0.6.33) |
| Where | api.geomind.team; project QA-TEST QA-AI-analysis-I 8 (485dbcfc-63f4-474f-a2dd-b94ab85bc34f); chat fb8fd813-1874-4583-b4e6-ca150c5d66ca; run 0f587461-d154-4317-be9f-a548197f5be2 |
| Fixer | m1 |

## Steps

1. In the old chat of project 8 (earlier answers and results say "gemini returns no P10/P90"), send: "Give me the P10, P50 and P90 ... (200 draws, seed 43)".
2. Compare with a fresh chat of the same project (run 84462291-a6fb-4672-8e2a-e5c18a51de74).

## Expected

The economist reads the corrected skill, passes `percentiles=[10, 90]` and answers P10/P50/P90.

## Actual

Old chat: sample_uncertainty without `percentiles`, answer "P10 and P90 are not available". Fresh chat: `percentiles: [10, 90]`, P10 41.035, P50 45.796, P90 50.722.

## Evidence

- Run JSON: `../evidence/QA-346/log-0f587461-d154-4317-be9f-a548197f5be2.json`

## Cause

Guess: the project state results/assumptions hold "gemini returns no P10/P90" (written under the old skill) and the chat history repeats it; the briefs and the economist trust that over the skill text read in the same run.

## Proposed fix

Prompts: a tool limit stated in state or history is re-checked against the skill/tool schema before it is repeated; or states do not store tool-capability claims, only values.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
