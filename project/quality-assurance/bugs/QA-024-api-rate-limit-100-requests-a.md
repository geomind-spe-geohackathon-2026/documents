# QA-024: API rate limit (100 requests a minute per user) blocks normal page loads; the page shows only Rate limit exceeded

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | backend |
| Reporter | qa-8 |
| Found | 2026-11-04 20:17 UTC |
| Versions | frontend bundle index-DnxCbfcj.js, backend 1.1.21 |
| Where | https://geomind.team/projects/55612f74-441f-4a37-9859-a7ea43ab6600/design/case; project QA qa-8 manual pipeline; no chat, no run; first page load after a deploy |
| Fixer | |

## Steps

1. Several people (here 8 QA sessions, each a browser) work on geomind.team at once with the same account (admin).
2. Open any project page, e.g. the Case page of a new project.

## Expected

The page loads. A short burst of requests (page load, polling) by one person never locks the app.

## Actual

The API answers 429 to the page's requests (console: `Failed to load resource: the server
responded with a status of 429`), and the whole page shows only the red text "Rate limit exceeded"
under "Projects" (screenshot 1). No retry, no wait time, no way on but to reload later.

## Evidence

- ![screenshot](../evidence/QA-024/1.png)

## Cause

Fact: `backend/src/core/ratelimit/middleware.py` counts per `user:<id>` (or per IP), with
`RATE_LIMIT_REQUESTS=100` and `RATE_LIMIT_WINDOW_SECONDS=60` in `backend/.env`. Every session that
logs in as the same user shares those 100 requests a minute; one browser tab with chat and run
polling already sends many. Guess: raise the limit (or key it per session/token), and let the
frontend wait for `Retry-After` and retry instead of replacing the page with the error. Part of the
frontend side may belong to hotfix-front.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
