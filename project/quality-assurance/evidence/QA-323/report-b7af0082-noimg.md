# QA-TEST QA-AI-analysis-I 1: QA-332 retest minimize

## 1 Summary

![Key figures](IMG)

*Figure 1.1 - Key figures of the design*

The design delivers 111.7 GWh of heat and 23.74 GWh of cold a year. The levelised cost is 31.49 EUR/MWh. Of the heating demand, geothermal brine heat 76 %, heat-pump electricity 4.2 %, backup 19 %. The largest rated units are Boiler 30 MW, Chiller cooler 24.39 MW, Chiller 10 MW. It emits 10.26 kt of CO2 over the run. All 15 assessed checks pass.

<div style="page-break-before: always"></div>

## 2 Case and demand

The design runs on case hackathon_2026, version 3. The simulation runs from 2027-01-01 to 2028-01-01, in steps of 1 d.

| Quantity | Value | Uncertainty |
| --- | ---: | --- |
| Air pressure | 101,300 Pa | - |
| Air temperature | 10 degC | - |
| Fluid density | 1,030 kg/m3 | - |
| Fluid viscosity | 0.4 mPa.s | - |
| Fluid dissolved gas CH4 | 0.8 | - |
| Fluid dissolved gas CO2 | 0.2 | - |
| Fluid gas liquid ratio | 0.8 Nm3/m3 | - |
| Fluid sand concentration | 20 mg/l | - |
| Ground gradient | 30 K/km | normal, 25 to 35 K/km |
| Ground surface temperature | 12 degC | - |
| Reservoir pressure | 250 barg | - |
| Reservoir thickness | 100 m | - |
| Reservoir permeability | 200 mD | triangular, 100 to 400 mD |
| Reservoir reference depth | 2,500 m | - |

*Table 2.1 - Site, reservoir and fluid values of the case*

The reservoir has a depth of 2,500 m, a thickness of 100 m and a permeability of 200 mD. 2 of the 14 values carry an uncertainty range, which the studies of section 7 can vary.

| Service | Supply | Return | Annual demand | Peak (daily mean) | Met |
| --- | ---: | ---: | ---: | ---: | ---: |
| Cooling | 20 degC | 25 degC | 23.74 GWh | 10 MW | 100 % |
| Heating | 100 degC | 60 degC | 111.7 GWh | 30 MW | 100 % |

*Table 2.2 - Demand of each service and how much of it was met*

Cooling demand totals 23.74 GWh with a peak daily mean of 10 MW on 2027-07-19 and a mean of 2.71 MW. Heating demand totals 111.7 GWh with a peak daily mean of 30 MW on 2027-01-28 and a mean of 12.75 MW. The demand profiles come from data/demand.csv (cooling_demand_MWcool) and data/demand.csv (heating_demand_MWth).

<div style="page-break-before: always"></div>

## 3 Plant design

Design QA-332 retest minimize from a study of kind Find the best design, plant type Hackathon plant.

*Figure 3.1 - Process flowsheet of the plant*

The flowsheet shows the 23 modules of the plant and the 39 connections between them, carrying air, brine, chemical, chilled_water, electricity, gas, heat, hot_water and waste. The costed units fall into 8 subsurface, 3 treatment and gas, 3 heating and 2 cooling units; subsections 3.1 to 3.5 give each group with its size and use.

### 3.1 Subsurface

| Module | Kind | Rated | Peak | Used | Capital cost |
| --- | --- | ---: | ---: | ---: | ---: |
| d0 | Production pump | 237.5 m3/h | 237.5 m3/h | 100 % | 0.1534 MEUR |
| d1 | Production pump | 237.5 m3/h | 237.5 m3/h | 100 % | 0.1534 MEUR |
| D0 well | Drilling | - | - | - | 3.185 MEUR |
| D1 well | Drilling | - | - | - | 3.185 MEUR |
| D0 riser | Drilling | - | - | - | 0.3773 MEUR |
| D1 riser | Drilling | - | - | - | 0.3773 MEUR |
| D0 injector | Drilling | - | - | - | 3.562 MEUR |
| D1 injector | Drilling | - | - | - | 3.562 MEUR |

*Table 3.1 - Subsurface units: rating, use and capital cost*

8 units make up the subsurface part, with a capital cost of 14.56 MEUR, 56 % of the plant's total. The largest is D0 injector. d0 and d1 ran at their full rating, so they limit what the plant can deliver.

### 3.2 Treatment and gas

