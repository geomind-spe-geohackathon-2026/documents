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

# Round 2 and retests (17:48-19:06 UTC)

Projects `QA-TEST QA-E2E-study-I 2` (8eabf827-1f43-4cf8-86a4-39147bea32a0) and
`QA-TEST QA-E2E-study-I 3` (ac687987-8bfe-452f-8013-7a4b577a3655), same seed as round 1.

| Request | Run | Wall time | Calls | Cost | Outcome |
|---|---|---|---|---|---|
| Chip "Optimise the design", first card denied with a reason | 83182f0e | 36 min (answer ready at 4 min) | 145 | 0.071 USD | denial kept; then 32 min on an unasked family (QA-276); estimate_costs internal error (QA-275); usage goes backwards (QA-277) |
| Sensitivity of plant v2 to discount rate and electricity (QA-152 retest) | 82efd097 | 1 min 24 s | 23 | 0.007 USD | passes; a reload during the run keeps the live steps |
| Optimise, "how many trials were feasible" (QA-205/209 retest) | 4885075b | 14 min 11 s | 107 | 0.037 USD | passes (240 trials, 3 feasible); 20 approval cards, 9 refused after approval (QA-296) |
| Compare plants v1 and v2 (QA-228 retest) | b709a671 | 1 min 7 s | 18 | 0.006 USD | passes (geothermal 43 626 MWh = Results); raw "improvement:" lines (QA-300) |
| Uncertainty, three prices, P10/P50/P90 (QA-248 retest) | ce4be675 | 2 min 36 s | 25 | 0.009 USD | subset passes; P10/P90 still missing; 15 digits (QA-099) |
| Use the best design as the project plant, simulate January | 9a45c7ce | 9 min 5 s | 96 | 0.047 USD | cannot adopt from chat (QA-312); January peak boiler 17.64 MW ok |
| Study page: Run again opt1 (no LLM) | study f37742d7 | 41 s | - | - | ok: lcts 49.268 EUR/MWh at 285 m3/h on plant v6, slightly below the chat's "cannot beat 49.281" at 300 m3/h |

Retest results: verified QA-152, QA-205, QA-209, QA-213, QA-228, QA-249; partly fixed and reopened
QA-214 (running time value), QA-215 (backend part), QA-248 (percentiles); QA-237 backend part passes
(no plant versions written by agents), but it removed the chat's only way to change the plant
(QA-312). QA-099 still shows for sensitivity and uncertainty figures.
