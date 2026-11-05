# Assumptions for the GEMINI hackathon case (2026)

Guidance for the GEMINI hackathon 2026 case only; a starting point, the agents may depart from it
with a recorded reason.

This file lives in the global Knowledge of geomind.team (never in a project's files). It holds
every value the case and the economics need that the three competition files
(`GEMINI_Heating_Demand_Daily_2027.csv`, `GEMINI_Cooling_Demand_Daily_2027.csv`,
`GEMINI_Hackathon_Challenge_Requirements.pdf`) do not give. Cite it as
`knowledge/hackathon-2026-assumptions.md`. The case lead puts these values in its ONE
confirmation question (case values) and its ONE `ask_economics` call (economics), each with this
file as the source; after the user approves them they are never asked again. A key this file marks "Not set, not
needed" stays open: never search for it and never ask the user for it. The method is
`knowledge/handbook-case.md`; how each competition file and value goes into the case is the last
section here, "How the competition files map to the case".

Each value says where it comes from:
- **Organisers**: answers of the organisers on Discord #technical-q-and-a, 2026-11-04.
- **Team**: the team's assumption (a placeholder with no verified source), taken from gemini's sample
  case (`gemini/examples/hackathon_2026/case.json` and `economics.json`).
- **Cited**: from gemini's sample case, which cites the source named in the row (details in
  `gemini/examples/hackathon_2026/README.md`); converted to EUR of 2015 with the euro-area HICP.

## Rules from the organisers (beyond the requirements PDF)

| Item | Value | Source |
|---|---|---|
| Return temperatures | A design choice of the team, within the constraints | Organisers |
| Grid electricity CO2 intensity | 0.3 kg/kWh (300 g/kWh) | Organisers |
| 330 days | The availability of a geothermal doublet; the whole system meets the demand on all 365 days | Organisers |
| Well depth | May change; use hydrostatic pressure and the 30 K/km gradient for another depth | Organisers (also in the PDF) |
| Associated gas | CO2 + CH4; several handling options are allowed (flare, boiler, CHP, ...) | Organisers |

## Case values

