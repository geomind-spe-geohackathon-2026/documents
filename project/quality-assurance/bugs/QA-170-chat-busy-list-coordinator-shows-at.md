# QA-170: Chat busy list: Coordinator shows at the bottom as 'Thinking, 0 steps' and its timer runs, although it finished routing at the start (1 step)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend,backend |
| Reporter | Sahand (screenshot), Manual QA-IV |
| Found | 2026-11-05 17:10 UTC |
| Versions | backend 1.1.104 (geomind 0.4.98, gemini 0.6.17), frontend live 2026-11-05 17:10 UTC |
| Where | https://geomind.team/projects/fcc641c0-0119-4182-9a72-adce5a17b3ed chat e53fccc1; run d4ab496f-4a1f-43fa-b760-0f550fda0714 (the hackathon report run) |
| Fixer | hotfix-front-VII |

## Steps

1. Send a design request in the chat; the coordinator routes it to the project lead, which asks the design lead and the team.
2. Look at the busy list under the chat while the run works.

## Expected

The Coordinator first (it is the first agent of the run), shown as done (1 step, about 2 s), with no running timer.

## Actual

The Coordinator is the last line: "Coordinator · Thinking · 0 steps · 1 min 25 s", with a running spinner, under the project lead, design lead and the engineers.
The API says otherwise: `GET /assistant/runs/{id}/agents` gives the coordinator session `...-route` with `status: finished`, `steps: 1`, `llm_calls: 1`.

## Evidence

- ![screenshot](../evidence/QA-170/1.png)

## Cause

Guess: the route session's events do not reach the busy list (or its finish event is missed). The list then treats it as a new
agent with no steps, still thinking, and adds it last. The run was resumed once after a celery restart (backend 1.1.104 deploy
at about 17:00 UTC); the replayed events may lack the route session. Places to look: `frontend/src/domains/assistant/chat/blocks.tsx`
(toLatest / toDoing give "Thinking" when no tool runs) and `busy.tsx`, and what the backend streams for the `-route` session on resume.
Note: the coordinator's `parent_session` is the project lead's session (the run id), so a tree built from parents puts it under the project lead.

## Fix

frontend 1.1.115 (commit e21ad67, bundle index-CEvw1roy.js). Cause (fact): the run's events are right (the coordinator's route session ends with run.finished, seq 8). The phantom line came from a later run-level event with agent "": `touchAgent` (`chat/view.ts`) made a node for it, never marked done, and `toAgentName("")` names it "Coordinator" (QA-146). Now an event with no agent makes no node. No backend change.
- 2026-11-05 17:18 UTC: frontend 1.1.115, commit e21ad67
## Retest

Not run (no tests now). Retest: during a design run the busy list has no "Coordinator · 0 steps" line.
