# GEMINI hackathon 2026: judging, deliverables and reference results

What the SPE Europe Energy GeoHackathon 2026 (GEMINI digital twin challenge) asks of the report,
and reference results to check against. Cite as `knowledge/hackathon-2026-brief.md`.

The competition has two files in Knowledge, with no overlap:

| File | Holds | Read by |
|---|---|---|
| `knowledge/hackathon-2026-assumptions.md` | everything the case and the design need: the organisers' rules, the PDF's limits and requirements, the team's assumed values, the economics, how the competition files map to the case | case lead, design team, economist |
| `knowledge/hackathon-2026-brief.md` (this file) | everything the report and its review need: judging criteria, deliverables, how the report answers them, reference results of gemini's sample | explainer, reviewer, project lead, analysis lead |

How to write a report in general is `knowledge/handbook-report.md`; how to cost a plant,
`knowledge/handbook-economics.md`.

Sources: the organisers' kick-off slides (shared by the team on 2026-11-05); the requirements PDF
(`GEMINI_Hackathon_Challenge_Requirements.pdf`, 2026-10-28); the organisers' answers on Discord
#technical-q-and-a (2026-11-04); gemini 0.6.17 runs of its sample case (2026-11-05).

## 1. Judging criteria

| Part | Weight | What is scored |
|---|---|---|
| Challenge 1: agentic AI engineering workflow | 50 % | the workflow analyses the problem, works with the GEMINI digital twin, selects and runs the right models, identifies missing modelling capabilities and integrates extra calculations or tools, compares alternatives, explains the reasoning behind the final configuration |
| Challenge 2: integrated heating and cooling system | 50 % | deep geothermal heat for direct heating and, where possible, for cooling; technologies selected and sized (heat exchangers, heat pumps, sorption or absorption cooling, chillers, storage, auxiliaries); the realised heating and cooling capacities; the designed system; the interaction with the agent (prompts, answers, tokens) |
| Bonus | | multi-agent collaboration, automated optimisation, uncertainty analysis, techno-economic assessment, automatic model generation, autonomous verification |

"Missing models are part of the challenge": a simplified model or an external tool is welcome
when its use is explained (`calculate`, `run_python`, `web_search`, with their sources).
Geothermal-driven cooling is scored.

## 2. Deliverables (hard limits)

| Deliverable | Limit |
|---|---|
| Technical report, or presentation | at most 5 pages, or at most 10 slides |
| Video pitch | at most 5 minutes: solution, key findings, design choices, novelty, main technical or economic results |
| Evidence | the agentic system, with its interactions recorded (prompts, answers, token use); the final configuration and its supporting calculations explained |
| Code | all contributions committed and pushed to GitHub (merging into main not required) |

The report covers the geothermal assessment, the system design and the heating and cooling
capacities, and documents the agent architecture, models and libraries.

## 3. Hard limits of the case

Not repeated here. Every limit of the PDF and every organisers' rule that the case needs, with
its requirement `name`, is in `knowledge/hackathon-2026-assumptions.md` ("Rules from the
organisers", "Competition: Requirements (8)").

## 4. How the report handbook applies

Map each criterion of §1 to a report section (`knowledge/handbook-report.md` §3.2, §16.1):

| Criterion | Report section |
|---|---|
| Problem analysed | problem and inputs: the three competition files, the case, one assumptions table with sources |
| Models selected and run, gaps filled | method and agent team: project lead; case lead and geoscientists; design lead with the process, integration, reservoir, well and energy engineers; reviewer; analysis lead and economist; explainer; gemini as the physics; the model behind the agents; Knowledge |
| Alternatives compared | at least two families simulated over the year and checked, the ranking table with its study key |
| Final configuration explained | decisions: family, depth and number of doublets, return temperatures (a team design choice), backup, cooling technology, gas handling, what the optimisation changed |
| Capacities | each unit against the 30.0 MW heat and 10.0 MW cold peaks (PDF p. 1) |
| Verification | gemini's verdict and each of the 8 requirements by `name` (listed in `knowledge/hackathon-2026-assumptions.md`) |
| Techno-economics, uncertainty | costs on the economics of `knowledge/hackathon-2026-assumptions.md` (EUR at 2015 prices); team placeholders (revenue 60 EUR/MWh each, most capex factors) named, so NPV and payback read as indicative |
| Agent interaction | prompts, answers, questions to the user, tokens and cost per agent |

## 5. Reference results: gemini's sample case

gemini ships a sample of this case (`examples/hackathon_2026`: `case.json`, `economics.json`,
six stored plants). Its economics are close to, not the same as, the assumptions document, so a
team run gives its own numbers. Use these only to check orders of magnitude; if the team's costs
differ much on similar economics, check the case's economics first.

gemini 0.6.17 (commit a872275d), stored designs as given, no search; MEUR, EUR/MWh, kt CO2e over
the 365-day run; carbon priced on the plant's own CO2 and methane only:

| Plant | Feasible | Capex | Opex/yr | LCTS | LCOH | LCOC | CO2 | Grid el. (MWh) | Gas bought (MWh) | NPV | Payback (yr) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HeatingHeatPumpCoolingPlant | yes | 33.02 | 3.39 | 42.34 | 41.07 | 48.29 | 12.40 | 26 295 | 35 | 33.73 | 6.97 |
| HackathonPlant | yes | 34.64 | 3.65 | 45.10 | 43.75 | 51.45 | 13.77 | 26 728 | 0 | 28.45 | 7.74 |
| HeatingAbsorptionCoolingPlant | yes | 23.96 | 4.98 | 49.28 | 47.81 | 56.21 | 20.96 | 9 134 | 65 190 | 20.47 | 7.60 |
| HeatingCoolingPlant | yes | 38.92 | 3.88 | 49.00 | 47.54 | 55.90 | 14.49 | 29 099 | 0 | 21.00 | 9.15 |
| HeatingFullCoolingPlant | yes | 27.86 | 5.05 | 51.82 | 50.27 | 59.11 | 20.92 | 9 174 | 64 908 | 15.61 | 9.03 |
| HeatingPlant | no: no cold | 16.86 | 4.00 | 46.48 | 46.48 | none | 16.89 | 8 576 | 51 221 | 21.29 | 6.23 |

Notes:

- HeatingHeatPumpCoolingPlant (two doublets at 2500 m, 15 MW heat pump, 30 MW peak gas boiler,
  10 MW compression chiller): opex 3.394 MEUR/yr = fixed 0.352 + electricity 2.783 + fuel 0.001
  + carbon 0.258; electricity is 82 % of the opex. Its own CO2e 4.52 kt/yr carries the carbon
  price; the grid's 7.89 kt does not. It has the lowest LCTS and CO2 and the highest NPV of the
  feasible plants.
- HeatingPlant's report shows `passed` true but its verdict is infeasible (`cold_delivered`):
  feasibility is the verdict.
- Before gemini 0.6.16 grid CO2 was priced too: the same plant then showed LCTS 45.66 EUR/MWh,
  opex 3.84 MEUR/yr. Figures in older notes (and the sample's search result of 40.34 EUR/MWh in
  gemini's README) predate that change.
- Economic levers of the leading plant over the sample's uncertainty ranges (design held fixed,
  derived): electricity 80 to 140 EUR/MWh moves LCTS 37.34 to 48.99; discount rate 0.02 to 0.08,
  37.53 to 47.88; carbon 30 to 110 EUR/t, 41.44 to 44.11; gas almost nothing.
