# QA-276: 'Optimise the design' chip: the answer is ready in 4 min, then the run spends 32 more min building an unasked heat-pump family (145 calls, 0.07 USD) that ends infeasible; the reported optimum (49.34) is worse than the stored plant (49.28)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 18:27 UTC |
| Versions | backend 1.1.108-1.1.11x during the run (geomind main 6724bdf at report time) |
| Where | project `QA-TEST QA-E2E-study-I 2` (8eabf827-1f43-4cf8-86a4-39147bea32a0); chat ae934804-eca5-4b3c-99a7-dd60665b5ee9; run 83182f0e-8ee2-4230-a98f-8f0bc905caf3 |
| Fixer | hotfix-python-lead-II |

## Steps

1. New chat, click the chip "Optimise the design" (sends "Optimise the design and simulate the best
   one.").
2. The first card asks build_plant 'start'; Deny with the reason "No, do not rebuild or change the
   plant. Optimise the stored plant version 2 as it is and leave the project plant alone."
3. Approve every later card.

## Expected

The stored plant v2 optimised (no rebuild), the best simulated, a short answer. If the search does
not beat the start, say so and keep the start.

## Actual

- Good: the denial is kept (a second build_plant is refused by the guard "the user denied this tool
  earlier"), no plant version is written; the design lead simulates plant_version 2, runs
  size_plant (adds a 3rd doublet) and optimize (30 evaluations) and finishes at 17:52:45: 4 min.
- Then the run goes on for 32 min (to 18:24:41): project_lead -> design_lead builds family B
  (HeatingHeatPumpCoolingPlant, 'familyB', not asked), energy_systems_engineer x3, patch_plant 25
  values, a 5-day simulate, evaluate_module refused twice (QA-149), patch_plant again, run_study
  ranking: family B is infeasible (cold unmet 2.2 % > 1 %, cooling supply 25 C > 20 C). Two more
  approval cards for the user.
- Accuracy: the answer calls design/best "the optimised design" with LCTS 49.34 EUR/MWh, CAPEX
  24.05 MEUR; the stored plant v2 as it is costs 49.28 EUR/MWh, CAPEX 23.96 MEUR (round 1, same
  case). The optimiser started from the sized 3-doublet design (53.32) and the answer reports "LCTS
  fell from 53.32 to 49.34" while the user's plant was already cheaper; "within 0.1 % of the stored
  plant's baseline" admits it, but the recommended design is the worse one.
- Total: 36 min, 90 steps, 145 tool calls, 2.68 M input tokens, 0.071 USD.

## Evidence

Run log: `../evidence/QA-276/run-83182f0e-log.json` (design_lead finish 17:52:45; family B from
17:53:18; run_study 18:16:41; end 18:24:41).

## Cause

Guess: the design skill asks the lead to try "a materially different family" after the first
optimum; optimize starts from size_plant's design, not from the stored plant, and nothing compares
the optimum with the start.

## Proposed fix

geomind design skill / project lead: an "optimise the design" request ends after the optimisation of
the stored plant; another family only on request (offer it as a next-step chip). optimize should seed
the stored plant as a candidate (or the lead compares best vs the start and keeps the better).

## Fix

- 2026-11-05 18:57 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
- 2026-11-05 19:12 UTC: QA-E2E-study-I: speed fixed (4.7 min); optimum still worse than the stored plant and compared only with the sized start
- 2026-11-05 19:34 UTC: geomind main 0df5771, gemini dev e6284347 (0.6.31); pending deploy
## Retest

## Retest

QA-E2E-study-I, 2026-11-05 19:11 UTC, project QA-TEST QA-E2E-study-I 4, run 5929c329-332d-4128-bfa2-983c9b57814e (chip "Optimise the design", approve all): speed part passes: 4 min 39 s, 28 steps, 52 calls, 0 approval cards, 0.015 USD, no unasked family. Accuracy part still fails: the answer compares the best (LCTS 49.33 EUR/MWh, capex 24.01 MEUR) only with the sized start design/v2_sized (53.32, 30.47 MEUR: "6.46 MEUR less investment") and never with the user's stored plant v2 as it is (LCTS 49.28, capex 23.96 MEUR, round 1), which is cheaper than the "optimised" design. A Study page "Run again" of the same search on plant v6 found 49.268 at 285 m3/h. Reopened for: seed the stored plant as a candidate, and compare best vs the stored plant.
