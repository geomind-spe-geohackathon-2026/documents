# QA-011: An OpenRouter 504 stops the whole nested case-lead run; nothing retries

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | Fatemeh (run), Claude (write-up) |
| Found | 2026-11-04 ~20:40 UTC (run started 18:51 UTC, still running) |
| Versions | frontend 1.1.33; backend as at 18:51 UTC (1.1.14, geomind 0.4.25, per QA-007) |
| Where | https://geomind.team/projects/886404e4-3b22-41bd-8986-1a8bc869e25e/assistant/chat/33c76f29-064f-4047-9926-ff8937beddf7; run a61cfb19bfb04ae99e92060fc5bd2e40; steps[2] (case_lead tool call), after steps[23] |
| Fixer | hotfix-python |

## Steps

1. As QA-009.
2. The first case lead run reaches its 17th LLM call (after the ask_economics refusal at steps[23]).

## Expected

A transient provider error (5xx, idle timeout) is retried with a back-off; the nested run goes on
from where it was.

## Actual

The case_lead tool returns `nested_stopped`: "case_lead: the nested run stopped with error:
OpenRouter: status = 504; Upstream idle timeout exceeded". The project lead starts a new case lead
(steps[26]), which reads all three files again and redoes the case work: about 10 minutes of the
run lost. The set_case already done survived; the economics work did not.

## Evidence

- Run JSON: [`../evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz`](../evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz)
  (gzip; one run for QA-007 and QA-009 to QA-014). `steps[i]` below is the 0-based index in its
  `steps` list.
- steps[2] tool_calls[1] output.

## Cause

Guess: the LLM call is not streamed, so a long generation (the case lead's earlier calls wrote
8,000 to 13,000 tokens) sends no bytes until the end and the upstream idle timeout fires; and the
loop has no retry for 5xx.

## Fix

hotfix-back (2026-11-04): not fixable in the backend. The backend only builds
`gd.providers.OpenRouter`; geomind's engine wraps it in `RetryLLM`, which already retries a 5xx
(prod `.env`: GEOMIND_RETRY_COUNT=5, GEOMIND_RETRY_DELAY=2, so about 62 s of back-off). The message
"status = 504; Upstream idle timeout exceeded" without a body is `_raise_api_error`: the error came
as a chunk inside the stream. The run has 8 `retry` events, so the 504 was most likely retried and
failed every time (the long generation that ran past the upstream idle timeout is repeated on each
try). What remains is geomind's: resume the nested run after a provider failure instead of
`nested_stopped`, and/or a longer back-off for 504. The run was on DeepSeek; production is on
nemotron since 19:56 UTC, so this may not occur the same way. Handed to hotfix-python.
- 2026-11-04 20:04 UTC: for hotfix-python: retry and nested-run recovery are in geomind (RetryLLM, Delegate); the backend only builds the provider. See Fix section.
- 2026-11-04 20:04 UTC: area moved to geomind for hotfix-python
- 2026-11-04 20:09 UTC: paused by coordinator: only analysed so far, no code changed. Seen: a 504 inside the stream is raised as retryable ProviderError, so RetryLLM retries it; open question is resuming the nested run instead of nested_stopped.
- 2026-11-04 20:26 UTC: hotfix-python: no hotfix. A stream 504 is already a retryable ProviderError and RetryLLM retries it (prod GEOMIND_RETRY_COUNT=5, DELAY=2). What is missing is resuming a nested run from its log after a provider failure, instead of nested_stopped and a fresh case lead: an engine change (Delegate/run_child/recover) that needs development mode with tests. A person can decide: a development-mode task for it, and/or a longer retry back-off in the prod .env (not editable by sessions).
- 2026-11-04 23:31 UTC: built in hotfix mode (Sahand 2026-11-05): geomind 0.4.53 (commit after d1e4d7b): the delegate reruns a nested run once after a provider failure (5xx, timeout), with a note to go on from the problem state; deploy with QA-013
## Retest
