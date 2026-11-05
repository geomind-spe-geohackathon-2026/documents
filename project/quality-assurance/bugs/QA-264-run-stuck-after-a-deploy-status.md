# QA-264: Run stuck after a deploy: status 'waiting' on request-1290 that the answer endpoint calls 'answered already' (409); run.usage reset to 0; the run does not go on

| Field | Value |
|---|---|
| Status | open |
| Severity | blocker |
| Area | backend |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 18:13 UTC |
| Versions | backend 1.1.112 -> 1.1.113 (deploy at about 18:12 UTC) |
| Where | run bfcec811-c5ad-496e-a829-6ec44de3251c (hackathon report run II), project 0b986dd6-8f95-4383-9d15-5e589ff122c9 |
| Fixer | |

## Steps

1. The run waits at request-1290 (design_lead, set_ranges approval).
2. A backend deploy restarts fastapi and celery (502 at about 18:06 and 18:12 UTC).
3. POST /assistant/runs/{id}/answer with request-1290 (approve).

## Expected

The answer is taken (or was taken before the restart) and the run goes on.

## Actual

- The first answer call hit 502 during the deploy; every later call returns 409 `Request request-1290 was answered already`.
- GET /assistant/runs/{id} still shows status `waiting` with `request` = request-1290, and `usage` 0 tokens, 0 USD (it was 4.8 M tokens, 0.109 USD before).
- No new step follows; celery shows `assistant.runs.resume` tasks but the run stays waiting. The run is stuck and its usage is lost from the run record.

## Cause

Guess: the answer was stored (or half-stored) while the worker restarted; on resume the run re-asks the same request id, and the answer endpoint refuses it because the request row is marked answered. The usage reset suggests the resumed run starts a new usage record.

## Fix

- 2026-11-05 18:18 UTC: Manual QA-IV 18:19 UTC on the backend that health reports: run bfcec811 still 'waiting' on request-1290, answer still 409 'answered already', usage 0; not fixed for this run
## Retest
