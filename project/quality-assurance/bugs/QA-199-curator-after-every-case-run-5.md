# QA-199: Curator after every case run: 5-9 lessons and user facts, each its own approval card; several are wrong or over-general and go into shared memory

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-case-I |
| Found | 2026-11-05 17:21 UTC |
| Versions | frontend 1.1.113, backend 1.1.102-1.1.104 (geomind 0.4.97-0.4.99) |
| Where | geomind.team; projects QA-TEST QA-E2E-case-I 1/2/3 (shared memory On); runs cf319cd4, a5118d9e, 6a2d6017; agent support_lead -> curator |
| Fixer | hotfix-python-lead |

## Steps

1. Run a case to the end (PDF + 2 CSVs, one request, answer the questions).
2. After the case lead's summary, the support lead starts the curator ("I'll start by reading what the memory already holds").

## Expected

At most a few lessons, each true to the handbook and to what happened, proposed in ONE approval card
(or written without a card, as memory is the app's own store). A user fact only after a pattern, not
after one answer.

## Actual

Speed: run 1: 9 `write_lesson` calls = 9 approval cards, 16:59:20-17:02:01 UTC (2 min 40 s of the
12 min 25 s run, 62 s support_lead + 33 s curator LLM time, 175 k input tokens); run 2: 8 cards
(17:16:50-17:19:20, 2 min 30 s, 84 s curator LLM); run 3: 2 cards. A user must click Approve 8-9 times
after every case.

Accuracy: lessons that are wrong or over-general, now in the shared memory every project reads:
- run 2 `case-lead-one-confirmation-question` (1st version): "**Set the case from the project files and the
  knowledge base's assumptions document first**, then gather every value those do not give into one
  confirmation question". This is the QA-153 defect written as a rule (Knowledge values stored before the
  user confirms them). The same id was rewritten 2 min later with a different text.
- run 3 `case-lead-dated-series-time-zone`: "name the missing time zone as open instead of assuming one".
  Against handbook-case (a zone no file states is an assumption to confirm) and QA-158; it makes every
  later set_case fail (no time_zone -> refused, QA-200). I pressed Deny with a reason on this card; the chat
  shows no denial and the log shows the lesson `written` (my click did not register, or the deny was lost:
  not clear). It must be removed from the memory.
- user facts from a single test answer: run 3 `user-fact-stops-instead-of-approving` ("The user answers
  stop rather than approving values ..."), run 1 `user-fact-prefers-unsourced-value-open`, run 2
  `user-fact-leaves-unsourced-value-open` although in the same run the user asked the agent to use
  its own assumption for the humidity (and approved 0.8).

## Evidence

- `../evidence/QA-199/run-cf319cd4-log.json.gz`, `run-a5118d9e-log.json.gz`: curator steps, `write_lesson` inputs.
- Run 3 log: `../evidence/QA-197/run-6a2d6017-log.json.gz` (curator 2).
- `../evidence/QA-199/lessons-seen.txt`: the cards as I saw them (times UTC; repeated ids there are stale card text, the log has one call each).

## Cause

Guess: the curator prompt asks for a lesson for each thing that went well or badly and for user facts
from the run; nothing checks a lesson against the handbook or against a later answer; each
`write_lesson` is a write tool, so each needs its own approval.

## Proposed fix

geomind `agents/support/curator.py` (prompt) and the memory tools: (1) one `write_lessons` call with a
list -> one approval card (or no card: auto-approve memory writes, they are reversible); (2) at most 3
lessons per run, only for a refused call that was then fixed, each citing the handbook section it agrees
with; never a lesson that contradicts a handbook or describes a defect as a rule; (3) no user fact from
one answer (needs >= 2 runs); (4) after a Deny with reason, never write that lesson. Data: delete
`case-lead-dated-series-time-zone`, `user-fact-stops-instead-of-approving`, `user-fact-prefers-unsourced-value-open`,
`user-fact-leaves-unsourced-value-open` from the shared memory, and check `case-lead-one-confirmation-question`.

## Fix

- 2026-11-05 18:30 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
## Retest
