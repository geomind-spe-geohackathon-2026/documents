# QA-163: Case confirmation question retypes a number with a wrong digit (N2 0.110838972435462335 shown, 0.11083897243546233 set)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 17:02 UTC |
| Versions | backend 1.1.104 |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 2 (cf19d767-b62b-4caa-a90e-4386e6e3c744); chat 078fe0bd-dac7-49cb-b34c-e8d993a55f43; run 519ccc65-564e-4d1e-9139-a23777cd1107; case_lead `ask_user` request-348 |
| Fixer | |

## Steps

1. New project with the three competition files; chat "Please set up the case from the uploaded
   brief and the two demand CSVs. Where the files say nothing, use your own reasonable assumptions."
2. Read the confirmation question (request-348), line 12.

## Expected

`prompts/case/lead.md`: "Copy every number digit for digit as its source writes it ... The same
holds for every number you write, in a question". `knowledge/hackathon-2026-assumptions.md`:
N2 0.11083897243546233 ("exact values of gemini's sample; do not round").

## Actual

- The question shows `N2 0.110838972435462335` (one extra digit "5" at the end).
- The `set_case` calls (steps 11, 12) send `0.11083897243546233`, so the case is right but the user
  approves a number that differs from the one stored. The question is written by the model, so any
  long number can be mistyped there.

## Evidence

- `../evidence/QA-163/answers-run2.json` (entry 3, `question.message`, line 12)
- Run log: `../evidence/QA-153/run-519ccc65.json`

## Cause

The question text is free text the model writes; it retypes the values from its context instead of
showing the values the case holds.

## Proposed fix

geomind: let the confirmation question list the values from the case itself, like `ask_economics`
does for economics (a tool, e.g. `ask_case_values(paths=[...], reasons={...})`, that reads each
value from the stored or proposed case and renders the lines), or at least have `ask_user` refuse a
question that names a case path with a number differing from the case's value. Prompt-only fix:
"for a composition, name the source and the sum; never retype a number longer than 6 digits".

## Speed and accuracy

Accuracy of what the user is shown: 1 value of 15 wrong in run 2 (run 1 showed it right). Stored
case right.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 18:55 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest

(Who, when, result.)
