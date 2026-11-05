# QA-086: design_lead stops every 30 steps and asks the user to continue, also with Auto-approve on

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | functional-qa-2 |
| Found | 2026-11-05 06:42 UTC |
| Versions | frontend 1.1.71, backend 1.1.71 (values set), read on backend 1.1.75; geomind 0.4.65 |
| Where | https://geomind.team/projects/aa8023ca-33b3-4e5a-a7ea-5afad6ed4c1e/design/case (Economics tab); project QA2 functional-qa-2 economics; chat f349646d-953b-41c5-a349-09903a5e29c5; runs 6921d00e (set at 04:3x UTC) and f59e5d2c |
| Fixer | hotfix-python |

## Steps

1. Start the run as in QA-084 with Auto-approve on.
2. Wait about 15-20 minutes into the design stage.
3. A card appears: 'design_lead: the run took its 30 steps; continue with 30 more, or stop and answer from what it has?' (continue / stop).

## Expected

With Auto-approve on, the step limit of the nested design_lead does not stop the run each time, or the limit is high enough for a design, or it only asks when no progress is made.

## Actual

The card appeared at least 4 times in two runs and needs a human click each time (auto-approve does not cover it). Run f59e5d2c has 5 design_lead sessions that each hit 25-30 steps; the run is at 14.8M input tokens and 815 tool calls after 2 h. An unattended run therefore stalls until someone clicks continue.

## Evidence

- Agents of run f59e5d2c (steps per session): `../evidence/QA-086/agents-f59e5d2c.json`

## Cause

Guess: design_lead has a fixed 30-step budget and the continue question is an ask_user, not an approval, so auto-approve skips it.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 10:01 UTC: geomind 0.4.78 + gemini 0.6.12 in backend 1.1.83 (5b2691e), deployed 2026-11-05 10:00 UTC by hotfix-python-II
## Retest

(Who, when, result.)
