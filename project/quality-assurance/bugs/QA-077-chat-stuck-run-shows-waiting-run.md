# QA-077: Chat stuck: run shows 'waiting' (run JSON says failed), no Cancel button, new messages refused with 'The chat has a run that is not finished'

| Field | Value |
|---|---|
| Status | open |
| Severity | blocker |
| Area | backend |
| Reporter | functional-qa-I |
| Found | 2026-11-05 04:15 UTC |
| Versions | backend 1.1.69 (health 2026-11-05 ~04:20 UTC) |
| Where | project 61134432, chat 81b51db5-1a6b-402a-9223-66c8af1c6403, run 861ef137-08a2-4252-bf30-437630caf747 |
| Fixer | |

## Steps

1. Run QA-076's start-to-end request; let it run until the usage pause and the later deploys.
2. Come back at 04:20 UTC, type a message and press Enter.

## Expected

The message is accepted, or the stuck run is shown as failed with a Retry/Cancel button.

## Actual

Runs and logs lists the run as 'waiting' (8,152,119 tokens); the exported run JSON says status 'failed', ended 01:49 UTC. The chat shows no Cancel button; sending a message gives 'The chat has a run that is not finished'. The user cannot go on in this chat (same family as QA-017/QA-056).
## Evidence

- ![screenshot](../evidence/QA-077/1.png)
- Run JSON: `../evidence/QA-077/run-<id>.json`

## Cause

Guess: the run ended failed in the worker but the DB status stayed waiting (deploys 1.1.65-1.1.69 during the run).

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
