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
