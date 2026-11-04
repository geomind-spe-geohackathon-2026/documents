# QA-014: Project lead calls read_case with sections the case does not have

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | Fatemeh (run), Claude (write-up) |
| Found | 2026-11-04 ~20:40 UTC (run started 18:51 UTC, still running) |
| Versions | frontend 1.1.33; backend as at 18:51 UTC (1.1.14, geomind 0.4.25, per QA-007) |
| Where | https://geomind.team/projects/886404e4-3b22-41bd-8986-1a8bc869e25e/assistant/chat/33c76f29-064f-4047-9926-ff8937beddf7; run a61cfb19bfb04ae99e92060fc5bd2e40; steps[25] |
| Fixer | hotfix-python |

## Steps

1. As QA-009. After the first case lead run stops, the project lead reads the case.

## Expected

The project lead reads the sections that exist (the error lists them), or describe_case first.

## Actual

Three refusals in one step: read_case(section='utilities'), 'initial_state' (both "unset"),
'economics' ("the case has no economics file in the run"). Each one costs a round of the agent's
context.

## Evidence

- Run JSON: [`../evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz`](../evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz)
  (gzip; one run for QA-007 and QA-009 to QA-014). `steps[i]` below is the 0-based index in its
  `steps` list.
- steps[25] tool_calls.

## Cause

Guess: the prompt or tool description names sections without saying they may be unset; read_case
could return an unset section as empty with a note, not as an error (like QA-001).

## Fix

- 2026-11-04 20:35 UTC: fixed in geomind 0.4.35 (commit a6a4595), backend 1.1.31, waiting for deploy
- 2026-11-04 21:05 UTC: shipped in backend 1.1.40 with geomind 0.4.42 (deployed 21:02 UTC); the fix is in the prod worker (checked: code/prompt present, QA-023 gives 'Design a plant' for a ready case). Live retest by the bug's steps still to do.
## Retest
