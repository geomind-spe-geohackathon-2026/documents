# QA-114: Agent states case version 16 (and problem state 19) while the app shows case Version 6

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | functional-qa-case-I |
| Found | 2026-11-05 10:59 UTC |
| Versions | backend 1.1.84 (geomind 0.4.80) |
| Where | https://geomind.team/projects/15b2f15f-46d0-4b09-a44b-0f849127c1f0 (QA3 case); chat 37fb7886-a3b0-46b3-b36f-6afb72971d14; third request |
| Fixer | |

## Steps

1. In the chat ask: "Change only the heating supply temperature to 95 degC".
2. Approve; then ask "put it back to the PDF value and tell me which case version that is now".
3. Compare the answer with the project Overview (Case card, Activity).

## Expected

The agent names the case version the user sees in the app (Overview shows "Version 6", Activity "Saved case version 6").

## Actual

The agent says "Case version 16, case reference result-eab06d74028558cb ... the problem state is now at version 19". The app shows Case Version 6. Earlier in the same chat it said "version 12" for the 95 degC edit (app: 5). The agent uses internal gemini/problem-state counters that mean nothing to the user.

## Evidence

- Chat text: `../evidence/QA-114/chat-text-revert.txt`

## Cause

Guess: the agent reads the version from a gemini or problem-state counter instead of the project case version.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