| Item | Value | Source |
|---|---|---|
| Simulation period | 2027-01-01 to 2028-01-01, daily steps | Team (the demand files are 2027, daily) |
| Heating network return temperature | 60 degC | Team (design choice) |
| Heating network return pressure | 6 bar | Team |
| Cooling network return temperature | 25 degC | Team (design choice) |
| Cooling network return pressure | 4 bar | Team |
| Cooling dew point margin | 1 K | Team |
| Indoor temperature / relative humidity (cooling) | 26 degC / 50 % | Team |
| Ambient air | 10 degC, 101325 Pa | Team |
| Outside air relative humidity (`site.air.relative_humidity`) | Not set, not needed: no module of this case reads it (gemini 0.6.17; a wet cooler uses the wet-bulb temperature instead). Do not ask for it | Team (the reference `case.json` leaves it open) |
| Sand in the brine | 20 mg/l | Team |
| Grid electricity CO2 intensity (`utilities.electricity.co2_intensity`) | 300 g/kWh | Organisers |
| Bought natural gas composition (mole fraction) | CH4 0.8249507401227822, C2H6 0.039549858193534584, C3H8 0.012748086337494389, CO2 0.011912342910726407, N2 0.11083897243546233 (sum 1, exact values of gemini's sample; do not round) | Team |
| Bought gas heating value (`utilities.gas.heating_value`) | Not set, not needed: gemini computes the heating value from the composition above. Do not ask for it | Team (the reference `case.json` leaves it open) |
| Heat pump / compression chiller efficiency | 50 % of the Carnot COP | Team (Frutschi, ABB Review 5/1996, pp. 33-34) |

## Requirements: tolerances the PDF does not give

| Requirement | Rule | Source |
|---|---|---|
| Heat delivered | Unmet share of the yearly heat demand at most 1 %, over all 365 days | Organisers (365 days), Team (1 %) |
| Cold delivered | Unmet share of the yearly cold demand at most 1 %, over all 365 days | Organisers (365 days), Team (1 %) |
| Supply temperatures 100 degC / 20 degC | Hold while that supply is running (a day with zero cooling demand is no violation) | Team |
| Equal production and injection volume | Reinjection ratio 0.99999 to 1.00001 while running | Team |
| Production flow 50-300 m3/h, brine cooling <= 40 K | Per doublet, in every step in which the doublet runs | PDF |
| Pump efficiency | 0.70 | PDF |
| Pump intake (only if the design checks it) | Free gas at most 18.75 % of the volume; intake pressure at least 5 bar | Team |
| Well depth search range | 2000 to 3500 m | Team |

## Economics

Currency EUR, price year 2015 (`currency`, `price_year`). Keys under `economics.` as in gemini's
`examples/hackathon_2026/economics.json`. The sample sets no `opex.per_energy` map and no
`revenue.subsidy`.

| Item | Value | Source |
|---|---|---|
| Discount rate (`discount_rate`) | 0.05 | Team |
| Analysis period (`analysis_period`) | 25 yr | Team (DEA sheets give 25 yr technical lifetime for heat pump and boiler) |
| Electricity price (`energy.electricity`) | 105.75 EUR/MWh | Cited: Eurostat nrg_pc_205, EU non-household, band IE, excl. VAT, 2025 |
| Natural gas price (`energy.gas`) | 39.92 EUR/MWh | Cited: Eurostat nrg_pc_203, EU non-household, band I4, excl. VAT, 2025 |
| CO2 price (`carbon.price`) | 57.03 EUR/t | Cited: Instrat, EU ETS 2025 average allowance price (8 Jan 2026) |
| Heat revenue / cold revenue (`revenue.heat`, `revenue.cold`) | 60 EUR/MWh each | Team |
| Cost share of heat (`accounting.allocation.heat_cost_share`) | 0.8 | Team |
| CH4 global warming potential (`accounting.gwp.CH4`) | 29.8 | Cited: IPCC AR6 WG1 table 7.15, GWP100, fossil methane |
| Chemicals / waste disposal (`opex.variable.chemical`, `opex.variable.waste_disposal`) | 3 EUR/kg / 0.2 EUR/kg | Team |

Capital cost (`capex.<kind>`) and fixed operating cost (`opex.fixed.<kind>`, % of capital cost per year). Source: Cited = Danish Energy
Agency, Technology Data for Generation of Electricity and District Heating, version 0019 (Aug 2026);
every other row is Team.

| Equipment | Capex | Fixed opex | Source |
|---|---|---|---|
| Drilling | 1239.13 EUR/m | 1 %/yr | Team (SDE+ 2013 reference case, Mijnlieff et al. 2013, not re-verified) |
| Heat pump | 0.738 EUR/W | 0.224 %/yr | Cited: DEA sheet 40 |
| Gas boiler | 0.0607 EUR/W | 3.25 %/yr | Cited: DEA sheet 44 |
| CHP | 0.962 EUR/W | 1.026 %/yr | Cited: DEA sheet 06 |
| Degasser | 1,000,000 EUR | 2 %/yr | Team |
| Compression chiller | 0.3 EUR/W | 2 %/yr | Team |
| Absorption chiller | 0.3 EUR/W | 2 %/yr | Team |
| Adsorption chiller | 0.3 EUR/W | 2 %/yr | Team |
| Production pump / injection pump | 0.5 EUR/W each | 2 %/yr | Team |
| Heat exchanger | 0.5 EUR/(W/K) | 1 %/yr | Team |
| Flare | 100,000 EUR | 2 %/yr | Team |
| Gas make-up | 50,000 EUR | 2 %/yr | Team |
| Cooler | 0.1 EUR/W | 2 %/yr | Team |
| Pipe | 500 EUR/m | 0.5 %/yr | Team |

## How the competition files map to the case

The method is general and lives in `knowledge/handbook-case.md` (cited by section below); this
section applies it to the competition only. Reference shape: `gemini/examples/hackathon_2026/case.json` and
`economics.json`. Values the competition files lack: the tables above.

### Competition: Inputs

| File | Holds |
|---|---|
| `GEMINI_Heating_Demand_Daily_2027.csv` | `date`, `heating_demand_MWth`: 365 daily values, 2027-01-01 to 2027-12-31 |
| `GEMINI_Cooling_Demand_Daily_2027.csv` | `date`, `cooling_demand_MWcool`: 365 daily values, same days |
| `GEMINI_Hackathon_Challenge_Requirements.pdf` | 2 pages, 28 October 2026: reservoir, brine and gas, constraints, supply temperatures |

The time column is `date` (named in `columns`), and its dates have no offset: each series needs
a `time_zone`, which no competition file gives. Propose it in the one question as an assumption
(QA-140 was refused without it). gemini's sample avoids this with UTC timestamps
(`2027-01-01T00:00:00Z`).

### Competition: Values for checking (PDF p. 1)

Heating peak 30.0 MWth on 28 January, 111.67 GWhth/year; cooling peak 10.0 MWcool on 19 July,
23.74 GWhcool/year. Checks only; the case takes the CSV series.

### Competition: Values from the files

| As written | Case path and value | Source |
|---|---|---|
| daily heating demand | `demand.heating.power`: heating CSV, column `heating_demand_MWth`, `MW` | CSV |
| daily cooling demand | `demand.cooling.power`: cooling CSV, column `cooling_demand_MWcool`, `MW` | CSV |
| time axis | `time.start` 2027-01-01, `time.end` 2028-01-01 (excluded), `time.step` 1 d | CSV `span` |
| heating supply 100 °C, fixed | `demand.heating.supply_temperature` 100 degC | PDF p. 2 |
| cooling supply 20 °C, fixed | `demand.cooling.supply_temperature` 20 degC | PDF p. 2 |
| reservoir midpoint 2,500 m TVD | `site.reservoir.reference_depth` 2500 m | PDF p. 2 |
| gross thickness 100 m | `site.reservoir.thickness` 100 m | PDF p. 2 |
| gradient 30 °C/km | `site.ground.gradient` 30 °C/km | PDF p. 2 |
| surface temperature 12 °C | `site.ground.surface_temperature` 12 degC | PDF p. 2 |
| reservoir pressure 250 bar(g) | `site.reservoir.pressure` 250 barg | PDF p. 2 |
| permeability 200 mD | `site.reservoir.permeability` 200 mD | PDF p. 2 |
| brine density 1,030 kg/m³ | `site.fluid.density` 1030 kg/m3 | PDF p. 2 |
| viscosity 0.40 mPa·s | `site.fluid.viscosity` 0.4 mPa.s | PDF p. 2 |
| gas-liquid ratio 0.8 Nm³/m³ | `site.fluid.gas_liquid_ratio` 0.8 Nm3/m3 | PDF p. 2 |
| 80 mol% CH₄, 20 mol% CO₂ | `site.fluid.dissolved_gas` CH4 0.8, CO2 0.2 (produced gas) | PDF p. 2 |

Not set: the reservoir temperature (gemini derives it); "for a different well depth, use
hydrostatic pressure and the gradient" is a reading instruction.

### Competition: values from this document

All in the ONE confirmation question, source `knowledge/hackathon-2026-assumptions.md` (this document):

| Path | Value | Origin in that document |
|---|---|---|
| `demand.heating.return_temperature` | 60 degC | team design choice (`knowledge/handbook-case.md` §7.3) |
| `demand.heating.return_pressure` | 6 bar | team |
| `demand.cooling.return_temperature` | 25 degC | team design choice |
| `demand.cooling.return_pressure` | 4 bar | team |
| `demand.cooling.dew_point_margin` | 1 K | team |
| `demand.cooling.indoor_temperature` | 26 degC | team |
| `demand.cooling.indoor_relative_humidity` | 50 % (0.5) | team |
| `site.air.temperature`, `site.air.pressure` | 10 degC, 101325 Pa (constant) | team |
| `site.fluid.sand_concentration` | 20 mg/l | team |
| `utilities.electricity.co2_intensity` | 300 g/kWh | organisers (QA-095) |
| `utilities.gas.composition` | CH4, C2H6, C3H8, CO2, N2 with every digit of the document | team (bought gas) |
| `site.air.relative_humidity`, `utilities.gas.heating_value` | not set, not needed: leave open, never search or ask (QA-161) | team |

### Competition: Requirements (8)

| `name` | Rule | From |
|---|---|---|
| `production_flow_range` | `doublet`, `production_flow`, `each`, `running`, min 50, max 300, `m3/h` | PDF p. 2; one rule (QA-080) |
| `brine_cooling_limit` | `doublet`, `brine_cooling`, `each`, `running`, max 40, `K` | PDF p. 2 |
| `running_time_limit` | `doublet`, `production_flow`, `duration`, `running`, max 330, `d` | PDF p. 2 |
| `pump_efficiency` | `doublet`, `pump_efficiency`, min 0.7, max 0.7 (no unit, over, when) | PDF p. 2 (70 %) |
| `full_reinjection` | `doublet`, `reinjection_ratio`, `each`, `running`, min 0.99999, max 1.00001 | PDF p. 2; band from the assumptions document (`knowledge/handbook-case.md` §6.7) |
| `doublet_count` | `doublet`, `count`, min 1, max 3 (no over, when, unit) | PDF p. 2 |
| `heat_delivered` | `heating_supply`, `unmet_share`, max 0.01 | organisers (365 days); 1 % from the assumptions document |
| `cold_delivered` | `cooling_supply`, `unmet_share`, max 0.01 | as above |

The supply temperatures are case values judged through `heat_delivered` and `cold_delivered`; a
temperature requirement, if written, is `when: running` (QA-091). The 330 days limit each doublet
only: the plant meets the demand on all 365 days. Pump intake limits (free gas at most 18.75 %,
intake pressure at least 5 bar) are in the assumptions document "only if the design checks it".

### Competition: Design freedoms

Never asked as missing case values:

- well depth (search range 2000 to 3500 m, assumptions document);
- number of doublets (1 to 3, bounded by `doublet_count`);
- return temperatures: 60 and 25 degC as team design choices; another value comes as
  `case change needed` (`knowledge/handbook-case.md` §7.4);
- backup policy, number and kind of units, associated gas handling (flare, boiler, CHP).

### Competition: Economics

One `ask_economics` question: each key the assumptions document gives as
`{key, value, unit, source}` with source `knowledge/hackathon-2026-assumptions.md`, so results
compare with gemini's sample. Every `opex.per_energy.*` and `revenue.subsidy.*` key is `open`:
there is no subsidy, and no source prices the chillers per MWh. Method:
`knowledge/handbook-economics.md`.

### Competition: Done when

- 8 requirements as above; no `when: always`.
- No reservoir temperature, depth or doublet count in the case.
- Both series with a confirmed `time_zone`.
- Assumption values confirmed in the one question; `plants_need` empty.
- Economics set (EUR, price year 2015).
- Only the three competition files are project files; handbooks and the assumptions document
  stay in global Knowledge.

## Uncertainty ranges (studies only)

| Value | Range |
|---|---|
| Electricity price | uniform 80 to 140 EUR/MWh |
| Natural gas price | triangular 25 to 70 EUR/MWh, mode 39.92 |
| CO2 price | triangular 30 to 110 EUR/t, mode 57.03 |
| Discount rate | normal, std 1 %, 2 to 8 % |
| Geothermal gradient | normal, std 2 K/km, 25 to 35 K/km |
| Permeability | triangular 100 to 400 mD, mode 200 |

## Plant design values (design team)

Values for the plant paths gemini asks for (`knowledge/handbook-design.md` section 0.7 says what
each means and how to choose it). They are the values of gemini's hackathon sample plants
(`gemini/examples/hackathon_2026/README.md`, "Values the plants state that a module no longer
defaults", and `plants/*.json`). Cited rows carry the source named; Team rows are assumptions of
the sample: record them as assumptions (`confirmed: false`) with this file as the source. `dN` is
each doublet. These are values only, never a plant template (IMP-023).

| Path | Value | Source |
|---|---|---|
| `dN.well_diameter` | 0.244 m | Team |
| `dN.drainage_radius` | 1000 m | Team (lower end of 1 to 2 km Dutch doublet spacing, Willems 2016) |
| `dN.roughness`, pipe `roughness` | 4.5e-5 m | Cited: new commercial steel, Moody (1944) |
| `dN.pump_efficiency`, `injection_pump.efficiency` | 0.7 | PDF |
| `dN.nominal_wellhead_pressure` | 10 bar | Team |
| `dN.reservoir.skin`, `dN.sink.skin` | 0 | Team |
| `dN.reservoir.decline_threshold`, `dN.sink.decline_threshold`, `heat_exchanger.fouling_threshold` | 0.15 | Team (alarm threshold) |
| `dN.well/riser/injector.friction_correlation` / `two_phase_friction_correlation` | `darcy_weisbach` / `BeggsBrill` | Team (model choice) |
| `dN.well/riser/injector.heat_transfer_coefficient` | 10 W/m2/K | Team (original GEMINI well model) |
| `dN.esp.pump_type` | `unspecified` (no curves) | Team |
| `dN.esp.minimum_intake_pressure` | 5 bar | Team (no verified source) |
| `dN.esp.maximum_gas_fraction` | 0.1875 | Cited: Baker Hughes, Ace Plus gas handler pumps (standard stages one fourth of 75 %) |
| `dN.esp.motor_efficiency` | 1.0 | Team |
| `degasser.separation_efficiency` / `nominal_pressure_drop` | 1.0 / 14900 Pa | Team |
| `filters.<f>.nominal_pressure_drop` / `clogging_pressure_drop` | 1600 Pa / 50000 Pa | Team |
| `desander.separation_efficiency` / `nominal_pressure_drop` | 0.9 / 20000 Pa | Team |
| `dosing.dose` / `product_concentration` | 10 ppm / 0.3 | Team |
| `flare.combustion_efficiency` | 0.98 | Cited: US EPA AP-42 13.5 |
| `heat_exchanger.thermal_conductance` / `arrangement` | 1.5e6 W/K / `counterflow` | Team |
| `heat_pump.cop_model`, `compression_chiller.cop_model` | `carnot` | Team (model choice) |
| `heat_pump.carnot_fraction`, `compression_chiller.carnot_fraction` | 0.5 | Cited: Frutschi, ABB Review 5/1996 |
| `heat_pump.lorenz_fraction`, `compression_chiller.lorenz_fraction` | 0.5 | Team |
| `heat_pump.minimum_temperature_lift`, `compression_chiller.minimum_temperature_lift` | 10 K | Cited: Arpagaus et al. (2018), lowest lift |
| `heat_pump.minimum_source_outlet_temperature` | 47 degC at 2500 m (production temperature less the 40 K cap; about 62 degC at 3000 m) | Derived from the PDF |
| `*.supply_margin` | 0 K | Team |
| `boiler.efficiency` (peak boiler) | 0.9 | Team |
| plant pipes `length` / `inner_diameter` / `elevation_change` / `heat_transfer_coefficient` | 100 m / 0.5 m / 0 m / 0 W/m2/K | Team |
| `absorption_chiller.thermal_cop` | 0.7 | Cited: Herold, Radermacher and Klein (2016) |
| `absorption_chiller.minimum_driving_temperature` | 353.15 K | Team (GEMINI LiBr operating limit) |
| `absorption_chiller.characteristic_slope` / `minimum_driving_difference` / `rejection_coefficient` / `evaporator_coefficient` / `auxiliary_power_ratio` | 700000 W/K / 10 K / 2.2 / 1.2 / 0.01 | Team |
| `adsorption_chiller.thermal_cop` | 0.55 | Cited: Wang and Oliveira (2006) |
| `adsorption_chiller.minimum_driving_temperature` / `maximum_driving_temperature` | 328.15 K / 363.15 K | Team (GEMINI silica-gel range) |
| `adsorption_chiller.characteristic_slope` / `minimum_driving_difference` / `rejection_coefficient` / `evaporator_coefficient` / `auxiliary_power_ratio` | 70000 W/K / 5 K / 2.0 / 1.0 / 0.02 | Team |
| coolers `cooler_type` / `approach` / `specific_fan_power` / `loop_pressure` | `dry` / 5 K / 0.02 / 3 bar | Team (dry approach 5 to 15 K, ASHRAE) |
| compression chiller cooler `capacity` / `flow` / `temperature_setpoint` | 20 MW / 400 kg/s / 25 degC | Team |
| absorption chiller cooler `capacity` / `flow` / `temperature_setpoint` | 40 MW / 800 kg/s / 15 degC | Team |
| search ranges (to propose to the user) | `size.doublets` 1 to 3; `dN.nominal_flow` 50 to 300 m3/h; `depth` 2000 to 3500 m; heat pump 3 to 30 MW; chillers 1 to 10 MW | PDF (doublets, flow); Team (depth, capacities) |

## What the limits mean for the design

- One doublet at the caps (300 m3/h, 40 K, 1030 kg/m3, c_p about 4.2 kJ/kg/K) gives about 14.4 MW;
  the 30 MW heating peak needs two or three doublets, or fewer with a heat pump and a boiler.
- At 2500 m the reservoir is 87 degC, below the 100 degC supply: the heat pump share of the peak
  (ideal exchanger) is (100 - 87) / (100 - 60) = 0.325, about 9.75 MW; direct supply needs about
  3000 m or more (102 degC less the approach).
- The 20 degC cold supply favours a compression chiller (gemini's sample study ranked heat pump +
  boiler + compression chiller first; absorption needs drive water above 80 degC).
- Gas per doublet at 300 m3/h: 240 Nm3/h (192 Nm3/h CH4, about 1.9 MW of fuel): burn it in the peak
  boiler first through a `GasMakeup`, flare only the surplus.
- One doublet at 50 m3/h and 40 K gives about 2.4 MW, just below the 2.673 MW heating minimum, so a
  doublet can run on the lowest days; the 330-day cap still takes 35 days off per doublet, placed by
  `lowest_demand` and covered by the backup (`peak`).
