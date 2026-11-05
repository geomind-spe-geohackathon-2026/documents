# QA-E2E-design-I, 2026-11-05

Section: chat to a plant design (S4 design part), from a reference case and economics loaded by
the API (`gemini/examples/hackathon_2026/case.json`, `economics.json`, `data/demand.csv`; case v3,
nothing missing). Chat-first with agent-browser on https://geomind.team; run logs read through the
API. Plan: `documents/project/plans/qa-round-e2e-ai.md`.

Projects (kept): `QA-TEST QA-E2E-design-I 1` (f1704a61-f1b8-4b63-84d3-20bd30beaed7),
`QA-TEST QA-E2E-design-I 2` (72df9c82-e577-4605-8743-ffcee53c3a73), `QA-TEST QA-E2E-design-I 3`
(d555740a-1054-4642-b905-4919d36702a7).

## Rounds

| Round | UTC | Request | Run | Outcome |
|---|---|---|---|---|
| 1 | 16:51-17:31 | "Design a heating and cooling plant ... 1-3 doublets, 50-300 m3/h, <= 40 K, 100 / 20 degC; check it against the requirements" | 76d19df6 | Feasible design (1 doublet x 300 m3/h, 10 of 10 checks), after 9 plant versions and 12 approval cards |
| 2 | 17:46-18:36 | "Design the plant for this case." Build card denied with a change (2 doublets, backup peak); pipe question answered by typing | dca5ed1a | Failed: build_plant blocked after the worded deny (QA-230); restarted; doublets 2 lost to 1 (QA-260); 31-min ESP patch loop (QA-287); cancelled at 50 min, no simulate |
| 3 | 18:36-18:50 | "Change the current plant to 4 doublets at 400 m3/h and allow 60 K, no peak boiler. Then check it." | 365bcbd3 | Variant built and simulated; the answer names the breached requirement (4 doublets) and that the flow stays at 300 m3/h; asked how to proceed; nothing silently clamped in the answer |
| 4 | 18:51-19:12 | "Design ... within its limits; size, simulate, check; also simulate 150 m3/h for comparison, keep the best design as the result" (project 3) | 06fd16f0 | Feasible 1 doublet x 300 m3/h, LCTS 37.49 EUR/MWh, unmet heat 0 and cold 0, 21 min, 3.18 M input tokens, 0.087 USD; 1,066-word answer; the Results row is still the 150 m3/h variant (QA-223 reopened) |

## Timing (round 1, run 76d19df6)

| Stage / agent | UTC | LLM time | Input tokens | Calls (refused) |
|---|---|---|---|---|
| Whole run | 16:51:52-17:31:10 (39 min) | | 5.56 M (0.155 USD) | 298 |
| Design lead | 16:52-17:17 | 373 s | 2.13 M | 67 (7) |
| Reservoir engineer | 16:55-17:04 | 698 s | 0.43 M | 51 (13) |
| Energy systems engineer | 16:55-17:14 | 506 s | 0.41 M | 40 (4) |
| Build to first full patch | 16:52-17:06 | | | 2 patches refused (bare values, ESP shapes) |
| Patch rounds until checkable | 17:06-17:12 | | | 7 one-value patches (QA-171) |
| size_plant, simulate, optimize | 17:13-17:17 | | | size 1.2 s, simulate 0.3-0.5 s, optimize 30 evals 16 s |
| Reviewer, analysis, economist, explainer (not asked) | 17:17-17:31 (14 min) | 680 s | 2.50 M | 133 (15) (QA-229) |

Round 2: 50 min, 6.07 M input tokens, 0.145 USD, no simulate. Round 3: 12 min to the question, 1.28 M input tokens.

## Accuracy (round 1 design vs. the competition data)

| Item | Competition / case | Agents' design | Verdict |
|---|---|---|---|
| Doublets | 1-3 | 1 | ok |
| Production flow | 50-300 m3/h | 300 m3/h | ok |
| Brine cooling | <= 40 K | 36.06 K | ok |
| Running time | <= 330 d | 330 d | ok |
| Pump efficiency | 0.70 | 0.70 | ok |
| Reservoir temperature | 12 + 30 x 2.5 = 87 degC | 87.0 degC | ok |
| Heating supply | 100 degC | min 100.20 degC | ok |
| Cooling supply | 20 degC | 10.35-25 degC at the consumer, chiller outlet down to 12.28 degC | wrong (QA-226) |
| Heat demand | 111,667.7 MWh, peak 30.0 MW | delivered 110,658.8 MWh, short 2.76 MWh every day (pipe loss) | 0.903 % unmet, near the 1 % limit (QA-225); the answer says peak demand 29.884 MW |
| Cold demand | 23,742.5 MWh, peak 10.0 MW | KPI 23,840.9 MWh (> demand), coverage 23,742.5, lcoc energy 23,758.8 | wrong (QA-226) |
| LCTS | | 49.695 EUR/MWh (best_v1); Results row shows 64.395 (the 50 m3/h what-if) | wrong row (QA-223) |
| Network pipes | not in the case | 1000 m, U 1 W/m2/K, "assumption" (round 1); round 2 asked the user (assumptions document: 100 m, U 0) | round 1 unsourced (QA-225) |
| ESP stage count | not in the case | 100, "plausible", no source (round 2) | unsourced (QA-287) |

## Bugs

| Id | Severity | Area | Title (short) | Status at report |
|---|---|---|---|---|
| QA-169 | major | geomind | Engineers' read_knowledge 16 of 50 refused (bare name, '3 Wells'), outline doubles numbers | verified (round 4: 1 of 48) |
| QA-171 | major | geomind,gemini | One approval card and plant version per missing setpoint (7 extra patches) | open (round 4: 3 extra patches) |
| QA-172 | minor | geomind | Patch card 'Change 0 value(s)' | verified (round 2) |
| QA-223 | major | backend | Results row is the what-if simulate, not the chosen design | reopened (round 4: a what-if stored as its own design still wins) |
| QA-225 | major | gemini,geomind | Heating short 2.76 MWh every day = pipe loss | fixing |
| QA-226 | major | gemini | Cold delivered > demand; supply 10.35 degC passes | fixing |
| QA-229 | major | geomind | 14 min of unrequested review/analysis/uncertainty after the design | open |
| QA-231 | minor | backend | Run usage jumps down and up during a run | open |
| QA-241 | major | backend,frontend | Plant page '3 values missing' on a complete plant (free_document drops backup/control/size) | open |
| QA-246 | major | frontend | One tab gets 429 rate_limited; Plant page fails | verified (round 4: 0 of 525) |
| QA-260 | major | geomind,gemini | patch_plant drops type and size: 2 doublets become 1; size_plant returns 1 for range 2-2 | open |
| QA-230 | blocker | geomind | (evidence added) worded deny blocks build_plant for the run | fixing |
| QA-254 | blocker | gemini | (evidence added) IndexError values.py:70 in patch_plant and size_plant, 17:57 and 18:02 UTC | verified; round 4 no IndexError in 13 calls |
| QA-287 | blocker | geomind,gemini | (evidence added) 31-min ESP / injection pump patch loop | open |

Not filed: agent-browser ref clicks on Approve sometimes did nothing (a DOM click worked, the
element was hit-tested correctly: tool, not app). Cancel run on a waiting card worked (round 2).

## Next

Round 5: a design with
a request for 3 doublets and an approve-all path once QA-230 and QA-287 are fixed.
