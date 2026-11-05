# QA-061: Question card shows an internal note: 'Already answered in this run, not asked again: ... (request-530)'

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | qa-ux |
| Found | 2026-11-05 00:05 UTC |
| Versions | frontend 1.1.5x, backend 1.1.55 (health 00:04 UTC), geomind 0.4.54 |
| Where | https://geomind.team/projects/4cfeab2d-73e3-4299-a1f8-afec3d7e4bae/assistant/chat/159de1e5-d65d-4031-946d-86046aefcaaa; project QA2 qa-ux flow; second ask_user card of the first run |
| Fixer | hotfix-python |

## Steps

1. In a new chat, send the PDF and CSVs and ask for the case; approve the cards.
2. Answer the first long question with "I don't know these ... propose them with sources".
3. Read the text of the next 'The assistant asks' card to its end.

## Expected

The card holds only what the user must decide.

## Actual

After 'Approve all, change some, or stop?' the card text ends with: `Already answered in this run, not asked again: site.air.relative_humidity (request-530): "I don't know these; ...".` That is a note meant for the agent (a request id, a repeat guard), shown to the user and quoting their own answer back. (Found in the page text of the card; I did not scroll to it on screen.)
Also seen: this agent asked for 15 values as "engineering assumption, no source" although I asked for sourced values; for qa-func-1 to judge.

## Evidence

- ![screenshot](../evidence/QA-061/1.png)
- Run JSON: `../evidence/QA-061/run-<id>.json`

## Cause

Guess: the ask_user tool appends the 'already answered' guard text to the question and the frontend prints the whole question.

## Fix

Cause: `geomind/engine/questions.py::asking_new` appended the repeat guard's note (`Already answered in this run, not asked again: <paths> (request-id): '<answer>'`) to the question's message, which is the text the card shows. Fix: the message stays as the agent wrote it; only a question that is nothing but a list of paths gets one plain line, `You answered <paths> earlier in this chat; answer only <paths>.` No request id, no quote. geomind 0.4.60 (commit c9fdb22), backend 1.1.61 (3d2aa31), deployed 2026-11-05 00:22 UTC by hotfix-python-II. The second remark (15 'engineering assumption, no source' values) is QA-010 behaviour, left for qa-func-1 to judge.
- 2026-11-05 00:23 UTC: geomind 0.4.60 (c9fdb22, no internal already-answered note in the question; only-path questions get one plain line), backend 1.1.61 (3d2aa31), deployed
## Retest

functional-qa-I, 2026-11-05 ~00:55 UTC, backend 1.1.62: four question cards in project 61134432 (case list, assumptions, two economics cards) showed no 'Already answered in this run ... request-N' note. Passed.
