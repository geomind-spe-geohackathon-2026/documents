# QA-060: During a deploy the site answers every page with a bare text '404 page not found' (no app shell, no retry)

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | infra |
| Reporter | qa-ux |
| Found | 2026-11-05 00:04 UTC |
| Versions | backend 1.1.55 (health at 00:04 UTC; 1.1.53 before), frontend 1.1.5x |
| Where | https://geomind.team/projects/4cfeab2d-73e3-4299-a1f8-afec3d7e4bae/assistant/chat, /design, /runs, /nope; about 00:01-00:03 UTC 2026-11-05 (deploy window) |
| Fixer | hotfix-back |

## Steps

1. Be signed in on geomind.team around a deploy (:00 UTC).
2. Open any page URL directly (I opened /projects/<id>, /library, /runs, /design, /nope and the chat URL in the agent-browser).
3. A minute or two later the same URLs return the app.

## Expected

During a deploy the user sees the app shell or a styled 'We are updating, back in a minute' page that retries by itself.

## Actual

Every URL I opened between about 00:01 and 00:03 UTC showed only the text `404 page not found` in a monospace font on a white page (HTTP 404, `text/plain`), also for valid routes such as the chat URL (screenshot). A little later (00:04 UTC) the same routes returned 200 `text/html`. A user in the middle of a chat who reloads then sees a dead page and may think the project is gone.

## Evidence

- ![screenshot](../evidence/QA-060/1.png)
- Run JSON: `../evidence/QA-060/run-<id>.json`

## Cause

Guess: the frontend container (or its reverse-proxy route) is replaced during the deploy and the proxy answers 404 until the new one is up.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
