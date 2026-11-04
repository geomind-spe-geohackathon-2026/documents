# QA-025: Chat shows 'internal error in geomind' for a run interrupted by an app restart; the run says send your message again

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | frontend |
| Reporter | qa-1 |
| Found | 2026-11-04 20:18 UTC |
| Versions | frontend bundle assets/index-DnxCbfcj.js, backend 1.1.19 at the run (1.1.21 after the restart) |
| Where | https://geomind.team/projects/541aa78f-8181-45f4-ac36-e47305e33f37/assistant/chat/062b25d8-1e4a-4b38-aed3-2209baba430a; project "QA qa-1 S1 end to end"; run 851e9794-7b7b-4e7c-b315-abec4a6d50f8; before the first step |
| Fixer | |

## Steps

1. In a new project, attach the challenge PDF and the two demand CSVs and send a design request (20:14:48 UTC).
2. The backend restarts during the run (the coordinator's announced restart to 1.1.21, about 20:16 UTC).
3. Look at the chat.

## Expected

The chat says what the run says: the app was updated or restarted, send your message again.

## Actual

The chat shows in red: "The assistant stopped with an internal error in geomind". The run itself
(`GET /assistant/runs/851e9794...`) holds `error.code = "interrupted"`, message "The run stopped
because the app was updated or restarted; send your message again." A user reads the chat line
as a geomind bug and does not know that sending the message again is the way on.

## Evidence

- ![screenshot](../evidence/QA-025/1.png)
- Run JSON: [run-851e9794.json](../evidence/QA-025/run-851e9794.json)

## Cause

Fact: `frontend/src/domains/assistant/chat/blocks.tsx` maps a stop with reason `error` to the
fixed text `internalFailure` and drops the message. Guess: the interrupted run reaches the chat
with reason `error`, so the run's own message is never shown; show the message (or map code
`interrupted` to it).

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
