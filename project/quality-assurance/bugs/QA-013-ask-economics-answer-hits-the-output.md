# QA-013: The case lead's ask_economics call hits the 16,000-token output limit and is cut

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | Fatemeh (run), Claude (write-up) |
| Found | 2026-11-04 ~20:40 UTC (run started 18:51 UTC, still running) |
| Versions | frontend 1.1.33; backend as at 18:51 UTC (1.1.14, geomind 0.4.25, per QA-007) |
| Where | https://geomind.team/projects/886404e4-3b22-41bd-8986-1a8bc869e25e/assistant/chat/33c76f29-064f-4047-9926-ff8937beddf7; run a61cfb19bfb04ae99e92060fc5bd2e40; steps[21], steps[22], steps[34], steps[37] |
| Fixer | |

## Steps

1. As QA-009. The case lead writes the economics question.

## Expected

The economics question is a short call.

## Actual

The case lead writes every economics key (about 55) with its row, `others` and a long note by
hand. steps[22]: 122 s and 13,244 output tokens, cut at the limit ("Your last answer stopped at the
output limit of one call (16000 tokens) and was cut, so nothing of it ran"). The other economics
calls are long too: steps[21] 87 s / 8,623 tokens, steps[34] 209 s / 8,241, steps[37] 149 s /
10,394.

## Evidence

- Run JSON: [`../evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz`](../evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz)
  (gzip; one run for QA-007 and QA-009 to QA-014). `steps[i]` below is the 0-based index in its
  `steps` list.
- The `llm_calls` of the steps above.

## Cause

The tool makes the agent list every key; the catalogue already marks a recommended row per key.
See IMPROVEMENTS.md, IMP-001.

## Fix

## Retest
