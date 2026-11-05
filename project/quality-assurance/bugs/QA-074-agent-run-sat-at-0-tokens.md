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

- 2026-11-05 hotfix-back (analysis, no change yet): "32 steps, 18 needed another try" means the
  model calls were failing and being retried, not that the worker or the queue sat idle: geomind
  retries a failed provider call up to GEOMIND_RETRY_COUNT=5 times with 2, 4, 8, 16, 32 s back-off
  (about a minute per call, then the fallbacks), and `usage` counts only calls that succeeded, so
  the run shows 0 tokens. Around 00:30 UTC the OpenRouter key was reaching its 10 USD limit
  (QA-068), which fits. Since then: the backend streams each retry as a live `retry` event
  (QA-021, 1.1.23) and names a provider refusal `provider_refused` with a plain message (QA-068,
  1.1.62); the chat showing the retry event is QA-030 (frontend).
- To confirm (production DB reads are refused to this session), a person runs on the Dell:
  `sg docker -c "docker exec -i geomind-postgres sh -c 'psql -U \$POSTGRES_USER -d \$POSTGRES_DB -At'" <<< "select sequence, type, left(data->>'error', 160), data->>'delay', data->>'message' from run_events where run_id='92971ce5-...' and type in ('retry','error','run.finished') order by sequence;"`
  (the full run id from the Runs page). 429/402/403 in the errors confirms the cause.

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
