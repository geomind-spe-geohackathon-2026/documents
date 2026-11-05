# QA-262: read_result with a group path 'd0' or 'd1' is refused (13 calls in 5 runs; analysis lead, economist, design lead, reviewer); speed, see QA-150

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | geomind |
| Reporter | speed-analysis-II |
| Found | 2026-11-05 18:07 UTC |
| Versions | backend 1.1.105+ (geomind 0.4.102-0.4.118) |
| Where | api.geomind.team run logs: QA-AI-project-I 1 194c3879 (economist 4, design_lead 2), QA-E2E-report-I 2 d8662b0d (analysis_lead 2), QA-AI-case-I 8 5a30bc42 (analysis_lead 2), QA-AI-project-I 3 436f8d53 (analysis_lead 2), QA-AI-design-I 3 5e847cc6 (reviewer 1) |
| Fixer | hotfix-python-lead |

## Steps

1. Ask for the doublet's or a well's results after a simulate (report, analysis or project questions).
2. Read the run log: `read_result` with module path `d0` or `d1`.

## Expected

Either read_result accepts a group path and returns its sub-modules (d0.reservoir, d0.well, d0.esp, d0.riser), or the prompts and the simulate summary name the full paths so the first call is right.

## Actual

`read_result` with module path `d0` / `d1` is refused 13 times in 5 runs by four agents ('Results: module path = d0; expected one of d0.reservoir, d0.well, ...'). Each refusal costs a model step and the agent then reads the sub-modules one by one.

## Evidence

- Analysis: `documents/project/plans/speed-case-plant-baseline-0.4.10x.md` (group B, T3/T7), scripts in `documents/project/plans/speed-baseline-scripts/`.

## Cause

Fact: results are stored per sub-module; the doublet group `d0` has no entry of its own. The agents take `d0` from the plant's module list (the doublet is one module in the plant). Fix in geomind's read_result (group path) or the result outline.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
