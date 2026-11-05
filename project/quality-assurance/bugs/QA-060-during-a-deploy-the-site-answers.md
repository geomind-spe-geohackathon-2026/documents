# QA-060: During a deploy the site answers every page with a bare text '404 page not found' (no app shell, no retry)

| Field | Value |
|---|---|
| Status | fixed |
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
- 2026-11-05 00:22 UTC: hotfix-back, infrastructure 6d81dc8: infrastructure/maintenance/ (nginx, Traefik router priority 1 for geomind.team and api.geomind.team): during a deploy the site gets a styled 'GeoMind is updating' page (503, reloads every 10 s) and the API a 503 JSON error, both Retry-After: 10; checked locally (both hosts). Starting it on production was not done by this session (a service start was refused before); a person runs: cd ~/geomind-spe-hackathon-2026/infrastructure/maintenance && sg docker -c 'docker compose up -d' . Then retest around a frontend deploy.
- 2026-11-05 00:24 UTC: geomind-maintenance up (Sahand).
## Retest

(Who, when, result.)
- 2026-11-05 00:24 UTC: hotfix-back 00:23 UTC, backend deploy 1.1.61 with api.geomind.team/api/v1/system/health polled every 0.5 s: 200 x25, then 502 text/plain x2 (old container stopping, its router still present), then 503 maintenance JSON {"error":{"code":"unavailable"}} x8, then 200; no bare 404. The geomind.team page (styled, self-reloading) is the same router; to be seen at the next frontend deploy. Left over: the two 502s at the start of a restart (would need a Traefik errors middleware or a stop delay).
