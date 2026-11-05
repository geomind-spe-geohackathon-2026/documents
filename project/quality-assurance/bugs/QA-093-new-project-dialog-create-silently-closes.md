# QA-093: New project dialog: Create silently closes the dialog and creates nothing when the window is short (Create below the fold) and Shared memory is left empty; no message

| Field | Value |
|---|---|
| Status | fixing |
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

Guess: the click lands on the overlay below the dialog (closing it), or validation of the required Shared memory select closes the dialog without a message.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
