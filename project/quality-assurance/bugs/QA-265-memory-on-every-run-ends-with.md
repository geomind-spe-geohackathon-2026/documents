# QA-265: Memory on: every run ends with 9 write_lesson approval cards; lessons are made for problems no team met (case lead never ran), and a denied lesson comes back under role 'all'

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 18:13 UTC |
| Versions | backend 1.1.107+ (geomind 0.4.98+, gemini 0.6.17) |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 3 (3ecb4493-3368-4bc2-b2f0-ca0b06670a86, memory on); chat 5db7a37c-b2ea-43d6-982f-5ebf2b8ad6a7; run 19dd2eff-2424-42f6-9758-ec275e3fa06e; requests request-319 to request-391 |
| Fixer | |

## Steps

1. New project with memory `on`; reference case, economics, demand and HackathonPlant loaded by API. First chat message "is the plant ok?" (tool loop, 2 min, fine).
2. Message: "Have the plant reviewed independently and explain the verdict. I read money in MEUR and want short answers."
3. Answer every card: deny 4 lessons with a reason, approve the rest.

## Expected

`prompts/project/lead.md`: "At the end, ask the support_lead once to keep the run's lessons: the problems each team met and how they were solved, and what the user said about how they work." A run with no problem keeps the two user facts (short answers, MEUR), at most one card, or none (a user fact the user just stated needs no approval).

## Actual

Review, design record and explanation took 3 min 32 s (18:03:07 to 18:06:32 UTC), fine. Then the memory stage:

- The project lead's brief to the support lead lists every team as if it met a problem: "case: the project's case ... was already accepted; no case step was needed" (the case lead never ran), "design: ... recorded it as design/v1", "reviewer: ... no failures", "explainer: produced the explanation".
- The support lead adds a "Fix/method:" line of its own to each (its prompt: "Never add a number, a value or a finding of your own").
- The curator turns each into a lesson; each `write_lesson` is a write and stops the run: 9 cards (request-319, 326, 333, 340, 348, 356, 376, 383, 391), 6 min of the user's time for a 3.5 min answer.
- Denied lessons: `case-lead-check-case-accepted-first` (role case_lead, "the case lead did not run") comes back as `all-check-case-accepted-before-case-step` (role `all`, source `support_lead`, same text, request-376). `design-lead-reuse-existing-plant-result` ("do not re-simulate" with no condition: wrong after a case change, see QA-227) was rewritten well after the reason. `reviewer-note-thin-margins-when-passing` (widens the reviewer's job, the cause of QA-187) came back for `analysis_lead` with the reviewer's words "route nothing to a team" (request-391).

## Evidence

- `../evidence/QA-265/19dd2eff-2424-42f6-9758-ec275e3fa06e.log.json`, `../evidence/QA-265/19dd2eff-2424-42f6-9758-ec275e3fa06e.trace.txt`: project_lead step 5 (brief), support_lead steps 1-2, curator steps 1-5 with each `write_lesson` input and its denial reason.
- Run totals: 33 LLM calls, 593 305 input tokens, 0.0145 USD; support_lead 12 s and curator 25 s of LLM time.

## Cause

- `prompts/project/lead.md` memory rule names "the problems each team met" but the lead lists every team that ran or was skipped; no rule says "only a problem that was met and solved; none -> only the user facts".
- `prompts/support/lead.md` lets the lead "give each request to the member" with no check that a lesson has a problem behind it; the support lead writes fixes itself.
- `write_lesson` is effect `write`, so each lesson is one card; the denial guard keys on the call, so the same text under another `id`/`role` is asked again.

## Proposed fix

- geomind `prompts/project/lead.md` (memory block): "Send the support_lead only the problems a team met and how it solved them (a refused call, a failed check, a repeat, a user correction), and the user's words on how they work. A run with none sends only the user's words."
- `prompts/support/lead.md` and `curator.md`: "No lesson without a problem in the material; a denied lesson is dropped, never re-sent under another id or role."
- `tools/memory.py` `write_lesson`: one call with a list of lessons (one card for the run), or the user facts the user stated in this chat written without approval; refuse a lesson whose text equals one denied in this run.

## Fix

## Retest
