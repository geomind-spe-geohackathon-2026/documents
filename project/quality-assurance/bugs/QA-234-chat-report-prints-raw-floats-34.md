# QA-234: Chat report prints raw floats (34.63640461864158 MEUR, 1.0178e-16 unmet share, 0.9999925 reinjection) instead of rounded values with units

| Field | Value |
|---|---|
| Status | verified |
| Severity | minor |
| Area | geomind |
| Reporter | QA-E2E-report-I |
| Found | 2026-11-05 17:44 UTC |
| Versions | backend 1.1.106 (geomind 0.4.106), frontend bundle index-TsXgd_n9.js |
| Where | https://geomind.team/projects/0e44cb05-6096-434e-95ee-56b434898015/assistant/chat/b31664b0-44c2-4d20-9ee7-987f592b5aff; run 3f8270d5-b11e-4c86-b3ca-b0b4d4feb61c; final answer |
| Fixer | |

## Steps

1. Ask the chat for the design report (QA-165 Steps 2) and read the final answer.

## Expected

Engineering precision, as the Report page shows: CAPEX 34.64 MEUR, LCOH 43.75 EUR/MWh, boiler
heat 254 MWh, brine cooling 35.5 K, unmet heat 0 %, reinjection 100 %.

## Actual

"Boiler heat 253.8975085761609 MWh", "Electricity bought 26727.91980017326 MWh", "CAPEX
34.63640461864158 MEUR", "LCOH 43.75277721956231 EUR/MWh", "brine_cooling_limit (d0)
35.515755069967724 K", "full_reinjection 0.9999925240970869 / limit 0.99999",
"heat_delivered (unmet share) 1.0178290352774679e-16 / 0.01". Requirement rows use gemini ids
(`production_flow_range`, `heat_delivered`) instead of the names the Report page uses
("Production flow range (d0)"). The same report on the Report page is rounded and named.

## Evidence

- Final chat answer text: `../evidence/QA-234/chat-answer.txt`

## Cause

Guess: the explainer/project lead copies tool output values verbatim; `handbook-report.md` or
the explainer prompt has no rounding rule (3-4 significant figures, units, % for shares).

## Fix

Proposal: a rounding rule in `geomind/prompts/project/explainer` and `knowledge/handbook-report.md`
(3-4 significant figures, shares in %, tiny values as 0), or round the numbers in the tools'
summaries (`compute_kpis`, `check_results`) as `compute_kpis` already does for some fields.
- 2026-11-05 18:59 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest

QA-E2E-report-I, 2026-11-05 19:45 UTC, project 3 runs 12115d92 and f1108405: headline figures are rounded (LCTS 45.10 EUR/MWh, CAPEX 34.636 MEUR, CO2 13.77 kt, 2.636 MW); no 16-digit floats left. Leftovers: unmet heat as 1.1366e-11 / 2.0103e-12 MW (should read 0), and 5 significant figures in cost parts (0.098042, 0.028643 MEUR). Verified for the main complaint; the e-12 leftovers are cosmetic.
- 2026-11-05 19:39 UTC: retest QA-E2E-report-I: headline figures rounded; e-12 unmet leftovers cosmetic
