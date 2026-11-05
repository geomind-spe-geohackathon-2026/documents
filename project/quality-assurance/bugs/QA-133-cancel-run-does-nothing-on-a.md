# QA-133: Cancel run does nothing on a run waiting at an approval card (stays 'waiting', 1 run active)

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | frontend,backend |
| Reporter | functional-qa-case-I |
| Found | 2026-11-05 14:20 UTC |
| Versions | backend 1.1.88 |
| Where | https://geomind.team/projects/15b2f15f-46d0-4b09-a44b-0f849127c1f0 (QA3 case); chat 37fb7886-a3b0-46b3-b36f-6afb72971d14; run 11597465 (Runs and logs) |
| Fixer | |

## Steps

1. Start a case request in the chat; leave the run at a "Set case" approval card (waits for your approval).
2. Press "Cancel run" (clicked 4 times, by ref, by role and by DOM click, also after a reload).
3. Look at the chat list, the header and Runs and logs.

## Expected

The run is cancelled: status cancelled, "1 run active" gone, the chat accepts a new message.

## Actual

No toast, no change. The chat still says "waits for your approval", the header still says "1 run active", Runs and logs lists run 11597465 as waiting. Runs and logs has no cancel action. The run has lived across deploys (1.1.84 to 1.1.88).

## Evidence

- ![screenshot](../evidence/QA-133/1.png)

## Cause

Guess: cancel is not handled for the waiting status, or a deploy resume left the run without a process (see QA-077).

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
