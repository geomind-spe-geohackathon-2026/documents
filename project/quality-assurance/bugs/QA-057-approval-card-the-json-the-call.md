# QA-057: Approval card: the JSON the call sends loses its indentation (pre-line, proportional font); nested values unreadable

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend |
| Reporter | qa-ux |
| Found | 2026-11-04 23:50 UTC |
| Versions | frontend 1.1.50 (per STATUS.md), backend 1.1.53 (health), geomind 0.4.54 |
| Where | https://geomind.team/projects/4cfeab2d-73e3-4299-a1f8-afec3d7e4bae/assistant/chat; project QA2 qa-ux flow; first run of the first chat; approval of set_case |
| Fixer | hotfix-front |

## Steps

1. New project, attach the three competition files, send "read them and help me set up the case".
2. Wait until the Approval needed card for set_case appears.
3. Read the "What the call sends" block.

## Expected

The call's input is readable: indentation kept, a monospace font or a formatted key/value list, long values wrapped.

## Actual

The block is JSON text, but every line starts at the left edge (nested objects not indented), in the proportional UI font. The card's element has `white-space: pre-line` (computed style), which collapses the leading spaces. Nesting depth cannot be seen. The title "Allow set_case (write)?" also uses the tool's internal name.

## Evidence

- ![screenshot](../evidence/QA-057/1.png)
- Run JSON: `../evidence/QA-057/run-<id>.json`

## Cause

Guess: the card text container uses class `whitespace-pre-line` (seen in the DOM); `whitespace-pre-wrap` with a `font-mono` block for the JSON part would keep the indentation.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 00:06 UTC: frontend 1.1.58 (742031b), pushed, build checked; deploy at 00:30 UTC
- 2026-11-05 00:31 UTC: frontend 1.1.58, commit 742031b, deployed (1.1.67)
## Retest

(Who, when, result.)
