# QA-AI-analysis-I, 2026-11-05

Backend layer only (https://api.geomind.team REST, run logs `/assistant/runs/{id}/log`), no frontend.
Agents in scope: `analysis/` lead, economist, reference; the study tools. Input: the competition data in
`gemini/examples/hackathon_2026/` (reference `case.json`, `economics.json`, `plants/HackathonPlant.json`)
set through the API. Versions: backend 1.1.102 -> 1.1.105 during the round (geomind 0.4.98 -> 0.4.102,
gemini 0.6.16 -> 0.6.17); two deploys hit live runs. Model of every agent:
`deepseek/deepseek-v4.1-flash-1017`. Every tool call of every run was read (trace per run in the
evidence folders).

## Projects (kept)

| Project | Id | What was loaded |
|---|---|---|
| QA-TEST QA-AI-analysis-I 1 | 4ce816b1-4bd1-48a5-8e77-9414c2b86301 | 3 competition files, reference case + economics, plant version 1 HackathonPlant; page studies (no LLM) as reference: run 817f5a54, sensitivity 957c9714, sample 5d7bbf26 (200, seed 42), minimize be37a85f (lcts, 30, seed 0, size) |
| QA-TEST QA-AI-analysis-I 2 | 3901ff00-1047-4f82-8329-2ee02e450025 | the same without `economics` in the case |
| QA-TEST QA-AI-analysis-I 3 | cdb636b7-f6ae-4395-b8c0-ad19bc5cacd4 | as project 1 (QA-152 retest) |

## Timing

Wall time from the run's start to its end (my approvals took <=15 s each; the one question in run 4 was
answered after ~40 s).

| Run | Request | Wall | LLM calls | Tool calls | Refused | Input tokens | Cost USD | Outcome |
|---|---|---|---|---|---|---|---|---|
| 389be3c3 (P1) | cost the plant: capex, opex, LCOH, LCOC, LCTS, NPV, CO2, sources | 1 min 13 s | 19 | 26 | 2 | 367 k | 0.0055 | right (economist 7 round trips for 2-3 needed, QA-159) |
| c2b815a8 (P1) | LCTS sensitivity to 3 drivers + p5/p50/p95 | 4 min 47 s | 45 | 56 | 19 | 828 k | 0.0153 | no number (QA-152, fixed and verified since), QA-154, QA-155 |
| 7a7ace73 (P1) | lowest LCTS within 1-3 doublets, 50-300 m3/h (optimisation) | 10 min 58 s | 61 | 97 | 14 | 1 664 k | 0.0362 | right; the study 26 s, the rest overhead (QA-179); card QA-172 |
| a5ea3998 (P2) | cost the plant, case without economics | 5 min 26 s | 31 | 46 | 7 | 1 188 k | 0.0182 | no number; economics written differ from the approved ones (QA-168) |
| 57c42f61 (P1) | sensitivity again on a chat-stored design | 3 min 05 s | 29 | 44 | 2 | 640 k | 0.0129 | right; deploy restart lost 1.6 min (QA-176 evidence); QA-195 |
| 7a70bf41 (P3) | QA-152 retest: sensitivity + uncertainty on the project plant | 1 min 56 s | 19 | 29 | 1 | 356 k | 0.0066 | right, at the first try |

Per stage (from the logs): `estimate_costs` 0.4 s; `simulate` (365 days) 0.3-0.4 s; `sensitivity` 0.6-0.9 s;
`sample_uncertainty` 200 draws 24.8-26.4 s; `run_study` minimize 3 designs 26.3 s. LLM round trips of the
analysis lead and the economist: 1.3-20 s each (median ~4 s). In every run more than 90 % of the wall
time is LLM round trips, not gemini.

## Accuracy

Agents' numbers against gemini's page studies on the same plant and case (no LLM) and the reference
`economics.json`.

