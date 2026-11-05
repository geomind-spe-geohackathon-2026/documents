# Handbook of Techno-Economic and Environmental Assessment of Geothermal Heating and Cooling Plants

A general reference for agents and engineers who cost, compare and judge geothermal heating and
cooling plants. Written for the GeoMind project, 2026-11-05.

---

## Preface

This handbook explains how to put a price and a carbon footprint on a geothermal plant that
delivers heat, cold or both, and how to use those numbers to choose between designs. It is
general: it holds for any case, any site and any set of prices. One chapter (chapter 17) works
through the GEMINI hackathon 2026 sample as an example, with numbers recomputed from
`gemini/examples/hackathon_2026` with gemini 0.6.13.

The method is the standard method of engineering economics for energy projects: present value,
annuity, levelised cost, net present value, payback, sensitivity and uncertainty. These
definitions are textbook material. A classic reference that sets them out for renewable energy is
Short, Packey and Holt (1995), *A Manual for the Economic Evaluation of Energy Efficiency and
Renewable Energy Technologies*, NREL/TP-462-5173. This handbook summarises that body of method
and applies it to geothermal heating and cooling. Where a formula is the one gemini uses, the
handbook says so and gives gemini's exact names (chapter 16).

Three rules run through every chapter:

1. **Every number has a source.** A value without a source is an assumption and is labelled as
   one. Values in this handbook carry their source in brackets or in the table beside them;
   values the handbook computed itself are marked **(derived)** with the inputs shown.
2. **No default values.** A missing price, rate or factor is a gap to fill from the user's files,
   the Knowledge base or a connector, with the user's approval. It is never filled silently.
3. **Real and nominal never mix.** Prices, the discount rate and the price year must belong to
   the same convention (chapter 4 and chapter 5).

The handbook does not explain how to call any agent tool. How to run costs, sensitivity and
uncertainty with the tools is written in one place only: the `economics` skill
(`geomind/geomind/skills/economics/SKILL.md`). Chapter 16 names the skill where a tool is needed.

## How to read this handbook

Each section (`###`) stands alone: it defines its terms, gives its formulas and its sources, and
names the sections it depends on. An agent that needs one answer reads one section. The table of
contents below gives the number and title of every section; search for the title.

Units follow SI with the display units of gemini: money in EUR or MEUR, energy in MWh, power in
MW, CO2 in t or kt, levelised costs in EUR/MWh.

---

## Table of contents

1. Scope and system boundary
   - 1.1 What a techno-economic and environmental assessment is
   - 1.2 System boundary, functional unit and reporting period
   - 1.3 The chain from case to decision
2. Capital cost (capex)
   - 2.1 Cost structure of a geothermal heating and cooling plant
   - 2.2 Drilling and wells: cost against depth
   - 2.3 Downhole and injection pumps
   - 2.4 Surface plant
   - 2.5 Cost bases, factor estimates and scaling
   - 2.6 Indirect costs, owner's costs and contingency
   - 2.7 Whole-plant benchmarks for checking an estimate
3. Operating cost (opex)
   - 3.1 Fixed operation and maintenance
   - 3.2 Variable operation and maintenance
   - 3.3 Energy bought: electricity and gas
   - 3.4 Chemicals and waste
   - 3.5 Well workovers and pump replacement
   - 3.6 Carbon cost in the opex
4. Prices, currency, price year and escalation
   - 4.1 Nominal and real money
   - 4.2 Price year and conversion with the HICP
   - 4.3 Currency conversion
   - 4.4 Escalation of energy and carbon prices
5. Discounting and the time value of money
   - 5.1 The discount rate
   - 5.2 Present value, annuity factor and capital recovery factor
   - 5.3 Analysis period, technical lifetime, replacements and residual value
   - 5.4 Timing conventions
6. Levelised costs
   - 6.1 Levelised cost of heat (LCOH)
   - 6.2 Levelised cost of cold (LCOC)
   - 6.3 Levelised cost of thermal supply (LCTS)
   - 6.4 Allocating shared costs between heat and cold
   - 6.5 What a levelised cost does not say
7. Revenue, profitability and subsidies
   - 7.1 Heat and cold prices
   - 7.2 Net present value, payback and break-even price
   - 7.3 Operating subsidies: SDE++ as an example
   - 7.4 Investment subsidies, risk schemes and taxes
8. Carbon pricing
   - 8.1 The EU Emissions Trading System
   - 8.2 Using a carbon price in an assessment
9. CO2 accounting
   - 9.1 Boundary and scopes
   - 9.2 Direct CO2 from produced gas and combustion
   - 9.3 Methane and global warming potentials (IPCC AR6)
   - 9.4 Grid electricity emission factors
   - 9.5 Reference systems and avoided emissions
   - 9.6 CO2 abatement cost
10. Energy prices
   - 10.1 Eurostat price statistics and consumption bands
   - 10.2 Choosing a band and a tax level
11. Cost data sources and their quality
   - 11.1 Main sources for geothermal heating and cooling
   - 11.2 Grading the quality of a figure
   - 11.3 Checklist before a figure enters a case
12. Sensitivity analysis
   - 12.1 One-at-a-time sensitivity
   - 12.2 Tornado charts
   - 12.3 Break-even and switching values
13. Uncertainty analysis
   - 13.1 Distributions for uncertain inputs
   - 13.2 Monte Carlo sampling
   - 13.3 Percentiles, risk and reporting
14. Comparing configurations and deciding
   - 14.1 Like-for-like comparison
   - 14.2 Decision criteria: cost, CO2, robustness
   - 14.3 Multi-criteria decisions and Pareto fronts
15. Common mistakes
16. How gemini computes economics
   - 16.1 The economics file (`economics.json`)
   - 16.2 Capex by equipment kind
   - 16.3 Opex
   - 16.4 Annualised cost, LCOH, LCOC, LCTS
   - 16.5 NPV, payback and subsidy
   - 16.6 CO2
   - 16.7 Conventions and limits
   - 16.8 Errors, missing values and tools
17. Worked example: GEMINI hackathon 2026
   - 17.1 The case
   - 17.2 Economic inputs and their sources
   - 17.3 Capex of HeatingHeatPumpCoolingPlant
   - 17.4 Opex
   - 17.5 Levelised costs by hand
   - 17.6 NPV, payback and break-even price
   - 17.7 CO2
   - 17.8 Sensitivity by hand
   - 17.9 Six configurations compared
   - 17.10 Lessons from the example
- Appendix A. Symbols and formulas
- Appendix B. References

---

## 1. Scope and system boundary

### 1.1 What a techno-economic and environmental assessment is

A techno-economic assessment (TEA) asks what a technical design costs over its life and what it
earns. An environmental assessment asks what it emits. For a geothermal heating and cooling
plant the two together answer:

- What is the investment (capex) and the yearly operating cost (opex)?
- What does one MWh of heat or cold cost over the life of the plant (levelised cost)?
- Does the plant pay back at the expected heat and cold prices (NPV, payback)?
- How much CO2-equivalent does it emit per year, and compared with what alternative?
- Which inputs drive these answers, and how sure are they (sensitivity, uncertainty)?
- Which design is best for the criteria the user sets?

