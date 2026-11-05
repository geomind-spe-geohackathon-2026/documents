# QA-249: Runs and logs: every run row shows the chat's title (its first message), not the request of that run; six runs of one chat look the same

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend,backend |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 17:49 UTC |
| Versions | backend 1.1.108 |
| Where | https://geomind.team/projects/8fcbf709-537a-40d9-ac1f-abadd1061775/assistant/runs |
| Fixer | hotfix-front-lead |

## Steps

One chat, six requests (simulate, sensitivity, optimise, compare, uncertainty cancelled, continue).
Open Runs and logs.

## Expected

Each row names its own request (the user message that started the run), so the user can find "the
optimisation run" for the agent log the judges ask for.

## Actual

All six rows show "Please simulate the current plant for the whole year 2027…" (the chat title).
The API's run object has `request: null` for every run, so the frontend has nothing else to show.
Only status, tokens and start time differ.

## Evidence

API: GET /assistant/runs?project=8fcbf709-... -> items[*].request = null.

## Proposed fix

backend: store the starting user message (first 120 characters) on the run as `request`;
frontend: show it in the Chat column (chat title as the secondary line).

## Fix

frontend 1.1.124 (commit 9e86452, bundle index-BJQNq3nH.js): each Runs and logs row shows the run's `prompt` (backend 1.1.111, first 120 characters), the chat title under it; without a prompt the chat title as before.

hotfix-back-lead, backend 1.1.111 (additive): every run of `GET /assistant/runs` has `prompt`, the user message that started it (one query per page).
- 2026-11-05 18:05 UTC: frontend 1.1.124 + backend 1.1.111
- 2026-11-05 18:05 UTC: backend 1.1.111
## Retest

Recipe: GET /assistant/runs?project=...: each item has prompt = the chat message text; front shows it in Runs and logs.

QA-E2E-study-I, 2026-11-05 18:40 UTC: verified: each row shows its own request (e.g. 'Compare the two plants of this project...'), the chat title under it.
