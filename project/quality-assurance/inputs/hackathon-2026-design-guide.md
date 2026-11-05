# Design guide: GEMINI hackathon 2026

Guidance for the GEMINI hackathon 2026 case only; a starting point, the agents may depart from it
with a recorded reason.

For the design lead and the reservoir, well, process, integration and energy systems engineers.
Cite as `knowledge/hackathon-2026-design-guide.md`. Your prompts and `read_skill('designing-a-plant')`
still hold: every number in a design comes from the case, a gemini tool, or a value with its
source. The numbers here are such sources (each names its file) and tell you where to start; gemini
decides whether a design passes.

## Key numbers (orientation; gemini computes the real ones)

| Number | Value | From |
|---|---|---|
| Reservoir temperature at 2500 m | 87 °C (12 °C + 30 K/km × 2.5 km) | PDF p. 2 values |
| ... at 3000 m / 3500 m | about 102 °C / 117 °C | same rule; depth may change (PDF p. 2, organisers) |
| Heat of one doublet at 300 m3/h and 40 K | about 14 MW (cp about 4.2 kJ/kg/K, an assumption; the PDF gives none) | PDF caps |
| Brine return at 87 °C and 40 K | 47 °C: the sample's `heat_pump.minimum_source_outlet_temperature` is 47 degC | `plants/HeatingHeatPumpCoolingPlant.json` |
| Heating peak / year | 30.0 MW (28 Jan) / 111.67 GWh; heat demand on all 365 days, lowest 2.673 MW | heating CSV, PDF p. 1 |
| Cooling peak / year | 10.0 MW (19 Jul) / 23.74 GWh; cold demand on 219 days | cooling CSV, PDF p. 1 |
| Heat + cold on one day | at most 30.0 MW | both CSVs |
| Associated gas per doublet at 300 m3/h | 240 Nm3/h gas, 192 Nm3/h CH4, about 1.9 MW of fuel (CH4 lower heating value about 35.8 MJ/Nm3, an assumption) | PDF p. 2 values |

