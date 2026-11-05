# QA-292: New chat: ask the user once in a small dialog whether to turn Auto-approve on for this chat

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | frontend,backend |
| Reporter | Sahand (screenshot) |
| Found | 2026-11-05 18:41 UTC |
| Versions | live 2026-11-05 19:40 Trondheim |
| Where | geomind.team chat, the Auto-approve toggle in the chat header |
| Fixer | front-m1 |

## Steps

1. Open a new chat in a project.

## Expected

When a new chat opens, a small dialog asks once: turn Auto-approve on for this chat? (Yes / No, with one line on what it does: agents' write steps run without approval cards). The answer sets the existing Auto-approve toggle; the user can still change it later with the toggle. Not asked again for that chat.

Clarified by Sahand (2026-11-05 20:56 Trondheim): ask only when the chat page opens AND the user has
not turned Auto-approve on before. If the user already turned it on, never ask again. The choice is
saved in the backend (per user, persisted, e.g. a user setting `auto_approve_default` or the chat's
saved flag), so the frontend reads it on page load and does not ask; the dialog's answer is written
to the backend. Area now frontend + backend.

## Actual

Auto-approve is only a toggle in the header; nothing asks the user, so most users never see it and get every approval card.

## Evidence

- ![screenshot](../evidence/QA-292/1.png)

## Cause

Feature request from Sahand (top priority, his bug). Frontend only, using the existing Auto-approve setting.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

Fix: frontend 1.1.129 (commit af01430, bundle index-DjK0zKa6.js), by front-m1: a new draft chat shows a dialog 'Turn on auto-approve for this chat?' (No/Yes, Esc = No); the answer goes to the chat's auto-approve, saved on the first message.
- 2026-11-05 18:54 UTC: frontend 1.1.129
- 2026-11-05 19:57 UTC: Sahand 20:56: ask only if Auto-approve was never turned on; save the choice in the backend
## Retest

(Who, when, result.)

Frontend part (reopen): frontend 1.1.142 (commit addd0be, bundle index-BUkidFKs.js), by front-m1: asks only when the user never chose; choice read/written via GET/PUT /assistant/preferences; hidden until back-m2's route is live.
- 2026-11-05 20:41 UTC: Manual QA-IV 21:42 CET, backend 1.1.130: GET/PUT /assistant/preferences works; with auto_approve true a new chat starts with auto-approve on, with false a new chat starts off; preference set back to false
