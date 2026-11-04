# QA-008: Runs and logs crashes while a run is active: "n.includes is not a function"

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | frontend |
| Reporter | Fatemeh (screenshots), Claude (write-up) |
| Found | 2026-11-04 ~19:00 UTC |
| Versions | frontend 1.1.33, backend 1.1.14 (geomind 0.4.25) |
| Where | https://geomind.team/projects/886404e4-3b22-41bd-8986-1a8bc869e25e/assistant/runs/a61cfb19-bfb0-4ae9-9e92-060fc5bd2e40?step=23 |
| Fixer | hotfix-front |

## Steps

1. Open Runs and logs while the run a61cfb19 is still running.
2. Open the run (step 23).

## Expected

The run's steps show as they come.

## Actual

The whole page is the error page: "Something went wrong / n.includes is not a function / Back to projects".

## Evidence

- No screenshot yet; the run JSON goes in `../evidence/QA-008/` once the run ends.

## Cause

Guess: the frontend calls `.includes` on a field it expects as a string or array, and this run's data holds another type there. One odd field must not take down the page. Check with the run's JSON once the run ends.

## Fix

- 2026-11-04 20:01 UTC: frontend 1.1.34, commit e7e40f1 on main (pushed): tool_calls[].error is boolean true in 14 calls of run a61cfb19; step detail now reads the failure from output.error. NOT deployed: hotfix_deploy.sh was denied by this session's permission check; a person must run it or allow it.
## Retest
