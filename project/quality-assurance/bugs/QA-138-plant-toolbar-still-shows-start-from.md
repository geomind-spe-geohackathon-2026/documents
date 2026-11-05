# QA-138: Plant toolbar still shows Start from template although templates were rejected (IMP-023)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend |
| Reporter | user via coordinator |
| Found | 2026-11-05 14:53 UTC |
| Versions | frontend 1.1.106, backend 1.1.95 (geomind 0.4.91) |
| Where | https://geomind.team/projects/cf0c3d9c-d925-4ffa-bd29-3ac8205090d3/design/plant; project geo mind testing |
| Fixer | hotfix-front-IV |

## Steps

1. Open the Plant page of a project with a plant.

## Expected

No "Start from template" button (user decision: no templates, IMP-023 rejected).

## Actual

The Plant toolbar showed "Start from template" beside History.

## Evidence

- Reported by the user via Coordinator-IV (no screenshot copied).

## Cause

The toolbar button and its replace-plant dialog were still wired in `domains/design/plant/page.tsx`.

## Fix

hotfix-front-IV: toolbar button, its dialog and state removed (`page.tsx`). The empty-plant card ("This project has no plant yet") still offers a template start; remove it too if the user wants. Frontend 1.1.108, commit 97dd942, live in 1.1.109 (bundle index-DwO4tlF4.js).
- 2026-11-05 14:58 UTC: frontend 1.1.108, commit 97dd942, deployed (1.1.109)
## Retest

hotfix-front-IV, live: 0 "Start from template" buttons on the Plant page of geo mind testing.
