# Handbook of Techno-Economic and Environmental Assessment of Geothermal Heating and Cooling Plants

How to cost a geothermal heating and cooling plant, put a carbon footprint on it, and use both to
choose between designs. General for any case; chapter 17 works a full example on invented
numbers. Checked against gemini 0.6.17 and the cost catalogue `knowledge/data-economics.csv` (154
rows) on 2026-11-05.

Cite as `knowledge/handbook-economics.md` with the section (for example
`knowledge/handbook-economics.md §6.3`). Every section stands alone: read the one you need
(`read_knowledge` with its number). Chapter 0 is the short version for agents.

This handbook explains no tool. Running costs, sensitivity and uncertainty: skill `economics`.
Setting economics in a case (`ask_economics`, `set_case`): skill `setting-the-case`. Defining the
rest of the case: `knowledge/handbook-case.md`. Reporting the numbers:
`knowledge/handbook-report.md`.

---

## 0. Quick reference for the agents

### 0.1 Rules that hold in every section

1. **gemini computes, agents quote.** Every capex, opex, levelised cost, NPV, payback and CO2 is
   gemini's (`estimate_costs`, `compute_kpis`, `compare`, the studies), quoted digit for digit
   in the unit the tool gives. Never compute, round, convert, add, share or average a number
   yourself. The formulas in this handbook explain what gemini did; they are not for use.
2. **No default values.** A price, rate or factor the case lacks is a gap: a tool reports it
   (`case_incomplete`, with its `economics.<key>` path). It is filled from a source with the
   user's approval (§0.2), never with a number of your own, and never costed around.
3. **One price year, one currency, one convention.** Catalogue values are EUR at 2015 prices;
   the case's `currency` and `price_year` say so. Real prices go with a real discount rate (§4.1).
4. **A cost counts only for a feasible design.** Cost the verified result; a design whose gemini
   verdict is not feasible is not compared with one that is (§14.1). The verdict is
   `check_results`'s `feasible`, not a count of passed checks.
5. **Every value carries its source**: file and page, Knowledge document and section, or
   catalogue row `id`.

### 0.2 Where an economics value comes from: decision order

Take the first that gives the key:

| Step | Source | Cite as |
|---|---|---|
| 1 | The user's files and answers (a contract price, a stated rate, a brief's table) | file and page, or "user, <date>" |
| 2 | An assumptions document in Knowledge written for this case or brief (search Knowledge for one first) | document and section |
| 3 | The cost catalogue `knowledge/data-economics.csv`: a row whose `path` is the key; its `value_2015` in `unit_2015` | row `id` |
| 4 | Nothing: the key stays `open` and the user gives it in the one economics question | "user" |

Choosing among catalogue rows for one key: prefer `verified` over `secondary`; prefer the row
nearest the case in size, depth, country and year; for a drilling depth search use the depth
rows as a table (§2.2). The `ask_economics` tool fills every key you do not name with its
recommended row and sets `currency` EUR and `price_year` 2015 itself (skill
`setting-the-case`).

### 0.3 Ask the user, or take it from Knowledge

| Situation | Do |
|---|---|
| A user file gives the value | Use it with its page. No question. |
| An assumptions document or a catalogue row gives it | Put it in the ONE economics question with its source; the user approves it once. |
| A perspective choice: discount rate, analysis period, `heat_cost_share` | Propose a catalogue row with a one-line reason (§5.1, §5.3, §6.4); the user decides. |
| A subsidy (`revenue.subsidy.*`) | Never recommended. Set it only when the user or the brief gives one. |
| Revenue prices (`revenue.heat`, `revenue.cold`) | Catalogue rows; say that a household tariff overstates what a producer earns (§7.1). |
| Grid CO2 intensity | A case value, `utilities.electricity.co2_intensity`, not economics. The value the brief or the client prescribes, else the newest Ember row for the country (§9.4). |
| Uncertainty ranges for studies | Only from the user or the case. Never invented. |
| A tool says a key is missing | Report it as missing with its path; the case lead asks the user. |
| No source gives it | `open`: the user gives it. |

### 0.4 Keys and the catalogue rows that feed them

Paths under `economics.` unless marked; values at 2015 prices from `knowledge/data-economics.csv`
(status v verified, s secondary). The unit tells gemini the basis (§16.2): a `%/yr` fixed opex
is a share of that kind's capex, `EUR/MW/yr` an amount per capacity.

