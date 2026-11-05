# QA-342: Finished run summary drops the time: 'Worked through 62 steps, 2 needed another try · 1.26 M tokens · 0.029 USD' must also show the total time

| Field | Value |
|---|---|
| Status | duplicate |
| Severity | minor |
| Area | frontend |
| Reporter | Sahand (screenshot) |
| Found | 2026-11-05 20:06 UTC |
| Versions | live 2026-11-05 21:05 Trondheim |
| Where | geomind.team chat, the summary line under a finished run |
| Fixer | |

## Steps

1. Let a chat run finish.

## Expected

The finished-run line keeps the run's total time, same field order as the busy list (QA-291/307): 'Worked through 62 steps, 2 needed another try · 1.26 M tokens · 0.029 USD · 14 min 05 s'.

## Actual

The time disappears once the run ends (screenshot).

## Evidence

- ![screenshot](../evidence/QA-342/1.png)

## Cause

Sahand's bug (top). Use the run's started/ended timestamps.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 20:07 UTC: duplicate of QA-341 (same request, already fixing)
## Retest

(Who, when, result.)
