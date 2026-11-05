# QA-164: Search dialog finds only projects of the first page (50): a newer project such as 'Hackathon report run' is not found by name

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend |
| Reporter | Sahand (screenshot), Manual QA-IV |
| Found | 2026-11-05 17:06 UTC |
| Versions | frontend live 2026-11-05 17:05 UTC, backend 1.1.104 |
| Where | https://geomind.team/projects, search dialog (Search in the sidebar) |
| Fixer | hotfix-front-VII |

## Steps

1. Have more than 50 projects (production has more).
2. Open Search and type `report`.

## Expected

Every project whose name holds `report`, also 'Hackathon report run 2026-11-05 16:58' (created 16:58 UTC).

## Actual

Only three: 'QA qa-5 outputs report e2e', 'QA3 report', 'QA-TEST QA-E2E-report-I 1'. The API with the same term
(`GET /workspace/projects?search=report`) returns four, the newest included.

## Evidence

- ![screenshot](../evidence/QA-164/1.png)

## Cause

Fact: `frontend/src/app/layouts/search-dialog.tsx:41` loads `useInfiniteQuery(projectsQuery(""))`, the first page (50)
of all projects with no search term, and the command list filters that page in the browser. Projects past the first
page are never matched. Fix: send the typed term to `projectsQuery(term)` (the API's `search` works), debounced.

## Fix

frontend 1.1.114 (commit 5fdd4ea, bundle index-Co1lDzOn.js): `search-dialog.tsx` keeps the typed term, debounces it (250 ms) and loads `projectsQuery(term)`, so the API `search` finds every project; the previous list stays while the next one loads.
- 2026-11-05 17:11 UTC: frontend 1.1.114, commit 5fdd4ea
## Retest

Not run (no tests now). Retest: Search, type `report`, the 16:58 'Hackathon report run' must show.
