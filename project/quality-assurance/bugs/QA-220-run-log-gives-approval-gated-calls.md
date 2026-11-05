# QA-220: Run log gives approval-gated calls and ask_user duration 0: a 6-13 min user wait between steps cannot be told from work; speed, see QA-150

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | geomind |
| Reporter | speed-analysis-II |
| Found | 2026-11-05 17:32 UTC |
| Versions | backend 1.1.100-1.1.103 (geomind 0.4.96-0.4.98) |
| Where | api.geomind.team `GET /assistant/runs/{id}/log`: run bf3990c4 (QA-E2E-economics-I 1) step 10 set_case then 755 s to step 11; run 4eb8e2f4 (QA-E2E-study-I 1) design_lead step 2 build_plant then 373 s to step 3; run cf319cd4 (QA-E2E-case-I 1) step 13 ask_user, 108 s |
| Fixer | |

## Steps

1. Read a run log of a run that showed an approval or question card.
2. Look at the duration of the tool call that showed the card, and the `ts` of the next step.

## Expected

The log says how long each card waited for the user (a `wait` duration on the call, or the card's shown/answered times), so speed analysis can split wall time into agent work and user wait.

## Actual

Approval-gated calls (`set_case`, `build_plant`, `patch_plant`, `ask_economics`) and `ask_user` have duration 0. The wait only shows as a gap between step `ts` values (12.6 min, 6.2 min, 1.8 min above), and such a gap cannot be told from hidden work (a nested run, a restart) without reading the chat. In bf3990c4 the wall time is 18.8 min and the model time 3.1 min. Part of QA-150 (speed measurement).

## Evidence

- Analysis: `documents/project/plans/speed-case-plant-baseline-0.4.10x.md`, script `documents/project/plans/speed-baseline-scripts/gaps.py`.

## Cause

Fact: tool duration is measured around the call that returns the pending card, not around the user's answer. Fix in backend (card answered time) or geomind (duration of the resumed call).

## Fix

Backend part, backend 1.1.117 (f9a8d40, back-m2): GET /assistant/runs/{id}/log has `waits`, one span per answered request card (request, kind, call_id, tool, agent, run_id, started, ended, decision, duration s) and `wait` (s) on the gated tool call. geomind part with hotfix-python-lead.

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 18:46 UTC: backend part 1.1.117 f9a8d40; geomind part open
## Retest

GET /assistant/runs/bf3990c4.../log: the set_case wait shows about 755 s in `waits` and as `wait` on its call.

(Who, when, result.)