| Key | Catalogue rows: `id` value_2015 unit (status v = verified, s = secondary) |
|---|---|
| `accounting.allocation.heat_cost_share` | `heat-cost-share-energy-fiaschi-2021` 0.87 - (s); `heat-cost-share-pes-fiaschi-2021-low` 0.71 - (s); `heat-cost-share-pes-fiaschi-2021-high` 0.76 - (s) |
| `accounting.gwp.CH4` | `gwp-ch4-fossil-ar6-ghgp-2024` 29.8 kg CO2e/kg CH4 (s); `gwp-ch4-non-fossil-ar6-ghgp-2024` 27 kg CO2e/kg CH4 (s); `gwp-ch4-ar6-ipcc-2021-sm` 27.9 kg CO2e/kg CH4 (v) |
| `accounting.gwp.standard` | `gwp-standard-ipcc-ar6-gwp100` IPCC AR6 GWP100  (v); `gwp-standard-eu-2020-1044-ar5` IPCC AR5 GWP100  (v) |
| `analysis_period` | `analysis-period-dea-2019-geothermal-dk` 25 yr (v); `analysis-period-sde-2025-subsidy-period` 15 yr (s) |
| `capex.absorption_chiller` | `absorption-chiller-ecos-2023` 0.2339 EUR/W (s); `absorption-chiller-kim-2008-low` 0.3283 EUR/W (s); `absorption-chiller-kim-2008-high` 0.4377 EUR/W (s); `absorption-chiller-bigee-105kw` 0.4091 EUR/W (s) |
| `capex.adsorption_chiller` | `adsorption-chiller-edinburgh-2023` 0.8266 EUR/W (s); `adsorption-chiller-bigee-100-150kw` 0.8589 EUR/W (s) |
| `capex.boiler` | `boiler-gas-dea-2018-2-3mw` 0.06 EUR/W (v) |
| `capex.chp` | `chp-gas-engine-dea-2018-1-10mwe` 0.95 EUR/W electric (v) |
| `capex.circulation_pump` | `circulation-pump-proxy-dea-2017-over-1mw` 0.09 EUR/W heat (s); `circulation-pump-proxy-dea-2017-under-1mw` 0.24 EUR/W heat (s) |
| `capex.compression_chiller` | `compression-chiller-ecos-2023` 0.1592 EUR/W (s) |
| `capex.cooler` | `dry-cooler-iea-2014-low` 0.04909 EUR/W (v); `dry-cooler-iea-2014-high` 0.1072 EUR/W (v); `cooling-tower-iea-2014-low` 0.02204 EUR/W (v); `cooling-tower-iea-2014-high` 0.02705 EUR/W (v) |
| `capex.degasser` | `degasser-nl-2013` 1006240 EUR (s) |
| `capex.drilling` | `drilling-nl-2013-2300m` 1247 EUR/m (v); `drilling-nl-2013-3000m` 1845 EUR/m (v); `drilling-nl-2013-4000m` 2075 EUR/m (v); `drilling-ecn-2012-2000m` 2237 EUR/m (s); `drilling-ecn-2012-3000m` 2273 EUR/m (s) |
| `capex.electric_boiler` | `boiler-electric-dea-2017-over-10mw` 0.07 EUR/W (v); `boiler-electric-dea-2017-1-5mw` 0.15 EUR/W (v) |
| `capex.flare` | `flare-capex-proxy-epa-2019` 57700 EUR (s) |
| `capex.gas_makeup` | `gas-makeup-capex-proxy-npro-chp-1mwe` 636893 EUR (s) |
| `capex.heat_exchanger` | `heat-exchanger-dea-2025-station` 0.1089 EUR/W (s) |
| `capex.heat_pump` | `heat-pump-dea-2025-10mw` 0.7379 EUR/W (s) |
| `capex.ice_storage` | `ice-storage-mlakar-2022-low` 23250 EUR/MWh cold (s); `ice-storage-mlakar-2022-high` 31704 EUR/MWh cold (s); `ice-storage-proxy-irena-2013-pcm-low` 10062 EUR/MWh cold (s); `ice-storage-proxy-irena-2013-pcm-high` 50310 EUR/MWh cold (s) |
| `capex.injection_pump` | `injection-pump-proxy-dh-station` 0.09903 EUR/W (s) |
| `capex.pipe` | `pipe-dea-2025-distribution-5-25mw` 1149 EUR/m (v); `pipe-dea-2025-distribution-1-5mw` 636 EUR/m (v); `pipe-dea-2025-transmission-0-50mw` 49.08 EUR/MW/m (v) |
| `capex.production_pump` | `esp-unit-2019` 763359 EUR (s); `production-pump-esp-kennisagenda-2016-250kwel` 0.7183 EUR/W electric (s); `production-pump-esp-kennisagenda-2016-500kwel` 0.5986 EUR/W electric (s); `production-pump-schlagermann-2023-332kwel` 1.546 EUR/W electric (v) |
| `capex.thermal_storage` | `thermal-storage-tank-dea-2025-3000m3` 168.6 EUR/m3 (v); `thermal-storage-pit-dea-2025-70000m3` 64.85 EUR/m3 (v) |
| `carbon.price` | `carbon-price-eu-ets-esma-2026` 57.48 EUR/t CO2e (v); `carbon-price-eu-ets-esma-2025` 51.56 EUR/t CO2e (v); `carbon-price-nl-co2-levy-rijksoverheid-2026` 61.1 EUR/t CO2 (v) |
| `discount_rate` | `discount-rate-financial-eu` 0.04 - (v); `discount-rate-social-eu` 0.03 - (v); `discount-rate-pbl-sde-2022-geothermal-nominal` 0.056 - (v); `discount-rate-pbl-sde-2022-geothermal-real` 0.04 - (v); `discount-rate-ebn-gn-2026-pbl-ort` 0.087 - (s); `discount-rate-nl-mkba-2020` 0.0225 - (v); `discount-rate-pbl-sde-2025-geothermal-nominal` 0.072 - (v); `discount-rate-pbl-sde-2025-geothermal-real` 0.051 - (v); `discount-rate-pbl-sde-2026-erratum-row4-nominal` 0.073 - (s); `discount-rate-pbl-sde-2026-erratum-row4-real` 0.052 - (s) |
| `energy.electricity` | `electricity-nl-eurostat-2024-band-id` 115 EUR/MWh (s); `electricity-nl-eurostat-2024-band-ie` 138 EUR/MWh (s) |
| `energy.gas` | `gas-nl-eurostat-2024-band-i4` 37.51 EUR/MWh (GCV) (s); `gas-nl-eurostat-2024-band-i3` 44.42 EUR/MWh (GCV) (s) |
| `opex.fixed.absorption_chiller` | `opex-absorption-chiller-iea-shc-2024` 3 %/yr (v); `opex-absorption-chiller-hre4-2017-500kw` 4 %/yr (s); `opex-absorption-chiller-hre4-2017-500kw` 6800 EUR/MW/yr (s) |
| `opex.fixed.adsorption_chiller` | `opex-adsorption-chiller-iea-shc-2024` 3 %/yr (v) |
| `opex.fixed.boiler` | `opex-boiler-gas-dea-2018` 1950 EUR/MW/yr (v) |
| `opex.fixed.chp` | `opex-chp-gas-engine-dea-2018` 9750 EUR/MW/yr (v) |
| `opex.fixed.circulation_pump` | `circulation-pump-om-vdi2067-vicus-2026-low` 2 %/yr (s); `circulation-pump-om-vdi2067-vicus-2026-high` 3 %/yr (s) |
| `opex.fixed.compression_chiller` | `opex-compression-chiller-hre4-2017-755kw` 4640 EUR/MW/yr (s); `opex-compression-chiller-tctc-2013-district` 4309 EUR/MW/yr (s) |
| `opex.fixed.cooler` | `opex-cooling-tower-wet-iea-shc-2024` 4 %/yr (v); `opex-dry-cooler-iea-shc-2024` 2 %/yr (v) |
| `opex.fixed.degasser` | `opex-degasser-proxy-schlagermann-2023` 3 %/yr (s) |
| `opex.fixed.drilling` | `opex-drilling-geophires-2026` 1 %/yr (v); `opex-drilling-schlagermann-2023` 0.5 %/yr (v) |
| `opex.fixed.electric_boiler` | `opex-boiler-electric-dea-2017` 1070 EUR/MW/yr (v) |
| `opex.fixed.flare` | `opex-flare-proxy-schlagermann-2023` 3 %/yr (s) |
| `opex.fixed.gas_makeup` | `opex-gas-makeup-proxy-npro-chp` 8 %/yr (s) |
| `opex.fixed.heat_exchanger` | `opex-heat-exchanger-proxy-vdi2067-low` 1.5 %/yr (s); `opex-heat-exchanger-proxy-vdi2067-high` 2.5 %/yr (s) |
| `opex.fixed.heat_pump` | `opex-heat-pump-dea-2025-10mw` 1652 EUR/MW/yr (s) |
| `opex.fixed.ice_storage` | `ice-storage-om-proxy-irena-2013-pcm-low` 1.667 %/yr (s); `ice-storage-om-proxy-irena-2013-pcm-high` 4.167 %/yr (s); `ice-storage-om-spice-2024-single-building-2000kwh` 0.8769 %/yr (s); `ice-storage-om-spice-2024-mid-size-10000kwh` 0.7427 %/yr (s); `ice-storage-om-spice-2024-district-cooling-50000kwh` 0.513 %/yr (s); `ice-storage-om-proxy-hao-2022-cooling-plant` 2 %/yr (s) |
| `opex.fixed.injection_pump` | `opex-injection-pump-proxy-schlagermann-2023` 3 %/yr (s) |
| `opex.fixed.pipe` | `opex-pipe-dea-2025-distribution` 776.7 EUR/MW/yr (v); `opex-pipe-dea-2025-transmission` 77.67 EUR/MW/km/yr (v); `pipe-om-vesta-mais-pbl-2026-transport` 1 %/yr (v); `pipe-om-vesta-mais-pbl-2026-distribution` 1 %/yr (v); `pipe-om-dea-2025-transmission-share` 0.1582 %/yr (s); `pipe-om-vdi2067-vicus-2026-low` 0.5 %/yr (s); `pipe-om-vdi2067-vicus-2026-high` 1 %/yr (s) |
| `opex.fixed.production_pump` | `opex-production-pump-ecn-2012-esp-replacement` 20 %/yr (s) |
| `opex.fixed.thermal_storage` | `opex-thermal-storage-tank-dea-2025` 0.2823 %/yr (v) |
| `opex.per_energy.boiler` | `per-energy-boiler-gas-dea-ch44-2020col` 1.1 EUR/MWh (v) |
| `opex.per_energy.chp` | `opex-variable-chp-gas-engine-dea-2018` 5.4 EUR/MWh electric (v) |
| `opex.per_energy.electric_boiler` | `per-energy-electric-boiler-dea-ch41-2020col` 0.9 EUR/MWh (v) |
| `opex.per_energy.heat_pump` | `per-energy-heat-pump-dea-ch40-excess-heat-10mw-2025col` 1.69 EUR/MWh (v); `per-energy-heat-pump-dea-ch40-seawater-20mw-2025col` 1.19 EUR/MWh (v) |
| `opex.variable.chemical` | `scale-inhibitor-proxy-watertap-2020` 2.908 EUR/kg (s); `scale-inhibitor-chemanalyst-2024-atmp-hamburg` 0.7695 EUR/kg (s); `scale-inhibitor-spitsov-2023-ro-jurbysoft` 2.146 EUR/kg (s); `scale-inhibitor-spitsov-2023-ro-aminat-k` 2.682 EUR/kg (s); `corrosion-inhibitor-indexbox-2026-eu-amine-low` 1.942 EUR/kg (s); `corrosion-inhibitor-indexbox-2026-eu-amine-high` 3.107 EUR/kg (s) |
| `opex.variable.waste_disposal` | `waste-disposal-proxy-sewage-sludge` 0.04971 EUR/kg (s); `waste-disposal-norm-proxy-covra-2026` 45.93 EUR/kg (s); `waste-disposal-tfa-france-2022` 1027 EUR/m3 (s); `waste-density-geothermal-filter-nrg-2020` 0.2656 t/m3 (s); `waste-disposal-tfa-france-per-kg-filter-density` 3.867 EUR/kg (s) |
| `revenue.cold` | `cold-price-no-2017` 103.5 EUR/MWh (s); `cold-price-eu27-alternative-2014` 81.15 EUR/MWh (s); `cold-price-eu27-new-investment-2014` 110.2 EUR/MWh (s) |
| `revenue.heat` | `heat-price-nl-cap-2026` 114.6 EUR/MWh (v); `heat-price-se-2019` 81.11 EUR/MWh (v); `heat-price-nl-2019` 93.51 EUR/MWh (v) |
| `revenue.subsidy.amount` | `sde-basisbedrag-geothermal-pbl-2026-over-20mw` 48.7 EUR/MWh (v); `sde-basisbedrag-geothermal-pbl-2026-under-12mw` 62.06 EUR/MWh (v); `sde-net-subsidy-geothermal-pbl-2026-over-20mw` 27.5 EUR/MWh (s) |
| `revenue.subsidy.cap` | `sde-full-load-hours-geothermal-pbl-2026-over-20mw` 6000 h/yr (v) |
| `revenue.subsidy.duration` | `sde-duration-geothermal-stcrt-2025` 15 yr (v) |
| `utilities.electricity.co2_intensity` | `co2-grid-organisers-2026` 300 g/kWh (v); `co2-grid-eu-2025` 209.2 g/kWh (v); `co2-grid-eu-2024` 211.5 g/kWh (v) |

