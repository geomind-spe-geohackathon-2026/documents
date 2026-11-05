# QA-139: Plant History version view has no Flowsheet view of that version's diagram

| Field | Value |
|---|---|
| Status | verified |
| Severity | minor |
| Area | frontend |
| Reporter | user via coordinator |
| Found | 2026-11-05 14:53 UTC |
| Versions | frontend 1.1.106, backend 1.1.95 (geomind 0.4.91) |
| Where | https://geomind.team/projects/cf0c3d9c-d925-4ffa-bd29-3ac8205090d3/design/plant; project geo mind testing |
| Fixer | hotfix-front-IV |

## Steps

1. Plant page, History, open a version.

## Expected

Beside "Changes from version N" and "All values", a "Flowsheet" view: the plant diagram of that version (modules and connections); for a compare, changed modules highlighted if cheap.

## Actual

Only the two table views; no way to see a version as a diagram.

## Evidence

- Reported by the user via Coordinator-IV (no screenshot copied).

## Cause

Missing feature in `shared/versions/history.tsx` VersionDetail.

## Fix

hotfix-front-IV: VersionDetail takes extra `views`; the plant passes "Flowsheet", drawn with the report's full flowsheet SVG (`toFullFlowsheetSvg`) from that version's modules and connections, zoomable; above it a line names the modules added or changed from the version before (type, title or module spec differ). No in-diagram highlight (the SVG drawer has no mark for it). Frontend 1.1.109, commit ebc5b51, deployed 2026-11-05 (bundle index-DwO4tlF4.js).
- 2026-11-05 14:58 UTC: frontend 1.1.109, commit ebc5b51, deployed
## Retest

hotfix-front-IV, live: version 21 of geo mind testing shows the Flowsheet tab with the full diagram and "No module changed from version 20.".
- 2026-11-05 14:58 UTC: live check /tmp/hf-check/qa137.js on geo mind testing
