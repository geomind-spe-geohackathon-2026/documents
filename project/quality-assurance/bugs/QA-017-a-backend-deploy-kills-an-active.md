# QA-017: A backend deploy kills an active run; it stays waiting forever with no message

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | backend |
| Reporter | Fatemeh (run), Claude (write-up) |
| Found | 2026-11-04 20:04 UTC |
| Versions | frontend 1.1.33; the run spans backend 1.1.14 to 1.1.16 (geomind 0.4.25/0.4.26), agents on deepseek-v4.1-flash |
| Where | https://geomind.team/projects/886404e4-3b22-41bd-8986-1a8bc869e25e/assistant/chat/33c76f29-064f-4047-9926-ff8937beddf7; project test hack; chat 33c76f29-064f-4047-9926-ff8937beddf7; run a61cfb19bfb04ae99e92060fc5bd2e40; the celery worker; run a61cfb19 at step 101 |
| Fixer | |

## Steps

1. A run is active (run a61cfb19, in fill_parts round 2).
2. A hotfix deploy restarts geomind-celery and geomind-fastapi (backend 1.1.17; the worker came up at 2026-11-04 20:02:34 UTC).

## Expected

A deploy waits for active runs, or marks each run it stops as failed or interrupted with a
message in the chat ("the run stopped because the app was updated; send again"), or resumes it.

## Actual

The run's process is gone (the worker started fresh; its log shows no task of this run). The row
still says `waiting` with the old approval request-1289 (QA-016) and `ended` empty, and the chat
still shows "1 run active" with nothing to answer. The run cannot end on its own.

## Evidence

- Postgres `runs` row of a61cfb19, read 20:03 UTC: status waiting, ended empty.
- `docker ps`: geomind-celery and geomind-fastapi up 52 s at 20:03 UTC.
- [`run-...-step101.json.gz`](../evidence/QA-016/run-a61cfb19bfb04ae99e92060fc5bd2e40-step101.json.gz) (run JSON at 101 steps; `steps[i]` is the 0-based index)

## Cause

Guess: no step at worker start (or in the deploy script) finds runs left `running` or `waiting`
without a process. Only the user's Stop (cancel) may end it now; not tried.

## Fix

## Retest
