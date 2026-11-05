# QA-AI-project-I, 2026-11-05: project team and support agents (backend layer)

Scope: `geomind/agents/project/` (coordinator, lead, drivers, review, reviewer, comparison,
explainer) and `support/` (lead, curator, summarizer), driven through api.geomind.team (REST,
run logs `/assistant/runs/{id}/log` and `/agents`), no frontend. Model
deepseek/deepseek-v4.1-flash-1017. Backend 1.1.102 at the start, 1.1.103 to 1.1.107 deployed
during the round (geomind 0.4.96 to 0.4.98+, gemini 0.6.16/0.6.17). Inputs: the reference
`case.json`, `economics.json`, `data/demand.csv` and `plants/HackathonPlant.json` of
`gemini/examples/hackathon_2026/`, loaded by API (no other thread's output).

Projects (kept): `QA-TEST QA-AI-project-I 1` (35a70dbe-5e24-4f51-9c6f-50e06d47fe82, case + plant,
chat 134dae07-2e37-4a3a-ae0b-83b5e812017e) and `QA-TEST QA-AI-project-I 2`
(dfe5d6e1-8fdc-404f-b150-b8e7d919f2a1, case only, chat f7b3b8fc-e5d2-453e-b524-e17e6733d0d9,
auto-approve on).

## Round 1: runs and timing

| # | Request | Route (coordinator) | Wall time | LLM calls | Tool calls | Input tokens | Cost USD | Outcome | Bugs |
|---|---|---|---|---|---|---|---|---|---|
| 1 | "Hello. What can your team do for this project?" | answer, 3.7 s (right) | 0:04 | 2 | 0 | 2 250 | 0.0001 | good answer, plant-stage chips | QA-190 |
| 2 | Check HackathonPlant, simulate the year, review, explain LCOH, limits, improvements | project (right) | 19:03 | 82 | 213 | 2 481 529 | 0.0667 | passed 15/15, LCOH 43.753 EUR/MWh, good explanation | QA-187, QA-189, QA-176 (was QA-188) |
| 3 | Units preference + reservoir p/T + smallest margin | tool, analysis_lead; preference kept (right) | 1:00 | 7 | 7 | 176 595 | 0.0035 | right: 250 barg, 87.0 degC from 12 + 30 K/km x 2.5 km | - |
| 4 | Handover summary for a colleague | project -> explainer (support_lead/summarizer not used) | 1:08 | 7 | 12 | 136 007 | 0.0042 | good summary; one chip only | QA-204 |
| 5 | Explain only: other configurations, why absorption | project -> explainer; nothing built (right) | 8:26 | 23 | 47 | 1 488 781 | 0.0343 | good text, slow | QA-218 |
| 6 | Case saved by hand (permeability 200 -> 150 mD), still OK? LCOH? | project with task (right) | 22:47 (3 cards, 1 step-limit question) | 113 | 279 | 3 947 660 | 0.0808 | feasible, LCOH 44.641 (+0.888) EUR/MWh | QA-224, QA-227, QA-245, QA-204 |
| 7 | Compare HP + compression chiller vs HP + absorption on LCTS (project 2) | compare (right) | 23:37 | 125 | 200 | 4 208 855 | 0.1084 | no comparison: neither family verified, no retry | QA-252 |

Per agent, run 2 (the reference flow): coordinator 2 s; project lead 6 calls 29 s; design lead 11
calls 51 s (+ one approval wait); reviewer 28 calls 393 s (two sessions, QA-187 and the deploy
restart); analysis lead 18 calls 185 s (two sessions); economist 7 calls 45 s; explainer 69 s.
The project lead's overhead between stages was 3 to 7 s per decision (good).

## Accuracy

| Value | Agents | Reference | Note |
|---|---|---|---|
| Heat delivered | 111670.0 MWh | demand 111.67 GWh/yr (README) | coverage 1.0 |
| Cold delivered | 23743.0 MWh | demand 23.74 GWh/yr | coverage 1.0 |
| Peaks | 30.0 MW / 10.0 MW | 30.0 MWth / 10.0 MWcool | equal |
| Reservoir temperature | 87.0 degC | 12 degC + 30 K/km x 2.5 km = 87 degC | equal |
| Reservoir pressure | 250 barg | 250 bar(g) | equal |
| Hard limits | flow 300.0 of 50-300 m3/h, brine cooling 35.5158/34.7711 K of 40, 2 doublets, 100/20 degC supply, 330 d | challenge limits | all within; flow, running time, supply temperatures at the limit |
| LCOH / LCOC / LCTS (200 mD) | 43.753 / 51.445 / 45.102 EUR/MWh | from gemini's `estimate_costs`, economics.json basis | every number in the final answers matched the tool outputs digit for digit (checked heat, cold, electricity, COP, boiler heat, capex, opex) |
| Permeability 150 mD | LCOH 44.641 EUR/MWh, flow unchanged, brine cooling -0.0072 K | - | plausible: more pump head, same flow |

No accuracy defect found in the project team's answers; the losses are speed, tokens and needless
user stops.

## Main findings

1. Review and explanation agents read far more than they need (QA-187 reviewer, QA-218
   explainer): 39 `read_result` after a verdict, 26 `search_rag` for sections it cannot open.
2. Briefs from the project lead widen a team's job (QA-187 reviewer asked for an engineering
   review; QA-245 design lead asked for a before/after diff without a compare tool).
