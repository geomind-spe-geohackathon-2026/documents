# QA-089: Runs and logs: the step list is one long flat column and the right pane starts empty

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | frontend |
| Reporter | Sahand |
| Found | 2026-11-05 09:18 UTC |
| Versions | frontend <x.y.z>, backend <x.y.z> (geomind <x.y.z>) |
| Where | <URL>; project <name/id>; chat <id>; run <id>; step <n> |
| Fixer | |

## Steps
1. Open Runs and logs for a run with nested agents (project 61134432, run 3bdd7ebb).

## Expected
A compact tree: agents nested under their caller, each collapsed with step count, tokens and status, opening to its steps; the first step selected so the right pane is never empty; a narrow list that scrolls on its own; no wrapped labels.

## Actual
One long flat column of every model step (Process engineer · step 1..10, Energy systems engineer · step 1..15, Design lead · step 1, 2, 14 mixed) with token counts; 'step' and its number wrap onto two lines; the wide right pane looks empty.

## Evidence
- Sahand's screenshot (in the chat with the coordinator, 2026-11-05).

## Cause

(Facts, or a guess marked as one.)

## Fix
frontend 1.1.80 (commit in git log, 'QA-089: ...'): agent tree with step count and tokens per agent, the selected step's agent open, a 260 px list with its own scroll beside the detail. Status per agent is not shown: the run log has no per-agent status.

## Retest

(Who, when, result.)
