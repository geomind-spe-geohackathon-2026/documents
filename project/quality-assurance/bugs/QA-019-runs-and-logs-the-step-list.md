# QA-019: Runs and logs: the step list's token numbers spill out of the card

| Field | Value |
|---|---|
| Status | verified |
| Severity | cosmetic |
| Area | frontend |
| Reporter | Fatemeh (screenshot), Claude (write-up) |
| Found | 2026-11-04 20:05 UTC |
| Versions | frontend 1.1.33 |
| Where | https://geomind.team/projects/886404e4-3b22-41bd-8986-1a8bc869e25e/assistant/runs/a61cfb19-bfb0-4ae9-9e92-060fc5bd2e40; the step list on the left |
| Fixer | hotfix-front |

## Steps

1. Open Runs and logs, then run a61cfb19 (a run with nested engineers).
2. Scroll the step list.

## Expected

Each row's agent name, step and token count fit inside the list's card.

## Actual

For long agent names (`energy_systems_engineer · step 1` ... `step 5`) the name wraps and the token
number (21,381; 31,425; 54,047; 37,347; 38,653) runs past the card's right border. The list is a
narrow column; the rest of the page to its right is empty.

## Evidence

- Screenshot sent by Fatemeh in the chat with Claude, 2026-11-04 ~20:10 UTC; not saved on disk.
  Add it as `../evidence/QA-019/1.png`.

## Cause

Guess: the row's number column has no room reserved (no `shrink-0` / fixed width) and the card has a
fixed narrow width.

## Fix

- 2026-11-04 20:29 UTC: fixed in frontend 1.1.46 (48616e5), waiting for deploy
- 2026-11-04 21:06 UTC: frontend 1.1.46, commit 48616e5, deployed (1.1.46, bundle index-DAOiLoAA.js, 20:30 UTC)
## Retest

- 2026-11-04 21:11 UTC: geomind.team 1.1.50, Playwright 21:15 UTC: run a61cfb19 step list 300 px, 101 rows, no token count past the card
