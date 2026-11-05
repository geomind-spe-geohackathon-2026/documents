# Assumptions for the GEMINI hackathon case (2026)

Upload this file next to the three competition files (`GEMINI_Heating_Demand_Daily_2027.csv`,
`GEMINI_Cooling_Demand_Daily_2027.csv`, `GEMINI_Hackathon_Challenge_Requirements.pdf`). It holds
every value the case and the economics need that the competition files do not give. The user
approves these values by uploading this file: use them as given, cite this file as their source,
and do not ask for them again.

Each value says where it comes from:
- **Organisers**: answers of the organisers on Discord #technical-q-and-a, 2026-11-04.
- **Team**: the team's assumption, taken from gemini's sample case
  (`gemini/examples/hackathon_2026/case.json` and `economics.json`).

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
| Sand in the brine | 20 mg/l | Team |
| Grid electricity CO2 intensity | 300 g/kWh | Organisers |
| Bought natural gas composition (mole fraction) | CH4 0.825, C2H6 0.040, C3H8 0.013, CO2 0.012, N2 0.111 | Team |
| Heat pump / compression chiller efficiency | 50 % of the Carnot COP | Team (Frutschi, ABB Review 5/1996, pp. 33-34) |

## Requirements: tolerances the PDF does not give

| Requirement | Rule | Source |
|---|---|---|
| Heat delivered | Unmet share of the yearly heat demand at most 1 %, over all 365 days | Team |
| Cold delivered | Unmet share of the yearly cold demand at most 1 %, over all 365 days | Team |
| Supply temperatures 100 degC / 20 degC | Hold while that supply is running (a day with zero cooling demand is no violation) | Team |
| Equal production and injection volume | Reinjection ratio 0.99999 to 1.00001 while running | Team |
| Production flow 50-300 m3/h, brine cooling <= 40 K | Per doublet, in every step in which the doublet runs | PDF |
| Pump efficiency | 0.70 | PDF |
| Pump intake (only if the design checks it) | Free gas at most 18.75 % of the volume; intake pressure at least 5 bar | Team |
| Well depth search range | 2000 to 3500 m | Team |

## Economics

Currency EUR, price year 2015.

| Item | Value | Source |
|---|---|---|
| Discount rate | 5 %/yr | Team |
| Analysis period | 25 years | Team |
| Electricity price | 105.75 EUR/MWh | Team |
| Natural gas price | 39.92 EUR/MWh | Team |
| CO2 price | 57.03 EUR/t | Team |
| Heat revenue / cold revenue | 60 EUR/MWh each | Team |
| Cost share of heat (allocation heat vs cold) | 0.8 | Team |
| CH4 global warming potential | 29.8 (IPCC AR6 WG1 table 7.15, GWP100 fossil methane) | Team |
| Chemicals / waste disposal | 3 EUR/kg / 0.2 EUR/kg | Team |

Capital cost and fixed operating cost (% of capital cost per year):

| Equipment | Capex | Fixed opex |
|---|---|---|
| Drilling | 1239.13 EUR/m | 1 %/yr |
| Heat pump | 0.738 EUR/W | 0.224 %/yr |
| Gas boiler | 0.0607 EUR/W | 3.25 %/yr |
| CHP | 0.962 EUR/W | 1.026 %/yr |
| Degasser | 1,000,000 EUR | 2 %/yr |
| Compression chiller | 0.3 EUR/W | 2 %/yr |
| Absorption chiller | 0.3 EUR/W | 2 %/yr |
| Adsorption chiller | 0.3 EUR/W | 2 %/yr |
| Production pump / injection pump | 0.5 EUR/W each | 2 %/yr |
| Heat exchanger | 0.5 EUR/(W/K) | 1 %/yr |
| Flare | 100,000 EUR | 2 %/yr |
| Gas make-up | 50,000 EUR | 2 %/yr |
| Cooler | 0.1 EUR/W | 2 %/yr |
| Pipe | 500 EUR/m | 0.5 %/yr |

## Uncertainty ranges (studies only)

| Value | Range |
|---|---|
| Electricity price | uniform 80 to 140 EUR/MWh |
| Natural gas price | triangular 25 to 70 EUR/MWh, mode 39.92 |
| CO2 price | triangular 30 to 110 EUR/t, mode 57.03 |
| Discount rate | normal, std 1 %, 2 to 8 % |
| Geothermal gradient | normal, std 2 K/km, 25 to 35 K/km |
| Permeability | triangular 100 to 400 mD, mode 200 |