| Module | Kind | Rated | Peak | Used | Capital cost |
| --- | --- | --- | --- | --- | ---: |
| Flare | Flare | - | - | - | 0.1 MEUR |
| Makeup | Gas makeup | - | - | - | 0.05 MEUR |
| Degasser | Degasser | - | - | - | 1 MEUR |

*Table 3.2 - Treatment and gas units: rating, use and capital cost*

3 units make up the treatment and gas part, with a capital cost of 1.15 MEUR, 4.4 % of the plant's total. The largest is Degasser.

### 3.3 Heating

| Module | Kind | Rated | Peak | Used | Capital cost |
| --- | --- | ---: | ---: | ---: | ---: |
| hx | Heat exchanger | 1.5 MW/K | - | - | 0.75 MEUR |
| Boiler | Boiler | 30 MW | 11.3 MW | 38 % | 1.822 MEUR |
| Heat pump | Heat pump | 3 MW | 3 MW | 100 % | 2.214 MEUR |

*Table 3.3 - Heating units: rating, use and capital cost*

3 units make up the heating part, with a capital cost of 4.785 MEUR, 18 % of the plant's total. The largest is Heat pump, rated 3 MW, which ran at up to 100 % of its rating. Heat pump ran at its full rating, so it limits what the plant can deliver.

### 3.4 Cooling

| Module | Kind | Rated | Peak | Used | Capital cost |
| --- | --- | ---: | ---: | ---: | ---: |
| Chiller | Absorption chiller | 10 MW | 10 MW | 100 % | 3 MEUR |
| Chiller cooler | Cooler | 24.39 MW | 24.39 MW | 100 % | 2.439 MEUR |

*Table 3.4 - Cooling units: rating, use and capital cost*

2 units make up the cooling part, with a capital cost of 5.439 MEUR, 21 % of the plant's total. The largest is Chiller, rated 10 MW, which ran at up to 100 % of its rating. Chiller and Chiller cooler ran at their full rating, so they limit what the plant can deliver.

### 3.5 Grids

The plant has no grids units.

<div style="page-break-before: always"></div>

## 4 Performance

| Figure | Value |
| --- | ---: |
| Gas bought | 11.72 GWh |
| Heat from the boilers | 24.69 GWh |
| Cold delivered | 23.74 GWh |
| Heat delivered | 111.7 GWh |
| Electricity bought | 10.36 GWh |
| Fuel burned on site | 30.49 GWh |
| Produced gas burned (fuel burned less gas bought) | 18.77 GWh |
| Heat per bought electricity | 10.78 |
| Heat pump COP | 5.52 |

*Table 4.1 - Energy balance of the run*

The plant delivers 111.7 GWh of heat against a demand of 111.7 GWh, so it meets 100 % of it. The boilers give 24.69 GWh, 22 % of the heat delivered. The plant burns 30.49 GWh of fuel on site: 11.72 GWh of gas bought and 18.77 GWh of gas produced with the brine. It buys 10.36 GWh of electricity and 11.72 GWh of gas. Of the heating demand, geothermal brine heat 76 %, heat-pump electricity 4.2 %, backup 19 %. Per unit of electricity bought the plant delivers 10.78 units of heat, a ratio of the whole plant, not the COP of a machine. The heat pumps give 5.52 units of heat per unit of the electricity they take, their COP.

![Days covered](IMG)

*Figure 4.1 - Source that covered the demand on each day*

Of the 365 cooling days, 219 had a demand and 146 had none. Of the days with a demand, 48 were covered by Absorption chiller (geothermal) alone, 171 also needed Peak boiler (chiller drive) and 0 fell short. Of the 365 heating days, 365 had a demand. Of the days with a demand, 48 were covered by Geothermal alone, 317 also needed Peak boiler and 0 fell short.

![Cooling: demand and supply](IMG)

*Figure 4.2 - Cooling: daily mean demand and supply*

Cooling demand peaks at 10 MW (daily mean) on 2027-07-19 and averages 2.71 MW. Peak boiler (chiller drive) runs on 171 days, at most 1.64 MW on 2027-07-19. 2.01e-12 MWh of demand is not met.

![Heating: demand and supply](IMG)

*Figure 4.3 - Heating: daily mean demand and supply*

Heating demand peaks at 30 MW (daily mean) on 2027-01-28 and averages 12.75 MW. Peak boiler runs on 317 days, at most 11.3 MW on 2027-01-28. 1.137e-11 MWh of demand is not met.

