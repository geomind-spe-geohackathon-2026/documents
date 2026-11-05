# QA-231: Run usage on GET /assistant/runs/{id} jumps down and up during a run (2.24 M -> 0.65 M -> 5.17 M input tokens within 15 min) and ends below the per-agent total (5.18 M vs 5.56 M, 0.133 vs 0.155 USD)

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | backend |
| Reporter | QA-E2E-design-I |
| Found | 2026-11-05 17:30 UTC |
| Versions | backend 1.1.102 -> 1.1.107 during the run (deploys at 16:56 and ~17:30), geomind 0.4.97 |
| Where | run 76d19df6-485f-46ee-a182-6b03ed70ab33 (project QA-TEST QA-E2E-design-I 1) |
| Fixer | |

## Steps

1. Start a design run in chat; poll GET /api/v1/assistant/runs/{id} and GET .../agents every 10-20 s.

## Expected

`usage` rises monotonically and ends equal to `agents.run` totals (QA-144: run totals count nested runs at any depth).

## Actual

| UTC | runs/{id} usage input | agents run input |
|---|---|---|
| 16:52 | 191,899 | |
| 17:04 | 597,619 | |
| 17:13 | 1,771,496 | |
| 17:16 | 2,242,124 | |
| ~17:29 | **652,415** (cost 0.0114) | 5,476,008 |
| ~17:30 | 5,165,910 | 5,546,063 |
| 17:31 (done) | 5,183,327 (0.1330 USD) | 5,563,480 (0.1546 USD) |

Manual QA-IV saw this run as "running with 0 tokens" around 17:00 (coordinator, 17:04 UTC). Runs and logs and any budget check that read `run.usage` show a wrong value, sometimes a fraction of the real spend.

## Evidence

Polled values above (scratch log of this session; reproducible by polling a running run).

## Cause

Guess: `run.usage` is rewritten from one session's usage (the current top-level agent) at some events and from the nested sum at others; deploys during the run (16:56, ~17:30) restarted the worker, and the resumed run may start the count again.

## Proposed fix

Compute `run.usage` as the sum over all sessions of the run (the same query as /agents), or only ever add to it; a test with a nested run resumed after a worker restart.

## Fix

Backend 1.1.117 (3113417, back-m2, lead hotfix-back-lead-II): UsageTree returns the tree totals for root usage events too and keeps each key's peak; set_values never writes a usage column below the row; on the root run.finished the recorder writes usage summed from every stored event (sessions.stored_totals, as /agents). Covers QA-144 and QA-277.

## Retest

Poll GET /assistant/runs/{id} during a run with nested agents: input_tokens only rises; at the end it equals the sum of GET /assistant/runs/{id}/agents.