| Value | Agents | Reference | Match |
|---|---|---|---|
| capex HackathonPlant | 34.636 MEUR | 34.636 MEUR (study 817f5a54) | yes |
| opex | 3.6539 MEUR/yr | 3.654 | yes |
| LCOH / LCOC / LCTS | 43.753 / 51.445 / 45.102 EUR/MWh | 43.753 / 51.445 / 45.102 | yes |
| CO2 | 13.774 kt | 13.774 | yes |
| NPV | 28.453 MEUR | 34.636 MEUR capex, 4.4763 MEUR/yr, 5 %, 25 yr -> 28.45 | yes |
| sensitivity LCTS effect: electricity / discount rate / carbon | 11.843 / 10.853 / 3.400 EUR/MWh | 11.843 / 10.853 / 3.400 (957c9714) | yes, same rank |
| LCTS p5 / p50 / p95, 200 draws, seed 42 | 37.97 / 46.10 / 54.31 EUR/MWh | 37.97 / 46.10 / 54.31 (5d7bbf26) | yes |
| optimised: doublets, LCTS, capex | 2, 41.300 EUR/MWh, 30.763 MEUR | 2, 41.300, 30.763 (be37a85f) | yes |
| prices used (P1) | the case's economics.json | economics.json | yes, but "no source" (IMP-031) |
| prices proposed without economics (P2) | electricity 145 asked, 115 written; heat 98 / 114.6; analysis period 15 / 25 yr; HX capex 0.1089 EUR/W | 105.75 EUR/MWh; 60; 25 yr; 0.5 EUR/(W/K) | no (QA-168) |
| hard limits on the optimised design | flow 300 of 300 m3/h, brine cooling 35.5 of 40 K, 330 of 330 d, reinjection 0.99999 | challenge limits | all pass (no margin on flow and days, reported) |

## Bugs (this round)

| Id | Sev | Status | Summary |
|---|---|---|---|
| QA-152 | major | verified | study tools refused the project plant; fixed in geomind 0.4.100, retested OK |
| QA-168 | major | open | without economics the analysis lead builds them by hand, writes values other than the approved ones, breaks simulate |
| QA-154 | minor | open | the economics skill's uniform-uncertainty recipe fails when the case has a normal (merge patch keeps `std`) |
| QA-155 | minor | open | update_state refuses a string citation; the error's shape says string is allowed (3 runs) |
| QA-159 | minor | open | economist re-reads case and outputs; unrelated skills attached per tool (~20 k chars) |
| QA-179 | minor | open | optimisation: 26 s study in 11 min (re-typed plant, serial reviewer/analysis/explainer, calculate refusals) |
| QA-195 | minor | open | economist records its own sample count/seed as a user-confirmed assumption |
| QA-180 | - | duplicate | of QA-172 (patch_plant card "Change 0 value(s)"), evidence added |
| QA-176 | (evidence) | | a deploy restarted a running economist (run 57c42f61) |
| IMP-031 | idea | | reference economics names its price sources |

## Judgement of the analysis team

- Routing: the coordinator sent every question to the analysis lead (tool loop) and the optimisation to
  the project loop: right. A case with no economics also went to the analysis lead, which then built the
  economics itself instead of the case lead's `ask_economics` (QA-168).
- Split: the lead delegates costs, sensitivity and sampling to the economist with clear briefs (design
  and result references, what to hand back); the economist's numbers are gemini's, never its own.
- Tools: right tools once a design reference exists; the economist re-reads the case and its own outputs
  (QA-159); the lead re-reads its own brief (`read_stored finding-...`) in 4 of 5 runs.
- Advice: `improvement:` lines are ranked by the size of a cost item only (e.g. "smaller heat pump" for a
  heat pump running at 100 % of its capacity in run 389be3c3); they are not checked against the result.
- Knowledge: enough for prices (`data-economics.csv`), but read by hand it is too long for `read_rag`
  (3 of 8 reads cut to the outline) and the `value_2015` column was not chosen (QA-168).
