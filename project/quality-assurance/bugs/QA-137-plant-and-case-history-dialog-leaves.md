# QA-137: Plant and Case History dialog leaves a large empty area under the version table and under a version's changes

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | frontend |
| Reporter | user via coordinator |
| Found | 2026-11-05 14:53 UTC |
| Versions | frontend 1.1.106, backend 1.1.95 (geomind 0.4.91) |
| Where | https://geomind.team/projects/cf0c3d9c-d925-4ffa-bd29-3ac8205090d3/design/plant; project geo mind testing |
| Fixer | hotfix-front-IV |

## Steps

1. Open the Plant page of project "geo mind testing" and click History.
2. Open a version (e.g. 21) on "Changes from version 20".
3. Do the same on the Case page.

## Expected

The window fits its content (height follows the rows, the list scrolls within a sensible maximum) or fills the space usefully.

## Actual

The window always filled the screen height: the version list showed about 10 rows, then blank; "Changes from version 21" showed 2 rows over a full-height empty panel. Same on Case History.

## Evidence

- Reported by the user via Coordinator-IV (no screenshot copied).

## Cause

`shared/layout/history-button.tsx` gave DialogContent a fixed `h-[calc(100svh-4rem)]`, and the tables inside were capped at 55-60vh.

## Fix

hotfix-front-IV: DialogContent `max-h` instead of `h` (height follows content, at most the screen); version list max `100svh-13rem`, changes/values tables max `100svh-20rem`, each scrolls inside. Frontend 1.1.109, commit ebc5b51, deployed 2026-11-05 (bundle index-DwO4tlF4.js).

## Retest

hotfix-front-IV, live, Playwright /tmp/hf-check/qa137.js: list window and version window size to their content; Flowsheet view fits.
