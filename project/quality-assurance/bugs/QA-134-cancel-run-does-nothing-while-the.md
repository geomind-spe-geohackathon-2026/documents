# QA-134: Cancel run does nothing while the run waits for an approval; Deny first is needed

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | frontend |
| Reporter | functional-qa-plant-I |
| Found | 2026-11-05 14:20 UTC |
| Versions | backend 1.1.86 (health 11:01 UTC) |
| Where | https://geomind.team/projects/c45a5382-af55-43fc-9340-dd1ab1245533/assistant/chat/6732957b-7035-481a-bc31-7f4abcda2a76; project QA3 plant |
| Fixer | hotfix-back-III |

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
## Retest

(Who, when, result.)
