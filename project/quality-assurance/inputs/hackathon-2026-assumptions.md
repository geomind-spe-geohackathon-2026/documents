# Assumptions for the GEMINI hackathon 2026

Guidance for the GEMINI hackathon 2026 only; a starting point, the agents may depart from it
with a recorded reason.

This file lives in the global Knowledge of geomind.team (never in a project's files). It holds
every value a full run needs, from the case to the report, that the three competition files
(`GEMINI_Heating_Demand_Daily_2027.csv`, `GEMINI_Cooling_Demand_Daily_2027.csv`,
`GEMINI_Hackathon_Challenge_Requirements.pdf`) do not give. It gives no value those files give:
read them yourself. It holds no design, no result and no ranking: the agents design, simulate and
compare by themselves.

Cite it as `knowledge/hackathon-2026-assumptions.md` with the section number (`section 3.2`).
Read the contents first, then only the sections you need, by number or by a word of the title
(`section="3; 4; 5"`, or `"Case values; tolerances; Economics"`). The case lead puts the case
values in its ONE confirmation question and the economics in its ONE `ask_economics` call, each
with this file as the source; after the user approves them they are never asked again. A key this
file marks "Not set, not needed" stays open: never search for it and never ask the user for it. A
value this file gives is never searched in the catalogues, the web or a connector. The method is
`knowledge/handbook-case.md`.

Sections: 1 Sources; 2 Rules from the organisers; 3 Case values; 4 Requirements and tolerances;
5 Economics; 6 Plant design values; 7 Uncertainty ranges; 8 How the competition files map to the
case; 9 Checklist of a full run; 10 Notes on the site, network and utility values; 11 Notes on
the prices against the catalogue; 12 Questions earlier runs asked, answered.

Who reads what: the case lead sections 3, 4 and 5 (and 12 when stuck); the design team section 6
(and 10 for the physics behind the values); the economist section 5 and 11; studies section 7;
the report sections 10 and 11 for limitations.

## 1 Sources of the values

Each value says where it comes from:

- **Organisers**: answers of the organisers on Discord #technical-q-and-a, 2026-11-04.
- **Team**: the team's assumption, taken from gemini's sample case
  (`gemini/examples/hackathon_2026/case.json`, `economics.json` and `plants/`). A Team value has
  no published source of its own; section 10 or 11 gives the reasoning behind it and the published
  values it was checked against.
- **Cited**: from gemini's sample case, which cites the source named in the row (details in
  `gemini/examples/hackathon_2026/README.md`); converted to EUR of 2015 with the euro-area HICP.
- **Catalogue**: a row of the general catalogues `knowledge/data-economics.csv` or
  `knowledge/data-equipment.csv`, cited by its row id.
- **Derived**: computed from the competition files or from a value here by a stated formula
  (gemini computes the same itself); a check, never a value to type into the case.

A Team value is a placeholder, not a fact: it is approved once by the user and reported as an
assumption (`knowledge/handbook-report.md`). Never replace it with a value of your own and never
"improve" it by a search: the comparison between designs needs the same basis in every run.

## 2 Rules from the organisers

Rules beyond the requirements file, from the organisers' answers (Discord #technical-q-and-a,
2026-11-04).

| Item | Value | How it enters the run | Source |
|---|---|---|---|
| Return temperatures | A design choice of the team, within the constraints | Section 3.2 and 3.3 give the team's choice; another value is a case change the user approves | Organisers |
| Grid electricity CO2 intensity | 0.3 kg/kWh (300 g/kWh) | `utilities.electricity.co2_intensity` = 300 g/kWh (section 3.5); never replaced by a country or EU value | Organisers |
| 330 days | The availability of a geothermal doublet; the whole system meets the demand on all 365 days | The doublets may stand still up to 35 days a year (maintenance); the backup or other units cover those days, and the delivered-heat and delivered-cold tolerances of section 4 count all 365 days | Organisers |
| Well depth | May change; use hydrostatic pressure and the 30 K/km gradient for another depth | A design variable (section 6.4); gemini derives the reservoir pressure and temperature at the chosen depth (section 10.4) | Organisers (also in the requirements file) |
| Associated gas | CO2 + CH4; several handling options are allowed (flare, boiler, CHP, ...) | A design choice; every option is costed (section 5) and its CH4 slip counted with the GWP of section 5.1 | Organisers |