| Service | Main supply | Days | Other supply | Days | Short | No demand |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| Cooling | Absorption chiller (geothermal) | 48 | Peak boiler (chiller drive) | 171 | 0 | 146 |
| Heating | Geothermal | 48 | Peak boiler | 317 | 0 | 0 |

*Table 4.2 - Days of each service by the units that covered them*

<div style="page-break-before: always"></div>

## 5 Economics

From case version 3, plant version 1.

| Figure | Value |
| --- | ---: |
| Cost of cold | 35.92 EUR/MWh |
| Cost of heat | 30.55 EUR/MWh |
| Cost of thermal supply | 31.49 EUR/MWh |
| Operating cost | 2.427 MEUR/yr |
| Investment | 25.93 MEUR |
| Annualised cost | 4.267 MEUR/yr |

*Table 5.1 - Cost figures of the design*

The levelised cost of thermal supply is 31.49 EUR/MWh, from an annualised cost of 4.267 MEUR/yr. The plant costs 25.93 MEUR to build and 2.427 MEUR/yr to run.

| Capital cost | Amount | Share |
| --- | ---: | ---: |
| Wells | 14.56 MEUR | 56 % |
| Surface plant | 11.22 MEUR | 43 % |
| Other | 0.15 MEUR | 0.58 % |

*Table 5.2 - Capital cost by part of the plant*

Wells take the largest share of the capital cost, 56 % (14.56 MEUR); the table splits the rest.

| Item | Amount | Unit cost | Source |
| --- | ---: | ---: | --- |
| Drilling | 14.25 MEUR | 1,239 EUR/m | economics.json, capex.drilling |
| Absorption chiller | 3 MEUR | 0.3 EUR/W | economics.json, capex.absorption_chiller |
| Cooler | 2.439 MEUR | 0.1 EUR/W | economics.json, capex.cooler |
| Heat pump | 2.214 MEUR | 0.7379 EUR/W | economics.json, capex.heat_pump |
| Boiler | 1.822 MEUR | 0.06073 EUR/W | economics.json, capex.boiler |
| Degasser | 1 MEUR | 1,000,000 EUR | economics.json, capex.degasser |
| Heat exchanger | 0.75 MEUR | 0.5 EUR/(W/K) | economics.json, capex.heat_exchanger |
| Production pump | 0.3067 MEUR | 0.5 EUR/W | economics.json, capex.production_pump |
| Flare | 0.1 MEUR | 100,000 EUR | economics.json, capex.flare |
| Gas makeup | 0.05 MEUR | 50,000 EUR | economics.json, capex.gas_makeup |

*Table 5.3 - Capital cost by kind of unit, with its unit cost*

The largest items are drilling (55 %), absorption chiller (12 %) and cooler (9.4 %); together they make 76 % of the capital cost.

| Operating cost | Amount | Share |
| --- | ---: | ---: |
| Electricity | 1.096 MEUR/yr | 45 % |
| Fuel | 0.468 MEUR/yr | 19 % |
| CO2 price | 0.4081 MEUR/yr | 17 % |
| Fixed | 0.3521 MEUR/yr | 15 % |
| Chemical | 0.09153 MEUR/yr | 3.8 % |
| Waste | 0.01066 MEUR/yr | 0.44 % |

*Table 5.4 - Yearly operating cost by component*

Electricity is the largest operating cost, 1.096 MEUR/yr or 45 % of the total.

<div style="page-break-before: always"></div>

## 6 Emissions

| Source | CO2 | Share |
| --- | ---: | ---: |
| Fuel burnt in the plant | 7.017 kt | 68 % |
| Methane released | 0.004493 kt | 0.044 % |
| Grid electricity bought | 3.108 kt | 30 % |
| Total | 10.26 kt | 100 % |

*Table 6.1 - CO2 emissions of the run by source*

The plant emits 10.26 kt of CO2 over the run, 75.76 kg/MWh of energy delivered. Fuel burnt in the plant is the largest source, 68 % of the total. They come from 30.49 GWh of fuel and 10.36 GWh of grid electricity.

<div style="page-break-before: always"></div>

## 7 Studies

The result comes from the find the best design study QA-332 retest minimize on cost of thermal supply.

This result is not a sensitivity or uncertainty study.

<div style="page-break-before: always"></div>

## 8 Checks

15 passed, 0 failed, 0 not assessed.

