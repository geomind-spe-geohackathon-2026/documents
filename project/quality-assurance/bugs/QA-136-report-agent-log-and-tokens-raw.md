# QA-136: Report, Agent log and tokens: raw figures (Input tokens 14837406, Cost 0.45972432399999985)

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | backend |
| Reporter | hotfix-front-III |
| Found | 2026-11-05 14:30 UTC |
| Versions | frontend 1.1.104 |
| Where | https://geomind.team/projects/cf0c3d9c-d925-4ffa-bd29-3ac8205090d3/design/report; run 32a12115 |
| Fixer | hotfix-back-III |

## Steps

1. Open Design > Report in project "geo mind testing" (cf0c3d9c); it opens on lcts_best with run 32a12115.
2. Read "Agent log and tokens".

1. 
2. 

## Expected

Tokens and cost read like the rest of the app (14.8 M tokens in, 625 K out, 0.46 USD), as Runs and logs shows them (QA-103).

## Actual

"Input tokens: 14837406 / Output tokens: 625009 / Cost: 0.45972432399999985" (frontend 1.1.104, live 14:27 UTC).

## Evidence

- Text read live with Playwright (`/tmp/hf-check/qa127.js`); no screenshot.

## Cause

Fact: `backend/src/api/v1/reporting/design/services.py` line 275 writes `f"- Input tokens: {run.input_tokens}"` and the cost the same way, unformatted; the frontend shows the preview text as the backend sends it.


## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
