# QA-070: Nested design_lead is 'interrupted by a crash' twice in one start-to-end run (duration 0 s); the project lead gives up the full brief and narrows the scope

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | functional-qa-I |
| Found | 2026-11-05 01:21 UTC |
| Versions | backend 1.1.62 (health 2026-11-05 ~01:20 local server time), geomind per backend |
| Where | https://geomind.team/projects/61134432-45fa-48db-afef-4f930f3825da/assistant/runs/861ef137-08a2-4252-bf30-437630caf747; project QA2 functional-qa-I full run; chat 81b51db5; run 861ef137; project_lead steps 3 and 4 (run JSON steps index 28 and 60) |
| Fixer | hotfix-python |

## Steps

1. New project with the PDF and both CSVs, auto-approve on; ask for the full challenge loop (design, check, improve, explain).
2. Answer the case questions; the design phase starts.

## Expected

The nested design_lead runs, or a real error is shown; if the process was interrupted it is resumed (QA-035), not reported as a crash.

## Actual

project_lead called design_lead twice; both returned {'error': {'code': 'internal', 'message': 'design_lead: interrupted by a crash; it may have run in part'}} with duration 0.0 s. Project lead then wrote: 'The design team has crashed twice on the full superstructure brief. Rather than repeat it a third time, I will narrow the scope to a single configuration build-and-simulate.' So the full-loop request (several configurations, comparison) was silently shrunk. Run JSON has 5 'interrupted by a crash' errors in total. Celery was restarted during the hour (hotfix deploys), so deploys may be the cause; the log shows no Python traceback.
## Evidence

- ![screenshot](../evidence/QA-070/1.png)
- Run JSON: `../evidence/QA-070/run-<id>.json`

## Cause

Guess: a worker restart (deploy) killed the nested run and the parent treated it as a crash instead of resuming; a second restart repeated it. Also, the project lead should not drop the user's scope (several configurations) without telling the user.

## Fix

Cause (code, hotfix-python-II): when a deploy restarts the worker, the backend resumes the run (QA-035) and geomind's `Engine.proceed` first ends every nested run left open (`end_orphans`, `interrupted by a crash`), then `settle_interrupted` turns each open call of a tool that is not idempotent into the error `<tool>: interrupted by a crash; it may have run in part` at once (0.0 s). A `Delegate` (the nested design lead) is not idempotent, so every restart during a nested run failed it; the 01:00 and 01:06 deploys match the two failures. The cause is in geomind, not the backend resume. Fix: `Delegate` and `Team` carry `reruns_after_crash`, and `settle_interrupted` leaves their open call to run again with the same brief (a new nested run), like an idempotent tool; the old nested run is still ended and its spending kept. The project lead's prompt: a failed team gets the same brief once more; a second failure is said plainly or asked, never a smaller task done silently.
- 2026-11-05 01:31 UTC: geomind 0.4.64 (d60481a: Delegate/Team calls left open by a restart rerun on resume; project lead never narrows the brief silently), backend 1.1.65 (599b639), deployed 01:30 UTC
## Retest

(Who, when, result.)