| Check | Status | Value | Limit | Margin | Worst day |
| --- | --- | ---: | --- | ---: | --- |
| Production flow range (d0) | pass | 237.5 m3/h | 50 to 300 m3/h | 62.5 m3/h | 2027-01-01 |
| Production flow range (d1) | pass | 50 m3/h | 50 to 300 m3/h | 0 m3/h | 2027-04-03 |
| Brine cooling limit (d0) | pass | 39.34 K | ≤ 40 K | 0.66 K | 2027-08-04 |
| Brine cooling limit (d1) | pass | 37.59 K | ≤ 40 K | 2.413 K | 2027-05-16 |
| Running time limit (d0) | pass | 330 d | ≤ 330 d | 0 d | - |
| Running time limit (d1) | pass | 330 d | ≤ 330 d | 0 d | - |
| Pump efficiency (d0) | pass | 70 % | = 70 % | - | - |
| Pump efficiency (d1) | pass | 70 % | = 70 % | - | - |
| Full reinjection (d0) | pass | 1 | 1 to 1 | 0 | 2027-03-29 |
| Full reinjection (d1) | pass | 1 | 1 to 1 | 0 | 2027-07-06 |
| Doublet count | pass | 2 | 1 to 3 | 1 | - |
| Heat delivered (Heat users) | pass | 0 % | ≤ 1 % | 1 % | - |
| Cold delivered (Cool users) | pass | 0 % | ≤ 1 % | 1 % | - |
| Heating supply temperature (Heat users) | pass | 100 degC | ≥ 100 degC | 0 degC | 2027-01-01 |
| Cooling supply temperature (Cool users) | pass | 20 degC | ≤ 20 degC | 0 degC | 2027-03-22 |

*Table 8.1 - Constraint checks of the design*

No check fails. Every check could be assessed.

The checks are the 15 rules of the case. They bound brine cooling, count, production flow, pump efficiency, reinjection ratio, temperature and unmet share on the cooling supply, doublet and heating supply. The engine can also bound approach, co2, cold output, cop, duty, electricity bought, fuel input, gas bought, gas burned, heat output, heat surplus, injection temperature, intake gas fraction, intake pressure, lift, power output, production temperature, pump power, unmet and wellhead pressure; the case sets no rule on them, so they are not checked. Every check judges the run of 365 d only: nothing that develops over a longer life of the plant is checked.

<div style="page-break-before: always"></div>

## 9 Assumptions and sources

| Input | Value | Source |
| --- | --- | --- |
| Case | hackathon_2026, version 3 | Project case |
| Plant | version 1 | Project plant |
| Economics | economics.json | Case file |
| Simulation period | 2027-01-01 to 2028-01-01, in steps of 1 d | Case |

*Table 9.1 - Inputs the result was computed from*

Every figure of this report is computed by the engine from these inputs; a value the inputs do not give is reported as missing, never assumed.

| Economic value | Amount | Source |
| --- | --- | --- |
| Currency | EUR | economics.json |
| Price year | 2,015 | economics.json |
| Discount rate | 0.05 | economics.json |
| Analysis period | 25 yr | economics.json |
| Capex drilling | 1,239 EUR/m | economics.json |
| Capex heat pump | 0.7379 EUR/W | economics.json |
| Capex boiler | 0.06073 EUR/W | economics.json |
| Capex chp | 0.9616 EUR/W | economics.json |
| Capex degasser | 1,000,000 EUR | economics.json |
| Capex compression chiller | 0.3 EUR/W | economics.json |
| Capex production pump | 0.5 EUR/W | economics.json |
| Capex injection pump | 0.5 EUR/W | economics.json |
| Capex absorption chiller | 0.3 EUR/W | economics.json |
| Capex adsorption chiller | 0.3 EUR/W | economics.json |
| Capex heat exchanger | 0.5 EUR/(W/K) | economics.json |
| Capex flare | 100,000 EUR | economics.json |
| Capex gas makeup | 50,000 EUR | economics.json |
| Capex cooler | 0.1 EUR/W | economics.json |
| Capex pipe | 500 EUR/m | economics.json |
| Opex fixed drilling | 1 %/yr | economics.json |
| Opex fixed heat pump | 0.2239 %/yr | economics.json |
| Opex fixed boiler | 3.25 %/yr | economics.json |
| Opex fixed chp | 1.026 %/yr | economics.json |
| Opex fixed degasser | 2 %/yr | economics.json |
| Opex fixed compression chiller | 2 %/yr | economics.json |
| Opex fixed production pump | 2 %/yr | economics.json |
| Opex fixed injection pump | 2 %/yr | economics.json |
| Opex fixed absorption chiller | 2 %/yr | economics.json |
| Opex fixed adsorption chiller | 2 %/yr | economics.json |
| Opex fixed heat exchanger | 1 %/yr | economics.json |
| Opex fixed flare | 2 %/yr | economics.json |
| Opex fixed gas makeup | 2 %/yr | economics.json |
| Opex fixed cooler | 2 %/yr | economics.json |
| Opex fixed pipe | 0.5 %/yr | economics.json |
| Opex variable chemical | 3 EUR/kg | economics.json |
| Opex variable waste disposal | 0.2 EUR/kg | economics.json |
| Energy electricity | 105.8 EUR/MWh | economics.json |
| Energy gas | 39.92 EUR/MWh | economics.json |
| Carbon price | 57.03 EUR/t | economics.json |
| Revenue heat | 60 EUR/MWh | economics.json |
| Revenue cold | 60 EUR/MWh | economics.json |
| Accounting allocation heat cost share | 0.8 | economics.json |
| Accounting gwp standard | IPCC AR6 WG1 table 7.15, GWP100 of fossil methane | economics.json |
| Accounting gwp CH4 | 29.8 | economics.json |

