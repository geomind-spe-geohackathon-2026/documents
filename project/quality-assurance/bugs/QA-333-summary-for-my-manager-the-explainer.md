# QA-333: Summary for my manager: the explainer is run three times (two identical briefs before the case reload is acted on), then a full re-simulate and review; 6 min 42 s for a 5-bullet summary

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 19:46 UTC |
| Versions | backend 1.1.123 |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 1 (35a70dbe-5e24-4f51-9c6f-50e06d47fe82); chat 134dae07-2e37-4a3a-ae0b-83b5e812017e (the long chat); run b848fa44-5833-4b39-bfee-19633798a880 |
| Fixer | hotfix-python-lead-II |

## Steps

1. The long chat of project 1; the project case was meanwhile saved by hand in another chat (170 mD, version 7), so the chat's case is older.
2. Message: "Summarize this whole chat in 5 bullet points for my manager."

## Expected

The newer project case is loaded by rule (it was, step 1, no card: good). Then either one summary that says the case changed since the chat's results, or, if the lead decides to re-check first, re-check once and then one summary. One explainer call.

## Actual

- 19:38:56 `set_case(source: project)` by rule; the coordinator task names the change.
- 19:38:56 project_lead step 2 -> `explainer` (45 s) -> a 5-bullet summary.
- 19:40:01 step 3 `read_case(site)`; 19:40:11 step 4 -> `explainer` again with the same brief (51 s).
- 19:41:18 step 5 `finish` is not the end: step 6 sends the design lead to re-simulate on 170 mD (108 s, 15 calls, 12 `read_result` after the check), step 7 the reviewer (66 s), step 8 the explainer a third time (20 s), step 9 finish at 19:45:37.
- 6 min 42 s for the summary; the explainer ran 3 times, the first two summaries thrown away.

## Evidence

- `../evidence/QA-333/b848fa44-5833-4b39-bfee-19633798a880.trace.txt` (every step with time and tool).

## Cause

Guess: the project lead plans the summary before it notices that the loaded case makes the chat's results stale; after the second summary it decides to re-check. The rule-loaded case change is in the coordinator task, but the lead's prompt has no rule "a newer project case first: re-check, then answer".

## Proposed fix

`prompts/project/lead.md`: "When the run starts with a newer project case loaded (the task says so), decide first: re-check the design on it (design lead, reviewer) or answer from the old results saying they are for the older case; then call the explainer once." Optional guard: an `explainer` call with the same brief as an earlier one in the run returns the earlier answer.

## Fix

- 2026-11-05 19:48 UTC: geomind main: one re-check after a case change (Verified guard kept), one explainer
## Retest
