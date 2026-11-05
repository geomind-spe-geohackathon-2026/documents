# QA-344: Sidebar chat dot: green and pulsing while the chat has a running run (grey when idle)

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | frontend |
| Reporter | Sahand (screenshot) |
| Found | 2026-11-05 20:09 UTC |
| Versions | live 2026-11-05 21:09 Trondheim |
| Where | geomind.team sidebar, Chats list, the dot before a chat's name |
| Fixer | |

## Steps

1. Start a run in a chat and look at the sidebar.

## Expected

While the chat has a running (or waiting) run, its dot is green and pulses (blinking animation); grey and still when nothing runs. Respect prefers-reduced-motion.

## Actual

The dot is grey and still while the chat is working (screenshot).

## Evidence

- ![screenshot](../evidence/QA-344/1.png)

## Cause

Sahand's request (top).

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
