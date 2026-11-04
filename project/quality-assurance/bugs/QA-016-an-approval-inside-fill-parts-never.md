# QA-016: An approval inside fill_parts never reaches the user, ignores auto-approve, loses the engineer's work and leaves the run waiting

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | Fatemeh (run), Claude (write-up) |
| Found | 2026-11-04 20:04 UTC |
| Versions | frontend 1.1.33; the run spans backend 1.1.14 to 1.1.16 (geomind 0.4.25/0.4.26), agents on deepseek-v4.1-flash |
| Where | https://geomind.team/projects/886404e4-3b22-41bd-8986-1a8bc869e25e/assistant/chat/33c76f29-064f-4047-9926-ff8937beddf7; project test hack; chat 33c76f29-064f-4047-9926-ff8937beddf7; run a61cfb19bfb04ae99e92060fc5bd2e40; steps[80] (fill_parts round 1), steps[88] onward |
| Fixer | hotfix-python |

## Steps

1. Run QA-009's chat with Auto-approve on (the chat's input shows it on).
2. The design lead calls fill_parts (steps[80]); the reservoir engineer works about 7 minutes (steps[81] to steps[87]) and calls patch_plant.

## Expected

With Auto-approve on, patch_plant runs without a question. Without it, the approval shows in the
chat, the run waits for it, and the engineer goes on from where it was.

## Actual

- patch_plant asks "Allow patch_plant (write)?" (request-1289) although Auto-approve is on.
- The request is not shown in the chat: the chat shows nothing to answer.
- fill_parts returns the request to the design lead as its tool output (steps[80] output:
  `{"reservoir_engineer": {"kind": "approval", "message": "Allow patch_plant (write)?", ...}}`),
  after 427 s. The design lead starts fill_parts again (steps[89] on): the reservoir engineer starts
  from nothing; its 7 minutes of work are lost.
- The run's row in Postgres stays `status = waiting` with that old request while the run goes on
  (read 2026-11-04 20:03 UTC: `{"kind": "approval", "agent": "reservoir_engineer", "request": "request-1289", ...}`).
  The backend treats a waiting run as having no process (an answer or a cancel queues a resume), so
  answering it could start a second process beside the running one (not tested; from the code).

## Evidence

- [`run-...-step101.json.gz`](../evidence/QA-016/run-a61cfb19bfb04ae99e92060fc5bd2e40-step101.json.gz) (run JSON at 101 steps; `steps[i]` is the 0-based index)

## Cause

Fact: backend `api/v1/assistant/runs/adapters/callbacks.py` RunRecorder sets the run to waiting on a
`request` event of any agent, nested ones too. Guess: fill_parts runs its engineers in a way that
neither applies the chat's auto-approve nor pauses the run on their requests; it hands the request
up as a result.

## Fix

hotfix-back (2026-11-04): the cause is in geomind, not the backend. `fill_parts` is a geomind
`Team` (`geomind/agents/design/lead.py:side_by_side`); a member's `request` comes back as the
Team's tool output instead of pausing the run. So the request never reaches the chat, the
browser's auto-approve (frontend `auto-approve.tsx`, which answers approval requests that reach
the chat) never sees it, and the engineer's work is dropped when the lead calls fill_parts again.
The backend's `RunRecorder` sets `waiting` on a request of any agent, which is right for Delegate
runs that do pause; once Team pauses the same way, the row is right too. A backend-only guess at
"the run went on after a request" could clear a real wait while side-by-side engineers still run,
so no backend change. Handed to hotfix-python.
- 2026-11-04 20:06 UTC: for hotfix-python: geomind Team (fill_parts) returns a member's request as output instead of pausing; the stale waiting row and the ignored auto-approve follow from that. See Fix section.
- 2026-11-04 20:25 UTC: fixed in geomind 0.4.30 (commit b6f61d6), backend 1.1.25 (da5e79a), waiting for deploy (hotfix-python's deploy refused again)
- 2026-11-04 20:31 UTC: shipped in backend 1.1.27 with geomind 0.4.32 (holds 0.4.30); prod worker has the beside rule. Live retest by the bug's steps still to do.
## Retest
