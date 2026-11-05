# QA-179: Optimisation request: the 26 s study is wrapped in 11 min: the design lead re-types the whole project plant (build_plant, 30 s output) and after the verified result the analysis lead re-reads the study in 22 steps (6 calculate refusals), then reviewer and explainer redo the same reads

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 17:12 UTC |
| Versions | backend 1.1.103/1.1.104 (geomind 0.4.98), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 1` (4ce816b1-4bd1-48a5-8e77-9414c2b86301); chat fa9cfafb-e39e-4ccd-9dfb-d8427f518c43; run 7a7ace73-e8b5-4291-9252-33fd7240be84 |
| Fixer | |

## Steps

1. Project 1 (reference case + economics, plant version 1 = HackathonPlant), after a costing and a
   sensitivity request.
2. Chat: "Find the design of this plant with the lowest LCTS within the challenge limits (1 to 3
   doublets, 50 to 300 m3/h per doublet): run an optimisation and tell me the best LCTS, capex and the
   number of designs tried."
3. Approve every card (3 cards, each within ~15 s).

## Expected

One `run_study(method=minimize)` over 1/2/3-doublet variants, a check, an answer: about 2-3 min.

## Actual

Accuracy is right: best design 2 doublets, LCTS 41.300 EUR/MWh, capex 30.763 MEUR, opex 3.4136
MEUR/yr, CO2 13.05 kt, exactly the page study `minimize` (lcts, 30 evaluations, seed 0, size first)
on plant version 1 (study be37a85f: 41.300 / 30.763 / 3.414 / 13.05, 10 s). The study itself took
26.3 s. The run took 11 min 6 s, 1.66 M input tokens, 0.0362 USD:

| Agent | Wall | Steps | Input tokens | Refused calls | What it did |
|---|---|---|---|---|---|
| project_lead | 17:01:39-17:12:23 | 6 | 85 k | 0 | plan, then reviewer, analysis_lead, explainer one after the other |
| design_lead | 17:01:50-17:08:03 (6.2 min) | 24 | 891 k | 6 | re-typed the whole project plant as `build_plant` (step 5, 29.9 s LLM output) to get a design reference; 2 handbook sections that do not exist; a class route that cannot take 3 doublets; a free-module 1-doublet build missing every parameter; a JSON-patch form patch_plant refuses; then 2 patches, run_study, simulate, check |
| reviewer | 17:08:22-17:08:43 | 5 | 84 k | 0 | check_results, compute_kpis again |
| analysis_lead | 17:09:19-17:11:19 (2 min) | 22 | 527 k | 8 | re-read the study the design lead had already read: 11 read_stored of the same study result, 6 calculate refusals (unit of a difference; 1 operand), list_studies |
| explainer | 17:11:39-17:11:46 (+37 s answer) | 3 | 72 k | 0 | read_case, read_plant, list_studies, compute_kpis, estimate_costs, read_study again |

After the design lead's verified result at 17:08:03 the user waited 4 min 40 s for answers that add
nothing new to it. The analysis lead's 6 refused `calculate` calls were to give "LCTS -3.802 EUR/MWh"
and "capex -3.873 MEUR" differences. The final answer also says "study setting is 30 evaluations;
gemini's found reports 80 evaluations per design ... not reconciled here".

## Evidence

- `../evidence/QA-179/run-7a7ace73-log.json`, `run-7a7ace73-trace.txt`, `approval-cards.log`.
- design_lead step 5 build_plant (the project plant re-typed), steps 6, 9, 13 refusals; analysis_lead
  steps 2-20.

## Cause

- The design lead has no way to use the project plant version as a design (same root as QA-152), so it
  re-types the plant JSON through the LLM (slow, and a silent copy error would change the design).
- The project lead's plan sends a verified design to reviewer, then analysis_lead, then explainer in
  series, each with the same brief, each re-reading the result and the study.
- `calculate` refusals: the analysis lead passes `lcts.value` (a bare number, dimensionless) where the
  tool wants the quantity `lcts`; the error says only "the result is dimensionless".
- `run_study` reports `found.evaluations` 80 for `evaluations` 30 without saying why (guess: gemini adds
  the sizing / polish trials); the agents cannot explain it.

## Proposed fix

1. QA-152 fix (a `plant_version` / adopt path), so `build_plant` of an existing plant is never needed.
2. Project lead prompt (`prompts/project/lead.md`): after a verified optimisation, run the analysis
   lead and the explainer at the same time (or skip the analysis lead when the task asked only for the
   best design and its numbers), and give each the references, not "read the study".
3. `calculate` error (`tools/calculator.py`): when an operand path ends in `.value`, suggest the path
   without `.value`.
4. `run_study` answer: give `evaluations_requested` and `evaluations_run` with the reason, from gemini.
