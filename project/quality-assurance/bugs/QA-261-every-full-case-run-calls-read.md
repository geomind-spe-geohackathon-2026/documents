# QA-261: Every full case run calls read_case before a case exists: 17 refused no_case calls in 6 case runs (case lead 1-4, project lead 1); speed, see QA-150

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | speed-analysis-II |
| Found | 2026-11-05 18:07 UTC |
| Versions | backend 1.1.105+ (geomind 0.4.102-0.4.118) |
| Where | api.geomind.team run logs: QA-TEST QA-AI-case-I 4 dd6b4700 (case_lead 4, project_lead 1), QA-E2E-case-I 4 679f3555 (3+1), QA-AI-case-I 6 6a8dba9a (2+1), QA-E2E-case-I 5 c17ca5fb (1+1), QA-E2E-case-I 4 ff712a26 (1+1), 6b77648d (project_lead 1) |
| Fixer | hotfix-python-lead |

## Steps

1. Start a case run on a project with files and no case (the QA-AI-case-I / QA-E2E-case-I prompt).
2. Read the run log and look for `read_case` with error code `no_case`.

## Expected

The project lead and the case lead see in the problem state that there is no case and go to set_case (or the question) at once; no read_case before the first set_case.

## Actual

Every full case run in group B calls `read_case` before any case exists: 17 refused `no_case` calls in 6 runs, the case lead 1 to 4 times, the project lead once. Each is a model step (case_lead ~9.6 s per call, 44 k input tokens median), so 10-40 s per run on the stage whose wall target is < 5 min.

## Evidence

- Analysis: `documents/project/plans/speed-case-plant-baseline-0.4.10x.md` (group B, T3/T7), scripts in `documents/project/plans/speed-baseline-scripts/`.

## Cause

Guess: the case lead's and project lead's prompts open with 'read the case' as the first step; the problem state already says no case. Fix in the prompts (or the state the lead gets says `case: none` in a way the model takes as final).

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 18:31 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
## Retest

(Who, when, result.)
