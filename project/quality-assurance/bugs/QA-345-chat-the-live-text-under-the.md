# QA-345: Chat: the live text under the busy list ('Now I'll brief the four module groups in one call.') does not say which agent wrote it; show the agent's name (e.g. 'Design lead: ...')

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | frontend,backend |
| Reporter | Sahand (screenshot) |
| Found | 2026-11-05 20:11 UTC |
| Versions | live 2026-11-05 21:10 Trondheim |
| Where | geomind.team chat, the streamed text line under the busy list during a run |
| Fixer | front-m2 |

## Steps

1. Run a design request; watch the text under the agent list.

## Expected

Every streamed text shows who says it: the agent's name (and instance, e.g. 'Design lead', 'Reservoir engineer I') as a small bold label before the text, in the same name style as the busy list; the final answer to the user stays unlabeled or labeled as the project lead.

## Actual

'Now I'll brief the four module groups in one call.' appears with no agent name; five agents are working (screenshot).

## Evidence

- ![screenshot](../evidence/QA-345/1.png)

## Cause

Sahand's request (top). text.delta events carry the agent and instance since IMP-025 (backend 1.1.94); the frontend should render it. If a text event lacks the agent, backend adds it.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
