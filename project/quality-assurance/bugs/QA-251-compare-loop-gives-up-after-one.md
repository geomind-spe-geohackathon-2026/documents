# QA-251: Compare loop gives up after one simulate per family: both families fail 365 of 365 steps (QA-250), the design lead runs no repair round, answers 'neither is feasible, no ranking' after 19.5 min; optimize on B: 'every trial failed'

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-design-I |
| Found | 2026-11-05 17:58 UTC |
| Versions | backend 1.1.104 at start, 1.1.109 from ~17:38 UTC (geomind 0.4.110 prompt from 17:38:17 UTC, gemini 0.6.17) |
| Where | api.geomind.team; project QA-TEST QA-AI-design-I 2 (3b95e854-f402-4f9b-9179-a6a820e7aac7); chat 85dbe5e6-dfea-4ffb-a7e3-b07487b3898d; run 5d0216a6-4acb-487b-a885-396a5e99366d (17:30:01-17:49:31 UTC) |
| Fixer | hotfix-python-lead |

## Steps

1. Reference case and economics loaded; chat auto-approve on.
2. "Compare a direct-use plant with absorption cooling against a heat pump plant with a compression chiller for this case. Use 1 to 3 doublets, keep every hard limit of the challenge, and tell me which one has the lower LCTS." -> `loop: compare` (comparison_driver).

## Expected

Each family gets the same treatment as a single design: build, size, simulate, and when the run fails, fix by the failure (handbook-design 0.4/0.5, the lead prompt's step 6 "Fix only what check_results or a run reports ... per round") until feasible or the 3-round rule; then rank by LCTS. Reference: HeatingHeatPumpCoolingPlant searched to LCTS 40.34 EUR/MWh (gemini sample README); run 1 of this thread reached 40.62 feasible on the same family.

## Actual

- comparison_driver: plan (design_lead, 17:30:05-17:31:08), family C `family_design_lead` 17:31:19-17:41:47, family B 17:41:47-17:48:41, then finish 17:49:31.
- Each family_design_lead: build, team, 7-8 patch_plant (QA-175/QA-212), size_plant, ONE simulate -> 365/365 failed steps (QA-250), check_results infeasible, (B only) optimize -> `"every trial failed"`, finish. No read of the failures, no repair patch, no second simulate.
- Final answer: "Two families were built, sized and simulated ... and **neither is feasible**. There is therefore no verified design, no LCTS for either family, and no ranking: I recommend none." The answer itself names the causes (ESP flow 0.0837 > 0.0833 m3/s; injection pump discharge below suction), both fixable by one patch each (run 1 fixed the same two in one round: nominal_flow 250 m3/h, injection_pump pressure_setpoint 30 bar).
- 19.5 min, 103 steps, 161 tool calls (8 refused), 3.67 M input tokens, 0.088 USD for no result.

Evidence: `../evidence/QA-251/run-5d0216a6-tool-calls.txt`.

## Cause

Fact: `geomind/agents/project/comparison.py` `after_batch` records a family without an entry as failed and `next_move` goes on; the `family_design_lead` task ends at the first verdict. Guess: the family task text (built in comparison.py) asks for "build, size, simulate, check, record" without the repair round of the single design loop, and `max_rounds=5` counts driver rounds, not repair rounds inside a family.

## Proposed fix

- geomind `agents/project/comparison.py` family task: "when the run fails, fix by the failures (0.5) and simulate again, at most 3 rounds, before you record the family"; or run the single-design DesignLoop per family.
- geomind comparison_driver: when every family is infeasible, start one repair round per family with the failures as its task before answering "no ranking".
- Also: an `optimize` whose every trial failed should not be run on a base design that failed every step (the lead could see it from the simulate just before).

## Fix

## Retest
