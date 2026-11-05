# QA-068: OpenRouter API key limit reached (403 'Key limit exceeded', 10 USD of 10 USD used): every agent run fails; the chat shows only 'internal error in geomind'

| Field | Value |
|---|---|
| Status | fixed |
| Severity | blocker |
| Area | infra |
| Reporter | qa-func-1 |
| Found | 2026-11-05 00:24 UTC |
| Versions | backend 1.1.61 (health 2026-11-05 00:30 UTC), frontend 1.1.61 clone |
| Where | https://geomind.team/projects/a0947848-b958-4ee9-8927-56ec0a9cff03/assistant/runs/6d47f7c9-db08-42da-aa66-f9c212991e41; project QA2 qa-func-1 S1 full case; chat 235c60c5-da86-4f21-9257-e21a6e400697; run 6d47f7c9 |
| Fixer | hotfix-back |

## Steps

1. Answer a question card in the chat (after the 00:22 UTC restart).
2. The run fails after the next LLM call.

## Expected

Runs go on; if the provider key is exhausted, the chat says so (key limit reached) and the operator is warned.

## Actual

Run log: 'OpenRouter: status = 403; Key limit exceeded (total limit) ... $10.00 of $10.00 used; does not reset' (limit_source openrouter_key_limit, limit_usd 10, spend 10.0014). The chat shows 'The assistant stopped with an internal error in geomind'. All sessions' new runs will fail until the key limit is raised. Run JSON in evidence. Also seen in the same run: set_case tried site.reservoir.pressure.hydrostatic, refused with unknown_name (no such key) - the agent invented a key for 'hydrostatic rule'.
## Evidence

- ![screenshot](../evidence/QA-068/1.png)
- Run JSON: `../evidence/QA-068/run-<id>.json`

## Cause

Fact: the OpenRouter key has a total cap of 10 USD that does not reset. Chat text is the generic internal error, not the provider message.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 00:26 UTC: hotfix-back, backend 1.1.62 (9223d0b), deployed: the error is not swallowed in geomind (run.finished has stop_reason error and OpenRouter's text); the frontend shows 'internal error in geomind' for every stop_reason error. The backend now maps a provider 401/402/403/429 in the failure message to stop_reason and error.code provider_refused with a plain message (403 key limit: 'The model provider refused: key limit exceeded; an admin must raise it.'), live, on replay and in the run row; the frontend then shows 'Run failed: <message>'. Checked with the QA-068 message. The key limit itself is Sahand's (raised separately).
## Retest

functional-qa-I, 2026-11-05 ~00:45 UTC, backend 1.1.62: the earlier failed run (6d47f7c9) now shows in the chat 'Run failed: The model provider refused: key limit exceeded; an admin must raise it.' (clear message). After the key limit was raised a new run starts and works (case lead thinking, steps streaming). Passed.
