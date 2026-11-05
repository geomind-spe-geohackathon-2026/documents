# QA-258: Changing two prices and asking the new LCTS takes 15 min, 2.7 M tokens and 0.060 USD: the economist costs the old result 4 times (35 steps, 29 read_stored) before anyone re-simulates, then design lead, analysis lead, explainer and a bookkeeping design lead run in series

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 18:03 UTC |
| Versions | backend 1.1.106-1.1.108 (geomind 0.4.107/0.4.108), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 5` (ed21ea3b-4489-498e-9f76-8f56eb15a39c), run ce5d9ffc-9717-4de4-92d9-bf971c20a0a9; also project `QA-TEST QA-AI-analysis-I 3` (cdb636b7-f6ae-4395-b8c0-ad19bc5cacd4), run 10fe31e7-bb12-43a3-ab5d-7a58e21c8e95 |
| Fixer | hotfix-python-lead |

## Steps

1. A project with a costed plant (case with economics, plant version 1, one simulate and estimate_costs done).
2. Chat: "Change two economics values to my own: discount rate 6 % and carbon price 80 EUR/t. Then give the new
   LCTS and NPV next to the old ones." (Project 3: "Set the electricity price to 120 EUR/MWh and the heat revenue to
   75 EUR/MWh (my own values), then give the new capex, LCOH, LCTS and NPV of the stored plant next to the old ones.")

## Expected

`set_case` (one card), then `simulate` on the new case and one `estimate_costs`, an answer: under 2 min. Gemini does it in
1 s (page `run` study after the change: LCTS 47.937, 0.4 s).

## Actual

The answer is right (LCTS 45.102 -> 47.937 EUR/MWh, NPV 28.453 -> 20.895 MEUR, LCOH 46.504, LCOC 54.68, opex 3.786
MEUR/yr, all equal to the page study on case version 4). But run ce5d9ffc took 15 min 0 s (17:47:12-18:02:15),
2.74 M input tokens, 0.0601 USD:

| Agent | Wall (UTC) | Steps | Input tokens | Calls | What it did |
|---|---|---|---|---|---|
| project_lead | 17:47:14-18:02:15 | 20 | 421 k | 23 | set_case, accept_case, then analysis_lead -> design_lead -> analysis_lead -> explainer in series, 3 `finish`, then a 2nd design_lead "to fix a bookkeeping mismatch in the problem state" |
| analysis_lead (1st) | 17:48:04-17:56:41 | ~10 | | | briefs the economist to cost the plant on the new case without a new simulation |
| economist | 17:48:13-17:58:20 | 35 | 1 051 k | 53 | `estimate_costs` on the OLD result 35e52d0f four times (17:48:13, 17:48:34, 17:50:12, 17:53:46), 29 `read_stored`, 7 `update_state`, then once on the new result (17:57:42) |
| design_lead | 17:56:47-18:02:07 | 20 | 645 k | 29 | only to `simulate` the same plant on the new case (6 refused calls), later again for state bookkeeping |
| explainer | 17:59:10-17:59:23 | 4 | 125 k | 14 | re-reads case, plant, studies, costs, 5 Knowledge reads |

Project 3 (run 10fe31e7, electricity 120, heat revenue 75): routed case_lead -> design_lead -> analysis_lead -> economist;
the design lead (no estimate_costs) spent 7 min (17:30:21-17:37:43) trying to get NPV by hand: 5 refused `calculate`, 5
refused `run_python`, 2 refused `run_study`, 6 refused read_result/read_stored of `npv`; the run ended after 37 min 8 s
(17:28:46-18:05:54), 3.98 M input tokens, 0.1143 USD. Its numbers are right too (LCOH 46.481, LCTS 47.914 EUR/MWh,
opex 4.035 MEUR/yr, equal to a page `run` study on that case version 4).

## Evidence

- `../evidence/QA-258/run-ce5d9ffc-log.json`, `../evidence/QA-258/run-10fe31e7-log.json`.

## Cause

- The coordinator routes a price change + cost question to the project loop (`loop: project`); the project lead's plan
  treats it as a design round (case -> design -> analysis -> explainer) and runs the stages in series.
- `estimate_costs` on a stored result uses the economics of the result's run or of the current case? The economist
  called it 4 times on the old result, apparently unsure whether the new prices were applied, and re-read its outputs
  (29 `read_stored`). Guess: the tool answer does not say which economics (case version / changed keys) it used.
- The design lead is asked for NPV, which only `estimate_costs` gives, and it has no such tool.

## Proposed fix

1. Coordinator prompt (`prompts/project/coordinator.md`): "a change of case values followed by a question about costs
   or results" -> `loop: tool`, agent `analysis_lead` (it has `set_case`, `simulate` and the economist).
2. Project lead prompt: when only economics changed, the plant need not be re-designed: `simulate` the stored version
   and one economist call; no design_lead, no explainer when the analysis lead's answer already answers the user.
3. `estimate_costs`: state in its answer the case version / economics digest it used and whether the result's run used
   the same case; if the case changed since the run, say "simulate again" (or re-cost on the current case itself).
4. Never call design_lead for state bookkeeping after the final answer.
