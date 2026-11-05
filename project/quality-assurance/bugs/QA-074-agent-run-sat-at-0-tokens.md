# QA-074: Agent run sat at 0 tokens for about 10 minutes (running, no steps) after the answer to a question, then had to be cancelled

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind,gemini,frontend |
| Reporter | functional-qa-I |
| Found | 2026-11-05 01:49 UTC |
| Versions | backend 1.1.53-1.1.62 (see Where), geomind per backend |
| Where | project a0947848, chat 235c60c5, run 92971ce5 (backend 1.1.62, started 00:28 UTC) |
| Fixer | hotfix-front-II |

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

- 2026-11-05: production DB read by Claude for Fatemeh (read-only), run 92971ce5-5972-4c7f-a0cb-839f893a1b09:
  - No `retry` and no `error` events at all, so not provider refusals. The run worked the whole
    time: 23 llm.completed (coordinator, project lead, then the case lead from 00:29:14 to 00:39:23),
    32 tool calls, and the runs row holds 708,733 input tokens. The "0 tokens, Steps so far (empty)"
    was the page, not the run (the chat and Runs and logs did not show the nested case lead's steps
    and usage while it ran).
  - "18 needed another try" = 17 `calculate` calls, all refused, plus the case_lead call. The case
    lead tried to compute the hydrostatic reservoir pressure (brine density x g x depth, "brief p.2
    rule") and calculate refused every unit it tried for g and for the intermediate:
    `kg/m2`, `m/s2`, `m/s^2`, `N/kg`, `m/s²`, `m/s/s` ... ("is not a unit gemini knows"),
    13 different refusals. Two slow calls on top: 200.9 s (00:32:53 to 00:36:14) and 81 to 83 s.
  - So the bug is two things: (1) calculate (gemini's unit registry) has no acceleration unit and no
    kg/m2, so rho*g*h cannot be written; (2) the chat does not show a nested agent's steps and tokens
    while they happen. Set back to open; areas geomind/gemini (calculate units) and frontend (live
    nested steps).

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 04:14 UTC: hotfix-back: most likely provider refusals retried with back-off (0 tokens = no call succeeded) around the key limit (QA-068), not an idle worker or queue; visible now through the retry event (QA-021) once QA-030 shows it, and provider_refused (QA-068). Needs a person to read the run's retry/error events (query in Fix) to confirm; prod DB reads are refused to me.
- 2026-11-05 09:15 UTC: DB read: no provider errors; 17 calculate calls refused (no unit for g: m/s2, N/kg ...); 708k tokens recorded, the page showed 0
- 2026-11-05 09:16 UTC: Cause found by a DB read 09:15 UTC: calculate has no unit for g (m/s2, N/kg, kg/m2 refused 17x) and the chat does not show a nested agent's live steps/tokens; routed to hotfix-python-II (units, constant g) and hotfix-front (live nested steps)
- 2026-11-05 09:18 UTC: frontend part by hotfix-front: 1.1.79 (e131a37), pushed and build-checked, held. Nested agents' events do reach the live stream (geomind's nested runs share the root's log; the backend publishes every public event). The chat now sums finished steps for tokens and cost while the usage total lags, and 'Steps so far' shows its count (it was collapsed, not empty). The 0 tokens in Runs and logs comes from the stored run row and log, not the chat.
## Retest

(Who, when, result.)
