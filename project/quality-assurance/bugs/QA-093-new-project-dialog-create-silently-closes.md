# QA-093: New project dialog: Create silently closes the dialog and creates nothing when the window is short (Create below the fold) and Shared memory is left empty; no message

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend |
| Reporter | functional-qa-3 |
| Found | 2026-11-05 09:27 UTC |
| Versions | frontend 1.1.71, backend 1.1.69-1.1.72 |
| Where | https://geomind.team/projects, button 'New project'; browser window about 1280x577 |
| Fixer | hotfix-front-II |

## Steps

1. In a short window (height about 580 px) open New project, type a name, leave Shared memory empty.
2. Click Create (below the visible part of the dialog).

## Expected

Either the project is created, or a message says what is missing (Shared memory not chosen).

## Actual

Created nothing, the dialog closed, no toast, no error, no request sent to the API (network log empty), no new project in the list; done three times. With the window made 1400 px high, Shared memory set to Off, Create worked at once ('Project created'). Which of the two (short window, empty Shared memory) causes it is not isolated.

## Evidence

- ![screenshot](../evidence/QA-093/1.png)
- Run JSON: `../evidence/QA-093/run-<id>.json`

## Cause

The dialog closed on any pointer-down outside it (Radix default), and in a 577 px window Create sat below the dialog's visible part, so a click aimed at it could land on the overlay and close the dialog with nothing sent. The Shared memory message appeared beside the select, out of view when the dialog was scrolled.

## Fix

frontend 1.1.81, commit 8eacf11 (hotfix-front-II): the dialog ignores clicks outside (Cancel, X and Escape still close it); Cancel and Create stick to the dialog's foot; a missing name or Shared memory scrolls to and focuses that field next to its message. Checked on a local build at 1280x577: Create visible at y=512, an outside click keeps the dialog open, Create with empty Shared memory shows the message and focuses the select, no POST. Deploy: 10:00 UTC window.
- 2026-11-05 10:02 UTC: frontend 1.1.81, commit 8eacf11, deployed 10:01 UTC (live 1.1.84)
## Retest

(Who, when, result.)
