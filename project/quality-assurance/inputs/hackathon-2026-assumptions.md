# Assumptions for the GEMINI hackathon case (2026)

Guidance for the GEMINI hackathon 2026 case only; a starting point, the agents may depart from it
with a recorded reason.

This file lives in the global Knowledge of geomind.team (never in a project's files). It holds
every value a full run needs, from the case to the report, that the three competition files
(`GEMINI_Heating_Demand_Daily_2027.csv`, `GEMINI_Cooling_Demand_Daily_2027.csv`,
`GEMINI_Hackathon_Challenge_Requirements.pdf`) do not give. It gives no value those files give:
read them yourself. It holds no design, no result and no ranking: the agents design, simulate and
compare by themselves.

Cite it as `knowledge/hackathon-2026-assumptions.md` with the section number (`section 3.2`).
Read only the sections you need (`read_knowledge("knowledge/hackathon-2026-assumptions.md",
section="3; 5")`). The case lead puts the case values in its ONE confirmation question and the
economics in its ONE `ask_economics` call, each with this file as the source; after the user
approves them they are never asked again. A key this file marks "Not set, not needed" stays open:
never search for it and never ask the user for it. A value this file gives is never searched in
the catalogues, the web or a connector. The method is `knowledge/handbook-case.md`; section 9
lists every value of a full run and where each comes from.

Sections: 1 Sources; 2 Rules from the organisers; 3 Case values; 4 Requirements; 5 Economics;
6 Plant design values; 7 Uncertainty ranges; 8 How the competition files map to the case;
9 Checklist of a full run.

## 1 Sources of the values

Each value says where it comes from:

- **Organisers**: answers of the organisers on Discord #technical-q-and-a, 2026-11-04.
- **Team**: the team's assumption (a placeholder with no verified source), taken from gemini's sample
  case (`gemini/examples/hackathon_2026/case.json`, `economics.json` and `plants/`).
- **Cited**: from gemini's sample case, which cites the source named in the row (details in
  `gemini/examples/hackathon_2026/README.md`); converted to EUR of 2015 with the euro-area HICP.
- **Catalogue**: a row of the general catalogues `knowledge/data-economics.csv` or
  `knowledge/data-equipment.csv`, cited by its row id.

## 2 Rules from the organisers

Rules beyond the requirements file.

| Item | Value | Source |
|---|---|---|
| Return temperatures | A design choice of the team, within the constraints | Organisers |
| Grid electricity CO2 intensity | 0.3 kg/kWh (300 g/kWh) | Organisers |
| 330 days | The availability of a geothermal doublet; the whole system meets the demand on all 365 days | Organisers |
| Well depth | May change; use hydrostatic pressure and the 30 K/km gradient for another depth | Organisers (also in the requirements file) |
| Associated gas | CO2 + CH4; several handling options are allowed (flare, boiler, CHP, ...) | Organisers |

## 3 Case values

### 3.1 Case name and time

| Item | Value | Source |
|---|---|---|
| Case name (`name`) | hackathon_2026 | Team: the name this file is found by (`<case name>-assumptions.md`); another name loses the link between the case and this file |
| Simulation period | 2027-01-01 to 2028-01-01 (end excluded), daily steps | Team (the demand files are 2027, daily) |
| Time zone of both demand series (`demand.heating.power.time_zone`, `demand.cooling.power.time_zone`) | UTC | Team: the files' dates carry no offset and the files name no site; each row is a daily average, so the zone shifts no energy. A zone with daylight saving time (such as Europe/Amsterdam) gives days of 23 and 25 hours, which a daily series cannot have |

### 3.2 Demand: the network side

