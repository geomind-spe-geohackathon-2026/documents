# QA-332: Every minimize study fails: internal "'bool' object has no attribute 'to_dict'" in backend core/gemini/study.py:185 plain_day (coverage_of) on gemini 0.6.31

| Field | Value |
|---|---|
| Status | open |
| Severity | blocker |
| Area | backend |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 19:43 UTC |
| Versions | backend 1.1.124 (geomind 0.4.131, gemini 0.6.31) |
| Where | project 2630a05f-3ef6-4618-8f08-53191b8c906e (no-agent rerun), studies e5d0dc3f, f7140d63, f96fd1fc, 8d762d63, 9bcfe88a; celery 20:42 CET |
| Fixer | |

## Steps

POST /design/study kind minimize (prepare size, lcts, 40 evaluations, seed 0) on any of the five sample candidate plants.

## Expected

Done with a result, as the same studies did at 19:56-20:05 CET on gemini 0.6.26 (project 8d5d21e0).

## Actual

All five fail at the end: `internal: 'bool' object has no attribute 'to_dict'`. Celery traceback: tasks.py:34 run_study -> services.py:578 run_study -> 542 compute -> core/gemini/study.py:268 run -> 195 coverage_of -> 185 plain_day.

## Cause

Fact: `plain_day` calls `value.to_dict()` on every non-string value of a coverage day; gemini's daily_coverage (0.6.31, probably the QA-238/322 cooling class change) now puts a bool in a day (for example a flag like 'backup' or 'plant only'). Fix: pass bools, numbers and None through as they are.
Every study with a full-year run is broken on production, agent runs included.

## Fix

## Retest
