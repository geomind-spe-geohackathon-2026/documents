# QA-035: A deploy ends every running agent run; runs should resume after the worker restarts

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | backend |
| Reporter | coordinator |
| Found | 2026-11-04 20:30 UTC |
| Versions | backend 1.1.19 to 1.1.27 (geomind 0.4.28 to 0.4.32) |
| Where | every hotfix deploy; reported by qa-5 (runs d0cced4f at 20:20, 9a33db47 at 20:30 UTC), qa-4 (82c36a57), and runs b894b090, b2088107 |
| Fixer | |

## Steps

1. Start a long agent run in chat (case to report).
2. While it runs, deploy the backend (`scripts/hotfix_deploy.sh`), which recreates the worker.

## Expected

The run goes on after the worker is back: geomind rebuilds a run from its event log ("resume,
crash recovery and replay are one mechanism", `geomind/engine/recovery.py`), so the worker should
resume every run it found `running` instead of ending it.

## Actual

Since QA-017 the worker ends such runs as failed/interrupted with a message, and the user must send
the message again. With several deploys an hour during QA, no long pipeline run reaches the report
(qa-5: 453k input tokens of a case-lead run lost at 20:30).

## Evidence

- ![screenshot](../evidence/QA-035/1.png)
- Run JSON: `../evidence/QA-035/run-<id>.json`

## Cause

Guess: the QA-017 start-up hook marks the runs failed; it could re-enqueue them for `assistant.runs.resume` (or a resume from the log) instead, as long as the run is not too old.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
