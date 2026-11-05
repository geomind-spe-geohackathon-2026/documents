# QA-E2E-report-I, 2026-11-05: chat to report (S5)

Thread QA-E2E-report-I, hotfix-mode QA round (`documents/project/plans/qa-round-e2e-ai.md`).
Tool: agent-browser (session `qa-e2e-report-I`) on https://geomind.team; set-up and run reads
through the API. Inputs: `gemini/examples/hackathon_2026/` (PDF, two CSVs, `case.json` with
`economics.json`, plants `HackathonPlant` and `HeatingAbsorptionCoolingPlant`).

## Projects (kept)

| Project | Id | Set up (API, as the Study page does) |
|---|---|---|
| QA-TEST QA-E2E-report-I 1 | 0e44cb05-6096-434e-95ee-56b434898015 | 3 documents; case v3 (case.json + demand.csv + economics.json); plant v1 HackathonPlant, v2 HeatingAbsorptionCoolingPlant; page `run` study of v1 (result a528d8da), later of v2 (result 31f5f0c8) to check QA-166 |
| QA-TEST QA-E2E-report-I 2 | fa329839-43df-48c3-81c3-89af503b92c0 | the same; page `run` study of v1 (result c0661c15) |

## Scenarios run

| # | Scenario | Result |
|---|---|---|
| R1 | Typed request: "Write the design report for the simulated HackathonPlant (plant version 1) ... check against the challenge limits" (project 1, run 3f8270d5) | Answer correct in the end, but routed as a redesign (QA-167), page result unreadable (QA-165), first chat simulate ran v2 under the v1 label (QA-166), finish loop on a false stale flag (QA-233), step-limit ask, "stop" marks the run failed (QA-242), raw floats (QA-234) |
| R2 | Report page and PDF of the newest result (project 1, v2) | PDF 8 pages in 7 s, every number equals the result; charts and diagram present |
| R3 | Chip "Write the report" (project 2, run d8662b0d), retest QA-165/166 | Report correct (v1 numbers); QA-166 verified; QA-165 reopened; unrequested sensitivity + 200-draw uncertainty (QA-257) |
| R4 | Explainer question: brine heat vs heat-pump electricity at the peak, 35 K vs 2 x 300 m3/h, why absorption (run 7bcc2a22) | No answer: run failed "internal error in geomind" after 15 min (QA-269) |
| R5 | Report page Options (design list, agent log run), Markdown export (project 2) | Agent log section right (3.11 M tokens, 0.07 USD); Markdown 168 kB; "Geothermal covers 100 %" with a heat pump (QA-270); chat studies not on the page (QA-274) |
| R6 | Next-step chips | Empty chat: Write the report / Explain the results / Sensitivity analysis. After R3: "Sensitivity on the ground gradient", "Compare plant families" (state based). After a run stopped at the step limit: none (QA-242) |

## Timing

| Run | Request | Wall time | Steps | Input tokens | Cost USD | Outcome |
|---|---|---|---|---|---|---|
| 3f8270d5 | R1 typed report request | 48 min 39 s (16:51:19-17:39:57 UTC, then stop) | 349 shown / 216 counted, 365 tool calls | 5.44 M (3.41 M cached) | 0.152 | failed (step_limit after "stop"), report delivered |
| d8662b0d | R3 chip Write the report | 17 min 8 s | 208 (17 retried) | 3.11 M | 0.065 | done |
| 7bcc2a22 | R4 design question | 14 min 41 s | 62 (15 retried) | 0.81 M | 0.034 | failed, no answer |
| page study | `run` of v1 / v2 (API) | about 1 min each | - | 0 | 0 | done |
| Report PDF | Export PDF | 7 s | - | 0 | 0 | 8 pages, 78 kB |

Stage times in R1: project lead plan 17 s; design lead to Build plant card 46 s; reviewer on the
unreadable page result 5 min (40 refused calls); design lead re-simulate 2 min; analysis lead
8.5 min; explainer 1 min; finish loop on stale_result 17 min (17:22-17:39).
In R3: reviewer + design lead 4 min, analysis lead + economist 4.5 min (sample_uncertainty 52.8 s),
explainer 6 min.

## Accuracy

Reference: the Study-page `run` of each plant on case v3 (same gemini as the chat), the CSVs
(heating 111.67 GWh, peak 30.0 MW; cooling 23.74 GWh, peak 10.0 MW) and the challenge limits.

