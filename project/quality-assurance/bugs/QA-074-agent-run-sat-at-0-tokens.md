# QA-074: Agent run sat at 0 tokens for about 10 minutes (running, no steps) after the answer to a question, then had to be cancelled

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | backend |
| Reporter | functional-qa-I |
| Found | 2026-11-05 01:49 UTC |
| Versions | backend 1.1.53-1.1.62 (see Where), geomind per backend |
| Where | project a0947848, chat 235c60c5, run 92971ce5 (backend 1.1.62, started 00:28 UTC) |
| Fixer | hotfix-back |

## Steps

1. Answer a question card (reservoir pressure), then send 'go on' about 00:28 UTC.
2. Look at Runs and logs for 10 minutes.

## Expected

Steps or tokens appear within a minute, or an error.

## Actual

Run status 'running', 0 tokens for about 10 min, chat showed 'Case lead Thinking, Steps so far' (empty). I cancelled it: 'Worked through 32 steps, 18 needed another try' (so there were retries). Deploys 1.1.61 to 1.1.62 happened around that time (QA-017 pattern: running with no process). Not tied to a deploy with certainty.

## Evidence

- ![screenshot](../evidence/QA-074/1.png)
- Run JSON: `../evidence/QA-074/run-<id>.json`

## Cause

Guess: the run was resumed after the 00:3x deploy and stalled, or the provider call retried 18 times without showing it (QA-030).

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
