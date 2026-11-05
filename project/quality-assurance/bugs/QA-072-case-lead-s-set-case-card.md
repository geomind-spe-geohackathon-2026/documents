# QA-072: Case lead's set_case card claims 'the user's instruction is that the times are UTC' when the user never said so

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | functional-qa-I |
| Found | 2026-11-05 01:49 UTC |
| Versions | backend 1.1.53-1.1.62 (see Where), geomind per backend |
| Where | project QA2 qa-func-1 S1 full case a0947848, chat 235c60c5, run 144ad9d5 (backend 1.1.54), first set_case card |
| Fixer | hotfix-python |

## Steps

1. Upload the PDF and CSVs, ask the chat to set up the case.
2. Read the first set_case card and the agent's text before it.

## Expected

The agent says the time zone is unknown and asks, or marks UTC as an assumption.

## Actual

Text: 'The files carry no time zone; the user's instruction is that the times are UTC, so I'll set that and record it.' The card sends time_zone UTC. The user never gave an instruction. I denied it; the agent then asked and later labelled UTC as an unconfirmed assumption. Invented user statement breaks the sourcing rule. (The Time tab also says no offset = UTC.)

## Evidence

- ![screenshot](../evidence/QA-072/1.png)
- Run JSON: `../evidence/QA-072/run-<id>.json`

## Cause

Guess: the model confused a rule 'times are UTC without an offset' with a user instruction.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 04:31 UTC: geomind 0.4.66 (6d46e72: shared rule, never attribute to the user what they did not write; case lead: UTC is gemini's reading, zone is an assumption), backend 1.1.71 (d68105b), deployed 04:30 UTC
## Retest

(Who, when, result.)