| Item | Value | Source |
|---|---|---|
| Heating network return temperature (`demand.heating.return_temperature`) | 60 degC | Team (design choice, section 2) |
| Heating network return pressure (`demand.heating.return_pressure`) | 6 bar | Team |
| Cooling network return temperature (`demand.cooling.return_temperature`) | 25 degC | Team (design choice, section 2) |
| Cooling network return pressure (`demand.cooling.return_pressure`) | 4 bar | Team |
| Cooling dew point margin (`demand.cooling.dew_point_margin`) | 1 K | Team |
| Indoor temperature (cooling) (`demand.cooling.indoor_temperature`) | 26 degC | Team |
| Indoor relative humidity (cooling) (`demand.cooling.indoor_relative_humidity`) | 0.5 | Team (50 %) |

### 3.3 Site: air and brine

| Item | Value | Source |
|---|---|---|
| Site location | Not given, not needed: no case key takes it, and the air below is a constant. Do not ask for it or fetch a weather series | Team |
| Outside air temperature (`site.air.temperature`) | 10 degC | Team (a constant for the whole year) |
| Outside air pressure (`site.air.pressure`) | 101325 Pa | Team (the standard atmosphere at sea level, ISO 2533) |
| Sand in the brine (`site.fluid.sand_concentration`) | 20 mg/l | Team |

### 3.4 Utilities

