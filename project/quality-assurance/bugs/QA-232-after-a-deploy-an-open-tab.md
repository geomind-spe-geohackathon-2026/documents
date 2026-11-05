# QA-232: After a deploy an open tab shows 'Something went wrong: Failed to fetch dynamically imported module .../page-D7FMcjkq.js' instead of reloading itself

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | frontend |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 17:40 UTC |
| Versions | backend 1.1.106 -> 1.1.108 (deploys at 17:24, 17:28, 17:39 UTC) |
| Where | https://geomind.team/projects/8fcbf709-537a-40d9-ac1f-abadd1061775/design/results |
| Fixer | |

## Steps

1. Keep a project page open (Design > Results) while a frontend deploy happens.
2. Navigate to another route of the app (or the "GeoMind is updating" page reloads itself).

## Expected

The app notices the new build (a chunk 404 / import error) and reloads the page once, so the user
lands on the same route in the new build.

## Actual

Full-page error: "Something went wrong — Failed to fetch dynamically imported module:
https://geomind.team/assets/page-D7FMcjkq.js — Back to projects". A manual reload a minute later
works. Seen once at 17:39:40 UTC, right after the API came back as 1.1.108.

## Evidence

Text of the page copied above (the screenshot was taken after the next reload, which showed the
"GeoMind is updating" page instead).

## Cause

Fact: the old index refers to a lazy chunk hash the new build no longer serves.

## Proposed fix

frontend: in the router's error boundary (or a `vite:preloadError` listener), on a dynamic import
failure reload the page once (guard with a sessionStorage flag to avoid a loop).

## Fix

## Retest
