# QA-291: Chat busy list: show tokens and cost per agent line, between steps and time (e.g. '2 steps · 12.4k tokens · 0.004 USD · 44 s')

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | frontend,backend |
| Reporter | Sahand (screenshot) |
| Found | 2026-11-05 18:38 UTC |
| Versions | live 2026-11-05 19:37 Trondheim |
| Where | geomind.team chat, busy list (one line per agent while a run is live) |
| Fixer | hotfix-front-lead |

## Steps

1. Start any agent run in chat.
2. Look at the busy list under the chat.

## Expected

Each agent line shows, in this order: steps, tokens (input+output, e.g. '12.4k tokens'), cost (e.g. '0.004 USD'), then time: 'Case lead · Asking the geoscientists · 3 steps · 12.4k tokens · 0.004 USD · 37 s'. The totals line ('Steps so far') shows the same for the whole run. Values update live.

## Actual

Only steps and time: 'Case lead · Asking the geoscientists · 3 steps · 37 s'.

## Evidence

- ![screenshot](../evidence/QA-291/1.png)

## Cause

Feature request from Sahand (top priority, his bug). Per-agent usage exists per instance in the run (Runs and logs shows per-agent tokens and cost; QA-144). Backend: stream usage per agent instance with step events (or a usage event) so the busy list can show it live; frontend: render tokens and cost between steps and time.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

Fix: frontend 1.1.128 (commit 19006f6, bundle index-bxsE_Wl4.js), by front-m1: AgentNode has tokens and cost summed from each step.finished usage per actor; busy line `Name · doing · N steps · tokens · cost · time`; totals line the same (time only while running). No backend field needed.
- 2026-11-05 18:46 UTC: frontend 1.1.128
## Retest

(Who, when, result.)
