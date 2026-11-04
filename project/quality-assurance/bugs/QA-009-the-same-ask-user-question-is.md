# QA-009: The same ask_user question is asked three times in one run

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | Fatemeh (run), Claude (write-up) |
| Found | 2026-11-04 ~20:40 UTC (run started 18:51 UTC, still running) |
| Versions | frontend 1.1.33; backend as at 18:51 UTC (1.1.14, geomind 0.4.25, per QA-007) |
| Where | https://geomind.team/projects/886404e4-3b22-41bd-8986-1a8bc869e25e/assistant/chat/33c76f29-064f-4047-9926-ff8937beddf7; run a61cfb19bfb04ae99e92060fc5bd2e40; steps[19], steps[35], steps[48] |
| Fixer | hotfix-python |

## Steps

1. Chat: "design heating and cooling based on files", with the challenge PDF and the two daily demand CSVs.
2. The case lead asks the user for the values the files leave open.
3. The user answers. The case lead's nested run ends; the project lead starts a new case lead.

## Expected

An answer the user gave is kept in the problem state and reaches every later agent. Nobody asks the
same question again; the project lead acts on the answer it already has.

## Actual

The user is asked three times for the same values (network return temperatures, site air
temperature, humidity and pressure, electricity import limit):
- steps[19], case lead run 1: answer "Use reasonable, documented engineering assumptions for all unspecified values".
- steps[35], case lead run 2: the same question, the same answer.
- steps[48], case lead run 3 (task from the project lead at steps[44]: "close the case values ... by asking the user yourself"): the same question, the same answer.
Each new case lead run starts without the earlier answer, and the project lead sends the same ask again.

## Evidence

- Run JSON: [`../evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz`](../evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz)
  (gzip; one run for QA-007 and QA-009 to QA-014). `steps[i]` below is the 0-based index in its
  `steps` list.
- The three ask_user tool calls and their `output`.

## Cause

Guess: ask_user answers live only in the nested run's messages, not in the problem state
(`/assumptions` gets one only at steps[50], after the third ask). The project lead's task text does
not carry the answer either.

## Fix

- 2026-11-04 20:08 UTC: fixed in geomind 0.4.29 (commit 0622c67), backend 1.1.20 (80eb493), waiting for deploy
## Retest
