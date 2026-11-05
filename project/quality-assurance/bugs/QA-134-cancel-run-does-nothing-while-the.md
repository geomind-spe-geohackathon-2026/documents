# QA-134: Cancel run does nothing while the run waits for an approval; Deny first is needed

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend |
| Reporter | functional-qa-plant-I |
| Found | 2026-11-05 14:20 UTC |
| Versions | backend 1.1.86 (health 11:01 UTC) |
| Where | https://geomind.team/projects/c45a5382-af55-43fc-9340-dd1ab1245533/assistant/chat/6732957b-7035-481a-bc31-7f4abcda2a76; project QA3 plant |
| Fixer | hotfix-front-III |

## Steps

1. Start a run that reaches an approval card ("Build plant"), do not answer it.
2. Click Cancel run (several times, over about two minutes).
3. Then click Deny on the card and click Cancel run again.

## Expected

Cancel run ends the run at once, also while it waits for an approval.

## Actual

With the approval card open, Cancel run did nothing (run stayed active, 4 clicks, also after a page reload). After Deny, one more Cancel run click cleared "1 run active" within 10 s. (Not certain whether Deny alone or Cancel ended it.)

## Evidence

- ![screenshot](../evidence/QA-134/1.png)
- Run JSON: `../evidence/QA-134/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 14:29 UTC: same cause as QA-133 (hotfix-back-III): the Cancel click sends no request while the approval card is open; after Deny the run resumes and the cancel flag/new state ends it. Frontend.

hotfix-front-III, frontend 1.1.105 (ff351c7), deployed 14:35 UTC (bundle index-CJFPBgLt.js). Cause (fact, reproduced at 1280x577 on QA qa-2 run 592f3730 with the cancel request intercepted): the request card in `chat/workspace.tsx` had no height limit, so a tall card filled the chat column and pushed the composer, with its Cancel run button, below the window where it could not be clicked (elementFromPoint at the button: nothing); at 1280x700 the same click sends POST /assistant/runs/{id}/cancel. Fix: the card is at most 45svh high and scrolls inside; Cancel run stays visible and sends the POST (checked intercepted on two waiting runs; no real run cancelled).
- 2026-11-05 14:35 UTC: frontend 1.1.105 deployed 14:35 UTC, bundle index-CJFPBgLt.js: card bounded, Cancel run reachable
- 2026-11-05 14:37 UTC: correction: not verified live. Checked on the identical build locally (1280x577, two waiting runs, cancel intercepted). Before the live check every waiting run in production was cancelled by someone else (run 592f3730 shows 'You denied Merge designs: cancelled'), so there is no waiting run left to test on; retest with the next approval card
## Retest

(Who, when, result.)
- 2026-11-05 14:36 UTC: live 1.1.105 at 1280x577: composer visible under the approval card, Cancel run hit-testable, click sends POST /assistant/runs/592f3730.../cancel (intercepted in the test, run not cancelled)
