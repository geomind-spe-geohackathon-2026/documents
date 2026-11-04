# QA-056: Chat shows an already answered question while the run waits on a design_lead approval; no approval card, auto-approve cannot fire, the run is stuck

| Field | Value |
|---|---|
| Status | open |
| Severity | blocker |
| Area | frontend |
| Reporter | qa-5 |
| Found | 2026-11-04 22:35 UTC |
| Versions | frontend bundle index-DnxCbfcj.js, backend 1.1.45 (geomind 0.4.46) |
| Where | https://geomind.team/projects/4d8fb808-9af1-493e-94e4-4d6d50916e5f/assistant/chat/f0388b3b-8f3a-4f97-8167-c7939e9bca9d; project QA qa-5 outputs report e2e; run 6c5b17e1-6ce7-4025-af28-fbb763938aaf; pending request-3455 (design_lead patch_plant) |
| Fixer | |

## Steps

1. Long pipeline run with Auto-approve on (tab open). At 22:32 UTC the case lead asks a question
   (merge min_stable_flow and max_production_flow into one production_flow_range requirement).
2. Click the chip "Approve: merge the two ..." (22:33 UTC).
3. The run goes on; the design lead calls patch_plant (write) and the run waits for its approval.
4. Reload the chat.

## Expected

The answered question closes; the chat shows the new approval card (or Auto-approve answers it).

## Actual

- `GET /assistant/runs/6c5b17e1...`: status `waiting`, request `{"kind": "approval", "agent": "design_lead",
  "message": "Allow patch_plant (write)? ...", "request": "request-3455"}`.
- The chat (also after a reload, 20 s wait) shows the answered case-lead question with its chips, 0 approval
  cards. Clicking a chip again: `POST /answer` returns 422 `{"request": "This is not the pending request"}`,
  shown as "Request validation failed".
- Auto-approve is on in the tab but cannot answer what the chat does not show: the run stays waiting.

## Evidence

- ![screenshot](../evidence/QA-056/1.png)
- Run JSON: [`../evidence/QA-056/run-6c5b17e1.json`](../evidence/QA-056/run-6c5b17e1.json)

## Cause

Guess: the chat takes the pending request from the run's events and the nested design_lead approval
event after the answered question is not one it reads (compare QA-016, fixed for fill_parts), so the
last question stays as the pending one. Workaround: answer request-3455 through the API.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
