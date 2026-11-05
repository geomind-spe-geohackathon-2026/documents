# QA-292: New chat: ask the user once in a small dialog whether to turn Auto-approve on for this chat

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | frontend |
| Reporter | Sahand (screenshot) |
| Found | 2026-11-05 18:41 UTC |
| Versions | live 2026-11-05 19:40 Trondheim |
| Where | geomind.team chat, the Auto-approve toggle in the chat header |
| Fixer | hotfix-front-lead |

## Steps

1. Open a new chat in a project.

## Expected

When a new chat opens, a small dialog asks once: turn Auto-approve on for this chat? (Yes / No, with one line on what it does: agents' write steps run without approval cards). The answer sets the existing Auto-approve toggle; the user can still change it later with the toggle. Not asked again for that chat.

## Actual

Auto-approve is only a toggle in the header; nothing asks the user, so most users never see it and get every approval card.

## Evidence

- ![screenshot](../evidence/QA-292/1.png)

## Cause

Feature request from Sahand (top priority, his bug). Frontend only, using the existing Auto-approve setting.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
