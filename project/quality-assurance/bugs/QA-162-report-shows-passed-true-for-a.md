# QA-162: Report shows passed=true for a plant that gives no cooling (verdict infeasible); prompts must use verdict.feasible, not passed

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | handbook-econ-report-I |
| Found | 2026-11-05 17:04 UTC |
| Versions | backend 1.1.104 (geomind 0.4.98, gemini 0.6.17) |
| Where | gemini report output (summary `passed` vs. verdict `feasible`); found by handbook-econ-report-I while re-running the hackathon example, thread message cmsg_016VUmQoW7nUde2xdqUWA2Po6ne8Dnsj2nWxqBVDEqMu82 |
| Fixer | hotfix-python |

## Steps

1. Simulate a plant that delivers no cooling against the competition cooling demand.
2. Read the report summary and the verdict.

## Expected

Agents and the report call such a plant infeasible; no field reads as a pass.

## Actual

`passed` is true while the verdict says the plant is infeasible (`feasible` false). An agent or report that reads `passed` tells the user the plant passes.

## Evidence

- ![screenshot](../evidence/QA-162/1.png)
- Run JSON: `../evidence/QA-162/run-<id>.json`

## Cause

Fix (proposed): geomind prompts and skills (design lead, reviewer, explainer, report) state that feasibility is `verdict.feasible`, never `passed`; the report template shows `feasible`. Whether gemini's `passed` should also consider unmet demand is a gemini question: list it for Sahand, do not ask gemini without his OK.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
