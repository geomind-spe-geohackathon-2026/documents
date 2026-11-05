# QA-274: Chat sensitivity and uncertainty studies (study/v1_sens_permeability_gradient, study/v1_unc_...) never reach the Report page: Design list has only the two simulations, section says 'not a sensitivity or uncertainty study'

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | backend |
| Reporter | QA-E2E-report-I |
| Found | 2026-11-05 18:33 UTC |
| Versions | backend 1.1.109 (geomind 0.4.110), frontend bundle index-TsXgd_n9.js |
| Where | https://geomind.team/projects/fa329839-43df-48c3-81c3-89af503b92c0/design/report; run d8662b0d |
| Fixer | hotfix-back-lead-II |

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

Backend 1.1.117 (8936366, back-m1): on a root chat run's finish each sensitivity or sample study the run started gets a Result (study_id, run.found = the study's stored result) with the report, coverage and design of the study's design on the case of the run's last plain simulate. A run with no plain simulate gives no study result (logged).

Proposal (backend, hotfix-back): save a chat study of kind sensitivity / uncertainty as a Result
with its tornado / spread (the fields the Results page already reads), named after the study.
- 2026-11-05 18:46 UTC: backend 1.1.117, 8936366
- 2026-11-05 19:38 UTC: retest QA-E2E-report-I 19:40 UTC: chat sensitivity (and chat simulate) not saved as results in project 3
- 2026-11-05 19:56 UTC: backend 1.1.117 8936366
## Retest

Chat: simulate a design, then a sensitivity study on it. Report page: the Design list offers the study and 'Uncertainty and sensitivity' shows its tornado.

QA-E2E-report-I, 2026-11-05 19:40 UTC, backend 1.1.122+, project QA-TEST QA-E2E-report-I 3 (a9ff33c4): STILL FAILS. In the chat: run 12115d92 simulated design/v1 (result/9b0db55da13a4a5b), run f1108405 compared v1 and v2 (v2 result/11c2e401cd91606b), run e458852b (chip "Sensitivity analysis", 19:35:22-19:36:56 UTC) ran gemini sensitivity `study/sens_v1_main_inputs` on design/v1 (6 drivers, LCTS swing 13.59 EUR/MWh for the ground gradient). Report page, Options, Design list: only "simulation HackathonPlant" (the seeded page study). `GET /design/results?project=a9ff33c4...` returns that one result only: neither the chat sensitivity nor the chat's last plain simulate (QA-135 option C) was saved. Guess: the chat result ids are content digests (result/9b0db55da13a4a5b is the same id in projects 1, 2 and 3), so a save keyed by that id may be skipped as already stored in another project. Reopened.
