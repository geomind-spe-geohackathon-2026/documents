# QA-285: gemini's LCTS optimum for HackathonPlant (41.30 EUR/MWh, heat pump 9.75 MW, 30 evaluations) is not the optimum: the same plant with a 5 MW heat pump simulates to 39.21 EUR/MWh, feasible, inside the plant's own range (3-30 MW)

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | gemini |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 18:32 UTC |
| Versions | backend 1.1.112 (gemini 0.6.19, geomind 0.4.119); the optimum from gemini 0.6.16/0.6.17 (17:13 UTC) |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 6` (d168c5d1-acd4-4795-9442-f2dbe56d0b2d), run 67af2520-0228-47e3-950f-93ef7de7a840; optimum: project `QA-TEST QA-AI-analysis-I 1` page study be37a85f (result 3945569f), agents' study lcts_doublets (run 7a7ace73) |
| Fixer | |

## Steps

1. Page study `minimize` (objective lcts, 30 evaluations, seed 0, prepare size) on plant version 1 =
   `gemini/examples/hackathon_2026/plants/HackathonPlant.json`, reference case + economics: best LCTS 41.300 EUR/MWh,
   capex 30.763 MEUR, heat pump 9.75 MW, 2 doublets x 300 m3/h, 2500 m (the showcase also has 41.3 for this plant).
2. Chat on the same plant and case (project 6): "Which part of the plant costs the most, and would a smaller heat pump
   lower the LCTS? Check it, do not guess." The analysis lead simulates plant version 1 with
   `changes={"heat_pump": {"capacity": ...}}`, nothing else changed.

## Expected

No feasible point in the search space better than the reported optimum, or an optimum within a small tolerance of it.

## Actual

| heat_pump.capacity | LCTS EUR/MWh | capex MEUR | CO2 kt | feasible | result |
|---|---|---|---|---|---|
| 15 MW (stored) | 45.102 | 34.636 | 13.774 | yes | result/9b0db55da13a4a5b |
| 10 MW | 41.407 | 30.947 | 13.033 | yes | result/99747dfcfd03ba4a |
| 9.75 MW (optimum of minimize) | 41.300 | 30.763 | 13.05 | yes | 3945569f (page study) |
| **5 MW** | **39.209** | 27.258 | 13.564 | yes, 0 failed steps, no unmet demand | result/3d90b7c17cd957a4 |
| 3 MW | 41.178 | 25.782 | 15.505 | yes | result/57757ab469941b97 |

So the minimiser's best (41.30) is 2.1 EUR/MWh (5 %) above a feasible point 1-D away in its own variable range
(`params.heat_pump.capacity.range` 3-30 MW in the plant file). The sized start (9.75 MW) is returned as the optimum: the
search seems not to move the heat pump capacity. This matters for the hackathon result (LCTS is the objective) and for
every agent answer that cites "the optimum".

Only the agent's 4 simulations show it (2 min 14 s, 0.0089 USD) - the agent's answer itself is right and well checked.

## Evidence

- `../evidence/QA-285/run-67af2520-log.json`: analysis lead steps 6, 7, 12 (simulate with changes) and its finish.
- Page minimize result 3945569f-7530-434b-9585-9a301783b87f in project `QA-TEST QA-AI-analysis-I 1`.

## Cause

Not known. Guesses: (a) the minimiser's 30 evaluations are spent over the other variables (depth, flow, chiller
capacity, doublet count) and never vary the heat pump capacity far from the sized start; (b) the sizing step fixes the
heat pump capacity and the search keeps it; (c) a 1-D local polish is missing at the end.

## Proposed fix

gemini `gm.study` minimize (prepare size): check which variables the search moves (history of heat_pump.capacity);
add a final coordinate polish of each continuous variable, or start points spread over each range. A test: HackathonPlant
on the hackathon case must find LCTS <= 39.3 EUR/MWh.

## Retest

- 2026-11-05 18:53 UTC, QA-AI-analysis-I, backend 1.1.118 (gemini 0.6.26, geomind 0.4.130): page study `minimize`
  (lcts, 30 evaluations, seed 0, size first) on plant version 1 HackathonPlant in project `QA-TEST QA-AI-analysis-I 1`
  (study "QA-285 retest minimize lcts", result bcf4fef1-04ca-4995-b487-7054f96b4ce1), 13 s: LCTS 32.535 EUR/MWh
  (was 41.300), capex 27.492 MEUR, CO2 10.259 kt, 15 of 15 checks passed; 2 doublets x 237.5 m3/h, depth 2875 m, heat
  pump 3.0 MW (moved from the 9.75 MW start), chiller 10 MW. Below the 39.21 the agent found by hand. Verified.
- 2026-11-05 18:54 UTC: retest QA-AI-analysis-I 18:53 UTC gemini 0.6.26: minimize gives 32.535 EUR/MWh, HP moves to 3 MW
- 2026-11-05 20:17 UTC: QA-E2E-study-II 2026-11-05 20:20 UTC, backend 1.1.125: page minimize lcts, 30 evaluations, seed 0, prepare [size] on plant v1: LCTS 32.53 EUR/MWh (result d88822c1), heat pump 3 MW (its lower bound), 2 x 237.5 m3/h, feasible; better than the 5 MW point 39.21 and the old 41.30
## Fix

- 2026-11-05 18:56 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
