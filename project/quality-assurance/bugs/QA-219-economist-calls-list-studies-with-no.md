# QA-219: Economist calls list_studies with no arguments 4-6 times in one run (3 of 5 economist runs); speed, see QA-150

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | speed-analysis-II |
| Found | 2026-11-05 17:32 UTC |
| Versions | backend 1.1.100-1.1.103 (geomind 0.4.96-0.4.98) |
| Where | api.geomind.team run logs: QA-TEST QA-AI-analysis-I 1 runs 57c42f61 (6 calls), c2b815a8 (4); QA-TEST QA-E2E-study-I 1 run d6f8e79a (6); agent economist |
| Fixer | |

## Steps

1. Ask a costing, sensitivity or uncertainty question on a project with studies (the QA-AI-analysis-I and QA-E2E-study-I prompts).
2. Read the run log (Runs and logs) and count the economist's `list_studies` calls.

## Expected

One `list_studies` per economist run; its answer is in the context after the first call.

## Actual

The economist calls `list_studies` with the same empty input 4 to 6 times in one run (3 of 5 economist runs in the 0.4.96-0.4.98 sample), each a full model step (6.8 s per economist call on average). Part of QA-150 (speed): about 20-35 s per run.

## Evidence

- Analysis: `documents/project/plans/speed-case-plant-baseline-0.4.10x.md` (section 'Where the time goes now'), scripts in `documents/project/plans/speed-baseline-scripts/` (`analyse.py` repeats).

## Cause

Guess: the economist re-lists studies after each refused `sensitivity`/`read_study` (QA-152 refs) to find a valid reference; check whether it still happens on 0.4.100+ where QA-152 is fixed (second pass of speed-analysis-II).

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 18:56 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest

(Who, when, result.)
