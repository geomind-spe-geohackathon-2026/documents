# QA-326: Case lead loops on files-only set_case after approve all: 24 refused calls in 7 min, case lead fails 3 times (nested_stopped), the project lead sets the case and the economics itself without ask_economics (geomind 0.4.131)

| Field | Value |
|---|---|
| Status | verified |
| Severity | blocker |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 19:25 UTC |
| Versions | backend 1.1.120, geomind 0.4.131 (API container started 19:06:54 UTC; includes 35c3a0c "set_case split into steps", 19:05 UTC) |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 12 (7be82545-0553-4f6b-ad77-7fbeab8da266); chat 73567385-49b4-4ef4-8af7-91da2b3a3e8f; run 9c02d335-d9e5-48a8-a687-1c244aeeaee4 |
| Fixer | hotfix-python-lead-II |

## Steps

1. New project with the three competition files.
2. Chat: "Set up the case for our geothermal heating and cooling plant from the uploaded challenge
   brief and the two daily demand files." (the same request as runs 1, 3, 6, 9 of this thread)
3. Approve every card; approve all on the confirmation question (19:11:51 UTC).

## Expected

One full `set_case` after approve all (runs 3, 6, 9: stored after 2-3 calls), then the ONE
`ask_economics` question, then `finish`: about 5 min, ~0.03 USD.

## Actual

- 19:11:52-19:15:47 UTC: the case lead sends **19 times the same call**
  `set_case(files=[heating csv, cooling csv], columns={...: {date: time}})` with no `changes`;
  each is refused `case_incomplete` "files = [...] and nothing else; nothing is stored. Send ONE call
  with changes ...". Each LLM step writes 800-1500 output tokens and says "Sending the whole case
  in one call" / "The previous calls carried no `changes` — that is the error. Sending the whole case
  now", but the recorded call (and the assistant message in the next step's history) holds only
  `files` and `columns`. It finishes "Stopped short of a stored case: nothing is saved yet".
- The project lead sends the case lead twice more (19:16:16, 19:17:55): 3 + 3 more files-only calls,
  both end `nested_stopped` ("the same call failed ...").
- The project lead then reads the case schema itself (`read_case(section="schema")`, 12 `read_stored`
  of the JSON schema, up to 43 k characters each), sends one files-only call (refused), then a full
  `set_case` with `changes` (19:20:36, stored), the requirements (19:20:59), asks its own
  economics question (`ask_user`, not `ask_economics`: no catalogue rows, no sources per key),
  and sets the economics by hand in 3 more `set_case` (one refused for `currency` format, one for
  `changes.economics`).
- Run: 15 min 0 s, 3.63 M input tokens, 0.067 USD (run 3: ~5 min, 0.031 USD). 27 refused
  `set_case` in the run. Approval cards: 2 `set_case` + 1 question + 2 `set_case` more.
- The stored case is right (8 requirements, all reference values); the economics are set without the
  per-key sources `ask_economics` records.

## Evidence

- `../evidence/QA-326/run-9c02d335.json` (run log; case_lead 19:11:52-19:15:59, project_lead 19:17:50-19:23:30)
- `../evidence/QA-326/answers.json`

## Cause

Not found; facts and two guesses:
- The model's tool call reaches geomind without `changes` although the step's output is ~1000
  tokens (guess 1: the provider or geomind's argument parser drops an invalid or over-long `changes`
  value and keeps the valid arguments; guess 2: the output tokens are reasoning and the model really
  sends files only, steered by the new error text "The columns ... are kept for that call", which
  reads as if files and columns are a first step).
- New in this deploy: 35c3a0c "Code quality: set_case split into steps" (`remembered_call`,
  `normalized_changes`, `stored_case`) and the QA-200/QA-222 changes that keep `columns` from a
  refused call. Runs 3, 6, 9 on 0.4.100-0.4.114 did not loop (2-3 refusals, then stored).
- The repeat guard did not stop the identical call for 19 steps (QA-269/QA-301 changed it the same hour).

## Proposed fix

- geomind: log the raw tool-call arguments as the provider returned them (before parsing) when a
  call is refused twice the same way, to see whether `changes` was sent.
- geomind `tools/gemini/case.py`: after one files-only refusal, the second identical call is
  answered with the skeleton to fill (`changes` with every series named) and the third is refused by
  the repeat guard; the error text should not suggest that files and columns are a step of their own.
- geomind `agents/project/lead.py`: the project lead never sets economics by hand; it re-sends the
  case lead with the step that failed, or asks the user.

## Speed and accuracy

+10 min and +0.036 USD over a normal run; the economics have no catalogue sources.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 19:33 UTC: geomind main 0df5771, gemini dev e6284347 (0.6.31); pending deploy
## Retest

(Who, when, result.)
- 2026-11-05 19:41 UTC, QA-AI-case-I: reproduced in run e4e3e1f7-e5ef-4a0c-8df8-da7d3b8c4419 (project QA-TEST QA-AI-case-I 13, ; same request, geomind 0.4.131): after approve all (19:28:03) the case lead sends files-only `set_case` 3 times and stops (nested_stopped); the project lead re-sends it twice more (6 + 3 files-only calls); the project lead then stores the case itself after 2 more files-only calls and 3 refused full calls (19:38:39). 16 files-only calls in total. The run then fails on QA-331. Evidence: `../evidence/QA-326/run-e4e3e1f7.json`. 2 of 2 runs on 0.4.131.
- 2026-11-05 19:58 UTC (20:58 CET), QA-AI-case-I, run 72ca5d30-a541-4359-b8ac-cff8fad9769f (project QA-TEST QA-AI-case-I 16, fa74ee82-efc9-4908-9b52-bb4ecff1cb3b; geomind 0.4.132, celery started 19:47 UTC; 19:50:40-19:55:25 UTC; log `../evidence/QA-326/run-72ca5d30.json`): same request as runs 12-13. After approve all (19:53:2x) one files-only `set_case` refused, the next call has the whole `changes` and is stored (19:53:32); `ask_economics` once; case lead finishes; the project lead does not touch the case. 4 min 45 s, 0.028 USD (runs 12-13: 15 min, 0.067 USD). Verified.
- 2026-11-05 19:56 UTC: QA-AI-case-I run 72ca5d30, geomind 0.4.132
