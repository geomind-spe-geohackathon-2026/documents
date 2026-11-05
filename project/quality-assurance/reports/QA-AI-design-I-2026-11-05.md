# QA-AI-design-I, 2026-11-05: the design team through the API

Thread QA-AI-design-I of `documents/project/plans/qa-round-e2e-ai.md`: backend layer only
(api.geomind.team REST, run logs `GET /assistant/runs/{id}/log`), the design lead and its engineers
(`geomind/agents/design/`). Input: the competition case of `gemini/examples/hackathon_2026/`
(`case.json`, `economics.json`, `data/demand.csv`, the PDF and the two CSVs uploaded), loaded by the
API with `backend/scripts/seed_qa_projects.py`'s functions; for run 3 also gemini's
`plants/HeatingHeatPumpCoolingPlant.json` as plant version 1. Every tool call and agent round trip
of each run was read from the run log (scripts in the thread's scratchpad; tool-call listings in the
bugs' evidence folders). All times UTC.

Versions: backend 1.1.102 at 16:50, deployed 1.1.103 to 1.1.110 during the round (geomind 0.4.98 to
0.4.110, gemini 0.6.16 then 0.6.17). Runs 1 and 2 were resumed after deploys; run 2's design lead
ran the QA-212 prompt (0.4.109+) from 17:38:17.

## Runs

| # | Project | Run | Request | Approvals | Result |
|---|---|---|---|---|---|
| 1 | QA-TEST QA-AI-design-I 1 | 0df89b7e | Design a plant that meets every hard limit, size, simulate the year, feasible? | auto-approved by script; step-limit question "continue"; one typed answer (below) | infeasible after 35 min (invented 5 km main, QA-210); after the typed answer feasible, LCTS 40.62 |
| 2 | QA-TEST QA-AI-design-I 2 | 5d0216a6 | Compare direct use + absorption against heat pump + compression chiller, 1-3 doublets, lower LCTS? | chat auto-approve on | no result: both families 365/365 failed steps, no repair, "no ranking" (QA-250, QA-251) |
| 3 | QA-TEST QA-AI-design-I 3 | 5e847cc6 | Size the stored plant: doublets 1-3, heat pump and boiler for the lowest LCTS | first build_plant denied with a reason, then script auto-approve | feasible, 1 doublet, HP 9.75 MW, boiler 30 MW, LCTS 37.97 EUR/MWh; search silently 1-2 doublets (QA-253) |
| 4 | QA-TEST QA-AI-design-I 3 | e5f1106e | Change: 2 doublets, heat pump 15 MW, simulate, LCTS and limits? | chat auto-approve on | feasible, LCTS 42.34 EUR/MWh (equal to the stored plant's baseline); 11 min 21 s; 3 build_plant (2 refused) and 2 patch_plant (1 refused) for a two-value change (QA-221, QA-247) |
| 5 | QA-TEST QA-AI-design-I 4 | 2b72af99 | Run 1's request again, on geomind 0.4.119 (QA-175/212 root fix) | chat auto-approve on | feasible at 18:29:22 (23.5 min, no hint needed), 1 doublet, 300 m3/h, geothermal heat share 0.725, CAPEX 22.63 MEUR; the answer gives no LCTS number; run 29 min 8 s, 115 steps, 192 tool calls, 5.03 M input tokens, 0.105 USD |

Run 1's typed answer (17:26) to the project lead's "accept or change heat_delivered" question: "Do
not change heat_delivered: it is a hard limit ... The 5 km heating main is not in the case or the
challenge; where does it come from? Fix the design ...".

## Timing

| Run | Stage | Start-end | Wall time | Notes |
|---|---|---|---|---|
| 1 | routing + project lead | 16:50:33-16:50:45 | 12 s | |
| 1 | lead reads, build_plant (111 missing) | 16:50:45-16:51:30 | 45 s | read_case whole, then 5 sections again |
| 1 | calculate reservoir T | 16:51:30-16:51:59 | 29 s | 2 of 4 refused (QA-235) |
| 1 | fill_parts, 4 engineers | 16:51:59-17:03:55 | 11 min 56 s | deploy at 16:56 restarted all four (QA-176); engineer LLM calls up to 143 s each |
| 1 | lead reads findings, evaluates | 17:03:55-17:06:00 | 2 min 5 s | 7 read_stored (both passes), 4 of 5 evaluate_module refused |
| 1 | patch chain to missing 0 | 17:06:00-17:11:43 | 5 min 43 s | 10 patch_plant, 3 refused (QA-175, QA-212) |
| 1 | size + first simulate | 17:11:49-17:11:56 | 7 s | 365/365 failed (QA-250) |
| 1 | repair rounds 1-2 | 17:11:56-17:25:36 | 13 min 40 s | 2 fill_parts (126 s, 194 s), 8 Pipe evaluations refused |
| 1 | user question, wait | 17:26:06-17:26:50 | (tester) | offers to relax a hard limit (QA-211) |
| 1 | fix after the answer | 17:27:51-17:30:58 | 3 min 7 s | one patch, feasible |
| 1 | review, economics, uncertainty, explainer | 17:30:58-17:39:02 | 8 min 4 s | not asked for |
| 1 | total | 16:50:33-17:39:02 | 48 min 29 s | 206 steps, 327 tool calls (43 refused), 6.02 M input tokens, 0.180 USD |
| 2 | plan call | 17:30:05-17:31:08 | 63 s | |
| 2 | family C | 17:31:19-17:41:47 | 10 min 28 s | team 6 min 48 s, 7 patch_plant, simulate 365/365 failed |
| 2 | family B | 17:41:47-17:48:41 | 6 min 54 s | 8 patch_plant, simulate 365/365 failed, optimize every trial failed |
| 2 | total | 17:30:01-17:49:31 | 19 min 30 s | 103 steps, 161 tool calls (8 refused), 3.67 M input tokens, 0.088 USD |
| 3 | project lead | 17:44:40-17:44:59 | 19 s | |
| 3 | lead re-types the plant, denied | 17:44:59-17:46:42 | 1 min 43 s | 3 build_plant (QA-247, QA-221) |
| 3 | set_ranges, size, optimize, compare study | 17:46:42-17:49:14 | 2 min 32 s | optimize 40 evaluations; doublets 1-2 only (QA-253) |
| 3 | review, analysis, economist, explainer | 17:49:14-17:56:58 | 7 min 44 s | |
| 3 | total | 17:44:40-17:56:58 | 12 min 18 s | 69 steps, 136 tool calls, 2.03 M input tokens, 0.041 USD |

Per agent (run 1): design lead 70 steps, 3.22 M input tokens, 863 s LLM; reservoir engineer 35
steps, 0.58 M, 701 s; energy systems engineer 42 steps, 0.89 M, 1010 s; well engineer never used
(QA-178). Most engineer time is single LLM calls of 40-143 s (deepseek), not tools.

## Accuracy

Reference: gemini's searched sample (`gemini/examples/hackathon_2026/README.md`): lowest LCTS among
designs that deliver heat and cold is HeatingHeatPumpCoolingPlant, 40.34 EUR/MWh; hard limits of
the case `requirements`.

| Quantity | Run 1 first answer | Run 1 final | Run 3 | Reference / limit |
|---|---|---|---|---|
| Family | B (HeatingHeatPumpCoolingPlant) | B | B (stored) | B best of 6 |
| Doublets | 1 (never searched) | 1 | 1 (searched 1-2) | 1-3 |
| Production flow | 55.4-250 m3/h | 250 m3/h | 300 m3/h | 50-300 m3/h |
| Brine cooling | 34.25 K | pass | pass | <= 40 K |
| Running time | 330 d | pass | pass | <= 330 d |
| heat_delivered unmet | 0.0114 (fail) | 0 | 0 | <= 0.01 |
| Heating supply | 100.68 degC | pass | pass | 100 degC |
| Heat from gas boiler | 49 % | 43 % | 23 % (26,066 MWh) | - |
| CAPEX | 27.55 MEUR | 22.55 MEUR | 22.73 MEUR | - |
| LCTS | 44.21 EUR/MWh (infeasible) | 40.62 | 37.97 | 40.34 |
| CO2 | 14.98 kt/yr | 14.81 | 12.90 | - |

Wrong or invented values: a 5 km heating and cooling main with U = 1 W/m2/K (source "assumption",
QA-210); ESP window copied from the case flow band and injection pump without a pressure setpoint
(QA-250); `drainage_radius` 1000 m, `top_depth` 2450 m and other "assumption" values reached the
plant without the user seeing them (approval card "Change 0 value(s)", QA-174).

## Retest of QA-175 / QA-212 on geomind 0.4.119 (run 5)

From build_plant (18:07:13) to `missing 0` (18:17:18): 5 patch_plant, 2 refused (case values given as plant values; a bare 0.7), 3 saved; the team patch left 1 missing value, the next revealed a tear stream that build_plant had not named, and `simulate` refused `injection_pump.frequency` as a parameter that patch_plant had accepted. Runs 1 and 2 took 7-10 patch_plant per plant. Improved, not fixed: QA-212 stays open with this note. The first simulate after optimize had 330 failed steps; one repair patch (3 calls, 2 refused on `gas_grid.composition.CH4` dotted keys) gave a feasible plant. No invented network this time.

## Bugs

New: QA-174, QA-175, QA-176, QA-178, QA-210, QA-211, QA-235, QA-236, QA-247, QA-250, QA-251,
QA-253. Evidence added: QA-169, QA-149. Retests: QA-212 not fixed on the 0.4.109+ prompt (reopened), improved on 0.4.119 (5 instead of 7-10 patch_plant, still open),
QA-221 not fixed for a single stored plant (reopened).

The largest costs, in order: (1) gemini reports a plant's missing values one stage at a time, so
every plant takes 7-10 patch_plant whatever the prompt says (QA-175, QA-212); (2) the first
simulate of every built plant fails all 365 steps on two engineer values (QA-250), and the compare
loop then gives up (QA-251); (3) engineers invent site values (QA-210); (4) deploys restart a whole
team (QA-176); (5) the lead never optimizes or tries a second family on its own (QA-211). Starting
from a stored, complete plant (run 3) avoids (1)-(3): 12 min, feasible, better LCTS than the
reference.