3. A case saved by hand costs three stops and a wrong question (QA-224, QA-227).
4. Compare loop: sequential and no retries in production (unset settings, QA-252).
5. Deploys restart the sub-agent in flight (QA-176).
6. Small: wasted opening calls of the project lead (QA-189), loop "tool" for a direct answer
   (QA-190), chips cut to the lead's one or two (QA-204).

Not exercised this round: `support_lead` and `curator` (the memory is off in these projects, so
the lead did not offer the support team; the handover went to the explainer).

## Round 2 (18:00 to 18:40 UTC, backend 1.1.107 to 1.1.114)

Projects added (kept): `QA-TEST QA-AI-project-I 3` (3ecb4493-3368-4bc2-b2f0-ca0b06670a86, memory on,
case + plant, chat 5db7a37c-b2ea-43d6-982f-5ebf2b8ad6a7) and `QA-TEST QA-AI-project-I 4`
(588c282d-fd39-4ea1-b495-d167817739c3, empty, chat 2083a333-28d2-4b82-9922-3d3073087b0d).

| # | Request | Route | Wall time | Input tokens | Cost USD | Outcome | Bugs |
|---|---|---|---|---|---|---|---|
| 8 | "is the plant ok?" (project 3) | tool, analysis lead | 1:56 | ~0.35 M | ~0.007 | right: simulate(plant_version 1), feasible, LCOH 43.75 | IMP-032 |
| 9 | Independent review + explain, MEUR, short answers (memory on) | project | 9:43 (6 min of it 9 memory cards) | 593 305 | 0.0145 | passed, short answer (959 chars) | QA-265 |
| 10 | Same case-edit message again after 150 -> 175 mD | tool (wrong: "nothing has changed") | 0:30 | 46 k | 0.0022 | wrong: answer on 150 mD | QA-266 |
| 11 | Retest QA-224/227 in a new chat (175 mD) | project | 6:16, one card | 535 047 | 0.0126 | right: LCOH 44.134 EUR/MWh, 15/15 | QA-227 verified, QA-224 open again |
| 12 | "design me a geothermal plant" (empty project) | project | 5:33 to the first question, stop 0:15 | 517 k | 0.017 | hackathon case assumed | QA-283 |
| 13 | "Make the heat pump smaller to lower LCOH", deny set_ranges with a reason | project | cancelled at 4:40 after 3 cards | ~0.2 M | ~0.006 | lead overrode the denial | QA-288 |

Accuracy, round 2: LCOH 43.753 (200 mD) -> 44.134 (175 mD) -> 44.641 EUR/MWh (150 mD): monotonic,
same flow, more pump head; numbers match `compute_kpis`. Wrong current-case statement in run 10
(QA-266).

Speed, retest: the case-edit flow went from 22:47 / 3.95 M tokens / 3 stops (run 194c3879) to
6:16 / 0.54 M tokens / 1 stop (run a4203016) after the QA-224/QA-227 fixes.

## Round 3 (18:37 to 19:01 UTC, backend 1.1.116)

| # | Request | Route | Wall time | Input tokens | Cost USD | Outcome | Bugs |
|---|---|---|---|---|---|---|---|
| 14 | Retest QA-187/245: case 175 -> 160 mD, re-check, review, "what moved against the last result" (new chat) | project | 8:17 (2 stops) | ~1.15 M | ~0.03 | reviewer 7 calls / 94 s, design lead 8 calls / 20 s; last result not found | QA-187, QA-245 verified; QA-294 |
| 15 | Retest QA-252: compare HP + compression vs HP + absorption on LCTS (project 2, new chat) | project -> comparison | 41:30 | 5 538 596 | 0.2023 | both families side by side, failed family retried, both 15/15; compression wins | QA-252 verified |
| 16 | Persian LCOH question right after a cancelled run | project (wrong: the cancelled request) | cancelled | - | - | patch_plant 10 MW asked again | QA-310 |
| 17 | Same Persian question in a new chat | tool | 2:14 | - | - | right: LCOH 43.753, heat pump 11.068 MEUR, electricity 2.8284 MEUR/yr; answer in Persian, chips English | - |

Accuracy, round 3: the comparison gives LCTS 33.66 EUR/MWh (HP + compression, 2 doublets 2500 m,
heat pump 9.75 MW) and 46.92 EUR/MWh (HP + absorption, 2 doublets 2875 m). gemini's README of the
sample (`gemini/examples/hackathon_2026/README.md`, the plants-folder search) gives 40.34 EUR/MWh for
`HeatingHeatPumpCoolingPlant`; that figure predates several gemini changes (QA-128 carbon cost and
others), so the gap is noted, not reported: worth a check by QA-AI-design-I or with gemini's own
`examples/hackathon.py` on the current version.

## Status of this thread's bugs at 19:01 UTC

Verified: QA-187, QA-227, QA-245, QA-252. Open: QA-189, QA-190, QA-204, QA-218, QA-224 (no-op load
card still asked), QA-266, QA-283, QA-288, QA-294, QA-310. Duplicates: QA-188 (= QA-176, fixed),
QA-265 (= QA-199). Idea: IMP-032.
