# QA-073: Approval card has only Approve, Deny and a reason box: a proposed value cannot be edited before approving

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend |
| Reporter | functional-qa-I |
| Found | 2026-11-05 01:49 UTC |
| Versions | backend 1.1.53-1.1.62 (see Where), geomind per backend |
| Where | https://geomind.team chat approval card (set_case), project a0947848 chat 235c60c5 |
| Fixer | hotfix-front |

## Steps

1. Reach any set_case approval card with auto-approve off.

## Expected

A way to edit a proposed value before approving (or a clear hint to use Deny with a reason).

## Actual

Card shows the JSON the call sends, a Reason box, Approve and Deny. No edit control. Editing works only by answering a question card with 'change some'.

## Evidence

- ![screenshot](../evidence/QA-073/1.png)
- Run JSON: `../evidence/QA-073/run-<id>.json`

## Cause

Product gap, not a defect in a working feature; severity minor.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 04:33 UTC: frontend 1.1.75 (2b275e7), pushed, build checked, deploy at 05:00 UTC: hint 'write the change and press Deny'. Editing values in the card needs the Approval answer to carry changed input (backend/geomind); not done.
- 2026-11-05 05:01 UTC: frontend 1.1.75, commit 2b275e7, deployed
## Retest

(Who, when, result.)