The physics comes first: the costs of energy bought, the sizes of equipment and the heat and cold
delivered all come from a simulation of the plant over a representative year. A TEA on numbers
that the plant cannot deliver is worthless; check the design against its requirements before
reading its costs.

### 1.2 System boundary, functional unit and reporting period

**System boundary.** State what is inside the plant: wells, pumps, gas handling, heat exchangers,
heat pumps, chillers, boilers, coolers, the pipes up to a stated delivery point. State what is
outside: the district network beyond that point, buildings, the electricity grid, the gas grid.
Energy that crosses the boundary is bought (electricity, gas) or sold (heat, cold, electricity).

**Functional unit.** The unit the cost is expressed per: 1 MWh of useful heat delivered, 1 MWh of
useful cold delivered, or 1 MWh of thermal supply (heat plus cold). Useful means delivered at the
boundary at the required temperature, not produced at the wellhead.

**Reporting period.** A simulation covers a period (often one year in daily or hourly steps). The
assessment scales it to a year and assumes that year repeats over the analysis period, unless the
method models degradation or changing prices year by year (section 5.3).

### 1.3 The chain from case to decision

1. **Case**: site, demand, requirements, utilities and economics (prices, rates, factors).
2. **Design**: a plant structure and its sizes.
3. **Simulation**: energy flows, temperatures, pump powers and emissions per step.
4. **Check**: requirements met or not (verdict).
5. **Costs and CO2**: capex, opex, levelised costs, NPV, payback, emissions.
6. **Robustness**: sensitivity and uncertainty of the costs.
7. **Decision**: compare designs on the user's criteria.

A change upstream invalidates everything downstream: a new price changes the costs but not the
simulation; a new return temperature changes the simulation and everything after it.

---

## 2. Capital cost (capex)

### 2.1 Cost structure of a geothermal heating and cooling plant

The capex is the investment needed before the plant runs. For a deep geothermal heating and
cooling plant it splits into:

| Block | Items | Typical cost basis |
|---|---|---|
| Subsurface | Drilling, casing, completion, well testing, drill site | per m of well, per well, per site |
| Production lift | Electric submersible pump (ESP) or line-shaft pump | per kW of shaft power, per unit |
| Injection | Injection pump, filters | per kW, per unit |
| Gas handling | Degasser (separator), flare, gas make-up, CHP or boiler on the produced gas | fixed amount, per kW |
| Heat transfer | Brine-to-water heat exchangers | per W/K of conductance, per W of duty |
| Heat upgrade | Heat pumps, peak boilers, electric boilers | per W of capacity |
| Cold | Absorption, adsorption or compression chillers, coolers (dry or wet) | per W of capacity |
| Distribution inside the boundary | Pipes | per m, or per MW and m |
| Storage | Hot water or ice storage | per m3 or per MWh |
| Indirect | Engineering, permits, project management, owner's costs, contingency | % of direct cost |

In deep geothermal plants the wells usually dominate. In the worked example (chapter 17) drilling
is 37.5 % of the capex of the design with a 15 MW heat pump, and the heat pump 33.5 %
**(derived: 12.39 / 33.02 and 11.07 / 33.02 MEUR, section 17.3)**.

### 2.2 Drilling and wells: cost against depth

Drilling cost rises faster than linearly with depth: deeper wells need more casing strings,
heavier rigs, more days and more risk. A single cost per metre is therefore valid only near the
depth it was measured at.

Sourced Dutch figures for a doublet (two wells) show the trend (gemini cost catalogue,
`gemini/docs/cost-sources/sources.csv`, rows `drilling-nl-2013-*`, from Mijnlieff, Ramsak, Lako
et al., EGC 2013 slides, slide 26, status *verified*):

| Depth of each well | Net drilling cost per doublet | Per metre (2013) | Per metre (EUR 2015) |
|---|---|---|---|
| 2300 m | 5.7 MEUR | 1239.1 EUR/m | 1246.83 EUR/m |
| 3000 m | 11.0 MEUR | 1833.3 EUR/m | 1844.74 EUR/m |
| 4000 m | 16.5 MEUR | 2062.5 EUR/m | 2075.37 EUR/m |

The per-metre figures divide the doublet cost by two wells times the depth; the catalogue notes
that the slide does not say "per doublet" explicitly. An ECN cost curve (Straathof 2012, MSc
thesis, ECN-O--12-043, p. 16, catalogue rows `drilling-ecn-2012-*`, status *secondary*) gives
cost in MEUR as `1e-7 x² + 0.0018 x + 0.3859` with `x` the well depth in m (R² = 0.596).

Rules:

- Price drilling by **measured depth** (along the hole), not true vertical depth, for deviated
  wells.
- Use a **depth table** when the design searches over depth; a single per-metre price favours
  deep wells unfairly. gemini accepts a table of cost per metre against depth (section 16.2).
- Add the **drill site** (location, access, mud handling) once per site: 300 000 EUR (2019) per
  location (catalogue row `drilling-location-surface`, from *Geothermal Energy* 2021, Table 4,
  status *secondary*).
- Drilling cost depends strongly on country, rig market and year; a figure from another market
  needs a stated reason to apply.

### 2.3 Downhole and injection pumps

The production well usually needs an electric submersible pump (ESP); reinjection may need a
surface injection pump. Their capex is small next to the wells, but their power drives the
electricity bill and their failures drive the opex (section 3.5).

Sourced figures (gemini cost catalogue):