## 3 Case values

Every value the case needs that the files do not give. Keys are the case paths.

### 3.1 Case name and time

| Item | Value | Source |
|---|---|---|
| Case name (`name`) | hackathon_2026 | Team: the name this file is found by (`<case name>-assumptions.md`); another name loses the link between the case and this file |
| Simulation period | 2027-01-01 to 2028-01-01 (end excluded), daily steps, 365 steps | Team (the demand files are 2027, daily; 2027 is no leap year) |
| Time zone of both demand series (`demand.heating.power.time_zone`, `demand.cooling.power.time_zone`) | UTC | Team: the files' dates carry no offset and the files name no site; each row is a daily average, so the zone shifts no energy. A zone with daylight saving time (such as Europe/Amsterdam) gives days of 23 and 25 hours, which a daily series cannot have |

### 3.2 Demand: the heating network

The heating supply temperature (100 degC) is in the requirements file. Reasons: section 10.1.

| Item | Value | Source |
|---|---|---|
| Heating network return temperature (`demand.heating.return_temperature`) | 60 degC | Team (design choice allowed by the organisers, section 2); 40 K below the supply |
| Heating network return pressure (`demand.heating.return_pressure`) | 6 bar | Team (absolute; well above the saturation pressure of water at the 100 degC supply, about 1.01 bar) |

### 3.3 Demand: the cooling network

The cooling supply temperature (20 degC) is in the requirements file. Reasons: section 10.2.

