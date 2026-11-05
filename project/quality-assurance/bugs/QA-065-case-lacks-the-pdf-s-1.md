# QA-065: Case lacks the PDF's 1-3 doublets rule, yet the design lead says 'the case fixes the number of doublets at 1-3'

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | geomind |
| Reporter | qa-func-1 |
| Found | 2026-11-05 00:11 UTC |
| Versions | backend 1.1.56 (health 2026-11-05 ~00:15 UTC) |
| Where | https://geomind.team/projects/a0947848-b958-4ee9-8927-56ec0a9cff03/design/case, tab Requirements; chat 235c60c5-da86-4f21-9257-e21a6e400697, design lead question about search ranges |
| Fixer | hotfix-python |

## Steps

1. Upload the challenge PDF and both CSVs, ask the chat to set up the case; approve the set_case cards.
2. Open Design, Case, Requirements.

## Expected

A requirement on the doublet count (quantity `count`, 1 to 3) next to the other PDF hard constraints, or the agents not claiming it is in the case.

## Actual

The case has 8 requirements (flow 50 and 300 m3/h, brine cooling 40 C, reinjection 1, 330 d, pump efficiency 0.7, supply 100 and 20 C); none bounds the number of doublets, although the quantity `count` exists. The design lead then asks: 'The case fixes the number of doublets at 1-3 (brief p.2) ... 1. size.doublets = 1 to 3 (from the case)'. The claim is false.

## Evidence

- ![screenshot](../evidence/QA-065/1.png)
- Run JSON: `../evidence/QA-065/run-<id>.json`

## Cause

Guess: the case lead did not map the PDF doublet rule to a requirement and the design lead assumed it did.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