| Row | Figure | Status |
|---|---|---|
| `esp-unit-2019` | 800 000 EUR per ESP unit, recurring every 5 years (*Geothermal Energy* 2021, Table 4, quoting van't Spijker and Ungemach) | secondary |
| `esp-geophires-500kw` | 0.593 USD/W at 500 kW, from the GEOPHIRES-X pump cost correlation (NREL open-source code) | secondary |
| `injection-pump-geophires-500kw` | 0.733 USD/W at 500 kW, same code | secondary |

A cost per W of shaft power needs the pump's rated flow and head. Rate a pump at its nominal
(design) flow and head, not at its average operating point.

### 2.4 Surface plant

**Heat exchangers.** Brine-to-water plate exchangers. Cost scales with area, which scales with
the conductance UA (W/K) for a given duty and temperature approach. A cost per W of duty hides the
approach temperature; a cost per W/K does not.

**Heat pumps.** Large electric heat pumps raise geothermal heat to the network temperature or
recover heat from the cooling side. Sourced: Danish Energy Agency (DEA), *Technology Data for
Generation of Electricity and District Heating*, version 0019 (August 2026), sheet "40 Comp. hp,
waste heat 10 MW": nominal investment 0.95 MEUR/MW of heat (EUR 2025), fixed O&M 2126.745
EUR/MW/yr (as quoted in `gemini/examples/hackathon_2026/README.md`).

**Boilers.** Gas peak and backup boilers: DEA version 0019, sheet "44 Natural Gas DH Only",
0.0638024 MEUR/MW (EUR 2020), fixed O&M 2073.58 EUR/MW/yr (same README).

**CHP on produced or bought gas.** DEA version 0019, sheet "06 Gas engines, natural gas",
1.01020 MEUR/MW electric (EUR 2020), fixed O&M 10367.88 EUR/MW_e/yr (same README).

**Chillers.** Absorption (LiBr, driven by heat at roughly 80 °C and above), adsorption (silica
gel, lower driving temperature) and compression chillers. The DEA electricity and district
heating catalogue has no chiller sheet (same README). Catalogue rows (EUR 2015 per W of cold):
absorption 0.234 to 0.438, compression 0.159, adsorption 0.827 to 0.859 (rows
`absorption-chiller-*`, `compression-chiller-ecos-2023`, `adsorption-chiller-*`; see the
catalogue for status).

**Coolers.** Dry coolers 0.049 to 0.107 EUR/W, wet cooling towers 0.022 to 0.027 EUR/W (EUR
2015, IEA 2014 rows `dry-cooler-iea-2014-*`, `cooling-tower-iea-2014-*`).

**Gas handling.** A degasser separates the associated gas before the exchangers; the gas is then
flared, burnt in a boiler or CHP, or sold. A Dutch reserve of 1 MEUR per project (2013) for
"separation of hydrocarbons" (catalogue row `degasser-nl-2013`, status *secondary*) is the only
sourced figure in the catalogue.

**Pipes.** DEA version 0019 distribution and transmission rows: 636 and 1148 EUR2015/m for
distribution pipes of 1 to 5 MW and 5 to 25 MW, 49 EUR2015/MW/m for transmission (catalogue rows
`pipe-dea-2025-*`).

### 2.5 Cost bases, factor estimates and scaling

A **cost factor** turns a size into money: EUR/m of well, EUR/W of capacity, EUR/(W/K) of
conductance, EUR per unit. The size must be the design (nameplate) size, not the average load.

**Economies of scale.** Equipment cost rarely scales linearly with size. The common power law is
`C2 = C1 · (S2 / S1)^n` with an exponent `n` below 1 (often quoted near 0.6 for process
equipment, the "six-tenths rule"; treat any exponent as an assumption unless a source gives it for
that equipment). A linear factor (EUR/W) taken from a 10 MW machine is fair for 5 to 20 MW and
poor for 0.5 MW or 100 MW. The DEA sheets give different specific costs for different sizes for
this reason.

**Factor estimate.** At early stages the total capex is the sum of the main equipment costs, each
from its factor, plus indirect costs as percentages (section 2.6). The accuracy of such an
estimate is low (section 11.2).

### 2.6 Indirect costs, owner's costs and contingency

Direct costs buy equipment and its installation. **Indirect costs** cover engineering, project
management, permits, insurance during construction, site surveys and commissioning. **Owner's
costs** cover the developer's own staff, land, legal and financing fees. **Contingency** covers
items that will be spent but cannot be named yet; it is not a margin for risks outside the scope.

Rules:

- State whether each cost factor already includes installation and indirect costs. The DEA sheets
  give a "nominal investment (total)"; read their notes for what "total" includes.
- Do not add contingency twice: a catalogue figure for a whole plant usually includes some.
- The size of the contingency depends on the maturity of the estimate (section 11.2); take it
  from a source or state it as an assumption with its reason. This handbook gives no default.
- For geothermal wells, a separate **exploration risk** (the chance that the reservoir does not
  deliver) is usually treated by insurance or guarantee schemes (section 7.4), not by contingency.

### 2.7 Whole-plant benchmarks for checking an estimate

A bottom-up capex should be checked against whole-plant figures. Sourced benchmarks (gemini cost
catalogue, all per W of heat capacity, including wells):

| Row | Plant | Figure | Price year |
|---|---|---|---|
| `plant-dea-2025-2000m-21mw` | DEA sheet 45.1.b, 2 wells of 2000 m, 21 MW, 80/40 °C, with heat pump | 1.9 EUR/W | 2025 |
| `plant-dea-2025-2000m-62mw` | DEA sheet 45.3, 6 wells of 2000 m, 62 MW | 1.75 EUR/W | 2025 |
| `plant-dea-2025-1200m-15mw` | DEA sheet 45.1.a, 1200 m, 15 MW | 2.436 EUR/W | 2025 |
| `plant-pbl-2026-under-12mw` | PBL, SDE++ 2026 final advice, NL deep geothermal below 12 MW (reference 8.7 MW), Table 11.7a | 2.463 EUR/W | 2026 |
| `plant-pbl-2026-12-20mw` | Same, 12 to 20 MW (reference 15.9 MW), Table 11.7b | 1.719 EUR/W | 2026 |
| `plant-pbl-2026-over-20mw` | Same, 20 MW and above (reference 27.4 MW), Table 11.7c | 1.34 EUR/W | 2026 |

All rows status *verified* in the catalogue. Use these to check the order of magnitude of a
design, never as its cost: they do not split by component, and they include items a component
estimate may leave out.

---

## 3. Operating cost (opex)

### 3.1 Fixed operation and maintenance

Fixed O&M is paid whether the plant runs or not: staff, inspection, insurance, routine
maintenance. It is given either as a share of capex per year (%/yr) or as an amount per MW of
capacity per year (EUR/MW/yr).

Sourced examples:

| Source | Figure | As % of capex (derived) |
|---|---|---|
| DEA 0019, large heat pump (sheet 40) | 2126.745 EUR/MW/yr over 0.95 MEUR/MW | 0.2239 %/yr |
| DEA 0019, gas boiler (sheet 44) | 2073.58 EUR/MW/yr over 0.0638 MEUR/MW | 3.25 %/yr |
| DEA 0019, gas engine CHP (sheet 06) | 10367.88 EUR/MW_e/yr over 1.0102 MEUR/MW_e | 1.026 %/yr |
| DEA 0019, geothermal plant 2000 m (sheet 45.1.b, row `opex-plant-dea-2025-2000m`) | 60 000 EUR/MW/yr | 3.2 %/yr of 1.9 EUR/W **(derived)** |
| PBL SDE++ 2026, NL plant below 12 MW (row `opex-plant-pbl-2026-under-12mw`) | 117 EUR/kW/yr | 4.75 %/yr of 2463 EUR/kW (catalogue note) |
| PBL SDE++ 2026, NL plant 20 MW and above (row `opex-plant-pbl-2026-over-20mw`) | 121 EUR/kW/yr | 9.0 %/yr of 1340 EUR/kW (catalogue note) |

The first three percentages are from `gemini/examples/hackathon_2026/README.md`. Note the spread:
a whole Dutch plant carries 4.75 to 9 % of capex per year, a heat pump alone 0.22 %. A whole-plant
figure includes well maintenance and pump replacements; a component figure does not. Do not add a
component fixed O&M and a whole-plant fixed O&M for the same equipment.

### 3.2 Variable operation and maintenance

Variable O&M scales with the energy produced: wear, consumables, part of the maintenance. DEA
version 0019 gives a plant variable O&M of 3.07 EUR/MWh of heat (EUR 2025) for its geothermal
sheets 45.1.b and 45.3 (catalogue row `opex-variable-dea-2025`, status *verified*; the row notes
that it includes chemical treatment). Do not add a separate chemical cost on top of a variable
O&M that already includes it.

### 3.3 Energy bought: electricity and gas

The largest running cost of a geothermal heat pump plant is usually electricity: ESPs, injection
pumps, circulation pumps, heat pumps and compression chillers. Gas is bought for peak boilers when
the produced gas does not suffice.

- Bill = energy bought in each step × price in that step, summed over the year.
- Price the energy at the **delivered price paid by the plant**: the consumption band, the network
  charges and the non-recoverable taxes that apply (chapter 10).
- For gas, state the heating value convention. Eurostat quotes gas prices per kWh of **gross**
  calorific value; a model that counts fuel on the **lower** heating value must convert, or the
  bill is off by the ratio of the two (about 10 % for natural gas; a general figure, check it for
  the gas in question). gemini prices gas per energy of its lower heating value (schema of
  `economics.energy.gas`).
- Co-produced gas burnt on site costs nothing to buy, but its combustion emits CO2 (chapter 9).

### 3.4 Chemicals and waste

Brines need scale and corrosion inhibitors; filters and desanders produce solid waste (sand,
scale) and sometimes contaminated sludge. Cost = mass used or discarded × price per kg. Sourced
data are scarce: the gemini catalogue has placeholders for scale and corrosion inhibitors, and a
proxy for non-hazardous waste of 64 EUR/t (Dutch sewage sludge processing, PBL SDE++ 2026 final
advice, p. 104, row `waste-disposal-proxy-sewage-sludge`, status *secondary*). The proxy is not
valid for naturally occurring radioactive material (NORM) or hazardous scale, which cost much more
to dispose of.

### 3.5 Well workovers and pump replacement

Wells need periodic interventions: cleaning, acid jobs, pump pulls, casing repairs. ESPs have
limited run lives. The gemini catalogue holds one sourced pair: an ESP costs 800 000 EUR (2019)
per unit and is replaced every 5 years (rows `esp-unit-2019` and `esp-replacement-interval`,
*Geothermal Energy* 2021, Table 4; the catalogue note says DEA note E agrees on roughly once every
five years). Model replacements either:

- as discrete cash flows in the years they fall (exact; needs a yearly cash-flow model), or
- as an equivalent yearly cost: the present value of the replacements spread with the capital
  recovery factor (section 5.2).

A whole-plant fixed O&M (section 3.1) may already include them. State which.

### 3.6 Carbon cost in the opex

Where a plant must pay for its emissions (chapter 8), the carbon cost is emissions × carbon price
and is part of the opex. Decide which emissions are priced: direct combustion and process
emissions are, under an emissions trading scheme, the operator's; the CO2 of grid electricity is
already in the electricity price where the generators pay for allowances. Pricing it again in the
plant's opex counts it twice **in a financial view**; in a social cost view it may be intended.
Say which view the assessment takes (gemini's convention: section 16.7).

---

## 4. Prices, currency, price year and escalation

### 4.1 Nominal and real money

- **Nominal** (current) money: amounts as they will be paid, including inflation.
- **Real** (constant) money: amounts in the purchasing power of one base year, the **price year**.

A real analysis uses real prices and a **real** discount rate; a nominal analysis uses escalated
prices and a **nominal** rate. The two give the same NPV when done consistently (Fisher relation:
`1 + i_nominal = (1 + i_real)(1 + inflation)`). Mixing them, for example real prices with a
nominal rate, undervalues every future year.

### 4.2 Price year and conversion with the HICP

Every money figure must be brought to the price year of the case before it is added to another.
In the euro area the usual index is the Harmonised Index of Consumer Prices (HICP):

`value_in_year_b = value_in_year_a × HICP(b) / HICP(a)`

Euro-area HICP, all items, annual average, 2015 = 100 (Eurostat `prc_hicp_aind`, unit
`INX_A_AVG`, coicop `CP00`, geo `EA`, update of 2026-02-06; as tabulated in
`gemini/docs/cost-sources/README.md`):

| 2008 | 2010 | 2012 | 2013 | 2014 | 2015 | 2017 | 2019 | 2020 | 2023 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| 91.38 | 93.14 | 98.05 | 99.38 | 99.81 | 100.00 | 101.78 | 104.80 | 105.06 | 123.15 | 128.75 |

(The 2020 value is from `gemini/examples/hackathon_2026/README.md`.)

Example **(derived)**: the DEA heat pump at 0.95 MEUR/MW in EUR 2025 is
`0.95 × 100 / 128.75 = 0.7379 MEUR/MW` in EUR 2015.

Caveats:

- The HICP is a consumer price index. Capital goods, drilling and steel can move faster or slower.
  The cost catalogue notes that DEA observed pipe prices rising faster than inflation, so values
  deflated from 2025 to 2015 with the HICP are approximate.
- Where an index year is not yet published (2026 at the time of the catalogue), state the proxy
  used; the catalogue uses the 2025 index, which makes 2026 values run high in 2015 money.
- A figure whose source gives no price year needs an assumed year, stated beside it.
- Industry-specific indices exist (for example drilling or plant cost indices); use one only with
  its source, and use the same index for all figures of a kind.

### 4.3 Currency conversion

Convert at the exchange rate of the **price year** of the figure, then deflate within the target
currency, or deflate first and convert at the base-year rate; do it the same way for every figure.
A purchasing-power-parity rate is more suitable than a market rate when the cost is local labour
and services. gemini does not convert currencies: `economics.currency` is a label (section 16.1).

### 4.4 Escalation of energy and carbon prices

In a real analysis a price that is expected to rise faster than general inflation needs a **real
escalation rate**. Energy and carbon prices are the usual candidates. Escalation is an assumption
that needs a source (for example a published price scenario). Without one, a constant real price
over the analysis period is the transparent choice, and the range of plausible futures goes into
the sensitivity and uncertainty analysis (chapters 12 and 13).

---

## 5. Discounting and the time value of money

### 5.1 The discount rate

The discount rate turns future money into present money. Its value is a choice of the
assessment, with large effect on capital-intensive plants such as geothermal.

| Perspective | Rate | Sourced example |
|---|---|---|
| Financial, real, EU cost-benefit analysis of funded projects | 4 % | Commission Delegated Regulation (EU) No 480/2014, Art. 19(3) (catalogue row `discount-rate-financial-eu`, verified) |
| Social, real, EU policy analysis | 3 % | European Commission, Better Regulation Toolbox (December 2025), Tool #64 (catalogue row `discount-rate-social-eu`, verified) |
| Investor | Weighted average cost of capital (WACC) of the project | project specific |

Rules:

- Name the perspective (investor, utility, society) and the convention (real or nominal).
- A higher rate favours designs with low capex and high opex (for example a gas boiler over a
  well); test the ranking at more than one rate (chapter 12).
- Risk belongs in the cash flows and in the uncertainty analysis; adding a risk premium to the
  rate penalises all future years in the same compounding way, which is rarely what is meant.

### 5.2 Present value, annuity factor and capital recovery factor

Present value of an amount `F` paid at the end of year `t` at rate `r`:

`PV = F / (1 + r)^t`

Annuity (present value) factor of a constant yearly amount over `n` years, paid at the end of
years 1 to `n`:

`A(r, n) = Σ_{t=1..n} 1 / (1 + r)^t = (1 − (1 + r)^−n) / r`, and `A = n` when `r = 0`.

Capital recovery factor (CRF), the yearly payment that repays 1 unit of capital over `n` years:

`CRF(r, n) = 1 / A(r, n) = r (1 + r)^n / ((1 + r)^n − 1)`

Values **(derived)**:

| r \ n | A(r, 25) | CRF(r, 25) |
|---|---|---|
| 3 % | 17.413 | 0.0574 |
| 4 % | 15.622 | 0.0640 |
| 5 % | 14.094 | 0.0710 |
| 6 % | 12.783 | 0.0782 |
| 8 % | 10.675 | 0.0937 |
| 10 % | 9.077 | 0.1102 |

At 5 %: A(5 %, 15) = 10.380, A(5 %, 20) = 12.462, A(5 %, 30) = 15.372 **(derived)**.

### 5.3 Analysis period, technical lifetime, replacements and residual value

- **Technical lifetime**: how long equipment lasts. DEA sheets give 25 years for the large heat
  pump and the gas boiler (as quoted in `gemini/examples/hackathon_2026/README.md`).
- **Analysis period** (economic lifetime): how many years the assessment counts. It is a choice;
  it need not equal any one technical lifetime.
- Equipment that lives shorter than the analysis period is **replaced** within it (a cash flow in
  the replacement year, or an equivalent yearly cost, section 3.5).
- Equipment that lives longer has a **residual value** at the end, discounted to the present and
  subtracted from the cost, or ignored on purpose (conservative).
- **Degradation**: reservoir temperature decline, scaling of exchangers and falling COPs reduce
  output over the years. A constant-year model ignores them; state that it does.

### 5.4 Timing conventions

- **End-of-year convention**: yearly flows are paid at the end of each year, the investment at
  year 0. This is the convention of the annuity factor in section 5.2 and of gemini.
- **Construction period**: deep wells take more than a year from first spend to first heat.
  Spending earlier than year 0 raises the present cost (interest during construction). A model
  that puts all capex at year 0 and first heat in year 1 ignores it.
- **Part years**: a simulation of 365 days is scaled to a year of 365.25 days in gemini (section
  16.7). Small, but it explains why per-year energies differ slightly from the run totals.

---

## 6. Levelised costs

### 6.1 Levelised cost of heat (LCOH)

The LCOH is the constant price of heat at which the discounted revenue equals the discounted cost
over the analysis period:

`LCOH = (I_0 + Σ_t C_t / (1+r)^t) / (Σ_t Q_t / (1+r)^t)`

with `I_0` the investment, `C_t` the yearly cost (opex) and `Q_t` the useful heat in year `t`.
With constant yearly cost `C` and heat `Q`:

`LCOH = (I_0 + C · A) / (Q · A) = (I_0 · CRF + C) / Q`

The heat is discounted as well as the cost; this is what makes the LCOH a price that breaks even.
Discounting cost but not energy gives a number that is not a break-even price.

For a plant that delivers only heat, the whole cost goes to the heat. For a plant that also
delivers cold, only the share of the cost charged to heat goes into the numerator (section 6.4).

### 6.2 Levelised cost of cold (LCOC)

The same formula with the useful cold delivered in place of the heat, and the share of the cost
charged to cold:

`LCOC = s_cold · (I_0 · CRF + C) / Q_cold`

Cold is counted as the heat removed from the cooling network at the delivery point (the energy
the chilled water gains across the users).

### 6.3 Levelised cost of thermal supply (LCTS)

The LCTS charges the whole cost to the sum of heat and cold:

`LCTS = (I_0 · CRF + C) / (Q_heat + Q_cold)`

It needs no allocation and gives one number per design, which makes it a natural objective for
ranking plants that deliver the same heat and cold. It treats 1 MWh of cold as worth 1 MWh of
heat; if their prices differ, NPV (section 7.2) is the better ranking.

Relation **(derived from the formulas)**: if the heat share `s_heat` equals the energy share
`Q_heat / (Q_heat + Q_cold)`, then LCOH = LCOC = LCTS.

### 6.4 Allocating shared costs between heat and cold

Wells, pumps and heat exchangers serve both products. There is no single correct split; there are
conventions, and the choice changes the LCOH and LCOC (not the LCTS or the NPV).

| Method | Share of heat | Comment |
|---|---|---|
| Fixed share | a stated number, for example 0.8 | simple; an assumption that needs a reason |
| Energy share | `Q_heat / (Q_heat + Q_cold)` | gives LCOH = LCOC = LCTS |
| Exergy share | exergy of heat / total exergy | values heat at 100 °C above cold at 20 °C; needs reference temperature |
| Separable cost (direct + share) | each product carries its own equipment, shared items split by one of the rules above | most transparent; needs a per-module cost |
| Avoided (alternative) cost | each product charged in proportion to what its cheapest stand-alone alternative would cost | needs a reference system for each product |
| Incremental (by-product) | heat carries everything except the extra cost of cold | answers "what does adding cooling cost" |

Rules:

- State the method and the share beside every LCOH and LCOC.
- Compare designs on LCOH or LCOC only with the same method.
- For a decision between designs, prefer LCTS or NPV, which need no allocation.

### 6.5 What a levelised cost does not say

- It is not the price a user pays: taxes, network costs and margins come on top.
- It does not show risk: two plants with equal LCOH can have very different spreads (chapter 13).
- It does not show scale: a small plant with low LCOH may not meet the demand.
- It ignores the timing of revenue and the value of flexibility.
- It is only as good as its weakest input; a placeholder capex makes the LCOH a placeholder too.

---

## 7. Revenue, profitability and subsidies

### 7.1 Heat and cold prices

The revenue is the useful heat and cold sold, times their prices. Sourced reference prices (gemini
cost catalogue, EUR 2015 values from the catalogue):

| Row | Figure | EUR 2015/MWh |
|---|---|---|
| `heat-price-se-2019` | Variable district heating tariff, Sweden, 85 EUR/MWh (2019), Copenhagen Economics for the Dutch Ministry of Economic Affairs and Climate (2021), p. 21 | 81.1 |
| `heat-price-nl-2019` | Variable district heating tariff, Netherlands, 98 EUR/MWh (2019), same report | 93.5 |
| `heat-price-nl-cap-2026` | Dutch regulated household ceiling, variable part incl. VAT, 2026 (ACM): 147.49 EUR/MWh | 114.6 |
| `cold-price-no-2017`, `cold-price-eu27-*-2014` | Cold prices, Norway 2017 and EU27 2014 | 103.5, 81.2, 110.2 |

A household tariff includes VAT and network costs; the price a heat producer receives from a
network operator is lower. Use a wholesale or contract price for the producer's revenue where one
is available.

### 7.2 Net present value, payback and break-even price

**Net present value**:

`NPV = −I_0 + Σ_t (R_t − C_t) / (1 + r)^t`, with constant yearly flows `NPV = −I_0 + (R − C) · A`.

A positive NPV means the project earns more than the discount rate.

**Internal rate of return (IRR)**: the rate at which NPV = 0. Useful for investors; ambiguous when
cash flows change sign more than once.

**Simple payback**: `I_0 / (R − C)` years, without discounting. It ignores the time value of money
and everything after the payback year; use it as a liquidity indicator, not a ranking.

**Discounted payback**: the first year in which the cumulative discounted cash flow turns
positive.

**Break-even price** **(derived from the formulas)**: with one price `p` for both heat and cold,
NPV = 0 when `p · (Q_heat + Q_cold) · A = I_0 + C · A`, that is when `p = LCTS`. A plant whose
heat and cold sell at the same price breaks even exactly at its LCTS.

### 7.3 Operating subsidies: SDE++ as an example

Many countries pay renewable heat producers an operating subsidy per MWh. The Dutch SDE++
(Stimulering Duurzame Energieproductie en Klimaattransitie) is a typical sliding feed-in premium
(RVO, "Berekening SDE++" and SDE++ brochures, https://www.rvo.nl/subsidies-financiering/sde):

- The **base amount** (basisbedrag) is the cost price of the technology per unit of energy, set per
  category; the applicant may ask for less (aanvraagbedrag), not more. It is fixed over the
  subsidy term.
- The **correction amount** (correctiebedrag) reflects the market value of the energy and is set
  every year; it never falls below a floor (the basisprijs).
- The subsidy per unit = base (or applied) amount − correction amount, paid on the eligible
  production up to a cap of full-load hours, for a **maximum term that differs per category**
  (RVO). Check the current term for geothermal in the year's regulation; this handbook does not
  state it (not verified).
- PBL publishes the cost basis per category each year (for example the *Eindadvies basisbedragen
  SDE++ 2026*, which also gives the whole-plant costs in section 2.7).

How to model it:

- A sliding premium pays `max(0, base − correction)` per MWh. With a constant market price it is a
  constant amount per MWh up to the cap.
- It is paid for its term only; after the term, the plant lives on market revenue.
- It counts in NPV and payback, not in the LCOH (the LCOH is a cost).

### 7.4 Investment subsidies, risk schemes and taxes

- **Investment grants** reduce `I_0` directly; state whether a capex figure is before or after them.
- **Exploration risk schemes** (guarantees that refund part of the drilling cost if a well fails)
  change the risk, not the expected capex; they belong in the uncertainty analysis.
- **Taxes**: corporate income tax, depreciation allowances and property tax change an investor's
  cash flows. A pre-tax analysis is simpler and common for comparing designs; say which is used.

---

## 8. Carbon pricing

### 8.1 The EU Emissions Trading System

The EU Emissions Trading System (EU ETS) caps the emissions of power generation, energy-intensive
industry and aviation in the EU and lets allowances (EUA, 1 t CO2-equivalent each) trade.
Combustion installations above a rated thermal input threshold are covered; small heat plants may
fall outside it, in which case they do not pay the ETS price directly (check the installation
against the ETS Directive 2003/87/EC, Annex I). A separate system for fuels used in buildings and
road transport ("ETS2") was added by the 2023 revision of that directive; its start date has to be
checked at the time of the assessment (not verified here).

Sourced price: the volume-weighted average allowance price of the 213 primary-market auctions of
2025 was 73.43 EUR/t (Instrat Foundation, W. Przedlacki, "EU ETS 2025 summary and the beginning of
2026 auctions", 8 January 2026, https://energy.instrat.pl/en/eu-ets-2025-summary/, as quoted in
`gemini/examples/hackathon_2026/README.md`; a secondary source). In EUR 2015: `73.43 / 1.2875 =
57.03 EUR/t` **(derived)**.

### 8.2 Using a carbon price in an assessment

- In a **financial** view, price only the emissions the operator pays for (its own combustion
  under the ETS, or a national carbon tax).
- In a **social** view, a shadow price of carbon may be applied to all emissions, including those of
  grid electricity; then do not also count the carbon cost inside the electricity price.
- Future carbon prices are uncertain and politically set; use a range (chapter 13).

---

## 9. CO2 accounting

### 9.1 Boundary and scopes

The Greenhouse Gas Protocol divides emissions into:

- **Scope 1**: direct emissions of the plant (combustion of gas in boilers, CHP and flares; CO2 and
  methane released from the brine).
- **Scope 2**: emissions of purchased electricity (and heat).
- **Scope 3**: everything else in the value chain (manufacture of equipment, drilling, end of
  life).

An operational assessment of a geothermal plant usually reports scope 1 and scope 2. Embodied
emissions of drilling and equipment (scope 3) are a life-cycle question; include them only with a
life-cycle source.

### 9.2 Direct CO2 from produced gas and combustion

Deep brines can carry dissolved gas (CO2, CH4, N2, H2S). When the gas comes out of solution in the
degasser:

- the **CO2** in it is released to the air unless it is reinjected or captured;
- the **CH4** is flared, burnt for heat or power, or vented. Combustion turns it into CO2
  (44/16 = 2.75 kg CO2 per kg CH4 burnt, from the molar masses; **derived**). Flaring is not
  complete: the unburnt part is released as methane (gemini's flare states a combustion
  efficiency of 0.98, cited to US EPA AP-42 section 13.5, `gemini/examples/hackathon_2026/README.md`).

Bought gas burnt in boilers adds its combustion CO2, from its composition.

### 9.3 Methane and global warming potentials (IPCC AR6)

Methane released unburnt is converted to CO2-equivalent with a global warming potential (GWP):

`CO2e = m_CO2 + GWP_CH4 · m_CH4`

| Value | Figure | Source |
|---|---|---|
| GWP100, fossil methane | 29.8 | IPCC AR6 WG1, chapter 7, table 7.15 (Forster et al. 2021), as quoted by Muñoz, Schmidt and Weidema (2024), *Environmental Research Letters* 19(12), 121002 |
| GWP100, biogenic methane | 27.0 | same |
| GWP20, fossil methane | 82.5 | secondary sources only (for example glossary sites quoting AR6); not read in the IPCC report: **not verified** |

Rules:

- Use fossil methane for methane from a reservoir.
- Use the 100-year horizon unless the user asks otherwise; report the standard (gemini:
  `economics.accounting.gwp.standard`).
- Do not mix AR5 and AR6 values in one assessment.

### 9.4 Grid electricity emission factors

Scope 2 emissions = electricity bought × emission factor (g CO2/kWh).

| Kind of factor | Meaning | When to use |
|---|---|---|
| Average, location-based | the mean intensity of the grid's generation in the year | default for reporting |
| Market-based | the factor of the contract (guarantees of origin) | when the plant buys certified power |
| Marginal | the intensity of the plant that changes when demand changes | for decisions that change demand at the margin |
| Hourly or daily profile | intensity per step | when a plant shifts its consumption in time |

Sourced averages (gemini cost catalogue, rows `co2-grid-eu-2025` and `co2-grid-eu-2024`, Ember
Yearly Electricity Data, EU power sector CO2 intensity, verified): **209.21 g/kWh (2025)**, 211.52
g/kWh (2024). The GEMINI hackathon organisers prescribe 300 g/kWh for their case
(`documents/project/quality-assurance/inputs/hackathon-2026-assumptions.md`). A factor for 2015
(528 g/kWh for Germany, Umweltbundesamt, Climate Change 11/2018) shows how much factors change over
a decade; a plant running from 2027 should use a factor of its years, or a projected range.

### 9.5 Reference systems and avoided emissions

A plant's emissions mean little alone. Report them next to a **reference system** that delivers the
same heat and cold, for example gas boilers and compression chillers on grid power. Avoided
emissions = emissions of the reference − emissions of the plant. State the reference, its
efficiencies and its factors; they are assumptions with sources like any other value.

### 9.6 CO2 abatement cost

`abatement cost = (annualised cost of the plant − annualised cost of the reference) / (yearly
emissions of the reference − yearly emissions of the plant)` in EUR/t CO2e. It compares climate
options on one scale. It is only defined when the plant emits less than the reference; a negative
value means the plant is cheaper and cleaner.

---

## 10. Energy prices

### 10.1 Eurostat price statistics and consumption bands

Eurostat publishes semi-annual electricity and gas prices by consumer type and size:

| Dataset | Content |
|---|---|
| `nrg_pc_204` / `nrg_pc_205` | electricity prices for household / non-household consumers, from 2007, semi-annual |
| `nrg_pc_202` / `nrg_pc_203` | natural gas prices for household / non-household consumers, semi-annual |

Electricity bands for non-household consumers (annual consumption):

| Band | Consumption |
|---|---|
| IA | below 20 MWh |
| IB | 20 to 499 MWh |
| IC | 500 to 1 999 MWh |
| ID | 2 000 to 19 999 MWh |
| IE | 20 000 to 69 999 MWh |
| IF | 70 000 to 149 999 MWh |
| IG | 150 000 MWh and above |

(Band codes and thresholds as published with the Eurostat datasets, codes `MWH_LT20` to
`MWH_GE150000`; read from Eurostat metadata and dataset mirrors, not from the nrg_pc_205 page
itself.)

Gas bands for non-household consumers are I1 to I6 by GJ per year; band I4 is 100 000 to 999 999
GJ/yr (as used in `gemini/examples/hackathon_2026/README.md`). The other gas band limits are not
quoted here (not verified).

Each price is given at three tax levels: excluding taxes and levies, excluding VAT and other
recoverable taxes (`X_VAT`), and all taxes included.

Sourced examples (EU27_2020 average, `X_VAT`, as used in the hackathon sample):

- Electricity, band IE, 2025-S1 0.1381 and 2025-S2 0.1342 EUR/kWh, mean 136.15 EUR/MWh (EUR
  2025), 105.75 EUR/MWh in EUR 2015 (Eurostat `nrg_pc_205`, API data of 2026-10-19).
- Gas, band I4, 2025-S1 0.0545 and 2025-S2 0.0483 EUR/kWh (gross calorific value), mean 51.4
  EUR/MWh (EUR 2025), 39.92 EUR/MWh in EUR 2015 (Eurostat `nrg_pc_203`).

### 10.2 Choosing a band and a tax level

- Choose the band from the plant's **yearly** consumption from the simulation. A plant that buys
  26 GWh/yr of electricity is in band IE (the worked example, section 17.4).
- A business that can recover VAT uses the price excluding VAT and recoverable taxes (`X_VAT`).
- Use the country of the site; use the EU average only when the case names no country, and say so.
- Average the two semesters of a year for a yearly price; note the year.
- Eurostat prices are averages over consumers; a large consumer with a negotiated contract can pay
  more or less. A contract price from the user beats a statistic.

---

## 11. Cost data sources and their quality

### 11.1 Main sources for geothermal heating and cooling

| Source | What it gives | Notes |
|---|---|---|
| Danish Energy Agency (DEA) and Energinet, *Technology Data for Generation of Electricity and District Heating* (version 0019, August 2026, with Excel data sheets) | capex, fixed and variable O&M, lifetimes, efficiencies per technology and size, for several years | cost data in stated EUR years; geothermal sheets 45.x give whole plants; no chiller sheet |
| PBL Netherlands Environmental Assessment Agency, SDE++ advice (yearly) | Dutch reference costs per subsidy category, including deep geothermal by size | used to set subsidy levels; whole plants |
| Eurostat energy price statistics | electricity and gas prices by band and tax level | section 10 |
| Eurostat HICP | price indices for conversion | section 4.2 |
| Ember yearly electricity data | grid CO2 intensity by country and year | section 9.4 |
| IPCC AR6 WG1 | global warming potentials | section 9.3 |
| GEOPHIRES-X (NREL, open source) | cost correlations for wells, pumps and surface plant | code, not a survey; status secondary |
| National geothermal reports (TNO, ECN, NLOG for the Netherlands) | drilling costs, reference cases | check year and scope |
| Peer-reviewed papers | component costs, case studies | check the year and what is included |

The project's own catalogue, `gemini/docs/cost-sources/sources.csv` (74 rows at 2026-11-01: 33
verified, 25 secondary, 16 placeholder, per its README), holds these figures with quote, price
year, 2015 value and the case key each feeds. It is reference data, not defaults.

### 11.2 Grading the quality of a figure

The cost catalogue grades each row:

- **verified**: the figure was read in the official source, dataset or report it is credited to;
- **secondary**: real and quoted, but from a thesis, a citing paper, code, or a proxy for another
  item;
- **placeholder**: no verified source; the gap is kept visible.

Estimate maturity matters as well. AACE International Recommended Practice 18R-97 defines estimate
classes from Class 5 (concept screening, widest range) to Class 1 (definitive, narrowest). The
ranges commonly quoted for Class 5 are about −20 % to −50 % on the low side and +30 % to +100 % on
the high side (quoted from general knowledge of the practice, not re-read for this handbook:
**not verified**). A plant costed from factors at the design-option stage is a Class 5 or Class 4
estimate; its capex is a range, not a point.

### 11.3 Checklist before a figure enters a case

1. Source: publisher, title, year, page or sheet, link, and the figure as stated (quote).
2. Price year and currency of the figure.
3. Scope: what it includes (installation, indirect costs, contingency, VAT) and excludes.
4. Basis: per W of heat, per W electric, per W of cold, per m, per unit, per W/K.
5. Size and conditions it holds for (capacity, depth, temperatures).
6. Conversion to the case's price year and currency, with the index and its values.
7. Status: verified, secondary or placeholder.
8. Approval: a value that no user file gives is approved by the user with its source before use.

---

## 12. Sensitivity analysis

### 12.1 One-at-a-time sensitivity

Change one input from its base value to a low and a high value, keep all others at base, and record
the change of each output (LCTS, NPV, CO2). The low and high values must come from a source or be
stated ranges (for example the bounds of the input's uncertainty, chapter 13). Equal percentage
changes (±20 %) for all inputs hide that some are far less certain than others; use sourced ranges
where they exist.

Two kinds of input:

- **Economic inputs** (prices, rates, cost factors): the simulation does not change; only the cost
  formulas run again. Cheap and exact.
- **Physical inputs** (reservoir permeability, temperature gradient, return temperatures): the
  simulation changes; each end needs a new run. A design may also fail its requirements at an end.

### 12.2 Tornado charts

Sort the inputs by the width of their output range (|output at high − output at low|) and draw
them as horizontal bars around the base value, widest at the top. The top bars are where better
data pay off most. Report the table beside the chart: input, low, high, output at low, output at
high.

### 12.3 Break-even and switching values

The **switching value** of an input is the value at which a decision changes: NPV crosses zero, or
the ranking of two designs flips. It answers "how wrong can this input be before the answer
changes?" and is often more useful than a tornado. For a price that enters linearly, the switching
value follows from the derivative of the output (for example ∂LCTS/∂p_el = E_el / (Q_heat + Q_cold),
**derived** from section 6.3).

---

## 13. Uncertainty analysis

### 13.1 Distributions for uncertain inputs

| Distribution | Parameters | Use |
|---|---|---|
| Uniform | min, max | only the bounds are known |
| Triangular | min, mode, max | a best guess and bounds; skew allowed |
| Normal (truncated) | mean, standard deviation, cut at min and max | symmetric errors around a measured value |
| Lognormal | mean and spread of the log | positive quantities with long upper tails (permeability, drilling overruns) |
| Discrete | values and probabilities | scenarios (policy on or off, one or two wells succeed) |

Every distribution is an assumption with a source or a stated reason. Correlated inputs (gas and
electricity prices, carbon and electricity prices) sampled independently understate or overstate
the spread; state whether correlations are modelled.

### 13.2 Monte Carlo sampling

Draw `N` sets of inputs from their distributions, run the evaluation for each, collect the outputs.

- Fix the random **seed** and report it, so the result can be reproduced.
- The number of draws sets the precision: the standard error of a mean falls as `1/√N`; tail
  percentiles need many more draws than the mean. A handful of draws gives an impression, not a
  percentile; say so.
- Draws whose simulation fails, or whose design breaks a requirement, are reported as a count and
  not silently dropped; a high failure share is itself a result (the design is fragile).
- Latin hypercube sampling spreads the draws more evenly than plain random sampling for the same N.

### 13.3 Percentiles, risk and reporting

Report the mean, the median (P50) and a range such as P5 to P95, with N and the seed. In energy
project finance P90 often denotes a value exceeded with 90 % probability (a conservative output);
say which convention is used. Compare designs on the same draws (common random numbers), so the
difference between them is not noise.

---

## 14. Comparing configurations and deciding

### 14.1 Like-for-like comparison

Designs are comparable only when:

- they meet the same requirements (a design that leaves demand unmet is cheaper and wrong);
- they use the same case: prices, price year, discount rate, analysis period, allocation method,
  emission factors;
- their costs cover the same scope (a design with a placeholder for a key component is not
  comparable with one without);
- they are evaluated with the same model version.

### 14.2 Decision criteria: cost, CO2, robustness

| Criterion | Measure | Note |
|---|---|---|
| Cost | LCTS, or NPV with the actual heat and cold prices | LCTS for equal deliveries; NPV when prices differ |
| Investment need | capex | financing limits |
| CO2 | t CO2e per year, or per MWh delivered | report scope 1 and scope 2 separately |
| Robustness | spread of LCTS (P5 to P95), switching values, share of failed draws | a slightly dearer design with a narrow spread may be preferred |
| Technical risk | number of wells, untested equipment, gas handling | qualitative unless modelled |
| Dependence on the grid | electricity bought, peak electric load | exposure to price and grid factors |

### 14.3 Multi-criteria decisions and Pareto fronts

When cost and CO2 pull in different directions:

- **Pareto front**: keep the designs that no other design beats on every criterion; present the
  front and let the user choose.
- **Carbon-priced cost**: put a price on CO2 and rank on the total; the ranking then depends on the
  price, which should be varied (chapter 12).
- **Weighted scores**: normalise each criterion and weight it; the weights are the user's choice and
  must be stated. Weighted sums hide trade-offs; show the raw criteria next to the score.
- **Constraint form**: minimise cost subject to CO2 below a limit, or the reverse.

---

## 15. Common mistakes

1. **Mixing price years**: adding a 2013 drilling cost to a 2025 heat pump price without conversion.
2. **Real prices with a nominal rate**, or the reverse (section 4.1).
3. **Discounting cost but not energy** in a levelised cost (section 6.1).
4. **A single drilling price per metre for all depths** in a depth search (section 2.2).
5. **Average instead of design size** for equipment cost (section 2.5).
6. **Double counting**: a whole-plant O&M plus component O&M; variable O&M that includes chemicals
   plus a chemical cost; carbon in the electricity price plus carbon on grid electricity
   (sections 3.1, 3.2, 3.6).
7. **Contingency on top of a figure that includes it** (section 2.6).
8. **Gross vs lower heating value** of gas prices (section 3.3).
9. **Household tariffs as producer revenue** (section 7.1).
10. **Ranking on LCOH or LCOC with different allocation methods**, or ranking on LCOH alone for
    a heat-and-cold plant (section 6.4).
11. **Comparing a design that fails its requirements** with one that passes (section 14.1).
12. **Equal ±% ranges for all inputs** in a sensitivity, hiding the true uncertainties (section
    12.1).
13. **Dropping failed Monte Carlo draws** without reporting them (section 13.2).
14. **Too few draws for a percentile** (section 13.2).
15. **Placeholders presented as data**: a figure without a source reported as a result.
16. **Old grid factors** for a future plant (section 9.4).
17. **Payback as the only criterion** (section 7.2).
18. **Forgetting replacements** (ESPs every few years) when the O&M figure does not include them
    (section 3.5).
19. **Defaults filled silently** where the case lacks a value (preface, rule 2).

---

> **Draft stop (2026-11-05, usage pause):** chapters 1 to 15 are written; chapter 16 (how gemini computes economics), chapter 17 (worked example, numbers already verified with gemini 0.6.13) and the appendices follow.