`currency`, `price_year` (EUR, 2015) are set by `ask_economics`. Keys with no row: the chillers'
`opex.per_energy`, `revenue.subsidy.capacity` (a project value). A plant needs a `capex` and an
`opex.fixed` value for every equipment kind it holds; once one `opex.per_energy` is given, every
producing kind of the plant needs one (§16.1).

### 0.5 What gemini returns, and how to read it

| Name | Title (display) | Unit | Read it as |
|---|---|---|---|
| `capex` | Investment | MEUR | sum over modules; quote the parts by module path as given |
| `opex` | Operating cost | MEUR/yr | parts: `fixed`, `electricity`, `fuel`, `waste`, `chemical`, `co2`, `per_energy` |
| `annualised_cost` | Annualised cost | MEUR/yr | capex annuity plus opex |
| `lcoh` | Cost of heat | EUR/MWh | needs `heat_cost_share` when the plant also delivers cold |
| `lcoc` | Cost of cold | EUR/MWh | the rest of the cost over the cold |
| `lcts` | Cost of thermal supply | EUR/MWh | whole cost over heat plus cold; no allocation; the ranking metric |
| `npv` | Net present value | MEUR | needs `revenue.*` |
| `payback` | Payback time | yr | simple, undiscounted; "never pays back" when revenue does not exceed opex |
| `co2` | CO2 | kt over the run | CO2-equivalent: direct + GWP × methane + grid electricity × intensity |

A value that is `None` comes with a `reason`: report the reason, never a number. A metric
reported as a study's `mean`, `p5`, `p50`, `p95` carries its study key and its `failed` count.

### 0.6 Hard limits of a case, and what they do to the costs

A brief's hard limits are requirements of the case (`knowledge/handbook-case.md`): taken from the
brief or its assumptions document, never chosen by an agent. A design that breaks one is not
feasible and is never ranked on cost (§14.1). Each kind of limit moves the costs in a known way:

| Kind of limit | Typical form | What it does to the costs |
|---|---|---|
| Number of doublets | a minimum and a maximum count | caps the geothermal capacity; each doublet adds drilling capex (§2.2) |
| Flow per doublet | a range in m3/h while running | sets pump size and pump electricity (§2.3, §3.3) |
| Brine cooling | a maximum temperature drop in K | caps the heat per doublet; the rest comes from a heat pump, a boiler or more wells |
| Running time of a doublet | a maximum share of the year | forces backup capacity for the days it stands still (boiler or electric boiler capex) |
| Equipment efficiency | a fixed pump efficiency | fixes the electricity per unit of flow and head |
| Mass balance | production equals injection | adds the injection pump and its electricity |
| Supply temperatures | a level per service | decides heat pump, boiler or deeper wells (§17.2) |
| Delivered energy | an unmet share of the yearly demand | sets how much backup the plant needs |
| Prescribed factors | a grid CO2 intensity, a price set by the client | moves CO2 and opex directly (§9.4) |

Read the limits before costing, and say in the report which of them drove the cost of the
chosen design.

### 0.7 Checklist before costs are reported

- [ ] The costed result is the verified one, and its verdict is feasible (§0.1 rule 4).
- [ ] Every key came from §0.2 and carries its source; open keys are named, not filled.
- [ ] Currency and price year stated once; all prices in that year.
- [ ] LCTS (and NPV when prices differ) used to rank; LCOH and LCOC given with the
      `heat_cost_share` they rest on (§6.4).
- [ ] Carbon cost read as gemini prices it: the plant's own CO2 and methane, not grid
      electricity (§3.6, §16.7).