| Figure | Page result v1 (a528d8da) | R1 chat, first (said "v1") | R1/R3 final chat (9b0db55d) | Report page v1 | Page result v2 (31f5f0c8) | Report page / PDF v2 |
|---|---|---|---|---|---|---|
| Heat delivered GWh | 111.67 | 111.67 | 111.67 | 111.7 | 111.67 | 111.7 |
| Cold delivered GWh | 23.74 | 23.74 | 23.74 | 23.74 | 23.74 | 23.74 |
| CAPEX MEUR | 34.64 | 23.96 (wrong plant) | 34.64 | - | 23.96 | 23.96 |
| OPEX MEUR/yr | 3.654 | 4.978 | 3.654 | - | 4.978 | 4.978 |
| LCOH EUR/MWh | 43.75 | 47.81 | 43.75 | - | 47.81 | 47.81 |
| LCOC EUR/MWh | 51.45 | 56.21 | 51.45 | - | 56.21 | 56.21 |
| LCTS EUR/MWh | 45.10 | 49.28 | 45.10 | 45.1 | 49.28 | 49.28 |
| CO2 kt | 13.77 | 20.96 | 13.77 | - | 20.96 | 20.96 |
| Checks passed | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 |
| Geothermal share of heat | 99.8 % (incl. heat pump) | - | "boiler a peak trim only" | 100 % (QA-270) | 39 % | 39 % |
| Doublets / flow | 2 x 300 m3/h | | 2 x 300 m3/h | 2 x 300 m3/h | 2 x 300 m3/h | 2 x 300 m3/h |
| Brine cooling | 35.5 / 34.8 K (<= 40) | | same | | 20.7 / 20.7 K | same |

Every page number equals its result. The chat numbers were wrong only in R1 before the agents
noticed the plant mix-up themselves (QA-166, verified fixed). Chat numbers are unrounded (QA-234).

## Bugs

| Id | Severity | Area | Title (short) | Status at end |
|---|---|---|---|---|
| QA-165 | blocker | geomind | Study-page result listed but unreadable by every result tool | reopened after retest |
| QA-166 | major | geomind | simulate(design=None) ran latest plant v2 under the v1 label | verified |
| QA-167 | major | geomind | Report request routed as a redesign; project lead sees no versions/studies | open (hotfix-back-VI) |
| QA-233 | major | geomind | finish refuses a fresh result as stale_result; 17 min loop | open |
| QA-257 | major | geomind | Unrequested sensitivity + 200-draw uncertainty; uncertainty summary unreadable | open |
| QA-269 | major | geomind | Design question fails after 15 min (evaluate_module fluid, guard kills run) | open |
| QA-270 | major | backend | "Geothermal covers 100 %" counts heat-pump electricity | open |
| QA-234 | minor | geomind | Raw floats in the chat report | open |
| QA-242 | minor | backend | "stop" at the step limit marks the run failed, no chips | open |
| QA-274 | minor | backend | Chat sensitivity/uncertainty studies never reach the Report page | open |

## Next round

A vague request ("summarise the results for my manager"), a report comparing the two plant
versions, a report after a case change (outdated warning), and retests of the bugs above as
they are fixed.

## Round 2 (18:24-19:40 UTC)

Project QA-TEST QA-E2E-report-I 3 (a9ff33c4-6e46-4eaf-be31-5277221dd51d) added, set up as 1 and 2.

| # | Scenario | Result |
|---|---|---|
| R7 | "Compare the two plant versions for my manager ... short form" (project 1, run cb6ce579) | Right answer (build v1) but 470 lines with the old report repeated (QA-289) |
| R8 | Case changed by hand (heating return 60 -> 50 degC, case v4), Report page | No warning (QA-290) |
| R9 | Chat: "Is the report still valid? Update it" (project 2, run 8efe3722) | Asks to load case v4, re-simulates v1, numbers equal a page study on v4 exactly; also answers the R4 questions from read_result; 20 min, 111 read_result |
| R10 | Retest R1 request (project 3, run 12115d92) | QA-165, QA-167, QA-257 verified; QA-233 reopened (finish result_off_case on the page result) |
| R11 | Retest R7 (project 3, run f1108405) | QA-289 verified (3 min, one table) |
| R12 | Retest Report banner (project 2) | QA-290 reopened: false "Out of date" when another plant (v2) exists |
| R13 | Chip "Sensitivity analysis" then Report page (project 3, run e458852b) | Sensitivity in 1.5 min; not on the Report page: QA-274 reopened |

| Run | Request | Wall time | Steps | Input tokens | Cost USD | Outcome |
|---|---|---|---|---|---|---|
| cb6ce579 | R7 compare for manager | 11 min 0 s | 84 | 1.61 M | 0.044 | done, too long |
| 8efe3722 | R9 report after case change | 19 min 55 s | 207 | 3.18 M | 0.087 | done, correct |
| 12115d92 | R10 report (retest) | 26 min 22 s | 114 | 3.96 M | 0.091 | done, correct, finish loop |
| f1108405 | R11 compare (retest) | 3 min 17 s | 30 | 0.69 M | 0.012 | done |
| e458852b | R13 sensitivity chip | 1 min 34 s | 15 | 0.35 M | 0.007 | done |

Accuracy in round 2: case v4 (return 50 degC), plant v1: page study LCOH 40.522, LCOC 47.647,
LCTS 41.772 EUR/MWh, OPEX 3.203 MEUR/yr, CO2 12.504 kt, electricity 22,458 MWh, boiler 0; the
chat (R9) gave the same to every digit. R11 v1/v2 figures equal the page studies.

Bug status at 19:40 UTC: verified QA-165, QA-166, QA-167, QA-257, QA-289; reopened QA-233,
QA-274, QA-290; open QA-234, QA-269, QA-270; QA-242 being fixed.