| Item | Value | Source |
|---|---|---|
| Grid electricity CO2 intensity (`utilities.electricity.co2_intensity`) | 300 g/kWh | Organisers |
| Bought natural gas composition (`utilities.gas.composition`), mole fraction | CH4 0.8249507401227822, C2H6 0.039549858193534584, C3H8 0.012748086337494389, CO2 0.011912342910726407, N2 0.11083897243546233 (sum 1, exact values of gemini's sample; do not round) | Team |

### 3.5 Keys that stay open

Not set, not needed. Leave each open; never search for it and never ask the user for it.

| Key | Why |
|---|---|
| `site.air.relative_humidity` | No module of this case reads it (a wet cooler uses the wet-bulb temperature instead); the reference `case.json` leaves it open |
| `utilities.gas.heating_value` | gemini computes it from the composition in section 3.4 |
| `site.reservoir.temperature` | gemini computes it from the surface temperature, the gradient and the depth, which the design may change |
| `site.fluid.dissolved_gas.H2S`, `site.fluid.dissolved_gas.N2` | The requirements file names only CH4 and CO2 in the gas |
| `utilities.electricity.import_limit`, `utilities.electricity.export_limit` | No grid limit is given: the grid takes and gives any power |
| `initial_state` | No storage in the plant families of this case; a design that adds a storage states its initial charge as a design assumption |
| `demand.heating.minimum_return_temperature`, `demand.heating.maximum_return_temperature`, `demand.cooling.minimum_return_temperature`, `demand.cooling.maximum_return_temperature` | The return temperatures are fixed values (section 3.2), not a band |

## 4 Requirements: tolerances the requirements file does not give

| Requirement | Rule | Source |
|---|---|---|
| Heat delivered | Unmet share of the yearly heat demand at most 1 %, over all 365 days | Organisers (365 days), Team (1 %) |
| Cold delivered | Unmet share of the yearly cold demand at most 1 %, over all 365 days | Organisers (365 days), Team (1 %) |
| Supply temperatures of the requirements file | Hold while that supply is running (a day with zero cooling demand is no violation) | Team |
| Equal production and injection volume | Reinjection ratio 0.99999 to 1.00001 while running | Team |
| Pump intake (only if the design checks it) | Free gas at most 18.75 % of the volume; intake pressure at least 5 bar | Team (catalogue rows `esp-maximum-gas-fraction`, `esp-minimum-intake-pressure`) |
| Well depth search range | 2000 to 3500 m | Team |

## 5 Economics

### 5.1 General values

Currency EUR, price year 2015 (`currency`, `price_year`). Keys under `economics.` as in gemini's
`examples/hackathon_2026/economics.json`. Every number in section 5 is the exact value of that
file: copy it digit for digit, never rounded (QA-191).

| Item | Value | Source |
|---|---|---|
| Currency (`currency`) | EUR | Team |
| Price year (`price_year`) | 2015 | Team (the year of the catalogue's prices) |
| Discount rate (`discount_rate`) | 0.05 | Team |
| Analysis period (`analysis_period`) | 25 yr | Team (DEA sheets give 25 yr technical lifetime for heat pump and boiler) |
| Electricity price (`energy.electricity`) | 105.75 EUR/MWh | Cited: Eurostat nrg_pc_205, EU non-household, band IE, excl. VAT, 2025 (catalogue row `electricity-eu-eurostat-price-2025-band-ie`) |
| Natural gas price (`energy.gas`) | 39.92 EUR/MWh | Cited: Eurostat nrg_pc_203, EU non-household, band I4, excl. VAT, 2025 (row `gas-eu-eurostat-price-2025-band-i4`) |
| CO2 price (`carbon.price`) | 57.03 EUR/t | Cited: Instrat, EU ETS 2025 average allowance price (8 Jan 2026) (row `carbon-price-eu-ets-instrat-price-2025`) |
| Heat revenue / cold revenue (`revenue.heat`, `revenue.cold`) | 60 EUR/MWh each | Team |
| Cost share of heat (`accounting.allocation.heat_cost_share`) | 0.8 | Team |
| CH4 global warming potential (`accounting.gwp.CH4`) | 29.8 | Cited: IPCC AR6 WG1 table 7.15, GWP100, fossil methane |
| GWP standard (`accounting.gwp.standard`) | IPCC AR6 WG1 table 7.15, GWP100 of fossil methane | Cited: the text exactly; never open |
| Chemicals (`opex.variable.chemical`) | 3 EUR/kg | Team |
| Waste disposal (`opex.variable.waste_disposal`) | 0.2 EUR/kg | Team |

### 5.2 Capital cost and fixed operating cost

Capital cost (`capex.<kind>`) and fixed operating cost (`opex.fixed.<kind>`, % of the capital cost
per year). Cited = Danish Energy Agency, Technology Data for Generation of Electricity and
District Heating, version 0019 (Aug 2026); every other row is Team.

| Key | Value | Source |
|---|---|---|
| Drilling (`capex.drilling`) | 1239.1304347826087 EUR/m | Team (SDE+ 2013 reference case, Mijnlieff et al. 2013, not re-verified) |
| Drilling (`opex.fixed.drilling`) | 1 %/yr | Team |
| Heat pump (`capex.heat_pump`) | 0.73786 EUR/W | Cited: DEA sheet 40 |
| Heat pump (`opex.fixed.heat_pump`) | 0.2239 %/yr | Cited: DEA sheet 40 |
| Gas boiler (`capex.boiler`) | 0.06073 EUR/W | Cited: DEA sheet 44 |
| Gas boiler (`opex.fixed.boiler`) | 3.25 %/yr | Cited: DEA sheet 44 |
| CHP (`capex.chp`) | 0.96155 EUR/W | Cited: DEA sheet 06 |
| CHP (`opex.fixed.chp`) | 1.0263 %/yr | Cited: DEA sheet 06 |
| Degasser (`capex.degasser`) | 1,000,000 EUR | Team |
| Degasser (`opex.fixed.degasser`) | 2 %/yr | Team |
| Compression chiller (`capex.compression_chiller`) | 0.3 EUR/W | Team |
| Compression chiller (`opex.fixed.compression_chiller`) | 2 %/yr | Team |
| Absorption chiller (`capex.absorption_chiller`) | 0.3 EUR/W | Team |
| Absorption chiller (`opex.fixed.absorption_chiller`) | 2 %/yr | Team |
| Adsorption chiller (`capex.adsorption_chiller`) | 0.3 EUR/W | Team |
| Adsorption chiller (`opex.fixed.adsorption_chiller`) | 2 %/yr | Team |
| Production pump / injection pump (`capex.production_pump`, `capex.injection_pump`) | 0.5 EUR/W each | Team |
| Production pump / injection pump (`opex.fixed.production_pump`, `opex.fixed.injection_pump`) | 2 %/yr each | Team |
| Heat exchanger (`capex.heat_exchanger`) | 0.5 EUR/(W/K) | Team |
| Heat exchanger (`opex.fixed.heat_exchanger`) | 1 %/yr | Team |
| Flare (`capex.flare`) | 100,000 EUR | Team |
| Flare (`opex.fixed.flare`) | 2 %/yr | Team |
| Gas make-up (`capex.gas_makeup`) | 50,000 EUR | Team |
| Gas make-up (`opex.fixed.gas_makeup`) | 2 %/yr | Team |
| Cooler (`capex.cooler`) | 0.1 EUR/W | Team |
| Cooler (`opex.fixed.cooler`) | 2 %/yr | Team |
| Pipe (`capex.pipe`) | 500 EUR/m | Team |
| Pipe (`opex.fixed.pipe`) | 0.5 %/yr | Team |

### 5.3 Keys that stay open

Every key of the variable operating cost per energy (the `opex.per_energy` map) and of the subsidy
(the `revenue.subsidy` map) is `open`: there is no subsidy in this case, and gemini's sample sets
neither map. Once one key of the per-energy map is set gemini needs it for every producing kind,
so set none. Never search the web or the catalogue for them.

### 5.4 Equipment the sample does not price

A design that adds a kind section 5.2 does not price (an electric boiler, a circulation pump, a
thermal or ice storage) takes its capital and fixed operating cost from the general catalogue
`knowledge/data-economics.csv` (the sourced row of that kind, EUR of 2015), shown to the user with
its row id in the same `ask_economics` call. No other kind needs a price.

## 6 Plant design values

### 6.1 The network: the plant at the consumer

The competition describes no district network: no route, length or elevation. The plant is modelled
at the consumer, as gemini's sample plants are: each plant pipe is short and loses no heat. Never
invent a network length; a longer network is a change of the case that only the user can make.

| Path | Value | Source |
|---|---|---|
| plant pipes `length` | 100 m | Team |
| plant pipes `inner_diameter` | 0.5 m | Team |
| plant pipes `elevation_change` | 0 m | Team |
| plant pipes `heat_transfer_coefficient` | 0 W/m2/K | Catalogue `pipe-heat-transfer-coefficient-insulated` |
| plant pipes `roughness` | 4.5e-5 m | Catalogue `roughness-new-commercial-steel-pipe` |

### 6.2 This case's own design assumptions

From gemini's sample plants for this case. `dN` is each doublet.

| Path | Value | Source |
|---|---|---|
| `heat_exchanger.thermal_conductance` | 1500000 W/K | Team (a starting value; the design checks it against its duty) |
| `injection_pump.efficiency` | The production pump efficiency the requirements file gives | Team (the same pumps) |
| `absorption_chiller.characteristic_slope` | 700000 W/K | Team |
| `adsorption_chiller.characteristic_slope` | 70000 W/K | Team |
| compression chiller cooler `capacity` / `flow` / `temperature_setpoint` | 20 MW / 400 kg/s / 25 degC | Team |
| absorption chiller cooler `capacity` / `flow` / `temperature_setpoint` | 40 MW / 800 kg/s / 15 degC | Team |
| adsorption chiller cooler `capacity` / `flow` / `temperature_setpoint` | 10 MW / 200 kg/s / 15 degC | Team |
| every cooler `loop_pressure` | 3 bar | Catalogue `cooler-loop-pressure` |

The cooler `flow` and `loop_pressure` are the first guess of a closed loop: give them with the
cooler, before sizing, so one patch carries them.

### 6.3 General equipment values

The general equipment parameters (roughness, skin, ESP limits and window, calibration factors,
heat pump and chiller efficiencies, treatment pressure drops, cooler settings, pump model and
frequency), each with its source or marked as a placeholder, are in the general catalogue
`knowledge/data-equipment.csv` (`knowledge/data-equipment.md`), cited by row id. Its
`data-equipment.md` also says where each size comes from (`size_plant`, the design duty).

### 6.4 Search ranges

To propose to the user in one question before `set_ranges`:

| Variable | Range | Source |
|---|---|---|
| `depth` | 2000 to 3500 m | Team |
| heat pump `capacity` | 3 to 30 MW | Team |
| chiller `capacity` (each kind) | 1 to 10 MW | Team |

The number of doublets and the flow per doublet are bounded by the limits the requirements file
gives: read them there.

## 7 Uncertainty ranges (studies only)

### 7.1 Economics

Set each as the value's `uncertainty` together with the value, exactly as gemini's sample
`economics.json` has it (QA-191):

| Key | `uncertainty` |
|---|---|
| `economics.discount_rate` | `{"kind": "normal", "std": 0.01, "min": 0.02, "max": 0.08}` |
| `economics.energy.electricity` | `{"kind": "uniform", "min": 80, "max": 140}` (EUR/MWh) |
| `economics.energy.gas` | `{"kind": "triangular", "min": 25, "max": 70}` (EUR/MWh; the mode is the value 39.92) |
| `economics.carbon.price` | `{"kind": "triangular", "min": 30, "max": 110}` (EUR/t; the mode is the value 57.03) |

### 7.2 Site

Team:

| Value | Range |
|---|---|
| Geothermal gradient | normal, std 2 K/km, 25 to 35 K/km |
| Permeability | triangular 100 to 400 mD, mode 200 |

## 8 How the competition files map to the case

The method is general and lives in `knowledge/handbook-case.md`; this section applies it to the
competition only. The values the competition files give are read from those files; the values they
lack are sections 3 to 7.

### 8.1 Read from the files, never from here

The time axis, both demand series (with the time zone of section 3.1), the supply temperatures,
the ground, reservoir, brine and gas values, the pump efficiency and the hard limits are in the
requirements file and the two CSVs: read them there and set them without asking.

### 8.2 Design freedoms

Never asked as missing case values:

- well depth (search range in section 6.4);
- number of doublets (bounded by the limit the requirements file gives);
- return temperatures: 60 and 25 degC as team design choices; another value comes as
  `case change needed` (`knowledge/handbook-case.md` §7.4);
- backup policy, number and kind of units, associated gas handling (flare, boiler, CHP).

### 8.3 Done when

- The requirements read from the requirements file, with the tolerances of section 4; no
  `when: always`.
- No reservoir temperature, depth or doublet count in the case.
- Both series with the time zone of section 3.1.
- The values of section 3 confirmed in the one question; `plants_need` empty.
- Economics set from section 5 (EUR, price year 2015).
- Only the three competition files are project files; handbooks and this file stay in global
  Knowledge.

## 9 Checklist of a full run

Every value a full run needs, in the order of the run, and where it comes from. "Files" is the
three competition files; a value marked gemini or `size_plant` is never asked or searched.

| Stage | Values | From |
|---|---|---|
| Case | time axis, demand series, supply temperatures, ground, reservoir, brine, gas, hard limits | Files (section 8.1) |
| Case | case name, time zone | Section 3.1 |
| Case | return temperatures and pressures, dew point margin, indoor conditions | Section 3.2 |
| Case | outside air, sand | Section 3.3 |
| Case | grid CO2, bought gas composition | Section 3.4 |
| Case | keys left open | Section 3.5 |
| Case | requirement tolerances | Section 4 |
| Economics | every key | Section 5; an unpriced kind from `knowledge/data-economics.csv` (section 5.4) |
| Design | plant family, units, backup, gas handling | The design team's choice (section 8.2), recorded as assumptions |
| Design | network pipes | Section 6.1 |
| Design | case-specific equipment values, cooler loops | Section 6.2 |
| Design | general equipment values | `knowledge/data-equipment.csv` (section 6.3) |
| Design | doublet flow, capacities, injection pump rating, ESP stages | `size_plant` and the search over section 6.4's ranges |
| Design | `params.control.dispatch`, `params.control.outages`, `params.backup` | The value gemini's check suggests |
| Simulate | nothing more: the daily time axis of the case | — |
| Studies | uncertainty ranges | Section 7 |
| Report | nothing more: costs, emissions and KPIs come from gemini's results | `knowledge/handbook-report.md` |