- [ ] Every number as the tool gave it, with its unit and the result reference.
- [ ] Sensitivity or uncertainty only when asked, with study key, samples, seed and failed draws.
- [ ] Placeholder or `secondary` inputs named, so the reader knows the estimate class (§11.2).

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

In deep geothermal plants the wells usually dominate, followed by a heat pump where one raises
the temperature; read gemini's capex by module to see which (§16.2).

### 2.2 Drilling and wells: cost against depth

Drilling cost rises faster than linearly with depth: deeper wells need more casing strings,
heavier rigs, more days and more risk. A single cost per metre is therefore valid only near the
depth it was measured at.

Sourced Dutch figures for a doublet (two wells) show the trend (cost catalogue
`knowledge/data-economics.csv`, rows `drilling-nl-2013-*`, from Mijnlieff, Ramsak, Lako et al.,
EGC 2013 slides, slide 26, status *verified*):

| Depth of each well | Net drilling cost per doublet | Per metre (2013) | Per metre (EUR 2015) |
|---|---|---|---|
| 2300 m | 5.7 MEUR | 1239.1 EUR/m | 1246.83 EUR/m |
| 3000 m | 11.0 MEUR | 1833.3 EUR/m | 1844.74 EUR/m |
| 4000 m | 16.5 MEUR | 2062.5 EUR/m | 2075.37 EUR/m |

The per-metre figures divide the doublet cost by two wells times the depth; the catalogue notes
that the slide does not say "per doublet" explicitly. An ECN cost curve (Straathof 2012, MSc
thesis, ECN-O--12-043, p. 16, catalogue rows `drilling-ecn-2012-*`, status *secondary*) gives
cost in MEUR as `1e-7 x² + 0.0018 x + 0.3859` with `x` the well depth in m (R² = 0.596); the
catalogue holds it at 2000 m (2236.51 EUR2015/m) and 3000 m (2272.92 EUR2015/m).

Rules:

- Price drilling by **measured depth** (along the hole), not true vertical depth, for deviated
  wells.
- Use a **depth table** when the design searches over depth; a single per-metre price favours
  deep wells unfairly. gemini accepts a table of cost per metre against depth (section 16.2).
- Add the **drill site** (location, access, mud handling) once per site: 300 000 EUR (2019),
  286 260 EUR2015, per location (catalogue row `drilling-location-surface`, from *Geothermal
  Energy* 2021, Table 4, status *secondary*). gemini has no key for it: it is a whole-plant item,
  named as left out or folded into a stated factor.
- Drilling cost depends strongly on country, rig market and year; a figure from another market
  needs a stated reason to apply.

### 2.3 Downhole and injection pumps

The production well usually needs an electric submersible pump (ESP); reinjection may need a
surface injection pump. Their capex is small next to the wells, but their power drives the
electricity bill and their failures drive the opex (section 3.5).

Sourced figures (cost catalogue, EUR 2015):

| Row | Figure | Status |
|---|---|---|
| `esp-unit-2019` | 763 359 EUR per ESP unit (800 000 EUR of 2019), replaced every 5 years (*Geothermal Energy* 2021, Table 4) | secondary |
| `production-pump-esp-kennisagenda-2016-250kwel`, `-500kwel` | 0.718 and 0.599 EUR/W electric | secondary |
| `production-pump-schlagermann-2023-332kwel` | 1.546 EUR/W electric | verified |
| `injection-pump-proxy-dh-station` | 0.099 EUR/W (a district heating station pump as proxy) | secondary |

gemini prices a pump per W of shaft power at its nominal flow (or a production pump per unit,
EUR); a row per W electric is used as the nearest basis and named so. The GEOPHIRES-X correlations
(USD, no price year) were removed from the catalogue (QA-045).

### 2.4 Surface plant

**Heat exchangers.** Brine-to-water plate exchangers. Cost scales with area, which scales with
the conductance UA (W/K) for a given duty and temperature approach. A cost per W of duty hides the
approach temperature; a cost per W/K does not. The catalogue's only row is per W of duty
(`heat-exchanger-dea-2025-station`, 0.109 EUR2015/W, secondary), a basis gemini accepts.

**Heat pumps.** Large electric heat pumps raise geothermal heat to the network temperature or
recover heat from the cooling side. Sourced: Danish Energy Agency (DEA), *Technology Data for
Generation of Electricity and District Heating*, version 0019 (August 2026), sheet "40 Comp. hp,
waste heat 10 MW": nominal investment 0.95 MEUR/MW of heat (EUR 2025), fixed O&M 2126.745
EUR/MW/yr.

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
"separation of hydrocarbons" (row `degasser-nl-2013`, 1 006 240 EUR2015, secondary). The flare
and the gas make-up have proxy rows only (`flare-capex-proxy-epa-2019`, 57 700 EUR;
`gas-makeup-capex-proxy-npro-chp-1mwe`, 636 893 EUR; both secondary).

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

A bottom-up capex should be checked against whole-plant figures. Sourced benchmarks (cost
catalogue, all per W of heat capacity, including wells; the EUR 2015 value is the row's
`value_2015`):

| Row | Plant | Figure | EUR 2015 |
|---|---|---|---|
| `plant-dea-2025-2000m-21mw` | DEA sheet 45.1.b, 2 wells of 2000 m, 21 MW, 80/40 °C, with heat pump | 1.9 EUR/W (2025) | 1.476 EUR/W |
| `plant-dea-2025-2000m-62mw` | DEA sheet 45.3, 6 wells of 2000 m, 62 MW | 1.75 EUR/W (2025) | 1.359 EUR/W |
| `plant-dea-2025-1200m-15mw` | DEA sheet 45.1.a, 1200 m, 15 MW | 2.436 EUR/W (2025) | 1.892 EUR/W |
| `plant-pbl-2026-under-12mw` | PBL, SDE++ 2026 final advice, NL deep geothermal below 12 MW (reference 8.7 MW), Table 11.7a | 2.463 EUR/W (2026) | 1.913 EUR/W |
| `plant-pbl-2026-12-20mw` | Same, 12 to 20 MW (reference 15.9 MW), Table 11.7b | 1.719 EUR/W (2026) | 1.335 EUR/W |
| `plant-pbl-2026-over-20mw` | Same, 20 MW and above (reference 27.4 MW), Table 11.7c | 1.34 EUR/W (2026) | 1.041 EUR/W |

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

The first three figures are DEA's in EUR 2025 (2020 for sheets 44 and 06); the catalogue carries the DEA 2018 and 2025 rows at 2015 prices
(`opex-heat-pump-dea-2025-10mw` 1652.04, `opex-boiler-gas-dea-2018` 1950,
`opex-chp-gas-engine-dea-2018` 9750 EUR/MW/yr). Note the spread:
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
data are scarce and all `secondary` in the catalogue: scale inhibitors 0.77 to 2.91 EUR2015/kg
(rows `scale-inhibitor-*`), corrosion inhibitors 1.94 to 3.11 EUR2015/kg
(`corrosion-inhibitor-indexbox-2026-eu-amine-*`), non-hazardous waste 0.0497 EUR2015/kg (Dutch
sewage sludge processing, `waste-disposal-proxy-sewage-sludge`). Radioactive (NORM) or hazardous
scale costs far more: 45.93 EUR2015/kg (`waste-disposal-norm-proxy-covra-2026`) or 3.87
EUR2015/kg for very-low-level filter waste (`waste-disposal-tfa-france-per-kg-filter-density`).
Choose the row by what the waste is, and say which.

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
plant's opex counts it twice.

