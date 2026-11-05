# QA-319: Run fails after the economics are stored: the case lead's last LLM call returns an empty answer, the nested run 'stopped with error', and the project lead's stale read_case/case_changes trip the repeat guard ('internal error in geomind')

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 19:20 UTC |
| Versions | backend 1.1.118 (geomind 0.4.130) |
| Where | project "QA-TEST QA-E2E-economics-I 11"; chat 20335356-7c60-41f8-8951-05bfa0c86d31; run 6bb98a04-1d74-4207-a96c-89aa9058909e |
| Fixer | hotfix-python-lead-II |

## Steps

1. Reference case, no economics. Chat (19:13:08 UTC): "Fill in the economics yourself with your
   own best guesses, including the per-MWh operating costs and a subsidy; I don't want to be
   asked."
2. Approve the case lead's `set_case` (19:20 UTC).

## Expected

The run ends with a summary of what was set.

## Actual

- The `set_case` runs (case v3, `economics.json` stored); the case lead reads it back (step 10),
  writes 12 assumptions with `update_state` (step 11), reads the case (step 12), then its step-13
  LLM call returns `answer: ""` with no tool call (1851 output tokens, 12.9 s).
- The project lead gets `case_lead: the nested run stopped with error; the detail is in the log`
  (step 3). Because the nested call is an error, it is not in `succeeded`, so its later
  `read_case {"section":"economics"}` (steps 4-7) is answered from step 2: "the case does not set
  'economics' yet", and `case_changes` from step 4: `[]`. Run failed 19:20:41 UTC with
  `read_case: the same call as an earlier successful one was sent in 3 steps in a row`; the chat
  says "The assistant stopped with an internal error in geomind".
- The economics are stored, so the user sees an error for work that was done.
- 7 min 33 s, 745k tokens, 0.023 USD.

## Evidence

- Run JSON: `../evidence/QA-319/run-6bb98a04.json.gz` (case lead steps 9-13; project lead 3-7)
- Chat: `../evidence/QA-319/chat.txt`

## Cause

Facts above. Two defects: (1) an empty final answer of a nested lead is an error instead of a
retry or a "finish with summary"; (2) the repeat guard (QA-181 family): a nested run that FAILED
after a write still changed the case, but the project lead's reads are served from before it.

## Proposed fix

geomind engine:
1. A nested run whose last LLM answer is empty gets one retry with "give your final answer" (or
   returns its last state summary), not an error.
2. `same_result`: treat a failed nested run (and any call after which the case version changed)
   as a possible write; simplest: key the repeat guard on the case/plant version, so any version
   change since the earlier call makes the call run again.

## Fix

## Retest
