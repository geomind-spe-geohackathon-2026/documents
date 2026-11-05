# QA-217: API returns 500 under load: Postgres pool (5 + 10) runs out at 17:29 UTC; 116 failed requests in 27 s, 95 of them GET /runs/{id}/agents, which is polled ~400 times a minute and takes up to 51 s

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | backend |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 17:29 UTC |
| Versions | backend 1.1.104 (geomind 0.4.100) |
| Where | api.geomind.team; seen by the QA-AI-case-I driver on `GET /assistant/runs/dd6b4700-3db4-43a7-8c48-4bf018600e1c` (project QA-TEST QA-AI-case-I 4) |
| Fixer | hotfix-back-VI |

## Steps

1. Nine QA threads run at once (5 browser E2E threads polling Runs and logs / chat, 4 API threads).
2. Poll `GET /assistant/runs/{id}` every 5 s from a script.

## Expected

Reads of a run answer in well under a second, whatever the number of open browser tabs; no 500.

## Actual

- 17:29:52 UTC: `GET /assistant/runs/dd6b4700-...` -> `500 {"error":{"code":"internal","message":"Internal server error"}}`.
- Backend log: `sqlalchemy.exc.TimeoutError: QueuePool limit of size 5 overflow 10 reached, connection
  timed out, timeout 30.00`. 116 requests failed between 17:29:25 and 17:29:52 UTC:
  95 `GET /assistant/runs/{id}/agents`, 12 `GET /assistant/chat`, 4 `GET /assistant/runs`,
  3 `GET /assistant/runs/{id}`, 1 `POST /assistant/chat`, 1 `GET /assistant/chat/{id}/state`.
  A `POST /assistant/chat` (a user creating a chat) failed too.
- Traefik, 17:20-17:31 UTC: 1555 `GET .../agents` requests (peaks 405 and 350 a minute at 17:28),
  mean 310 ms, slowest 51.4 s, 51.3 s, 36.1 s (499: the client gave up), 22.5 s, 17.9 s.
- The settings are `POSTGRES_POOL_SIZE = 5`, `POSTGRES_MAX_OVERFLOW = 10`
  (`backend/src/core/settings.py` lines 35-36).
- Earlier the same day the API also answered 504/502 during hotfix deploys (16:56, 17:16 UTC):
  expected during a deploy (QA-060), not part of this bug.

## Evidence

- `../evidence/QA-217/failed-requests.txt` (every failed request, 17:00-17:31 UTC)
- `../evidence/QA-217/traceback.txt` (one full traceback)
- `../evidence/QA-217/traefik-agents.log` (all `/agents` requests 17:20-17:31 with their times)

## Cause

Guess from the log: `/runs/{id}/agents` rebuilds every agent session from all stored events of a
run (`read_agents` -> `events.after(run.id, -1)` and `agent_sessions`, `backend/src/api/v1/assistant/runs/services.py`)
on each poll, holding a DB connection for the whole read; the chat page polls it for each live
run every second or two, so a few open tabs with long runs (thousands of events) hold all 15
connections, and every other request waits 30 s and fails.

## Proposed fix

- backend: release the DB session before the CPU work in `read_agents` (load rows, close, then
  build sessions), and cache the result per run by its newest event id (Redis), so a poll with no
  new event costs one small query.
- backend: raise the pool (`POSTGRES_POOL_SIZE` 20, `POSTGRES_MAX_OVERFLOW` 20; Postgres default
  max_connections is 100) and lower the pool timeout to fail fast (5 s, 503 with Retry-After
  instead of 500).
- frontend (other session): poll `/agents` only while the step list is open, and use the run's
  event stream (`/events`) for updates instead of polling.

## Speed and accuracy

27 s in which no user could load a chat or a run. Read times up to 51 s for one `/agents`.

## Fix

hotfix-back-VI, backend 1.1.108 (tag v1.1.108), deployed 2026-11-05 ~17:37 UTC. Cause: every poll of
`/assistant/runs/{id}/agents` read all events of the run (thousands of rows with LLM payloads)
and held its pool connection meanwhile. Now `services.cached_events` keeps each run's events in
memory (64 runs, LRU) and reads only those newer than the last read; the sessions are computed
again only when new events came. Postgres pool 20 + 20 (was 5 + 10) in all four env files
(max_connections 100; 45 in use before).
- 2026-11-05 17:39 UTC: backend 1.1.108
## Retest

Recipe: with 2-3 tabs on a running run, the agents view answers in well under a second, no 500
in the fastapi log (`QueuePool limit`), and its numbers still match `/runs/{id}/log`.