gemini's convention (since 0.6.16, QA-128): `carbon.price` applies to the plant's own CO2 and
methane (as CO2-equivalent) only. Grid electricity's CO2 is in the `co2` metric but not priced
(section 16.7).

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
`INX_A_AVG`, coicop `CP00`, geo `EA`, update of 2026-02-06; the index the catalogue's
`value_2015` column uses, `knowledge/data-economics.md`):

| 2008 | 2010 | 2012 | 2013 | 2014 | 2015 | 2017 | 2019 | 2020 | 2023 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| 91.38 | 93.14 | 98.05 | 99.38 | 99.81 | 100.00 | 101.78 | 104.80 | 105.06 | 123.15 | 128.75 |

(All values from the same Eurostat series.)

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
  pump and the gas boiler; the catalogue's `analysis-period-dea-2019-geothermal-dk` gives 25 yr
  for a Danish geothermal plant, `analysis-period-sde-2025-subsidy-period` 15 yr (the SDE++
  term).
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

The revenue is the useful heat and cold sold, times their prices. Sourced reference prices (cost
catalogue, EUR 2015 values from the catalogue):

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
2026 auctions", 8 January 2026, https://energy.instrat.pl/en/eu-ets-2025-summary/; a secondary
source). In EUR 2015: `73.43 / 1.2875 = 57.03 EUR/t` **(derived)**. The catalogue's verified rows: EU ETS
57.48 EUR2015/t (2026, `carbon-price-eu-ets-esma-2026`) and 51.56 (2025), Dutch CO2 levy 61.10
(2026).

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
  efficiency of 0.98, cited to US EPA AP-42 section 13.5).

Bought gas burnt in boilers adds its combustion CO2, from its composition.

### 9.3 Methane and global warming potentials (IPCC AR6)

Methane released unburnt is converted to CO2-equivalent with a global warming potential (GWP):

`CO2e = m_CO2 + GWP_CH4 · m_CH4`

| Value | Figure | Source |
|---|---|---|
| GWP100, fossil methane | 29.8 | IPCC AR6 WG1, chapter 7, table 7.15 (Forster et al. 2021), as quoted by Muñoz, Schmidt and Weidema (2024), *Environmental Research Letters* 19(12), 121002 |
| GWP100, biogenic methane | 27.0 | same |
| GWP100, methane without the fossil carbon split | 27.9 | IPCC AR6 WG1 chapter 7 supplementary material (catalogue `gwp-ch4-ar6-ipcc-2021-sm`, verified) |
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

Sourced averages (cost catalogue, rows `co2-grid-eu-2025` and `co2-grid-eu-2024`, Ember Yearly
Electricity Data, EU power sector CO2 intensity, verified): **209.21 g/kWh (2025)**, 211.52 g/kWh
(2024). A client or a brief may prescribe its own factor (the catalogue keeps one such row,
`co2-grid-organisers-2026`, 300 g/kWh); then the prescribed value is the case's. The key is a case value,
`utilities.electricity.co2_intensity`, not an economics key. A factor for 2015
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
GJ/yr. The other gas band limits are not
quoted here (not verified).

Each price is given at three tax levels: excluding taxes and levies, excluding VAT and other
recoverable taxes (`X_VAT`), and all taxes included.

Sourced examples (EU27_2020 average, `X_VAT`):

- Electricity, band IE, 2025-S1 0.1381 and 2025-S2 0.1342 EUR/kWh, mean 136.15 EUR/MWh (EUR
  2025), 105.75 EUR/MWh in EUR 2015 (Eurostat `nrg_pc_205`, API data of 2026-10-19).
- Gas, band I4, 2025-S1 0.0545 and 2025-S2 0.0483 EUR/kWh (gross calorific value), mean 51.4
  EUR/MWh (EUR 2025), 39.92 EUR/MWh in EUR 2015 (Eurostat `nrg_pc_203`).

The catalogue's rows are Dutch, 2024 (secondary): electricity band ID 115.02 and band IE 138.02
EUR2015/MWh (`electricity-nl-eurostat-2024-band-*`), gas band I4 37.51 and I3 44.42 EUR2015/MWh
on the gross calorific value (`gas-nl-eurostat-2024-band-*`). It has no EU-average row.

### 10.2 Choosing a band and a tax level

- Choose the band from the plant's **yearly** consumption from the simulation. A plant that buys
  26 GWh/yr of electricity is in band IE (20 000 to 69 999 MWh).
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

The project's own catalogue, `knowledge/data-economics.csv` (154 rows at 2026-11-05: 75
verified, 79 secondary, no placeholder; notes and batches in `knowledge/data-economics.md`),
holds these figures with quote, price year, `value_2015` and the case key (`path`) each feeds.
It is reference data, not defaults: a row enters a case only through the user's approval
(§0.2).

### 11.2 Grading the quality of a figure

The cost catalogue grades each row:

- **verified**: the figure was read in the official source, dataset or report it is credited to;
- **secondary**: real and quoted, but from a thesis, a citing paper, code, or a proxy for another
  item;
