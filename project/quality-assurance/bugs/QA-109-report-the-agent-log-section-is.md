# QA-109: Report: the Agent log section is empty by default ('No assistant run was chosen'); the run that made the result is not picked

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | frontend |
| Reporter | Fatemeh (screenshots), Claude (write-up) |
| Found | 2026-11-05 10:43 UTC |
| Versions | backend 1.1.84 |
| Where | https://geomind.team/projects/cf0c3d9c-d925-4ffa-bd29-3ac8205090d3/design/report?chat=27379f2e-0103-4ddf-a020-f0cd4deb20a6 (report of sized1) |
| Fixer | hotfix-front-III |

## Steps

1. Open Design > Report for the result sized1 (made by the assistant's run 32a12115).
2. Scroll to "Agent log and tokens".

## Expected

The section shows the run that made the result (the study's `started_by_run_id`), or the chat's latest run, without opening Options.

## Actual

"No assistant run was chosen." The user must open Options and pick "Run 32a12115 (running)" by hand; then the URL gets `&run=...`.

## Evidence

- ![report, empty agent log](../evidence/QA-109/1.webp)
- ![Options, run picked by hand](../evidence/QA-109/2.webp)

## Cause

Fact: `frontend/src/domains/design/report/report-editor.tsx` line 67, `const run = params.get("run") ?? ""`: no run unless the URL has one. Fix: default to the result's study `started_by_run_id` (or the chat's latest run when `chat=` is in the URL).

## Fix

## Retest