| Item | Value | Source |
|---|---|---|
| Cooling network return temperature (`demand.cooling.return_temperature`) | 25 degC | Team (design choice allowed by the organisers, section 2); 5 K above the supply |
| Cooling network return pressure (`demand.cooling.return_pressure`) | 4 bar | Team (absolute) |
| Cooling dew point margin (`demand.cooling.dew_point_margin`) | 1 K | Team (the supply must stay this far above the room's dew point; at 26 degC and 50 % the dew point is 14.8 degC, so the 20 degC supply keeps 5.2 K: the margin never binds, section 10.2) |
| Indoor temperature (cooling) (`demand.cooling.indoor_temperature`) | 26 degC | Team; the upper limit of EN 16798-1:2019 category II for the cooling season (23 to 26 degC operative) |
| Indoor relative humidity (cooling) (`demand.cooling.indoor_relative_humidity`) | 0.5 | Team (50 %); below the 60 % EN 16798-1 assumes for the cooling season |

### 3.4 Site: air and brine

The ground, reservoir, brine and produced gas are in the requirements file. Reasons: section 10.3.

| Item | Value | Source |
|---|---|---|
| Site location | Not given, not needed: no case key takes it, and the air below is a constant. Do not ask for it, do not assume a town or country, and do not fetch a weather series | Team |
| Outside air temperature (`site.air.temperature`) | 10 degC | Team (a constant for the whole year; a temperate North-West European annual mean: KNMI De Bilt 1991-2020 normal 10.5 degC) |
| Outside air pressure (`site.air.pressure`) | 101325 Pa | Cited: the standard atmosphere at sea level, ISO 2533:1975 |
| Sand in the brine (`site.fluid.sand_concentration`) | 20 mg/l | Team (no measurement exists for a synthetic site; it sizes the desander and the filter waste only) |

### 3.5 Utilities

| Item | Value | Source |
|---|---|---|
| Grid electricity CO2 intensity (`utilities.electricity.co2_intensity`) | 300 g/kWh | Organisers (section 2); never the EU or a country value of the catalogue |
| Bought natural gas composition (`utilities.gas.composition`), mole fraction | CH4 0.8249507401227822, C2H6 0.039549858193534584, C3H8 0.012748086337494389, CO2 0.011912342910726407, N2 0.11083897243546233 (sum 1, exact values of gemini's sample; do not round) | Team: a nitrogen-rich low-calorific (L-gas) type; gemini derives LHV 39.99 MJ/kg and 203.1 kg CO2/MWh (section 10.5) |

### 3.6 Keys that stay open

Not set, not needed. Leave each open; never search for it and never ask the user for it.

| Key | Why |
|---|---|
| `site.air.relative_humidity` | No module of this case reads it (a wet cooler uses the wet-bulb temperature instead); the reference `case.json` leaves it open. A dry cooler needs none |
| `utilities.gas.heating_value` | gemini computes it from the composition in section 3.5 |
| `site.reservoir.temperature` | gemini computes it from the surface temperature, the gradient and the depth, which the design may change |
| `site.fluid.dissolved_gas.H2S`, `site.fluid.dissolved_gas.N2` | The requirements file names only CH4 and CO2 in the gas |
| `utilities.electricity.import_limit`, `utilities.electricity.export_limit` | No grid limit is given: the grid takes and gives any power |
| `initial_state` | No storage in the plant families of this case; a design that adds a storage states its initial charge as a design assumption |
| `demand.heating.minimum_return_temperature`, `demand.heating.maximum_return_temperature`, `demand.cooling.minimum_return_temperature`, `demand.cooling.maximum_return_temperature` | The return temperatures are fixed values (sections 3.2 and 3.3), not a band |
| Site location, elevation, weather series | Section 3.4: the air is a constant; elevation 0 m is implied by the sea-level pressure |
| Network length, route, elevation | Section 6.1: the plant is modelled at the consumer |

## 4 Requirements: tolerances the requirements file does not give

The requirements file gives each limit; this section gives only how strictly each is held. Write
each as one requirement of the case, never `when: always`.

| Requirement | Rule | Source |
|---|---|---|
| Heat delivered | Unmet share of the yearly heat demand at most 1 %, over all 365 days (the doublets' 35 idle days included) | Organisers (365 days), Team (1 %) |
| Cold delivered | Unmet share of the yearly cold demand at most 1 %, over all 365 days | Organisers (365 days), Team (1 %) |
| Supply temperatures of the requirements file | Hold while that supply is running (a day with zero cooling demand is no violation) | Team |
| Doublet flow limits of the requirements file (maximum, minimum stable) | Per doublet, while that doublet runs; a stopped doublet (zero flow) is no violation of the minimum | Team (reading of "while active" in the file) |
| Brine cooling limit of the requirements file | Producer to injector temperature drop, per doublet, while running | Team (reading of "producer to injector" in the file) |
| Equal production and injection volume | Reinjection ratio 0.99999 to 1.00001 while running | Team |
| Doublet operating days | The 330 days of the requirements file: days with production flow, per doublet, over the year | Organisers (section 2) |
| Pump intake (only if the design checks it) | Free gas at most 18.75 % of the volume; intake pressure at least 5 bar | Team (catalogue rows `esp-maximum-gas-fraction`, `esp-minimum-intake-pressure`) |
| Well depth search range | 2000 to 3500 m | Team |

A 1 % tolerance is the margin of a daily model against a synthetic profile, not a service level a
utility would sign; a design that meets 100 % is better, and the report says how much it misses.

How gemini takes each (one requirement each; the limits are the requirements file's, the
tolerances above; the form is that of gemini's sample `case.json`):

| Requirement | on / quantity / over / when |
|---|---|
| Doublet flow range | doublet / production_flow / each / running; min and max in m3/h |
| Brine cooling limit | doublet / brine_cooling / each / running; max in K |
| Operating days | doublet / production_flow / duration / running; max in d |
| Pump efficiency | doublet / pump_efficiency / (none) / (none); min = max |
| Full reinjection | doublet / reinjection_ratio / each / running; min and max |
| Number of doublets | doublet / count / (none) / (none); min and max |
| Heat delivered, cold delivered | heating_supply, cooling_supply / unmet_share / (none) / (none); max 0.01 |

The supply temperatures are `demand.*.supply_temperature`, not requirements. This case has no
yearly energy cap; never write one with `over: sum`, which adds the daily power values and gives
no energy (a cap would be `over: mean` with the energy divided by the period).

## 5 Economics

Currency EUR, price year 2015. The keys are gemini's `economics` keys, written here without the
leading `economics.` (`discount_rate` is `economics.discount_rate`), as in gemini's
`examples/hackathon_2026/economics.json`; the uncertainty table (section 7) writes the full path.
Every number is the exact value of that file: copy it digit for digit, never rounded (QA-191).
Every price here is already in EUR of 2015: never convert it again. Notes and cross-checks:
section 11.

### 5.1 General values

| Item | Value | Source |
|---|---|---|
| Currency (`currency`) | EUR | Team |
| Price year (`price_year`) | 2015 | Team (the year of the catalogue's prices) |
| Discount rate, real (`discount_rate`) | 0.05 | Team; real, as gemini discounts constant 2015 prices (PBL SDE++ 2025 geothermal: 5.1 % real, row `discount-rate-pbl-sde-2025-geothermal-real`) |
| Analysis period (`analysis_period`) | 25 yr | Team (DEA sheets give 25 yr technical lifetime for heat pump and boiler; row `analysis-period-dea-2019-geothermal-dk`) |
| Electricity price (`energy.electricity`) | 105.75 EUR/MWh | Cited: Eurostat nrg_pc_205, EU non-household, band IE, excl. VAT, 2025: 136.15 EUR/MWh in EUR of 2025, x 100/128.75 (HICP) = EUR of 2015 (row `electricity-eu-eurostat-price-2025-band-ie`) |
| Natural gas price (`energy.gas`) | 39.92 EUR/MWh | Cited: Eurostat nrg_pc_203, EU non-household, band I4, excl. VAT, 2025: 51.4 EUR/MWh (gross calorific value) in EUR of 2025, x 100/128.75 = EUR of 2015 (row `gas-eu-eurostat-price-2025-band-i4`) |
| CO2 price (`carbon.price`) | 57.03 EUR/t | Cited: Instrat, EU ETS 2025 average allowance price (8 Jan 2026): 73.43 EUR/t in EUR of 2025, x 100/128.75 = EUR of 2015 (row `carbon-price-eu-ets-instrat-price-2025`) |
| Heat revenue / cold revenue (`revenue.heat`, `revenue.cold`) | 60 EUR/MWh each | Team (a flat sale price; section 11.3) |
| Cost share of heat (`accounting.allocation.heat_cost_share`) | 0.8 | Team (share of the shared cost borne by heat; heat is 82 % of the delivered energy: 111.67 of 135.41 GWh) |
| CH4 global warming potential (`accounting.gwp.CH4`) | 29.8 | Cited: IPCC AR6 WG1 table 7.15, GWP100, fossil methane |
| GWP standard (`accounting.gwp.standard`) | IPCC AR6 WG1 table 7.15, GWP100 of fossil methane | Cited: the text exactly; never open |
| Chemicals (`opex.variable.chemical`) | 3 EUR/kg | Team (catalogue corrosion inhibitor 1.94 to 3.11 EUR/kg) |
| Waste disposal (`opex.variable.waste_disposal`) | 0.2 EUR/kg | Team (filter sand and scale; section 11.2) |

### 5.2 Capital cost

`capex.<kind>`. Cited = Danish Energy Agency (DEA), Technology Data for Generation of Electricity
and District Heating, version 0019 (Aug 2026); every other row is Team. Section 11.1 compares each
Team value with the catalogue.

| Key | Value | Source |
|---|---|---|
| Drilling (`capex.drilling`) | 1239.1304347826087 EUR/m | Team (SDE+ 2013 reference case, 2300 m, Mijnlieff et al. 2013; row `drilling-nl-2013-2300m`) |
| Heat pump (`capex.heat_pump`) | 0.73786 EUR/W | Cited: DEA sheet 40 |
| Gas boiler (`capex.boiler`) | 0.06073 EUR/W | Cited: DEA sheet 44 |
| CHP (`capex.chp`) | 0.96155 EUR/W | Cited: DEA sheet 06 (per W electric) |
| Degasser (`capex.degasser`) | 1,000,000 EUR | Team (row `degasser-nl-2013`) |
| Compression chiller (`capex.compression_chiller`) | 0.3 EUR/W | Team |
| Absorption chiller (`capex.absorption_chiller`) | 0.3 EUR/W | Team |
| Adsorption chiller (`capex.adsorption_chiller`) | 0.3 EUR/W | Team |
| Production pump / injection pump (`capex.production_pump`, `capex.injection_pump`) | 0.5 EUR/W each | Team |
| Heat exchanger (`capex.heat_exchanger`) | 0.5 EUR/(W/K) | Team (per W/K of thermal conductance, not per W of duty) |
| Flare (`capex.flare`) | 100,000 EUR | Team |
| Gas make-up (`capex.gas_makeup`) | 50,000 EUR | Team |
| Cooler (`capex.cooler`) | 0.1 EUR/W | Team |
| Pipe (`capex.pipe`) | 500 EUR/m | Team |

### 5.3 Fixed operating cost

`opex.fixed.<kind>`, % of the capital cost per year. Cited = DEA (as in 5.2), each the DEA fixed
O&M over the DEA investment; every other row is Team.

| Key | Value | Source |
|---|---|---|
| Drilling (`opex.fixed.drilling`) | 1 %/yr | Team (row `opex-drilling-geophires-2026`: 1 %/yr) |
| Heat pump (`opex.fixed.heat_pump`) | 0.2239 %/yr | Cited: DEA sheet 40 |
| Gas boiler (`opex.fixed.boiler`) | 3.25 %/yr | Cited: DEA sheet 44 |
| CHP (`opex.fixed.chp`) | 1.0263 %/yr | Cited: DEA sheet 06 |
| Degasser (`opex.fixed.degasser`) | 2 %/yr | Team |
| Compression chiller (`opex.fixed.compression_chiller`) | 2 %/yr | Team |
| Absorption chiller (`opex.fixed.absorption_chiller`) | 2 %/yr | Team |
| Adsorption chiller (`opex.fixed.adsorption_chiller`) | 2 %/yr | Team |
| Production pump / injection pump (`opex.fixed.production_pump`, `opex.fixed.injection_pump`) | 2 %/yr each | Team |
| Heat exchanger (`opex.fixed.heat_exchanger`) | 1 %/yr | Team |
| Flare (`opex.fixed.flare`) | 2 %/yr | Team |
| Gas make-up (`opex.fixed.gas_makeup`) | 2 %/yr | Team |
| Cooler (`opex.fixed.cooler`) | 2 %/yr | Team |
| Pipe (`opex.fixed.pipe`) | 0.5 %/yr | Team |

### 5.4 Keys that stay open

Every key of the variable operating cost per energy (the `opex.per_energy` map) and of the subsidy
(the `revenue.subsidy` map) is `open`: there is no subsidy in this case, and gemini's sample sets
neither map. Once one key of the per-energy map is set gemini needs it for every producing kind,
so set none, even though the catalogue has per-energy rows for the boiler, the heat pump and the
CHP: it has none for any chiller, and earlier runs lost dozens of searches looking for one. Never
search the web or the catalogue for them. The electricity, gas and CO2 a unit uses are costed by
gemini from the prices of section 5.1; only the non-fuel wear per MWh is left out (about 1 to
2 EUR/MWh for the DEA boiler and heat pump, under 2 % of the energy cost).

### 5.5 Equipment the sample does not price

A design that adds a kind sections 5.2 and 5.3 do not price (an electric boiler, a circulation
pump, a thermal or ice storage) takes its capital and fixed operating cost from the general
catalogue `knowledge/data-economics.csv` (the sourced row of that kind, its `value_2015`), shown
to the user with its row id in the same `ask_economics` call. No other kind needs a price.

## 6 Plant design values

### 6.1 The network: the plant at the consumer

The competition describes no district network: no route, length or elevation. The plant is modelled
at the consumer, as gemini's sample plants are: each plant pipe is short and loses no heat. Never
invent a network length; a longer network is a change of the case that only the user can make.

| Path | Value | Source |
|---|---|---|
| plant pipes `length` | 100 m | Team |
| plant pipes `inner_diameter` | 0.5 m | Team (DN500: at 300 m3/h the velocity is 0.42 m/s, a negligible pressure drop) |
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
cooler, before sizing, so one patch carries them. A cooler rejects to the constant 10 degC air of
section 3.4 with the dry-cooler approach of the catalogue (`cooler-approach-dry`, 5 K).

### 6.3 General equipment values

The general equipment parameters (well diameter and roughness, skin, ESP limits and window,
calibration factors, heat pump and chiller efficiencies, boiler efficiency, flare combustion
efficiency, degasser, filter and desander values, cooler settings, pump model and frequency), each
with its source or marked as a placeholder, are in the general catalogue
`knowledge/data-equipment.csv` (`knowledge/data-equipment.md`), cited by row id. Its
`data-equipment.md` also says where each size comes from (`size_plant`, the design duty). Never
ask the user for a pump curve, a datasheet or stage coefficients: the ESP is
`esp-pump-type-unspecified` and `size_plant` sets its rating.

### 6.4 Search ranges

To propose to the user in one question before `set_ranges`:

| Variable | Range | Source |
|---|---|---|
| `depth` | 2000 to 3500 m | Team |
| heat pump `capacity` | 3 to 30 MW | Team (up to the 30 MW heating peak of the requirements file) |
| chiller `capacity` (each kind) | 1 to 10 MW | Team (up to the 10 MW cooling peak of the requirements file) |

The number of doublets and the flow per doublet are bounded by the limits the requirements file
gives: read them there.

## 7 Uncertainty ranges (studies only)

### 7.1 Economics

Set each as the value's `uncertainty` together with the value, exactly as gemini's sample
`economics.json` has it (QA-191):

| Key | `uncertainty` |
|---|---|
| `economics.discount_rate` | `{"kind": "normal", "std": 0.01, "min": 0.02, "max": 0.08}` |
| `economics.energy.electricity` | `{"kind": "uniform", "min": 80, "max": 140}` |
| `economics.energy.gas` | `{"kind": "triangular", "min": 25, "max": 70}` |
| `economics.carbon.price` | `{"kind": "triangular", "min": 30, "max": 110}` |

Units: EUR/MWh for both energies, EUR/t for CO2, all EUR of 2015. A triangular range takes the
value of section 5.1 as its mode (39.92 and 57.03).

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
| Case | return temperatures and pressures, dew point margin, indoor conditions | Sections 3.2, 3.3 |
| Case | outside air, sand | Section 3.4 |
| Case | grid CO2, bought gas composition | Section 3.5 |
| Case | keys left open | Section 3.6 |
| Case | requirement tolerances | Section 4 |
| Economics | every key | Section 5; an unpriced kind from `knowledge/data-economics.csv` (section 5.5) |
| Design | plant family, units, backup, gas handling | The design team's choice (section 8.2), recorded as assumptions |
| Design | network pipes | Section 6.1 |
| Design | case-specific equipment values, cooler loops | Section 6.2 |
| Design | general equipment values | `knowledge/data-equipment.csv` (section 6.3) |
| Design | doublet flow, capacities, injection pump rating, ESP stages | `size_plant` and the search over section 6.4's ranges |
| Design | `params.control.dispatch`, `params.control.outages`, `params.backup` | The value gemini's check suggests |
| Simulate | nothing more: the daily time axis of the case | — |
| Studies | uncertainty ranges | Section 7 |
| Report | nothing more: costs, emissions and KPIs come from gemini's results; limitations from sections 10 and 11 | `knowledge/handbook-report.md` |

## 10 Notes on the site, network and utility values

Why each Team value of section 3 is what it is, and the checks behind it. Read it to explain a
value to the user or to write the report's limitations; never to change a value.

### 10.1 Heating network

- The requirements file fixes the supply at 100 degC. That is a high supply by today's standard:
  in the district heating generations of Lund et al. (2014, Energy 68, 1-11) the third generation
  runs below 100 degC and the fourth at 50 to 60 degC. Buildings that need 100 degC are older
  stock, whose returns are high; 60 degC is a conservative return for them.
- The return sets the brine's useful cooling: every kelvin the network returns lower lets the
  heat exchanger cool the brine further, within the brine cooling limit of the requirements file.
  A lower return is a case change (section 8.2), not a tuning knob of the design.
- 6 bar (absolute) keeps the water far above its saturation pressure at 100 degC (1.01 bar) and
  is a usual static level of a pressurised network; it is the boundary pressure only, the plant
  pipes lose almost none of it (section 6.1).

### 10.2 Cooling network and comfort

- The requirements file fixes the supply at 20 degC: high-temperature cooling for sensible-only
  terminals (radiant ceilings, chilled beams, slab cooling), not the 5 to 7 degC of a
  conventional chilled-water network. The latent load (dehumidification) lies outside this case.
- 25 degC return gives 5 K of rise, typical of such terminals.
- Indoor 26 degC and 50 %: EN 16798-1:2019 category II keeps 23 to 26 degC operative in the
  cooling season and assumes 60 % relative humidity there. The dew point (Magnus formula,
  Alduchov and Eskridge 1996) is 14.8 degC at 26 degC and 50 %, and 17.6 degC at 60 %.
- With 20 degC supply the margin above the dew point is 5.2 K (2.4 K at 60 %): the 1 K
  `dew_point_margin` is a guard, it never limits this case. Never lower the supply to gain
  capacity: it is fixed by the file.

### 10.3 Site air and brine

- No site: the files describe a synthetic plant. The air is a constant 10 degC for the whole
  year, close to the KNMI De Bilt 1991-2020 annual normal of 10.5 degC. It is not the 12 degC
  reference surface temperature of the requirements file, which is the ground's, for the gradient.
- The air feeds the coolers and the atmosphere module only. A constant annual mean understates
  the summer air temperature, so a dry cooler in July rejects heat more easily in the model than
  in reality: state this in the report's limitations.
- 101325 Pa is the ISO 2533 sea-level pressure; it implies an elevation of 0 m.
- 20 mg/l sand is a placeholder for a sandstone doublet with sand control; it changes only the
  desander's catch and the waste cost (section 5.1), never the heat balance.

### 10.4 Reservoir at another depth (Derived)

gemini derives both from the requirements file's values; these are checks, never case values.
Pressure p(z) = rho g z with rho = 1030 kg/m3 and g = 9.80665 m/s2: 252.5 bar at 2500 m, which
matches the file's 250 bar(g). Temperature T(z) = 12 degC + 30 K/km x z. Over the search range:
2000 m 202 bar, 72 degC; 2500 m 253 bar, 87 degC; 3000 m 303 bar, 102 degC; 3500 m 354 bar,
117 degC. A deeper well is hotter but costs more per metre (section 11.1).

### 10.5 Gases (Derived, by gemini's own functions)

- Bought gas (section 3.5): molar mass 18.62 g/mol, normal density 0.831 kg/Nm3, lower heating
  value 39.99 MJ/kg (33.2 MJ/Nm3), combustion CO2 203.1 kg per MWh of LHV. It is close to Dutch
  Groningen L-gas (about 81 % CH4 and 14 % N2, Gasunie).
- Produced gas (requirements file, 80 % CH4 and 20 % CO2): LHV 29.66 MJ/kg, normal density
  0.965 kg/Nm3. With the file's gas-liquid ratio this is about 22.9 MJ of gas per m3 of brine, a
  small fuel stream next to the brine's heat: it decides the gas handling (flare, boiler, CHP),
  not the plant's size.
- Grid electricity: 300 g/kWh (organisers), above the 2025 EU mean (209 g/kWh, Ember, row
  `co2-grid-eu-2025`): use the organisers' value only.

## 11 Notes on the prices against the catalogue

The Team prices of section 5 against the sourced rows of `knowledge/data-economics.csv`
(`value_2015`, EUR of 2015). Use it to explain a price, to choose a sensitivity, or for the
report's limitations; never to replace a value of section 5.

### 11.1 Capital and fixed operating cost

| Kind | Section 5 | Catalogue rows (value_2015) | Note |
|---|---|---|---|
| Drilling | 1239.13 EUR/m | 1246.83 at 2300 m, 1844.74 at 3000 m, 2075.37 at 4000 m (`drilling-nl-2013-*`, verified) | One price per metre for every depth: the 3000 m row is 49 % higher, so a design deeper than 2300 m is underpriced. Report it, or run a sensitivity on drilling cost |
| Heat pump | 0.73786 EUR/W | 0.737864 (`heat-pump-dea-2025-10mw`) | Same source |
| Gas boiler, CHP | 0.06073, 0.96155 EUR/W | 0.06, 0.95 (DEA 2018 rows) | Same source, other edition |
| Compression chiller | 0.3 EUR/W | 0.159 (`compression-chiller-ecos-2023`) | Placeholder above the source |
| Absorption chiller | 0.3 EUR/W | 0.234 to 0.438 (ecos, kim, bigee rows) | Within the range |
| Adsorption chiller | 0.3 EUR/W | 0.827 to 0.859 (edinburgh, bigee rows) | Placeholder about a third of the sources: a design that picks adsorption looks cheaper than it is. Say so in the report |
| Production pump (ESP) | 0.5 EUR/W | 0.60 to 0.72 EUR/W electric (kennisagenda 2016), 1.55 (schlagermann 2023) | Placeholder below the sources |
| Injection pump | 0.5 EUR/W | 0.099 (DH pump station proxy) | Placeholder above the proxy |
| Heat exchanger | 0.5 EUR/(W/K) | 0.109 EUR/W of duty (DEA station) | Different units: not comparable directly |
| Degasser | 1,000,000 EUR | 1,006,240 (`degasser-nl-2013`) | Same source |
| Flare, gas make-up | 100,000, 50,000 EUR | 57,700 (EPA flare proxy); 636,893 (a 1 MWe CHP, other scope) | Placeholders |
| Cooler | 0.1 EUR/W | 0.049 to 0.107 (IEA dry cooler) | At the high end |
| Pipe | 500 EUR/m | 636 to 1149 EUR/m (DEA distribution) | Below, for short plant pipes |
| Fixed O&M | 2 %/yr (most Team rows) | chillers 2.9 to 4 %, pumps and flare 3 %, heat exchanger 1.5 to 2.5 %, pipe 0.5 to 1 %, ESP replacement every 5 yr | Team rows sit at or below the sources |

### 11.2 Energy, carbon and other prices

- Electricity 105.75, gas 39.92, CO2 57.03: EUR of 2015, already deflated (section 5.1); the
  2024 rows of the catalogue are lower (CO2 51.56).
- The gas price is per MWh of gross calorific value (Eurostat), while gemini burns gas by its
  lower heating value: for the bought gas of section 3.5 the GCV is about 11 % above the LHV, so
  the model's gas cost is about 10 % low. A limitation to report, not a value to change.
- Chemicals 3 EUR/kg sits at the top of the catalogue's 1.94 to 3.11 EUR/kg (corrosion
  inhibitor). Waste 0.2 EUR/kg lies between sludge disposal (0.05) and filter waste disposal (3.87).
- Discount rate 0.05 real: PBL SDE++ 2025 geothermal 5.1 % real; EU financial 4 %, social 3 %.

### 11.3 Revenue and cost share

- 60 EUR/MWh for heat and cold is below the catalogue's market rows (heat: NL 2019 tariff 93.5,
  Sweden 2019 81.1, NL 2026 household ceiling 114.6; cold: EU27 alternative 81.2, Norway 103.5),
  so the net present value is conservative. Revenue changes no cost per MWh (LCOH, LCOC).
- 0.8 of the shared cost to heat; heat is 82 % of the delivered energy and the catalogue's
  geothermal CHP allocation by energy gives 0.87 (`heat-cost-share-energy-fiaschi-2021`).

### 11.4 A price the user gives in another year

All prices are EUR of 2015. A price the user gives in EUR of year Y is multiplied by 100 / HICP(Y)
(Eurostat prc_hicp_aind, euro area, 2015 = 100), the index the catalogue's `conversion` column
uses: 2019 104.80; 2022 116.82; 2023 123.15; 2024 126.07; 2025 128.75; a 2026 price takes the
2025 index (no annual 2026 index yet). Example: 80 EUR/MWh of 2026 = 80 x 100/128.75 = 62.14 EUR/MWh
of 2015. Ask once which year a user's price is in; never convert a value of this file.

## 12 Questions earlier runs asked, answered

From the questions and searches of recorded QA runs. Each answer is final for this competition.

| Question | Answer |
|---|---|
| Where is the site? Which country, town, elevation? | None: the files describe a synthetic site. Never assume one (section 3.4) |
| Which time zone are the demand dates in? | UTC (section 3.1) |
| Should the air be a weather series (open-meteo, KNMI)? | No: a constant 10 degC, no fetch (section 3.4) |
| The outside air relative humidity? | Open, no module reads it (section 3.6) |
| Return temperatures 50, 55, 40 degC instead? | 60 and 25 degC; another value is a case change the user approves (section 8.2) |
| Grid CO2 of the Netherlands, the EU or Ember? | 300 g/kWh from the organisers (section 2) |
| Gas heating value, H2S, N2 in the brine gas? | Open; gemini computes the heating value (section 3.6) |
| Grid import or export limit? | Open: none (section 3.6) |
| Network length, pipe route? | None: plant at the consumer (section 6.1) |
| Variable O&M per MWh of a chiller? | Open, set no per-energy key (section 5.4) |
| A price of 2025 or 2026? | Multiply by 100/HICP of its year (section 11.4); this file's prices are already 2015 |
| ESP curves, stage count, pump model? | Not needed: unspecified pump, `size_plant` sizes it (section 6.3) |
| Boiler efficiency, flare combustion efficiency, degasser, filter values? | `knowledge/data-equipment.csv` (section 6.3) |
| Initial state of a storage? | Open; only a design that adds a storage states it (section 3.6) |
| Reservoir pressure at another depth? | gemini derives it (sections 2 and 10.4); never type it into the case |