- **placeholder**: no verified source; the gap is kept visible. Since 2026-11-05 the catalogue
  holds none (rows without a source were removed); a placeholder may survive in an example case
  and must be named as one in any report.

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
   (sections 3.1, 3.2, 3.6; gemini prices only the plant's own CO2).
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
19. **Defaults filled silently** where the case lacks a value (§0.1, rule 2).
20. **Numbers of your own**: a sum, share, difference or conversion of gemini's values in an
    agent's answer instead of the tool's value (§0.1, rule 1).
21. **`passed` read as feasible**: feasibility is the verdict's `feasible` (§16.7).

---

## 16. How gemini computes economics

This chapter describes what gemini (`import gemini as gm`) computes and under which names, read
from the code of gemini 0.6.17 (`gemini/gemini/evaluate/costs.py`, `evaluate/_utils/cost.py`,
`evaluate/_utils/levelised.py`, `evaluate/_utils/cashflow.py`, `evaluate/emissions.py`,
`case/economics.py`, `case/_utils/kinds.py`, `study/metrics.py`). How an agent calls these through
its tools is in the `economics` skill (`geomind/geomind/skills/economics/SKILL.md`), and only there.

### 16.1 The economics file (`economics.json`)

The economics of a case is one JSON file with the header `format`, `kind: "economics"`, `name`.
Every value is `{"value": ..., "unit": ...}`; nothing has a default, and a value that is absent is
missing (section 16.8). Keys (paths as gemini names them in errors, prefixed `economics.`):

| Key | Meaning |
|---|---|
| `currency` | a label for every amount (text); gemini converts no currency |
| `price_year` | the year the prices are in (whole number) |
| `discount_rate` | real discount rate per year, a fraction (0.05 is 5 %) |
| `analysis_period` | years of the analysis (yr) |
| `capex.<kind>` | capex factor of each equipment kind (section 16.2); `capex.drilling` may be a depth table `{depth: {value: [...], unit: "m"}, cost_per_metre: {value: [...], unit: "EUR/m"}}`, interpolated linearly, no extrapolation (`out_of_bounds`) |
| `opex.fixed.<kind>` | fixed O&M of each kind: share of its capex per year (`%/yr`, `1/yr`), or for a kind sized by a power an amount per capacity and year (`EUR/MW/yr`) |
| `opex.per_energy.<kind>` | optional variable O&M per energy produced (EUR/MWh) for the producing kinds `boiler`, `electric_boiler`, `chp`, `heat_pump`, `compression_chiller`, `absorption_chiller`, `adsorption_chiller`; once given, every producing kind of the plant needs one |
| `opex.variable.chemical` | price of dosed chemicals per kg (constant or series) |
| `opex.variable.waste_disposal` | cost of waste disposal per kg (constant or series) |
| `energy.electricity` | price of grid electricity (constant or series) |
| `energy.gas` | price of bought gas per energy of its **lower** heating value (constant or series); co-produced gas costs nothing |
| `carbon.price` | price of CO2-equivalent emitted, added to the opex (constant or series) |
| `revenue.heat`, `revenue.cold` | price of useful heat and cold delivered (constant or series) |
| `revenue.subsidy` | `amount` (per year, or per energy of useful heat as SDE++ pays), `duration` (yr), optional `cap` (MWh/yr, or full-load hours h/yr times `capacity` MW) |
| `accounting.allocation.heat_cost_share` | share of the cost charged to heat (0 to 1); LCOC gets the rest |
| `accounting.gwp.standard`, `accounting.gwp.CH4` | the name of the GWP set, and the GWP of methane |

Any value may carry an `uncertainty`: `{kind: "uniform", min, max}`, `{kind: "triangular", min,
max}` (the value is the mode) or `{kind: "normal", std, min, max}` (cut at min and max). A normal
run uses only the value; the studies draw from the uncertainty. The grid emission factor is not in
the economics but in the case: `utilities.electricity.co2_intensity` (g/kWh, constant or profile).
`gm.Case.schema()` and `Economics.schema()` give the full JSON Schema; an agent asks
`describe_case("economics.<key>")` for the units a key accepts.

### 16.2 Capex by equipment kind

Each module that is equipment declares a kind; its capex is the factor of its kind times its cost
size. The capex of the plant is the sum over modules; the result lists every module path with its
kind and capex, and the price year. The kinds and their bases (`case/_utils/kinds.py`):

| Kind | Basis of `capex.<kind>` | Other accepted bases |
|---|---|---|
| `drilling` | per m of well (EUR/m), or depth table | |
| `production_pump`, `injection_pump`, `circulation_pump` | per W of shaft power at nominal flow (EUR/W) | `production_pump`: per unit (EUR) |
| `heat_pump`, `boiler`, `electric_boiler`, `absorption_chiller`, `adsorption_chiller`, `compression_chiller`, `cooler` | per W of capacity | |
| `chp` | per W of electric capacity | |
| `heat_exchanger` | per W/K of conductance | per W of nominal duty |
| `pipe` | per m | per MW and m |
| `thermal_storage`, `ice_storage` | per m3 | per MWh of energy capacity; `ice_storage` is priced only when its capex is given |
| `degasser`, `flare`, `gas_makeup` | fixed amount (EUR) | |

The unit of the factor tells gemini which basis is meant. Wells are priced as their sections: in
gemini's plant classes a production doublet has `dN.well` (below the pump), `dN.riser` (above
it) and `dN.injector`, each of kind `drilling`; their lengths add to the well depth.

### 16.3 Opex

`gm.evaluate.opex` returns the yearly operating cost with `components`:

- `fixed`: per kind, `opex.fixed.<kind>` × capex of that kind (or × capacity for EUR/MW/yr);
  listed in `fixed_by_kind`;
- `electricity`, `fuel`, `waste`, `chemical`: what the run bought or discarded × its price, step
  by step (a price series follows the run);
- `co2`: the plant's own CO2-equivalent of every step (CO2 released and methane × GWP, not the
  CO2 of grid electricity) × `carbon.price`, when a carbon price is given;
- `per_energy` (and `per_energy_by_kind`): only when `opex.per_energy` is given.

The run is scaled to a year: amount over the run × 365.25 d / duration of the run.

### 16.4 Annualised cost, LCOH, LCOC, LCTS

With `A = (1 − (1 + r)^−n) / r` (the annuity factor of section 5.2, `n` the analysis period; `A =
n` at `r = 0`) and constant yearly opex, heat and cold:

| Name (gemini) | Formula | Unit (display) |
|---|---|---|
| `annualised_cost` | `capex / A + opex` | MEUR/yr |
| `lcoh` | `s_heat · (capex + opex · A) / (Q_heat · A)` | EUR/MWh |
| `lcoc` | `(1 − s_heat) · (capex + opex · A) / (Q_cold · A)` | EUR/MWh |
| `lcts` | `annualised_cost / (Q_heat + Q_cold)` | EUR/MWh |

`s_heat` is `accounting.allocation.heat_cost_share`. A plant that delivers only heat charges it the
whole cost (`s_heat` not needed); a plant that delivers heat and cold without a share gets no LCOH
or LCOC, with the reason "the split of its cost is not defined". `lcts` needs no share. Heat is
the useful heat delivered to the heating grid, cold what the water gains across the cooling grid,
both per year as scaled from the run.

### 16.5 NPV, payback and subsidy

| Name | Formula |
|---|---|
| `npv` | `−capex + (revenue − opex) · A + subsidy · A(r, min(duration, n))` |
| `payback` | `capex / (revenue − opex + subsidy)` years, without discounting; with a subsidy shorter than the payback, the years after it count at `revenue − opex` only |

`revenue` = heat × `revenue.heat` + cold × `revenue.cold` per year. A subsidy pays from the first
year for its `duration`; a subsidy per energy pays on the useful heat of a year up to its `cap`. A
subsidy with only one of `amount` and `duration` earns nothing. A plant whose yearly revenue does
not exceed its yearly cost has no payback ("never pays back").

### 16.6 CO2

`gm.evaluate.co2` returns the CO2-equivalent over the run (kg; display kt), step by step:

`co2 = direct + GWP_CH4 · methane + grid_energy · co2_intensity`

with parts `direct` (CO2 released: from the brine gas and from combustion in boilers, CHP and the
flare), `methane` (mass of CH4 released, before the GWP), `electricity` (CO2 of grid electricity),
`fuel_energy`, `grid_energy` and `window`. On-site generation offsets grid consumption first; a
surplus earns no credit. The CO2 follows the gas composition of the case, because each module
computes what it burns or releases. The `co2` metric holds all three parts; the carbon price in
the opex applies to `direct` and `GWP_CH4 · methane` only (section 16.7).

### 16.7 Conventions and limits

- One representative run, scaled to a year of 365.25 days, repeated over the analysis period: no
  degradation, no replacements, no residual value, no tax, no escalation, no construction period
  (sections 5.3, 5.4).
- All capex at year 0; yearly flows at the end of years 1 to `n`.
- `currency` is a label; prices must be converted to `price_year` before they enter the file
  (chapter 4).
- The carbon price applies to the plant's own CO2 and methane only (`priced_steps` in
  `evaluate/_utils/co2_steps.py`, since gemini 0.6.16, QA-128). Grid electricity's CO2 is counted
  in the `co2` metric but not priced again: the electricity price already carries the
  generators' ETS cost (section 3.6). Before 0.6.16 it was priced too; a cost figure from an
  older run or document can be higher for that reason.
