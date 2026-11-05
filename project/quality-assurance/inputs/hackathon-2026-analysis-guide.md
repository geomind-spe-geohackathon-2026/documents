# Analysis guide: GEMINI hackathon 2026

Guidance for the GEMINI hackathon 2026 case only; a starting point, the agents may depart from it
with a recorded reason.

For the analysis lead and the economist. Cite as `knowledge/hackathon-2026-analysis-guide.md`.
Your prompts and `read_skill('economics')` still hold: every number comes from a gemini tool, and
a share, sum or difference of gemini's values is never yours.

## Metrics (gemini's names, `gemini/gemini/evaluate/`)

| Name | What gemini computes | Unit gemini shows |
|---|---|---|
| `lcoh` | (capex + opex x A) / (heat x A), A the annuity factor over `analysis_period` at `discount_rate`; with cooling, only `accounting.allocation.heat_cost_share` (0.8) of the cost | EUR/MWh |
| `lcoc` | the same for the cold, with the share the heat leaves (0.2) | EUR/MWh |
| `lcts` | annualised cost / (heat + cold): one cost over both products, no share needed. The objective of gemini's sample study | EUR/MWh |
| `co2` | CO2 burnt or released + methane released x `accounting.gwp.CH4` (29.8) + grid electricity x `utilities.electricity.co2_intensity` (300 g/kWh); on-site power offsets the grid first | kt |
| `npv`, capex, opex | `estimate_costs`, capex by module and opex by part as gemini gives them | MEUR, MEUR/yr |

LCTS is the fair single number to rank plants that deliver both heat and cold; give LCOH and LCOC
beside it. The CO2 includes the associated gas: CH4 that is vented counts 29.8 times its mass,
burnt CH4 counts as its CO2, and the brine's own CO2 counts when it is released.

## Which study for what

| Question | Tool | Notes |
|---|---|---|
| Sizes for the case under the backup policy | `size_plant` | before any search; the design lead runs it |
| Best values of one design | `optimize` (objective `lcts`) | at least 5 evaluations per searched continuous leaf |
| Rank two or more configurations | `run_study(method="minimize", objective="lcts", evaluations, seed, prepare=["size"])` | gemini's sample: 20 evaluations, seed 0, `metrics` `co2` too |
| Rank stored designs or results as they are | `run_study(method="run")`, `compare(references, by=["lcts", "co2"])` | `compare` gives `ranks`, `pareto`, `feasible` |
| Uncertainty of the verified design | `sample_uncertainty(design, metrics=["lcts", "co2"], samples, seed, name)` | gemini's sample: 5 draws, seed 1; more draws, more time |
| What drives the cost | `sensitivity(design, metrics=["lcts"], name)` | one value at a time, each at its two ends |

No `evolve_structure` for this case: compare named configurations with `run_study` instead.
Uncertainty and sensitivity run only when the task asks for them.

The case declares six uncertain values (`knowledge/hackathon-2026-assumptions.md`, "Uncertainty
ranges"): electricity price, gas price, CO2 price, discount rate, geothermal gradient,
permeability. A run, `size_plant` and `optimize` use only their values.

## What gemini's sample found (for comparison, not as your result)

From `gemini/tests/e2e/expected/hackathon.txt` (the output of `examples/hackathon.py`):

- Ranking with the pump intake limits: `HeatingHeatPumpCoolingPlant` 40.34 EUR/MWh, 12.9 kt
  (rank 1); `HeatingCoolingPlant` 42.54 EUR/MWh, 10.34 kt (rank 2, lowest CO2); both on the
  Pareto front.
- Sensitivity of LCTS on the best design, effect from low to high end: gradient 25 to 35 K/km
  13.4 EUR/MWh (47.16 to 33.76), electricity 80 to 140 EUR/MWh 8.101, CO2 price 30 to 110 EUR/t
  7.621, gas 25 to 70 EUR/MWh 7.467, discount rate 0.02 to 0.08 7.151, permeability 100 to 400 mD
  2.337.
- 5 draws: LCTS mean 44.56, p5 40.85, p95 49.41 EUR/MWh; CO2 mean 13.83, p5 12.54, p95 15.22 kt.

The ground (gradient) is the largest uncertainty: say so in the analysis. If your numbers differ
much from these on the same economics, check the economics of the case first.

## How to compare configurations

- Compare only results that were simulated for the whole year and checked (`design.result`,
  `design.alternatives`, `design.start_result`). A family not simulated is not compared.
- Report each metric with `compare`'s `ranks` and both values as gemini gives them; name the
  `study/<name>` it relies on and whether it is `current`.
- Name the trade-off: lowest LCTS against lowest CO2, and which uses geothermal heat for cooling
  (absorption chiller), since the jury scores geothermal-driven cooling.
- `improvement: <what>: <why>` lines for the design lead: for example a smaller boiler when gemini
  shows it barely runs, another depth when the gradient dominates.

## Economics inputs

All from `knowledge/hackathon-2026-assumptions.md` (EUR, price year 2015), set by the case lead:
discount rate 0.05, 25 yr, electricity 105.75 EUR/MWh, gas 39.92 EUR/MWh, CO2 57.03 EUR/t, heat and
cold revenue 60 EUR/MWh, heat cost share 0.8, CH4 GWP 29.8, the capex and fixed opex table. No
subsidy and no per-energy O&M map. `estimate_costs` names a missing price by its path: report it
for the case lead, never fill it.