What follows: 87 °C cannot give a 100 °C supply directly. Reach it with a heat pump on the brine,
a peak boiler, or deeper wells (above about 3000 m, minus the exchanger's approach). One doublet
cannot meet the 30 MW peak at the 40 K cap, so the peak needs 2 to 3 doublets, or a heat pump and
a boiler on top. Cooling at 20 °C supply can come from an absorption chiller driven by the brine
(drive at least 80 °C in the sample, `minimum_driving_temperature` 353.15 K) or a compression
chiller.

## Starting configurations (gemini's sample plants)

The six plants of `gemini/examples/hackathon_2026/plants/` are gemini plant classes
(`read_plant(plant_class=...)`); their files give a complete set of design values. Common to all
(class plants): 2 doublets (`size.doublets`, range 1 to 3), `depth` 2500 m (range 2000 to 3500 m),
`d0.nominal_flow` 300 m3/h (range 50 to 300), `d0.well_diameter` 0.244 m, `d0.pump_efficiency`
0.7, `d0.nominal_wellhead_pressure` 10 bar, `d0.drainage_radius` 1000 m, `d0.roughness` 4.5e-05 m,
`d0.esp.pump_type` `unspecified`, `d0.esp.minimum_intake_pressure` 5 bar,
`d0.esp.maximum_gas_fraction` 0.1875, `params.backup` `peak`, `control.dispatch` `least_cost`,
`control.outages` `lowest_demand`, `peak_boiler.capacity` 30 MW (efficiency 0.9),
`injection_pump.nominal_flow` 600 m3/h and `nominal_head` 15.74 bar, heat pumps and chillers
`cop_model` `carnot`, `carnot_fraction` 0.5.

| Class | Heating | Cooling (starting size, range) |
|---|---|---|
| `HeatingHeatPumpCoolingPlant` | heat pump 15 MW (3 to 30) + boiler | compression chiller 10 MW (1 to 10) |
| `HeatingCoolingPlant` | heat pump 15 MW + boiler | absorption 7 MW, adsorption 1 MW, compression 5 MW (each 1 to 10) |
| `HeatingFullCoolingPlant` | doublets + boiler | absorption 7, adsorption 1, compression 5 MW |
| `HeatingAbsorptionCoolingPlant` | doublets + boiler | absorption chiller 10 MW (1 to 10) |
| `HeatingPlant` | doublets + boiler | none: fails `cold_delivered` by structure |
| `HackathonPlant` (free plant) | heat pump 15 MW + boiler 30 MW, desander, inhibitor dosing | one absorption chiller 10 MW |

Searched best designs (size, then minimize LCTS, 20 evaluations, seed 0, with the pump intake
limits; `gemini/tests/e2e/expected/hackathon.txt`, the output of `examples/hackathon.py`):

| Plant | LCTS [EUR/MWh] | CO2 [kt] | Rank (LCTS) | Feasible |
|---|---|---|---|---|
| `HeatingHeatPumpCoolingPlant` | 40.34 | 12.9 | 1 | yes, Pareto |
| `HeatingCoolingPlant` | 42.54 | 10.34 | 2 | yes, Pareto |
| `HackathonPlant` | 44.25 | 13.05 | 3 | yes |
| `HeatingAbsorptionCoolingPlant` | 50.5 | 20.96 | 4 | yes |
| `HeatingFullCoolingPlant` | 55.57 | 22.16 | 5 | yes (1 doublet at 2456 m, README) |
| `HeatingPlant` | 29.79 | 7.827 | 6 | no, `cold_delivered` |

The superstructure search (`examples/evolve.py`, `tests/e2e/expected/evolve.txt`: 32 valid
structures, small budget) finds heat pump + boiler + compression chiller best: 34.58 EUR/MWh,
8.70 kt CO2. Without the intake limits, deep searched designs (3 doublets at 3319 m) reach 35.7 %
free gas at the pump intake (README "Pump intake limits"): keep both limits on every `esp`.

Recommended start: `HeatingHeatPumpCoolingPlant` as family A, `HeatingCoolingPlant` (geothermal
absorption cooling, which the jury scores) as family B.

## Order of work

1. `read_case`, `read_profile` of both services (peaks, energy, overlap).
2. `list_plants`; `read_plant(plant_class=...)` of family A; fill its `issues` from the values
   above (engineers through `fill_parts`, each its own part); `build_plant`. Simulate only when
   `missing` is 0.
3. `size_plant`, then `simulate` a short window around the heat peak (late January) to check
   quickly, then the whole year (no `start`, `end`), `check_results`.
4. Fix what `check_results` names, owner by owner; never loosen a requirement.
5. `run_study(designs=[A, B], method="minimize", objective="lcts", evaluations=20, seed=0,
   prepare=["size"], name=...)`; `simulate` the best for the whole year; record
   `design.reference`, `design.result`, `design.alternatives`, `design.study`.

After every full-year simulation that runs, record it with `update_state` (`design.reference`,
`design.result`): a result only in a note is lost (QA-090, QA-092).

## Failure patterns seen in QA (stop early)

- One failing rule chased for 15 variants (QA-090, 2 h 40 min, 17.7M tokens): after 3 rounds on
  the same failing requirement with no progress, stop. Record the best variant and hand over with
  the passing rules, the failing one by `name`, gemini's reason and its owner.
- A zero-cooling day failing a supply temperature rule `when: always` (QA-091) is a case flaw:
  `case change needed: requirements: <name> holds only while the supply runs`, never a bypass or a
  forced circulation (those broke the mass balance in QA-090).
- Case values (gradient, surface temperature, permeability, thickness, reservoir pressure) never go
  into the plant: `patch_plant` refuses them (QA-082).
- An inlet or outlet is `<module>.<port>`, never a bare name (QA-083). After an `internal` error,
  change the input; never repeat the same call.
- Never ask the user for a pump curve: `esp.pump_type` `unspecified` derives it (design lead prompt).
- Do not web-search a value this guide or the assumptions file gives (QA-087).