- A replacement (for example ESPs every 5 years) is not modelled; fold it into `opex.fixed` as an
  equivalent yearly share if needed, and say so.
- The metrics a study reads are `heating_coverage`, `cooling_coverage`, `cop`, `peak_heat`,
  `peak_cold`, `lcoh`, `lcoc`, `lcts`, `annualised_cost`, `co2` (`gm.study.metrics()`); `npv` and
  `payback` are functions of `gm.evaluate`, not study metrics.
- `gm.evaluate.report` gives `heat_delivered`, `cold_delivered`, `boiler_heat`,
  `electricity_bought`, `gas_bought`, `capacities`, `capex`, `opex`, `lcts`, `lcoh`, `lcoc`, `co2`,
  `requirements`, `passed`, `verdict`, `failed_steps`, `failures`, `services`; costs are read with
  `on_error="record"`, so a cost that cannot be given is `None` with a `reason`. Feasibility is
  `verdict` (`feasible`), not `passed`: `passed` tallies only the checks that ran, so a plant
  that delivers no cold to a case with a cooling demand can show `passed` true while its verdict
  is not feasible (`cold_delivered`).

### 16.8 Errors, missing values and tools

- A factor, price or rate the plant needs and the case lacks raises `ValidationError` with code
  `missing_assumption` and the `path` of the missing key (for example
  `economics.capex.heat_pump`); geomind's tools pass it on as `case_incomplete` with that path.
  gemini never estimates it. The fix is to find a sourced value (§0.2) and have the user approve
  it, then set it in the case.
- With `on_error="record"` the value is `None` with a `reason`, so a report of many designs stays
  comparable.
- The agent tools that compute these numbers (`estimate_costs`, `compute_kpis`,
  `sample_uncertainty`, `sensitivity`) and the studies are documented in the `economics` skill.
  Read the skill for their arguments; this handbook does not repeat them.

---

## 17. Worked example: a deep doublet plant for heating and cooling

Every number in this chapter is **invented** to show the method; none is a price, a cost or a
result to use. The arithmetic is shown so the reader sees what gemini does; an agent never does
it and quotes gemini's tools instead (§0.1).

### 17.1 The case

A town needs 100 000 MWh/yr of heat (peak 25 MW) and 20 000 MWh/yr of cold. A deep reservoir
gives brine with dissolved gas. The economics: EUR at one price year, real discount rate 0.05,
analysis period 25 yr, so `A(5 %, 25) = 14.0939` (§5.2); electricity 100 EUR/MWh, gas 40 EUR/MWh,
carbon 60 EUR/t on the plant's own emissions, grid 0.25 t CO2/MWh, heat and cold sold at
70 EUR/MWh, `heat_cost_share` 0.8. Every one of these is, in a real case, a sourced value the user
approved (§0.2).

### 17.2 Three configurations

| Plant | How the supply temperature is reached | How cold is made |
|---|---|---|
| A | geothermal heat raised by an electric heat pump | compression chiller |
| B | geothermal heat topped up by a gas boiler | absorption chiller driven by hot water |
| C | deeper wells, hot enough without a heat pump | absorption chiller |

All three meet the same requirements in a full-year run; only then are they compared (§14.1).

### 17.3 Capex and opex of plant A

Capex 30.0 MEUR (wells, pumps, heat exchanger, heat pump, chiller, boiler for backup). Yearly
opex 2.78 MEUR: fixed O&M 0.40, electricity 22 000 MWh × 100 EUR/MWh = 2.20, carbon on the
plant's own 3 000 t CO2e × 60 EUR/t = 0.18. The grid electricity's 22 000 × 0.25 = 5 500 t is in
the CO2 figure but carries no carbon cost: the electricity price holds it (§3.6).

### 17.4 Levelised costs

- annualised cost = 30.0 / 14.0939 + 2.78 = 2.129 + 2.78 = 4.909 MEUR/yr;
- LCTS = 4 908 574 / 120 000 = 40.90 EUR/MWh;
- LCOH = 0.8 × 4 908 574 / 100 000 = 39.27 EUR/MWh;
- LCOC = 0.2 × 4 908 574 / 20 000 = 49.09 EUR/MWh.

The energy share of heat is 100 000 / 120 000 = 0.833; with that share LCOH = LCOC = LCTS. The
fixed 0.8 makes cold look dearer than heat: an allocation effect, not a property of the plant
(§6.4). Rank on LCTS.

### 17.5 NPV and payback

Revenue 70 × 120 000 = 8.40 MEUR/yr; net 8.40 − 2.78 = 5.62 MEUR/yr; NPV = 5.62 × 14.0939 − 30.0
= 49.21 MEUR; simple payback 30.0 / 5.62 = 5.34 yr. Break-even price for heat and cold alike =
LCTS = 40.90 EUR/MWh (§7.2).

### 17.6 CO2

