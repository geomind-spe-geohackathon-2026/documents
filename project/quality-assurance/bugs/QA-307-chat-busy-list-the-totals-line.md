# QA-307: Chat busy list: the totals line reads 'Total · 77 steps · 2.2 M tokens · 0.05 USD · 7 min 23 s' in the same format as the agent lines, always last

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | frontend |
| Reporter | Sahand (screenshot) |
| Found | 2026-11-05 18:57 UTC |
| Versions | live 2026-11-05 19:54 Trondheim (after QA-291) |
| Where | geomind.team chat, busy list under a running run |
| Fixer | |

## Steps

1. Run any agent request in chat and look at the busy list.

## Expected

The last line, below all agent lines, reads 'Total · 77 steps · 2.2 M tokens · 0.05 USD · 7 min 23 s': label 'Total' in the same bold style as the agent names, then the same fields in the same order and separators as the agent lines (steps · tokens · cost · time).

## Actual

'Steps so far (77 steps) · 2.2 M tokens · 0.05 USD · 7 min 23 s' in a different style.

## Evidence

- ![screenshot](../evidence/QA-307/1.png)

## Cause

Follow-up of QA-291, Sahand's request (top priority).

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
