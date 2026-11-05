# QA-277: Run usage goes backwards during a run: 1.34 M input tokens at 17:56, 1.01 M at 18:10, 1.77 M at 18:11 (GET /assistant/runs/{id})

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | backend |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 18:27 UTC |
| Versions | backend 1.1.108-1.1.11x during the run (geomind main 6724bdf at report time) |
| Where | project `QA-TEST QA-E2E-study-I 2` (8eabf827-1f43-4cf8-86a4-39147bea32a0); chat ae934804-eca5-4b3c-99a7-dd60665b5ee9; run 83182f0e-8ee2-4230-a98f-8f0bc905caf3 |
| Fixer | |

## Steps

Poll GET /api/v1/assistant/runs/83182f0e-8ee2-4230-a98f-8f0bc905caf3 every 20 s during the run.

## Expected

usage.input_tokens grows monotonically.

## Actual

17:56:53 input 1 335 681 (cost 0.0334); 18:10:42 input 1 009 575 (cost 0.0260); 18:11:24 input
1 766 579 (cost 0.0420); end 2 675 394 (0.0708). Runs and logs and the chat usage show the same
dips (they read the same field).

## Cause

Guess: run.usage is rebuilt from a subset of sessions (finished sub-agents only, or the latest
session row) while a sub-agent is active; QA-144 made it update during a run.

## Proposed fix

backend: compute running usage as the sum over all sessions of the run (finished and active), or
only ever increase it.

## Fix

## Retest
