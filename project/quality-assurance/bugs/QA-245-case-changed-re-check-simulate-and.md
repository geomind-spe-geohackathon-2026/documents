# QA-245: Case changed, re-check: simulate and check done at step 3, then the design lead spends 27 steps (5 min) diffing old vs new results by read_result pairs and read_stored requirements/0..14, hits the 30-step question

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 17:45 UTC |
| Versions | backend 1.1.107 (geomind 0.4.98+, gemini 0.6.17) |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 1 (35a70dbe-5e24-4f51-9c6f-50e06d47fe82); chat 134dae07-2e37-4a3a-ae0b-83b5e812017e; run 194c3879-076e-4e3a-b6bf-8f54da25a7ae; design_lead steps 1-30 (17:39:10-17:44:10 UTC), request-615 |
| Fixer | |

## Steps

As QA-227 (case saved by hand, permeability 200 -> 150 mD; question "Does the plant still meet the requirements, and what does it do to LCOH?"), approve the three cards.

## Expected

Design lead: `simulate` on the new case, `check_results`, record `design.result`, finish with the verdict and the moved KPIs. A comparison of the old and the new result is one call of gemini's `compare` (`tools/gemini/study.py`, both result references, `by: [lcoh, lcts, ...]`). About 1 min.

## Actual

- Steps 1-3 (17:39:10-17:39:17, 7 s): `read_case`, `read_plant`, `simulate` -> `result/186602ec8d13b459`, `check_results`. The real work is done.
- Steps 4-30 (17:39:17-17:44:10, ~5 min): the lead diffs the two results by hand: 46 `read_result` in pairs (`d0.esp`, `d1.esp`, `flare`, `grid`, `production` three times, `heat_pump`, `d0/d1.injector`, `d0/d1.reservoir`, `chiller_cooler`, `waste`, `hx`, the whole results), two refused `read_result(path: d0)`, `read_stored` of the check's `requirements/0` to `requirements/14` one index at a time (steps 21-24), `metrics/lcoh`, `/lcoc`, `/capex`, `/lcts`, `/opex` one at a time (29), two refused `calculate` sums of `loss_out`, one refused `update_state`.
- Step limit reached: the user is asked "design_lead: the run took its 30 steps; continue with 30 more, or stop and answer from what it has?" (17:44:10). Answered `stop`.

## Evidence

- `../evidence/QA-245/194c3879-076e-4e3a-b6bf-8f54da25a7ae.log.json`: `agent: design_lead` steps after 17:39.
- Brief from the project lead (project_lead step 6): "What to hand back: the new result reference; whether the run is feasible ...; each requirement's value against its limit with the worst step, flagging any that now fail or that moved; and the KPIs that the permeability can move (production flow, brine cooling, pump power, heat and cold delivered, electricity bought, boiler heat, gas bought, losses, CO2)."

## Cause

1. The project lead's brief asks the design lead for a before/after diff of ~10 KPIs and every requirement with worst steps: analysis work, which the lead prompt gives to `analysis_lead`.
2. The design lead has no `compare` (it is not in `GEMINI_TOOLS`, `agents/design/lead.py`; only the economist has it) and no `compute_kpis`, so it reads each module of both results.
3. `read_stored` of a list is read index by index (`requirements/0..14`), one call each.

## Proposed fix

- `prompts/project/lead.md`: "After a case change, the design team's brief is: simulate the current design on the case, check it, record `design.result`, hand back the result reference and the verdict. What moved and by how much is the `analysis_lead`'s, with `compare` on the old and the new result."
- geomind `agents/design/lead.py`: add `compare` (and `compute_kpis`) to the design lead's tools, and in its prompt: "to compare two results, one `compare` call; never `read_result` the same path of two results".
- `read_stored` of a list path returns the whole list when it is small (here 15 items), so the agent never walks it by index.

## Fix

## Retest
