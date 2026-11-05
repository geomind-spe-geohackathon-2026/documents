# QA-354: Auto-approve on, but the run waited 10+ min on a case_lead question (request-443) with no automatic answer, after the deploy 62 restart; answered by hand to go on

| Field | Value |
|---|---|
| Status | fixing |
| Severity | blocker |
| Area | backend,geomind |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 20:52 UTC |
| Versions | backend 1.1.130 (geomind 0.4.135); run started on 1.1.128 before deploy 62 |
| Where | run b3a69d7c-58c4-4322-a747-203c5e206af6 (clean report run), project bf1bccef-f12e-43e5-b273-9040337062cc, chat 185e5160 (auto_approve true) |
| Fixer | m2 |

## Steps

1. Chat with auto-approve on (GET /assistant/chat/185e5160.../auto-approve -> true); run started 21:33 CET.
2. The case lead asks request-443 ("The case is not saved yet ... approve all / change some / stop") at about 21:41 CET; deploy 62 (backend 1.1.130) restarts the API and the worker at about 21:40.

## Expected

Answered automatically within seconds (QA-339 test run 7fb2db3c did this on 1.1.128).

## Actual

The run stayed 'waiting' on request-443 until 21:52 CET (11 min, steps and cost unchanged); answered by hand ("approve all") to let the report run go on.

## Cause

Guess: the automatic answer is scheduled in the worker when the request opens; a request opened just before or during the restart is not re-scheduled on resume (like QA-264 for answers).

## Fix

## Retest
