# QA-123: Capacities answer says the heat exchanger is not used, a later answer shows it runs at 7.8 MW mean

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | functional-qa-report-I |
| Found | 2026-11-05 11:17 UTC |
| Versions | backend 1.1.84 (geomind 0.4.80), frontend not read |
| Where | https://geomind.team/projects/91b202b6-6236-45e7-8860-a58437d6eb98/assistant/chat; project QA3 report; run result/11c2e401cd91606b |
| Fixer | hotfix-python |

## Steps

1. Ask: "What heating and cooling capacities does the design actually realise? ..." (answer: heat_exchanger capacity 1500000 W/K, "gemini reports no use of this module in the run (peak null)").
2. Ask the explainer question (see QA of the same day): it reports the exchanger duty mean 7.85 MW, max 12.36 MW and adds "Correction to an earlier capacities read".

## Expected

One consistent statement of the exchanger use; the capacities report must not call a working module unused.

## Actual

Two answers in one chat contradict each other; the first would make a reader think CAPEX 0.75 MEUR was spent on an idle module.

## Evidence

- Chat text: `../evidence/QA-123/chat.txt` (the answer is after the question quoted in Steps)

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 14:28 UTC: gemini 0.6.14 (capacities reason for unmeasured ratings) + geomind 0.4.86 skill, backend 1.1.89, deployed 14:27 UTC
## Retest

(Who, when, result.)
