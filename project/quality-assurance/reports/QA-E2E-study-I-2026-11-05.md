# QA-E2E-study-I, 2026-11-05: studies and results through the chat (round 1)

Tester: QA-E2E-study-I (agent-browser on https://geomind.team, chat-first). Backend 1.1.102 ->
1.1.108 during the round (six deploys, the API down 30 s-3 min each time; runs survived).
Project `QA-TEST QA-E2E-study-I 1` (8fcbf709-537a-40d9-ac1f-abadd1061775), seeded by API with the
reference `case.json` + `economics.json` and the plants HackathonPlant (v1) and
HeatingAbsorptionCoolingPlant (v2) from `gemini/examples/hackathon_2026/`. One chat
(c0cae905-a2a8-44cf-8bec-f4899f313e8b), six runs.

## Timing

| Request | Run | Wall time | Steps | Calls | Input tokens | Cost | Outcome |
|---|---|---|---|---|---|---|---|
| Simulate the current plant for 2027 | 61721f4c | 40 s | 15 | - | 0.20 M | 0.002 USD | ok |
| Price sensitivity of lcts | d6f8e79a | 7 min 29 s | 50 | 83 | 0.98 M | 0.024 USD | no result (QA-152, since verified) |
| Optimise doublets, flow, chiller for lcts | 4eb8e2f4 | 21 min 17 s (about 6 min waiting for my approval) | 78 | 173 | 2.41 M | 0.058 USD | ok, but rests on 27 of 240 trials (QA-205) |
| Compare the two plants, recommend one | 52383511 | 7 min 40 s | 61 | 100 | 1.54 M | 0.035 USD | ok, wrong geothermal heat (QA-228), switched the plant (QA-237) |
| Uncertainty P10/P50/P90 of lcts | fd4b7e2c | 54 s, cancelled by me | 5 | - | 0.10 M | 0.003 USD | cancel ok in 13 s |
| "Please continue" | 01222f3a | 2 min 24 s | 14 | 18 | 0.33 M | 0.007 USD | resume ok; P5/P95 only (QA-248) |

gemini's own calls are fast (optimize 240 trials 45 s, sensitivity 1.3 s, simulate < 1 s); the
time goes into agent round trips, re-reads (read_stored 85 calls in the optimisation run) and
duplicated writers (design lead twice, explainer twice in the comparison).

## Accuracy

| Figure | App / agent | Reference | Verdict |
|---|---|---|---|
| Heat delivered 2027 | 111 667.68 MWh | CSV sum 111 667.68 MWh | ok |
| Cold delivered 2027 | 23 742.53 MWh | CSV sum 23 742.53 MWh | ok |
| Energy basis of lcts | 111 744.16 / 23 758.79 MWh | 365-day sums above | 365.25-day year, not explained (QA-099 reopened) |
| Peak heat / cold | 30.0 / 10.0 MW | 30.0 / 10.0 MW | ok |
| Production flow | 300 m3/h per doublet | 50-300 m3/h | ok (at the cap) |
| Brine cooling | 20.7 K (HAC), 35.5 K (Hackathon) | <= 40 K | ok |
| Supply temperatures | 100 C / 20 C | 100 C / 20 C | ok |
| Geothermal heat, HAC plant | chat 34 837.7 MWh; Results 43 626 MWh | one value | wrong in chat (QA-228) |
| Heat exchanger use | Results "not used" | carries all geothermal heat | wrong (QA-213) |
| Doublet running days vs geothermal days | 330 d each vs geothermal off 125 d | consistent | contradiction (QA-214) |
| CO2 | chat run 1 "18.22 kt" (co2_emitted, direct) ; Results 20.96 kt (CO2e) | - | both correct, two names, chat later gives both |
| Optimisation best | 2 doublets, 300 m3/h, 10 MW chiller, lcts 49.281 | start point | plausible, sample of 27 trials read |
| Sensitivity rank | gas 21.7 > carbon 10.8 > electricity 4.0 EUR/MWh | follows opex split | plausible |
| Comparison | HackathonPlant lcts 45.10 vs 49.28 EUR/MWh | - | plausible; the heat pump avoids the boiler |

## Bugs

New: QA-205 (major), QA-209, QA-213, QA-214, QA-215 (fixed within the round: tab labels now carry
plant version and time), QA-228 (major), QA-232, QA-237 (major), QA-248, QA-249. Evidence added:
QA-152. Reopened: QA-099.

## Works

Simulate from chat; optimise from chat; comparison and recommendation; Results page economics,
energy balance, capacities, days covered, constraints; Compare chart and table; "Use this design as
the plant" (Plant v6 saved, toast); Runs and logs list, run page, per agent and per model, Export
JSON (3.2 MB, no secrets, no Claude model); Cancel run; continue after cancel.