Own emissions 3 000 t (the brine's CO2 and the burnt or flared gas, §17.7) plus grid 5 500 t =
8 500 t CO2e/yr; 71 kg per MWh delivered. Two thirds is grid power, so the footprint follows the
grid factor of the years the plant runs (§9.4).

### 17.7 Co-produced gas: vent, flare, boiler or CHP

The brine carries gas: 150 m3/h of brine, gas-liquid ratio 0.8 Nm3/m3, 80 mol% CH4 and 20 mol%
CO2, 8 000 running hours a year.

- CH4: 150 × 0.8 × 0.8 = 96 Nm3/h × 0.717 kg/Nm3 = 68.8 kg/h, 551 t/yr; at 50 MJ/kg it is
  0.96 MW of fuel, 7 650 MWh/yr.
- CO2 from the brine: 150 × 0.8 × 0.2 = 24 Nm3/h × 1.977 kg/Nm3 = 47.4 kg/h, 380 t/yr. It leaves
  whatever is done with the methane (unless reinjected).

| Option | CO2e (t/yr) | Carbon cost at 60 EUR/t (MEUR/yr) | Energy gained (MWh/yr) | Value of the energy (MEUR/yr) |
|---|---|---|---|---|
| Vent | 551 × 29.8 + 380 = 16 790 | 1.01 | none | none |
| Flare (98 % combustion) | 0.98 × 551 × 2.75 + 0.02 × 551 × 29.8 + 380 = 2 190 | 0.13 | none | none |
| Boiler (90 %) | 551 × 2.75 + 380 = 1 890 | 0.11 | 6 880 heat | 0.31 (gas a boiler would otherwise buy: 6 880 / 0.9 × 40) |
| CHP (35 % electric, 50 % heat) | 1 890 | 0.11 | 2 680 electricity, 3 820 heat | 0.27 + 0.17 |

Lessons:

1. Venting methane is never cheap once it is priced: at GWP 29.8 it is almost eight times the
   flare's CO2e (§9.3).
2. Burning the gas changes the CO2e little against flaring but earns energy; the choice between
   boiler and CHP turns on the extra capex and the electricity price.
3. In gemini each choice is a module (flare, boiler, CHP on the gas line); its capex kind, its
   fuel and its emissions follow from the case's gas composition, and the carbon price applies
   to what it emits (§16.6). Compare the options as whole designs on LCTS and CO2.

### 17.8 Sensitivity of plant A

For economic inputs the simulation does not change, so the LCTS moves linearly:

| Input | Low | High | LCTS at low | LCTS at high | Swing |
|---|---|---|---|---|---|
| Electricity price | 80 EUR/MWh | 130 EUR/MWh | 37.24 | 46.40 | 9.17 |
| Discount rate | 0.03 | 0.08 | 37.52 | 46.59 | 9.06 |
| Carbon price | 30 EUR/t | 100 EUR/t | 40.15 | 41.90 | 1.75 |

Method: electricity `ΔLCTS = Δp · 22 000 / 120 000`; carbon `Δp · 3 000 / 120 000` (own emissions
only); discount rate `capex · (1/A(r) − 1/A(5 %)) / 120 000` with A(3 %, 25) = 17.4131 and
A(8 %, 25) = 10.6748. Physical inputs (permeability, gradient) need new runs: gemini's
`sensitivity`, through the skill `economics`.

### 17.9 Comparing the configurations

| Plant | Capex (MEUR) | Opex (MEUR/yr) | LCTS at 5 % | LCTS at 3 % | LCTS at 8 % | CO2e (t/yr) | NPV at 5 % (MEUR) |
|---|---|---|---|---|---|---|---|
| A | 30.0 | 2.78 | 40.90 | 37.52 | 46.59 | 8 500 | 49.21 |
| B | 22.0 | 4.40 | 49.67 | 47.20 | 53.84 | 17 000 | 34.38 |
| C | 36.0 | 2.30 | 40.45 | 36.40 | 47.27 | 4 500 | 49.97 |

Reading:

- B has the lowest capex and the highest cost and CO2: it is dominated (§14.3).
- At 5 % and 3 %, C beats A on LCTS and CO2: C dominates. At 8 % A is cheaper: the ranking flips
  between 5 % and 8 %. That discount rate is a **switching value** (§12.3); report it, because
  the choice rests on it.
- C's advantage rests on its deeper wells, so its drilling cost needs a depth table (§2.2) and
  its reservoir temperature an uncertainty range (§13).

### 17.10 Lessons from the example

1. Rank on LCTS or NPV; give LCOH and LCOC only with their allocation.
2. A capital-heavy design wins at a low discount rate and loses at a high one: test the ranking
   over the plausible rates.
3. Price carbon on the plant's own emissions; report the grid CO2 beside it.
4. Associated gas is a design choice with a cost, a CO2 effect and an energy value: compare the
   options as whole designs.
5. A comparison holds only for designs that pass the same requirements on the same case.

---

## Appendix A. Symbols and formulas

| Symbol | Meaning | Unit |
|---|---|---|
| `I_0`, capex | investment at year 0 | EUR |
| `C`, opex | yearly operating cost | EUR/yr |
| `R` | yearly revenue | EUR/yr |
| `Q_heat`, `Q_cold` | useful heat and cold delivered per year | MWh/yr |
| `r` | real discount rate | - |
| `n` | analysis period | yr |
| `A(r, n)` | annuity factor `(1 − (1+r)^−n)/r` | yr |
| `CRF` | capital recovery factor `1/A` | 1/yr |
| `s_heat` | share of cost charged to heat | - |

- Present value: `PV = F/(1+r)^t`
- Annualised cost: `I_0 · CRF + C`
- LCOH: `s_heat · (I_0 · CRF + C) / Q_heat`; LCOC: `(1 − s_heat) · (I_0 · CRF + C) / Q_cold`
- LCTS: `(I_0 · CRF + C) / (Q_heat + Q_cold)`
- NPV: `−I_0 + (R − C) · A`; payback: `I_0 / (R − C)`
- Price conversion: `x_b = x_a · HICP(b)/HICP(a)`
- Fisher: `1 + i_nom = (1 + i_real)(1 + π)`
- CO2e: `m_CO2 + GWP_CH4 · m_CH4 + E_grid · f_grid`
- Abatement cost: `ΔAnnualised cost / ΔEmissions`

## Appendix B. References

Sources marked *as quoted* were read through the named project file, not re-opened for this
handbook.

- AACE International, Recommended Practice 18R-97, Cost Estimate Classification System (ranges not
  re-read; section 11.2).
- Copenhagen Economics (2021), *District Heating Tariffs in Europe*, for the Dutch Ministry of
  Economic Affairs and Climate, p. 21 (as quoted in the cost catalogue).
- Danish Energy Agency and Energinet (2026), *Technology Data for Generation of Electricity and
  District Heating*, version 0019, with data sheets, https://ens.dk/en/analyses-and-statistics/technology-data-generation-electricity-and-district-heating
  (as quoted in the cost catalogue).
- Ember, Yearly Electricity Data (as quoted in the cost catalogue, rows `co2-grid-eu-*`).
- European Commission (2025), Better Regulation Toolbox, Tool #64 Discount factors (as quoted in
  the cost catalogue).
- Commission Delegated Regulation (EU) No 480/2014, Art. 19(3) (as quoted in the cost catalogue).
- Directive 2003/87/EC establishing the EU Emissions Trading System, as amended.
- Eurostat, `prc_hicp_aind`, `nrg_pc_203`, `nrg_pc_205` (as quoted in the sample README and the
  cost catalogue); band codes from Eurostat dataset metadata.
- Forster, P. et al. (2021), IPCC AR6 WG1 chapter 7, table 7.15, as quoted by Muñoz, Schmidt and
  Weidema (2024), *Environmental Research Letters* 19(12), 121002, https://doi.org/10.1088/1748-9326/ad8edd.
- Geothermal Energy (2021), "Economic and fault stability analysis of geothermal field development
  in direct-use hydrothermal reservoirs", Table 4 (as quoted in the cost catalogue).
- Instrat Foundation (W. Przedlacki, 2026), "EU ETS 2025 summary and the beginning of 2026
  auctions", https://energy.instrat.pl/en/eu-ets-2025-summary/ (as quoted in the sample README).
- Mijnlieff, H., Ramsak, P., Lako, P. et al. (2013), *Geothermal energy and support schemes in The
  Netherlands*, EGC 2013 slides, slide 26 (as quoted in the cost catalogue).
- PBL (2026), *Eindadvies basisbedragen SDE++ 2026*, Tables 11.7a to c, p. 104 (as quoted in the
  cost catalogue).
- RVO, SDE++ pages "Berekening SDE++" and "Kenmerken", https://www.rvo.nl/subsidies-financiering/sde.
- Short, W., Packey, D. J. and Holt, T. (1995), *A Manual for the Economic Evaluation of Energy
  Efficiency and Renewable Energy Technologies*, NREL/TP-462-5173, https://www.nrel.gov/docs/legosti/old/5173.pdf
  (the reference for the standard definitions; not re-read for this handbook).
- Straathof, D. (2012), *Costs of Deep Geothermal Energy in the Netherlands*, MSc thesis,
  ECN-O--12-043 (as quoted in the cost catalogue).
- US EPA, AP-42, section 13.5, flares (as cited by gemini for its flare).
- Project files: `knowledge/data-economics.csv` and `.md` (cost catalogue), gemini 0.6.17 source
  code (chapter 16).
