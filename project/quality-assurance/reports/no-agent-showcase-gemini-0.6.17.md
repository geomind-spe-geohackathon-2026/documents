# No-agent showcase: gemini 0.6.17 on the hackathon case (2026-11-05)

Written by Manual QA-IV for the hackathon report, on Sahand's request: before the live agent run, the best
result gemini gives by itself and the features that answer the bonus challenge. No LLM was used.
gemini v0.6.17 (a872275d, the version live on geomind.team), run from a clean `git archive` copy on the Dell
(CPU nice 10, 8 processes). Inputs: `gemini/examples/hackathon_2026/` (the organiser files unchanged, plus
the example's case.json and economics.json). Logs of every script are kept with the session notes.

**Read this first:** the example's economics are placeholders without a source (for example heat and cold
revenue 60 EUR/MWh, return temperatures, search ranges, 1 % unmet band; see the example README). The agent
takes these values from the Knowledge base with a source, so its LCTS (72.94 EUR/MWh in run 32a12115) is
not comparable to the numbers here. The ranking and the method are the point, not the absolute LCTS.

## 1. Six plant structures sized, optimised and ranked (`examples/hackathon.py`, 1 min 13 s)

`gm.Study`: every candidate is sized (`prepare: size`), then searched on LCTS (`minimize`, 20 evaluations per
doublet count, seed 0), simulated over 365 daily steps and checked against every requirement of the brief.

| Plant | LCTS EUR/MWh | CO2 kt/yr | Rank LCTS | Rank CO2 | Pareto | Feasible |
|---|---|---|---|---|---|---|
| HeatingFullCoolingPlant | **36.0** | **7.74** | 1 | 1 | yes | yes |
| HeatingHeatPumpCoolingPlant | 38.0 | 12.90 | 2 | 3 | | yes |
| HackathonPlant | 41.3 | 13.05 | 3 | 4 | | yes |
| HeatingCoolingPlant | 41.9 | 10.55 | 4 | 2 | | yes |
| HeatingAbsorptionCoolingPlant | 49.3 | 20.96 | 5 | 5 | | yes |
| HeatingPlant | 27.9 | 7.52 | 6 | 6 | | no: no cooling (cold_delivered) |

Trials: 80 to 240 per plant (735 simulations of a full year in total). The ranking with the brief's rules only
and the ranking with the standard pump-intake limits (at most 18.75 % free gas, at least 5 bar) give the same
table: the intake limits do not bind on the searched designs.

**Best design (HeatingFullCoolingPlant):** 3 doublets, well depth 3,358 m, 168.7 m3/h per doublet, chiller
capacity 8.39 MW; heat 111,744 MWh/yr and cold 23,759 MWh/yr delivered (demand met), annualised cost
4.88 MEUR/yr, CO2 7.74 kt/yr (5.90 kt direct, 1.64 kt from 5,460 MWh of grid electricity, methane 6.7 t),
fuel 24,713 MWh/yr (the produced gas used on site). Verdict: feasible, no violation.

## 2. Sensitivity of the best design (`study_sensitivity.json`, one at a time)

| Parameter | Low | High | LCTS at low | LCTS at high | Swing EUR/MWh |
|---|---|---|---|---|---|
| Geothermal gradient (K/km) | 25 | 35 | 52.8 | 34.5 | **18.3** |
| Discount rate | 0.02 | 0.08 | 29.6 | 43.4 | 13.8 |
| Carbon price (EUR/t) | 30 | 110 | 34.8 | 38.4 | 3.6 |
| Electricity price (EUR/MWh) | 80 | 140 | 35.0 | 37.4 | 2.4 |
| Gas price (EUR/MWh) | 25 | 70 | 35.5 | 37.1 | 1.6 |
| Permeability (mD) | 100 | 400 | 36.9 | 35.5 | 1.4 |

The subsurface (gradient) and finance (discount rate) drive the cost; energy prices matter little because the
plant buys little energy.

## 3. Uncertainty (Monte Carlo draws, `gm.study.sample`)

- Best design, 5 draws (seed 1): LCTS mean 42.1, p5 37.0, p95 51.5 EUR/MWh; CO2 mean 9.85, p5 7.54, p95 13.21 kt.
- `examples/uncertainty.py` (a fixed sample design, 20 draws): LCTS mean 50.2 (p5 40.2, p95 66.5); CO2 mean 16.5 (p5 12.7, p95 18.9) kt.

## 4. Automatic model generation: structure search on a superstructure (`examples/evolve.py`, 20 s)

One plant file holds every candidate at once (heat pump optional; peak boiler with its gas chain on or off;
cooling on or off; absorption, adsorption and compression chiller each on or off): **32 valid structures**.
`gm.study.evolve` (NSGA-II, population 16, 64 simulations, seed 0) searches structure and sizes together on
LCTS and CO2. 7 structures were refused as invalid. Best and only front member: heat pump on, boiler on,
cooling with the compression chiller only: **37.3 EUR/MWh, 10.87 kt CO2, feasible.** The budget is small, so
this is a first look; with a larger budget it should reach the 36.0 of the enumerated search.

## 5. Techno-economics and verification (`examples/costs.py`, `quickstart.py`, `plant.py`)

- Capex per module (wells, pumps, heat pump, chillers, coolers, pipes, flare ...) from cited catalogue rows,
  opex, LCTS and CO2; e.g. one sample design: capex 38.9 MEUR, opex 3.88 MEUR/yr, LCTS 49.0 EUR/MWh,
  CO2 14.5 kt.
- A limit on bought electricity added as a case requirement and checked (5.33 MW against 6 MW: passed).
- A missing price is reported by name (`missing_assumption: economics.capex.heat_pump`), never filled with a default.
- `gm.check` before a run ("Check: ready"), the verdict on every requirement, failed steps grouped by cause.

## How this maps to the brief

| Brief | Shown here by gemini (no agent) | What the agent adds in the live run |
|---|---|---|
| Challenge 2: select and size technologies, realised capacities | 6 structures sized and searched, capacities and energies of the best | Builds the case from the PDF and CSVs, sources every value |
| Bonus: automated optimisation | `minimize` per structure, Pareto front | Chooses the candidates and ranges, runs the study |
| Bonus: uncertainty analysis | sensitivity (6 drivers) and Monte Carlo draws | Sets the ranges with sources, reads the result |
| Bonus: techno-economic assessment | capex, opex, LCTS, LCOH/LCOC, CO2 per module | Cost catalogue from the Knowledge base with sources |
| Bonus: automatic model generation | superstructure, 32 structures, `evolve` | Proposes configurations, writes the plant |
| Bonus: autonomous verification | `gm.check`, requirement verdicts, failure groups | Reviewer agent checks the final result |
| Bonus: multi-agent collaboration | not applicable | The agent team (case, design, analysis leads, engineers, reviewer) |
