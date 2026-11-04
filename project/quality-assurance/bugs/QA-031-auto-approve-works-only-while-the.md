# QA-031: Auto-approve works only while the chat tab is open; with the tab closed the run waits for an approval

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | frontend |
| Reporter | qa-5 |
| Found | 2026-11-04 20:25 UTC |
| Versions | frontend 1.1.33 (deployed), backend 1.1.22 (geomind 0.4.29) |
| Where | https://geomind.team/projects/4d8fb808-9af1-493e-94e4-4d6d50916e5f/assistant/chat/f0388b3b-8f3a-4f97-8167-c7939e9bca9d; project QA qa-5 outputs report e2e; run 9a33db47-648f-435a-a3e1-a6ad0665b16b; case lead's set_case approval (request-179) |
| Fixer | |

## Steps

1. In a project chat, turn on Auto-approve (the button says "Auto-approve is on: tool calls run without asking").
2. Send a long request (case, economics, design, simulation, report), 20:21 UTC.
3. Close the tab (or open the chat in another browser) while the run goes on.

## Expected

With Auto-approve on, the run's tool calls run without asking, whether or not the tab stays open;
a long pipeline run can be left alone.

## Actual

- At 20:24:56 UTC the run went to `waiting` with request `{"kind": "approval", "agent": "case_lead",
  "message": "Allow set_case (write)?"}` and stayed there until a tab with Auto-approve on was opened again.
- Opened in another browser (fresh profile), the chat shows Auto-approve off and the approval card.

## Evidence

- ![screenshot](../evidence/QA-031/1.png)

## Cause

Fact (frontend source, `src/domains/assistant/chat/auto-approve.tsx`): Auto-approve is a browser
setting in localStorage per project; `useApproveByItself` sends the approval from the open tab. The
backend does not know about it, so with no tab open nobody approves. The button's title promises more
than it does. A fix: send the setting with the message (or store it on the chat) and let the
backend approve, or at least say "while this tab is open" on the button.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
