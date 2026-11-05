# QA-319: Run fails after the economics are stored: the case lead's last LLM call returns an empty answer, the nested run 'stopped with error', and the project lead's stale read_case/case_changes trip the repeat guard ('internal error in geomind')

| Field | Value |
|---|---|
| Status | fixed |
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

- 2026-11-05 19:41 UTC: geomind 0.4.132 a04e761; pending deploy
## Retest

## The nested error (QA-E2E-economics-I, 2026-11-05 19:32 UTC, for the fixer)

Correction to "Actual": the case lead's step 13 did NOT end with an empty answer; it called
`finish` (19:20:13 UTC, call `call-7b0bbdb9-9fbb-44bd-ad30-5a51631eb371`, a full summary of the
economics). The nested run then ended with, from `GET /assistant/runs/6bb98a04-.../events`
(`../evidence/QA-319/events-6bb98a04.txt.gz`, event id 251):

    event: run.finished
    {"status": "failed", "stop_reason": "error", "message": "'str' object has no attribute 'get'",
     "agent": "case_lead", "parent": "6bb98a041d744207a96c89aa9058909e"}

No `error_class` or `where` (file:line) is in the events, the run log or `/agents` for this
nested failure (only the message). It is an AttributeError while finishing. Guess: the step-9
`set_case` stored `economics.about.sources` as a STRING ("All values are cost-catalogue rows
...", see QA-320), and code that runs at `finish` (a summary of sources / assumptions, or the
case-change record) calls `.get` on each source entry. The previous `set_case` succeeded, so the
string reached the stored case (v3).
Also: the nested failure event lacks error_class/where although QA-083 promised class, message,
file:line for internal errors.

- 2026-11-05 19:43 UTC, QA-E2E-economics-I (observation; status left to the fixer): the same
  request on geomind 0.4.131 (with fbefa51, without 81bb3ef) in project "QA-TEST
  QA-E2E-economics-I 14", run 2f10d82c-cb49-45c2-91b4-e6b92a34047d, now goes through ONE
  `ask_economics` (sources per key, no string sources), approve all, and ends `done` at 7 min 7 s,
  0.022 USD. I will retest the exact crash path when 81bb3ef is deployed and the bug is `fixed`.
