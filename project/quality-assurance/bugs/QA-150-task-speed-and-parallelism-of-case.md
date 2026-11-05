# QA-150: Task: speed and parallelism of case and design stages (baseline top 10, plan B2-B5)

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | Coordinator-V |
| Found | 2026-11-05 16:51 UTC |
| Versions | frontend 1.1.113, backend 1.1.101 (geomind 0.4.97, gemini 0.6.16) |
| Where | Task (Sahand 2026-11-05 16:51 UTC: all work goes to hotfix threads as bugs or tasks); `documents/project/plans/speed-case-plant-baseline.md` (top 10 causes), `documents/project/plans/speed-case-plant.md` (B2-B5, C) |
| Fixer | hotfix-python |

## Steps

1. Take the top 10 causes in speed-case-plant-baseline.md and plan items B2-B5 / C.
2. Fix them in geomind (parallel sub-agents per IMP-025, fewer re-reads, fewer hand patches, fewer simulate round trips).

## Expected

Case stage and design stage run their sub-agents in parallel; design run well under the 70 min of QA-145; no needless re-reads; accuracy unchanged or better.

## Actual

Baseline: 41 runs, 17% refused, plant ~78 active min/run, 1 of 17 done (speed-case-plant-baseline.md).

## Evidence

See Where.

## Cause

See the baseline report. New evidence will come from QA-AI-case-I, QA-AI-design-I and speed-analysis-II; fold their bugs in here or file them separately.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
