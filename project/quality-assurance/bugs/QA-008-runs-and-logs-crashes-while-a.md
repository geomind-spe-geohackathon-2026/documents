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

- qa-7 (2026-11-04 20:33 UTC, frontend bundle index-DnxCbfcj.js, backend 1.1.27): the crash is not only
  during a run. Run 668fb412 (project "QA qa-7 runs and logs", ended `cancelled`):
  https://geomind.team/projects/b3245cdd-63d3-49d3-91e9-e3ec459cb7c1/assistant/runs/668fb412-f060-4bc5-92bf-5836ce5420d1?step=6
  shows "Something went wrong / n.includes is not a function" (stack: usage-line-CYISQ_6h.js, log-page-8BupBPUp.js).
  Steps 1, 2, 3 and 6 crash, exactly the steps with a tool call whose `error` is `true`; steps 0 and 7 open.
  ![qa-7: run log step 6 of a cancelled run](../evidence/QA-008/qa-7-1.png)
  Run JSON: [`../evidence/QA-008/run-668fb412.json`](../evidence/QA-008/run-668fb412.json)

## Cause

Guess: the frontend calls `.includes` on a field it expects as a string or array, and this run's data holds another type there. One odd field must not take down the page. Check with the run's JSON once the run ends.

## Fix

- 2026-11-04 20:01 UTC: frontend 1.1.34, commit e7e40f1 on main (pushed): tool_calls[].error is boolean true in 14 calls of run a61cfb19; step detail now reads the failure from output.error. NOT deployed: hotfix_deploy.sh was denied by this session's permission check; a person must run it or allow it.
- 2026-11-04 20:02 UTC: fixed in frontend 1.1.34 (e7e40f1), waiting for deploy
## Retest
