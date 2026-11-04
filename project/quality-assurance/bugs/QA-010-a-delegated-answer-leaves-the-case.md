# QA-010: The user delegates the open values to the agent; the agent sets nothing and proposes nothing

| Field | Value |
|---|---|
| Status | blocked |
| Severity | major |
| Area | geomind |
| Reporter | Fatemeh (run), Claude (write-up) |
| Found | 2026-11-04 ~20:40 UTC (run started 18:51 UTC, still running) |
| Versions | frontend 1.1.33; backend as at 18:51 UTC (1.1.14, geomind 0.4.25, per QA-007) |
| Where | https://geomind.team/projects/886404e4-3b22-41bd-8986-1a8bc869e25e/assistant/chat/33c76f29-064f-4047-9926-ff8937beddf7; run a61cfb19bfb04ae99e92060fc5bd2e40; steps[19], steps[35], steps[48], steps[57] |
| Fixer | hotfix-python |

## Steps

1. As QA-009.
2. To the case lead's question the user answers "Use reasonable, documented engineering assumptions for all unspecified values".

## Expected

The agent finds candidate values with a source (knowledge base, a connector such as a weather
source, or a cited standard design value), puts them to the user to approve (approve all / change
some), and sets them. If no source exists, the run ends with one clear message saying which
values the user must type and in what unit, and the design waits.

## Actual

The case lead sets nothing and proposes nothing (finish at steps[57]: "a delegation to reasonable
assumptions cannot be turned into case values without inventing them"). The case stays incomplete:
site.air.temperature, relative_humidity, pressure, demand.heating.return_temperature,
demand.cooling.return_temperature, utilities.electricity.import_limit. After about 26 minutes the
design has not started.

## Evidence

- Run JSON: [`../evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz`](../evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz)
  (gzip; one run for QA-007 and QA-009 to QA-014). `steps[i]` below is the 0-based index in its
  `steps` list.
- steps[57] finish answer; the search_rag calls listed above.

## Cause

The no-default-values rule (a value no file gives comes from RAG or MCP and the user approves it
with its source) is right, but the agent has no path for a delegating answer. Its RAG searches for
these values (steps[30], [49], [51], [54], [55]) find nothing, and it does not offer what it found.
Needs Sahand's decision: what the agent does when the user delegates and no source exists.

## Fix

- 2026-11-04 20:08 UTC: needs Sahand's decision (as STATUS.md says): what the agent does when the user delegates open values and no RAG/MCP source exists; the no-default-values rule forbids inventing them. hotfix-python did not change it.
## Retest
