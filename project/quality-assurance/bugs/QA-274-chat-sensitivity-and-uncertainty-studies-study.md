# QA-274: Chat sensitivity and uncertainty studies (study/v1_sens_permeability_gradient, study/v1_unc_...) never reach the Report page: Design list has only the two simulations, section says 'not a sensitivity or uncertainty study'

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | backend |
| Reporter | QA-E2E-report-I |
| Found | 2026-11-05 18:33 UTC |
| Versions | backend 1.1.109 (geomind 0.4.110), frontend bundle index-TsXgd_n9.js |
| Where | https://geomind.team/projects/fa329839-43df-48c3-81c3-89af503b92c0/design/report; run d8662b0d |
| Fixer | |

## Steps

1. Run d8662b0d (QA-257) runs `sensitivity` (study/v1_sens_permeability_gradient, 2 drivers,
   10 metrics) and `sample_uncertainty` (study/v1_unc_permeability_gradient, 200 draws) in chat.
2. Open the Report page, Options, Design list.

## Expected

The chat's sensitivity (and uncertainty) studies are selectable results, and the report section
"Uncertainty and sensitivity" shows their tornado/spread, as it does for page studies.

## Actual

Design list: "simulation HackathonPlant" (page study) and "simulation v1" (the chat's last plain
simulate, QA-135 option C) only. Section text: "This result is not a sensitivity or
uncertainty study." The sensitivity numbers exist only as raw floats in the chat answer.

## Evidence

- Report page text: `../evidence/QA-270/report-page-text.txt` (same page)

## Cause

Guess: the backend saves only the last plain simulate of a run as a Result (QA-135 option C);
gemini studies run by the agents (sensitivity, sample_uncertainty, run_study) are not saved
as Results with tornado/spread.

## Fix

Proposal (backend, hotfix-back): save a chat study of kind sensitivity / uncertainty as a Result
with its tornado / spread (the fields the Results page already reads), named after the study.

## Retest

(Who, when, result.)