*Table 9.2 - Economic values of the case*

The case states 44 economic values. 4 of them carry an uncertainty range.

<div style="page-break-before: always"></div>

## Appendix A - Agent log and tokens

No assistant run was chosen.

<div style="page-break-before: always"></div>

## Appendix B - Modules and connections

Plant: HackathonPlant

| Module | Type | Category | Connected to | Parameters |
| --- | --- | --- | --- | ---: |
| d0 | Doublet | plants | return_in <- injection.branch1_out, power_in <- grid.power_out | 85 |
| d1 | Doublet | plants | return_in <- injection.branch2_out, power_in <- grid.power_out | 85 |
| hx | HeatExchanger | exchangers | hot_in <- dosing.fluid_out, cold_in <- heat_return.fluid_out | 8 |
| air | Atmosphere | environment | gas_in <- boiler.flue_out, gas_in <- flare.flue_out, heat_in <- flare.loss_out, heat_in <- boiler.loss_out, air_in <- chiller_cooler.air_out | 1 |
| grid | ElectricityGrid | grids |  | 2 |
| flare | Flare | treatment | gas_in <- makeup.excess_out | 1 |
| loads | Splitter | piping | fluid_in <- boiler.fluid_out | 0 |
| waste | WasteGrid | grids | waste_in <- desander.waste_out | 0 |
| boiler | Boiler | heating | fuel_in <- makeup.fuel_out, fluid_in <- heat_pump.sink_out | 3 |
| dosing | InhibitorDosing | treatment | fluid_in <- desander.fluid_out, chemical_in <- chemicals.chemical_out | 1 |
| makeup | GasMakeup | piping | gas_in <- degasser.gas_out, grid_in <- gas_grid.gas_out | 0 |
| chiller | AbsorptionUnit | cooling | power_in <- grid.power_out, generator_in <- loads.branch2_out, chilled_in <- cool_users.return_out, cooling_in <- chiller_cooler.fluid_out | 10 |
| degasser | Degasser | treatment | fluid_in <- production.fluid_out | 4 |
| desander | Desander | treatment | fluid_in <- degasser.liquid_out | 3 |
| gas_grid | GasGrid | grids |  | 1 |
| chemicals | ChemicalGrid | grids |  | 0 |
| heat_pump | HeatPump | heating | source_in <- hx.hot_out, power_in <- grid.power_out, sink_in <- hx.cold_out | 9 |
| injection | Splitter | piping | fluid_in <- heat_pump.source_out | 0 |
| cool_users | CoolingGrid | grids | supply_in <- chiller.chilled_out | 5 |
| heat_users | HeatingGrid | grids | supply_in <- loads.branch1_out | 4 |
| production | Mixer | piping | branch1_in <- d0.supply_out, branch2_in <- d1.supply_out | 0 |
| heat_return | Mixer | piping | branch1_in <- heat_users.return_out, branch2_in <- chiller.generator_out | 0 |
| chiller_cooler | Cooler | exchangers | power_in <- grid.power_out, fluid_in <- chiller.cooling_out, air_in <- air.air_out | 6 |

Total parameters: 231
