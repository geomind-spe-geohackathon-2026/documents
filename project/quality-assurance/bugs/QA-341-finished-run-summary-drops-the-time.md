# QA-341: Finished run summary drops the time: 'Worked through 62 steps, 2 needed another try · 1.26 M tokens · 0.029 USD' must also show the total time (steps · tokens · cost · time)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend |
| Reporter | Sahand (screenshot) |
| Found | 2026-11-05 20:05 UTC |
| Versions | frontend <x.y.z>, backend <x.y.z> (geomind <x.y.z>) |
| Where | <URL>; project <name/id>; chat <id>; run <id>; step <n> |
| Fixer | front-m1 |

## Steps

1. 
2. 

## Expected

Added by Sahand (2026-11-05 21:07 Trondheim): after the run finishes, keep the whole busy list too,
not only the summary line: one line per agent with steps · tokens · cost · time, and the Total line
(QA-291/307), frozen at their final values (activity shown as 'done'), collapsible but not removed,
and still there after a page reload.

## Actual

## Evidence

- ![screenshot](../evidence/QA-341/1.png)
- Run JSON: `../evidence/QA-341/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 20:16 UTC: frontend 1.1.140 (bundle index-CzdSC_uX.js)
## Retest

(Who, when, result.)
