# QA-118: Gas composition set by chat: approval card shows rounded values, case page shows other digits than the Knowledge row

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | frontend |
| Reporter | functional-qa-case-I |
| Found | 2026-11-05 11:06 UTC |
| Versions | backend 1.1.84 (geomind 0.4.80) |
| Where | https://geomind.team/projects/15b2f15f-46d0-4b09-a44b-0f849127c1f0 (QA3 case); chat 37fb7886-a3b0-46b3-b36f-6afb72971d14; request "look the corrected gas composition up again"; Set case approval card, then Design > Case > Utilities |
| Fixer | hotfix-front-III |

## Steps

1. After QA-112 was corrected in Knowledge, ask the chat to close the open gas composition from the corrected document.
2. Read the "Set case" approval card.
3. Approve, open Design > Case > Utilities, read the composition fields.

## Expected

The card shows the values that are stored; stored values equal the Knowledge row (CH4 0.8249507401227822, C2H6 0.039549858193534584, C3H8 0.012748086337494389, CO2 0.011912342910726407, N2 0.11083897243546233), sum exactly 1 (the row says "do not round").

## Actual

The approval card showed CH4 0.825, C2H6 0.03955, C3H8 0.01275, CO2 0.01191, N2 0.1108 (rounded; these add to 1.00001). The case page shows 82.49510192871094, 3.954989910125733, 1.274809956550598, 1.191230058670044, 11.083900451660156 mol% (sum 100.00003 %), which match neither the card nor the Knowledge row from the 7th digit. The agent says it took the values "digit for digit" and that the sum is exactly 1.0.

## Evidence

- ![screenshot](../evidence/QA-118/1.png) (taken on the Utilities tab)
- Chat text: `../evidence/QA-118/chat-text.txt`

## Cause

Guess: the card rounds for display and the case page reads a float32; or the agent sends rounded values. Not separated.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 14:15 UTC: for hotfix-front-III (hotfix-back-III): backend stores and returns the exact Knowledge values (GET /design/case and /design/case/versions/7 and /8 of 15b2f15f: CH4 0.8249507401227822, C2H6 0.039549858193534584, C3H8 0.012748086337494389, CO2 0.011912342910726407, N2 0.11083897243546233; sum 1). No backend rounding in approvals. Both faults are display: the Set case card rounds to 4 significant digits, and the Utilities fields show float32-like digits after the fraction->mol% conversion (82.49510192871094 = float32 of 0.824951). Show stored digits (or label as rounded), and convert in float64.
## Retest

(Who, when, result.)
