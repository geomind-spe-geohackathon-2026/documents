# QA-211: Design accuracy: one family only, 1 doublet never sized or searched, no optimize; result infeasible with 49 % of heat from the gas boiler and LCTS 44.2 vs 40.3 EUR/MWh of gemini's searched reference; project lead offers to relax the hard limit

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-design-I |
| Found | 2026-11-05 17:30 UTC |
| Versions | backend 1.1.102 at run start, 1.1.104-1.1.106 during the run (geomind 0.4.98, gemini 0.6.16 then 0.6.17) |
| Where | api.geomind.team; project QA-TEST QA-AI-design-I 1 (b9ef5c9a-e030-4357-91ee-b17dabfdeaa6); chat efb95fd0-f997-4530-a314-f93baf64ef5f; run 0df89b7e-69e0-46b3-abe1-231e51d9570a; design_lead steps #1-#59 (16:50-17:25 UTC); project_lead question request-1729 (17:26 UTC) |
| Fixer | hotfix-python-VIII |

## Steps

1. As QA-210: "Design a geothermal heating and cooling plant for this case that meets every hard limit of the challenge, size it, simulate it for the full year and tell me if it is feasible."

## Expected

handbook-design 0.2 / 0.4 (the lead's own chapter): compare at least two materially different families (10.7), size, simulate, check, optimize few leaves including the doublet count (1-3, a design variable of the challenge), compare families in one study, simulate the best. Reference: gemini's searched sample (`gemini/examples/hackathon_2026/README.md` lines 265-271, `study.json`): lowest LCTS among designs that deliver heat and cold is HeatingHeatPumpCoolingPlant at 40.34 EUR/MWh (2 doublets in the stored plant).

## Actual

| | Agents (`design/fixed2`, `result/f12021b231881f34`) | Reference |
|---|---|---|
| Families tried | 1 (B, HeatingHeatPumpCoolingPlant) | 6 plants searched |
| Doublets | 1, never sized or searched (`size_plant` once, no `optimize`, no `run_study`) | 2 in the stored plant; search over 1-3 |
| Feasible | no: heat_delivered 0.0114 > 0.01 | yes |
| LCTS | 44.21 EUR/MWh | 40.34 EUR/MWh |
| Fuel (gas boiler) | 54,206 MWh/yr (49 % of 110,470 MWh heat) | - |
| CO2 | 14.98 kt/yr (11.42 direct) | - |
| CAPEX | 27.55 MEUR (incl. 6 MEUR of the 5 km pipes, QA-210) | - |

Timing: build 16:50:58, team 16:52-17:04 (with a deploy restart, QA-176), 7+3 patch_plant to 17:11:43 (QA-175), first simulate 17:11:53 (21 min after the request), two repair rounds, finish 17:25:36: 35 min, 59 lead steps (30-step limit hit once, user asked to continue), 3.8 M input tokens, 0.107 USD. Tool calls: 213, 34 refused (read_knowledge 15, evaluate_module 11, patch_plant 3, calculate 2, read_result 1, update_state 1).

The project lead's question (17:26 UTC) offers "Accept the design with heat_delivered open (recommended)" or "Change the heat_delivered requirement": both drop a hard limit of the challenge, while a second doublet, a larger heat pump share, or removing the invented main (QA-210) were never tried. The lead reports "Three design changes were already spent on it", i.e. it stopped by the handbook's 3-round rule (0.4) on a cause it had itself introduced.

## Cause

Facts: `prompts/design/lead.md` steps 2-5 say "Choose the family ... build it ONCE" and go straight from simulate to fix; nothing in the prompt makes the lead size the doublet count, optimize, or compare a second family before it finishes; the handbook's "compare at least two families" (0.2) and step 6 "Optimize" (0.4) are not in the prompt's numbered steps. The project lead prompt lets a question offer a requirement change for a case limit.

## Proposed fix

- geomind `prompts/design/lead.md`: after the first feasible-or-not full-year simulate, always (a) `optimize` with `size.doublets` 1-3 and the base/peak split leaves (QA-129 made doublets searchable), (b) compare with a second family by one `run_study` when the case has cooling (A/C/E vs B); finish only with the best feasible design or with the list of what was tried.
- geomind `prompts/project/lead.md` (and the coordinator rules): a requirement of the case that comes from the brief (`heat_delivered`, flow band, brine cooling, doublet count) is never offered as an option to change; the options are design changes.
- geomind `engine` step limit: count the run toward a goal (a feasible result) rather than asking the user to continue at step 30 when nothing was simulated yet (see QA-086).

## Fix

- 2026-11-05 17:39 UTC: geomind 0.4.109, deployed: best family plus a materially different alternative; size doublets and optimize before a verdict
## Retest
