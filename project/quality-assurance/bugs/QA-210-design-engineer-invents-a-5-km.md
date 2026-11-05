# QA-210: Design engineer invents a 5 km heating and cooling main (source 'assumption', no case or Knowledge value): 4.3 GWh/yr pipe loss makes heat_delivered fail (1.14 % unmet), 3 fix rounds go to the pipe

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind,data |
| Reporter | QA-AI-design-I |
| Found | 2026-11-05 17:30 UTC |
| Versions | backend 1.1.102 at run start, 1.1.104-1.1.106 during the run (geomind 0.4.98, gemini 0.6.16 then 0.6.17) |
| Where | api.geomind.team; project QA-TEST QA-AI-design-I 1 (b9ef5c9a-e030-4357-91ee-b17dabfdeaa6); chat efb95fd0-f997-4530-a314-f93baf64ef5f; run 0df89b7e-69e0-46b3-abe1-231e51d9570a; energy_systems_engineer finish 16:56:50 and 17:01:14 UTC; design_lead #41-#58; project_lead question 17:26 UTC |
| Fixer | hotfix-python-VIII |

## Steps

1. Reference case and economics of `gemini/examples/hackathon_2026` loaded; chat asks for a plant that meets every hard limit.
2. The lead builds HeatingHeatPumpCoolingPlant; `heating_supply_pipe.length` and the other pipe values are among the 111 missing values; Energy systems engineer I gets them in its brief.

## Expected

The challenge and the case give no network: the plant is at the consumer (gemini's own `plants/HeatingHeatPumpCoolingPlant.json`: pipes 100 m, U 0 W/m2/K, the value the sample searched to LCTS 40.34 EUR/MWh). A value no file gives comes from Knowledge or a connector and the user approves it with its source (AGENTS.md: "No default values"); a missing site value is a question to the user or a `case_changes` entry, not an invented number.

## Actual

- Energy systems engineer I (both passes, 16:56:50 and 17:01:14): `params.heating_supply_pipe.length` = 5000 m, source `assumption`, "The case gives no network length; 5 km is the assumed route ... To be replaced by the project's network length." Same for return and cooling pipes, U 1 W/m2/K, d 0.35 m.
- The lead patches it in without asking (the approval card said "Change 0 value(s)", QA-174, so the user could not see it).
- Full-year result `result/d36921e2af8344a1`: heating supply pipe loss 4,310 MWh/yr; heating supply 94.4 degC < 100 degC on low-flow days.
- Three fix rounds on the pipe (17:15-17:24 UTC, one fill_parts of 194 s, 8 refused evaluate_module on Pipe): supply margin 2->3 K, diameter 0.35->0.5 m, U 1->0.2 W/m2/K. Final `design/fixed2`: heat_delivered unmet 0.0114 > 0.01 (1,273 MWh/yr of 111,668, a constant ~0.145 MW = the main's loss).
- The project lead then asks the user to accept or to change the requirement (QA-211); the cause, an invented 5 km main, is named but never removed.

Speed: ~11 min and ~1 M input tokens of the run went to a pipe the challenge does not have.

## After the user's answer (17:26-17:39 UTC)

The tester answered the question in text: "Do not change heat_delivered: it is a hard limit ... The 5 km heating main is not in the case or the challenge; where does it come from? Fix the design so it meets every limit (you may use 1 to 3 doublets) ...". The design lead then removed the main and the 3 K margins in ONE patch (`design/fixed3`, 17:28:23) and the full-year result `result/e7301855ea3b38df` is feasible (0 reasons): LCTS 40.62 EUR/MWh (reference 40.34), LCOH 39.41, LCOC 46.34, CAPEX 22.55 MEUR, CO2 14.81 kt/yr, 43 % of heat from the gas boiler, still 1 doublet at 250 m3/h, no optimize. The fix took the agents 3 min once a person named the cause. The project lead then added review, economics and a 200-draw uncertainty sample nobody asked for (17:31-17:39, 8 min). Run total: 48.5 min, 206 steps, 327 tool calls (43 refused), 6.0 M input tokens, 0.18 USD.

## Cause

Facts: `prompts/design/energy.md` and the brief give the pipe paths to the engineer with no rule for a network the case does not describe; `hackathon-2026-assumptions.md` (Knowledge) and the case hold no network length; the engineer prompt allows `source: assumption` for any value.

## Proposed fix

- geomind `prompts/design/energy.md` (and `proposal.py` schema note): a value that belongs to the site or the network (length, elevation, route) is never an assumption: return it in `case_changes`/`couplings` as a question for the lead; for "no network in the case" use the plant-at-consumer convention (short pipe, the reference plant's values) and say so.
- geomind `prompts/design/lead.md` step 4: an engineer `assumption` that changes a delivered requirement (pipe length, U) goes to the user in one ask_user before the patch.
- Knowledge `hackathon-2026-assumptions.md` (data): state the network convention for the competition case (plant at the consumer; pipe 100 m, U 0, as gemini's sample), with its source.
- gemini sample: none needed.

## Fix

- 2026-11-05 17:39 UTC: geomind 0.4.109, deployed: pipe/network length never invented; case change needed
## Retest
