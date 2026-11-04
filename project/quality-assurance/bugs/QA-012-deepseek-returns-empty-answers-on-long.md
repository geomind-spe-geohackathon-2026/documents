# QA-012: DeepSeek returns an empty answer on long contexts; the call is lost

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | Fatemeh (run), Claude (write-up) |
| Found | 2026-11-04 ~20:40 UTC (run started 18:51 UTC, still running) |
| Versions | frontend 1.1.33; backend as at 18:51 UTC (1.1.14, geomind 0.4.25, per QA-007) |
| Where | https://geomind.team/projects/886404e4-3b22-41bd-8986-1a8bc869e25e/assistant/chat/33c76f29-064f-4047-9926-ff8937beddf7; run a61cfb19bfb04ae99e92060fc5bd2e40; steps[16], steps[17], steps[56] |
| Fixer | |

## Steps

1. As QA-009. The case lead's context grows past about 70,000 input tokens.

## Expected

Every LLM call returns a tool call or a finish.

## Actual

Three calls return an empty `answer` and no tool call: steps[16] (78,423 input tokens),
steps[17] (78,469), steps[56] (73,912, 1 output token). Each is a lost call (and a lost step of the
run's step budget).

## Evidence

- Run JSON: [`../evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz`](../evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz)
  (gzip; one run for QA-007 and QA-009 to QA-014). `steps[i]` below is the 0-based index in its
  `steps` list.
- The `llm_calls` of the three steps.

## Cause

Guess: the provider or model fails on long contexts. The context is large because the case lead
holds the full PDF, both 365-row CSVs and many catalogue rows (see IMPROVEMENTS.md, IMP-005).

Correction (2026-11-04, from the run JSON at 101 steps): after each of these three calls the loop's
next message is "Your last answer stopped at the output limit of one call (16000 tokens) and was cut,
so nothing of it ran", but the recorded output tokens are 337, 185 and 1. So either the call really
was cut (and the recorded token count is wrong), or the loop reads an empty answer as a cut one and
gives the agent a wrong instruction. Same family as QA-013.

## Fix

## Retest
