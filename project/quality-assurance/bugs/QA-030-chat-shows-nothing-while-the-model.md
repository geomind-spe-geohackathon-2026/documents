# QA-030: Chat shows nothing while the model provider is retried; show the live retry event

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | frontend |
| Reporter | hotfix-back |
| Found | 2026-11-04 20:25 UTC |
| Versions | frontend 1.1.33+, backend 1.1.24 (geomind 0.4.29) |
| Where | any chat with a run whose model calls fail and are retried (follow-up of QA-021) |
| Fixer | |

## Steps

1. Send a message while the model provider answers 429 or 5xx (QA-021 saw this on the free nemotron tier).

## Expected

Beside the running step, the chat says the provider is busy and when it tries again, e.g. "The model provider is busy (429); trying again in 8 s", until the next event of that agent.

## Actual

The chat shows only "Thinking" for minutes. Since backend 1.1.23 the run stream carries a live `retry` event `{agent, parent, attempt, model, delay, status}` (never stored, no `id`); the frontend ignores it.

## Evidence

- Backend contract: `backend/docs/app-build/contracts.md`, live event table, row `retry`.
- QA-021 (evidence: celery-429.log).

## Cause

Fact: the frontend has no handler for the `retry` event type (it skips unknown types).

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
