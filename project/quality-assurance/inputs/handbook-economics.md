**Handbook of Techno-Economic and Environmental Assessment of Geothermal Heating and Cooling Plants**

How to cost a geothermal heating and cooling plant, put a carbon footprint on it, and use both to
choose between designs. General for any case; chapter 17 works a full example on invented
numbers. Checked against gemini 0.6.34 (chapters 2, 18) and 0.6.17 (chapter 16) and the cost catalogue `knowledge/data-economics.csv` (157
rows) on 2026-11-05.

Cite as `knowledge/handbook-economics.md` with the section (for example
`knowledge/handbook-economics.md §6.3`). Every section stands alone: read the one you need
(`read_knowledge` with its number). Chapter 0 is the short version for agents; chapter 18 holds
the lessons from practice (source order, units, basis, analysis period, stale results, sizing);
chapter 19 says where to find a value the catalogue lacks (other countries, grid CO2, chillers).

This handbook explains no tool. Running costs, sensitivity and uncertainty: skill `economics`.
Setting economics in a case (`ask_economics`, `set_case`): skill `setting-the-case`. Defining the
rest of the case: `knowledge/handbook-case.md`. Reporting the numbers:
`knowledge/handbook-report.md`.

**Outline** (read the section you need, not the whole book):

| Ch. | Topic | Start with |
|---|---|---|
| 0 | Rules, value sources, catalogue keys (0.4.1 capex, 0.4.2 opex, 0.4.3 prices), checklist | 0.1, 0.2 |
| 1 | Scope, boundary, energy by source | 1.4 |
| 2 | Capex: structure, drilling, pumps, surface plant, scaling, benchmarks, step by step | 2.8 |
| 3 | Opex: fixed, variable, energy, chemicals, workovers, carbon, step by step | 3.7 |
| 4 | Nominal and real money, price year (HICP), currency, escalation | 4.2, 4.5 |
| 5 | Discount rate, annuity and CRF, lifetimes, timing, replacements, WACC | 5.2 |
| 6 | LCOH, LCOC, LCTS, allocation, worked LCOH, mapping to gemini | 6.6 |
| 7 | Revenue, NPV, IRR, payback, subsidies, worked NPV | 7.5 |
| 8, 9 | Carbon price; CO2 accounting, GWP, grid factors, footprint example | 9.7 |
| 10, 11 | Energy price statistics; data sources and estimate classes | 11.2 |
| 12, 13 | Sensitivity, switching values; uncertainty and number of draws | 12.4, 13.4 |
| 14, 15 | Comparing and deciding (worked 14.4); common mistakes | 14.4, 15 |
| 16 | How gemini computes economics (keys, bases, formulas, errors) | 16.1 |
| 17 | Full worked example on invented numbers | 17.1 |
| 18 | Lessons from practice (QA): source order, units, basis, stale results, sizing | 18.1 |
| 19 | Finding a value the catalogue lacks (other countries, grid CO2, chillers, GCV) | 19.1 |

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
   verdict is not feasible is not compared with one that is (§14.1). Feasible means
   `check_results`'s `feasible` true, never the report's `passed`: `passed` counts only the checks
   that ran, so a plant that leaves a whole service unmet can show `passed` true and still be
   infeasible.
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
is a share of that kind's capex, `EUR/MW/yr` an amount per capacity. The rows are split in three
sections: capex keys (§0.4.1), opex keys (§0.4.2), and prices, revenue, finance and accounting
(§0.4.3). Read only the one you need.

`currency`, `price_year` (EUR, 2015) are set by `ask_economics`. Keys with no row: the chillers'
`opex.per_energy`, `revenue.subsidy.capacity` (a project value). A plant needs a `capex` and an
`opex.fixed` value for every equipment kind it holds; once one `opex.per_energy` is given, every
producing kind of the plant needs one (§16.1).

A row's unit must fit the key's basis: a pump row in EUR/W of heat is not a price per W of shaft
power (§18.3). A row that is a proxy (`proxy` in its id) says what it stands for in the catalogue.

#### 0.4.1 Capex keys

| Key | Catalogue rows: `id` value_2015 unit (status v = verified, s = secondary) |
|---|---|
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

#### 0.4.2 Opex keys

| Key | Catalogue rows: `id` value_2015 unit (status v = verified, s = secondary) |
|---|---|
| `opex.fixed.absorption_chiller` | `opex-absorption-chiller-iea-shc-2024` 3 %/yr (v); `opex-absorption-chiller-hre4-2017-500kw-share` 4 %/yr (s); `opex-absorption-chiller-hre4-2017-500kw-per-mw` 6800 EUR/MW/yr (s) |
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

#### 0.4.3 Prices, revenue, finance and accounting keys

| Key | Catalogue rows: `id` value_2015 unit (status v = verified, s = secondary) |
|---|---|
| `accounting.allocation.heat_cost_share` | `heat-cost-share-energy-fiaschi-2021` 0.87 - (s); `heat-cost-share-pes-fiaschi-2021-low` 0.71 - (s); `heat-cost-share-pes-fiaschi-2021-high` 0.76 - (s) |
| `accounting.gwp.CH4` | `gwp-ch4-fossil-ar6-ghgp-2024` 29.8 kg CO2e/kg CH4 (s); `gwp-ch4-non-fossil-ar6-ghgp-2024` 27 kg CO2e/kg CH4 (s); `gwp-ch4-ar6-ipcc-2021-sm` 27.9 kg CO2e/kg CH4 (v) |
| `accounting.gwp.standard` | `gwp-standard-ipcc-ar6-gwp100` IPCC AR6 GWP100  (v); `gwp-standard-eu-2020-1044-ar5` IPCC AR5 GWP100  (v) |
| `analysis_period` | `analysis-period-dea-2019-geothermal-dk` 25 yr (v); `analysis-period-sde-2025-subsidy-period` 15 yr (s) |
| `carbon.price` | `carbon-price-eu-ets-esma-price-2025` 57.48 EUR/t CO2e (v); `carbon-price-eu-ets-esma-price-2024` 51.56 EUR/t CO2e (v); `carbon-price-nl-co2-levy-price-2026` 61.1 EUR/t CO2 (v); `carbon-price-eu-ets-instrat-price-2025` 57.03 EUR/t CO2e (s) |
| `discount_rate` | `discount-rate-financial-eu` 0.04 - (v); `discount-rate-social-eu` 0.03 - (v); `discount-rate-pbl-sde-2022-geothermal-nominal` 0.056 - (v); `discount-rate-pbl-sde-2022-geothermal-real` 0.04 - (v); `discount-rate-ebn-gn-2026-pbl-ort` 0.087 - (s); `discount-rate-nl-mkba-2020` 0.0225 - (v); `discount-rate-pbl-sde-2025-geothermal-nominal` 0.072 - (v); `discount-rate-pbl-sde-2025-geothermal-real` 0.051 - (v); `discount-rate-pbl-sde-2026-erratum-row4-nominal` 0.073 - (s); `discount-rate-pbl-sde-2026-erratum-row4-real` 0.052 - (s) |
| `energy.electricity` | `electricity-nl-eurostat-price-2024-band-ie` 115 EUR/MWh (s); `electricity-nl-eurostat-price-2024-band-if` 138 EUR/MWh (s); `electricity-eu-eurostat-price-2025-band-ie` 105.8 EUR/MWh (s) |
| `energy.gas` | `gas-nl-eurostat-price-2024-band-i5` 37.51 EUR/MWh (GCV) (s); `gas-nl-eurostat-price-2024-band-i4` 44.42 EUR/MWh (GCV) (s); `gas-eu-eurostat-price-2025-band-i4` 39.92 EUR/MWh (GCV) (s) |
| `revenue.cold` | `cold-price-no-2017` 103.5 EUR/MWh (s); `cold-price-eu27-alternative-2014` 81.15 EUR/MWh (s); `cold-price-eu27-new-investment-2014` 110.2 EUR/MWh (s) |
| `revenue.heat` | `heat-price-nl-cap-2026` 114.6 EUR/MWh (v); `heat-price-se-2019` 81.11 EUR/MWh (v); `heat-price-nl-2019` 93.51 EUR/MWh (v) |
| `revenue.subsidy.amount` | `sde-basisbedrag-geothermal-pbl-2026-over-20mw` 48.7 EUR/MWh (v); `sde-basisbedrag-geothermal-pbl-2026-under-12mw` 62.06 EUR/MWh (v); `sde-net-subsidy-geothermal-pbl-2026-over-20mw` 27.5 EUR/MWh (s) |
| `revenue.subsidy.cap` | `sde-full-load-hours-geothermal-pbl-2026-over-20mw` 6000 h/yr (v) |
| `revenue.subsidy.duration` | `sde-duration-geothermal-stcrt-2025` 15 yr (v) |
| `utilities.electricity.co2_intensity` | `co2-grid-organisers-2026` 300 g/kWh (v); `co2-grid-eu-2025` 209.2 g/kWh (v); `co2-grid-eu-2024` 211.5 g/kWh (v) |

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
- [ ] Every number read from the tool that holds it (§0.8); the economics are the approved ones
      (§0.9).
- [ ] `estimate_costs` says `same_as_case` true; rated capacities checked against peak duty
      (§18.5, §18.7).

### 0.8 Which tool gives which number

Ask each tool only for what it holds; a name it does not hold is refused and costs a round trip.

| You need | Tool | Not from |
|---|---|---|
| capex (by module), opex (by component), `annualised_cost`, `lcoh`, `lcoc`, `lcts`, `npv`, `payback` | `estimate_costs` on the result | `compute_kpis` (it has no `annualised_cost`, `npv` or `payback`), `read_result` |
| energies delivered and bought, coverage, peaks, COP, capacities, the `co2` metric | `compute_kpis` on the result | `read_result` |
| feasible or not, and why | `check_results`: `feasible` and `reasons` | the report's `passed` |
| one module's series (a flow, a temperature, a day range) | `read_result` with that module's `path` | it holds module columns only: never `costs`, `lcts` or a cost name |
| the prices, rates and factors the costs used | `read_case` with section `economics` | `read_knowledge` (economics is a case file, not a document) |
| a ranking, a range or a sensitivity | `read_study` of its `study/<name>` | recomputing it |

### 0.9 A case without economics

Costs need every economics key the plant uses. When a case has none, or lacks some:

1. The agent that owns the case (the case lead) asks the user ONE economics question
   (`ask_economics`), which fills catalogue rows with their `value_2015` and sources (§0.2). Any
   other agent reports the missing keys with their paths and hands the work back; it does not
   build the economics itself.
2. What is written into the case is exactly what the user approved: the same number, unit and
   source. Never convert a unit or a price year between the question and the write, never pick
   a different row, never add a key the question did not show.
3. Ask once. After the approval the keys are set; a later question about costs reads them with
   `read_case`, never asks again.

Invented example of what goes wrong: the user approves "electricity 0.145 EUR/kWh (2024)" and the
case receives 115 EUR/MWh (converted to 2015 by the agent). The user approved one number and the
plant is costed on another; the card must show 115 EUR/MWh at 2015 prices from the start, as the
catalogue's `value_2015` gives it.

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

### 1.4 Energy accounting: heat by source when one unit drives another

Costs, CO2 and every "share from geothermal" rest on an energy balance at the system boundary
(§1.2). Units in a plant are often in series, and then one unit's output is not a share of the
delivered energy:

- **A heater that drives another unit.** A boiler (or the geothermal water) that heats the
  generator of an absorption chiller sends part of its heat into the chiller, not to the heating
  users. The heating users' heat by source is therefore not `heat_delivered − boiler_heat`.
- **A heat pump.** Its heat output is the heat it lifts from the brine plus its compressor work
  (electricity). The brine gave the output minus that work: output / COP of it is electricity.
- **A CHP.** Its fuel gives electricity and heat; the heat to the users is its heat output, the
  electricity is sold or offsets grid power.

Rules:

1. Take the split by source from gemini (its per-service coverage: geothermal, backup and short,
   as the result's coverage gives it), never by subtracting one unit's output from a total.
2. When no tool gives the split you need, say so; do not derive it.
3. For a heat pump plant, state the brine's heat and the compressor's electricity apart.

Invented example: heating demand 100 000 MWh/yr. The boiler makes 40 000 MWh, of which 12 000
drive the absorption chiller and 28 000 go to heating. Geothermal heat to the heating users is
100 000 − 28 000 = 72 000 MWh, not 100 000 − 40 000 = 60 000 (20 % too low). A heat pump that
delivers 50 000 MWh at a seasonal COP of 4 takes 12 500 MWh of electricity and 37 500 MWh from
the brine; "50 000 MWh from geothermal" overstates the brine by a third.

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
- Count **every drilled section once**. A producer with a pump inside is one hole: the part above
  the pump (the riser) and the part below it (the well) together are the drilled length. In
  gemini both modules carry the WHOLE path and the pump depth cuts it (`segment` `above_esp` /
  `below_esp`); a riser and a well given different paths are refused as `incompatible`
  (gemini `engine/check.py`, QA-321). Check drilled metres = sum of the measured depths of all
  wells before quoting a drilling cost.
- Drilling prices move with the oil and gas market, not with general inflation: Lukawski et al.
  (2014) built a drilling cost index from US well data 1976 to 2009 and found it rose about 70 %
  more than the producer price index between 2003 and 2008. A HICP-converted drilling price is
  a price-year conversion, not a market forecast (§4.2). The same paper finds a learning effect:
  later wells of a field cost less than the first ones, so the first well of a new area is
  priced at the upper end of a range.

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

### 2.8 Step by step: a capex estimate and its check

1. **List the equipment** of the design by gemini kind (§16.2) with its cost size: well metres
   (measured depth, every section once), pump shaft power, capacities in W, conductance, pipe
   metres, fixed items.
2. **Pick one factor per kind** from §0.2's order, in the case's price year, with the basis the
   unit says (§18.3). For drilling over a range of depths, a depth table (§2.2).
3. **Multiply and sum** (gemini does this: `estimate_costs`, capex by module).
4. **Add what the factors leave out**, as stated items: drill site, indirect costs and
   contingency when the factors are bare equipment prices (§2.6). gemini adds none of them; a
   report says whether they are in or out.
5. **Check against whole-plant benchmarks** per W of heat (§2.7) and find the largest items.

Worked example (invented factors, EUR of the case's year): a doublet of two 2 500 m wells, a
geothermal exchanger of 8 MW, a heat pump of 4 MW and a gas boiler of 6 MW; peak heat 12 MW.

| Item | Size x factor | MEUR |
|---|---|---|
| Wells | 5 000 m x 1 400 EUR/m | 7.00 |
| Drill site | one site | 0.30 |
| Production pump | 0.40 MW shaft x 0.60 EUR/W | 0.24 |
| Injection pump | 0.15 MW shaft x 0.30 EUR/W | 0.05 |
| Heat exchanger | 8 MW x 0.10 EUR/W | 0.80 |
| Heat pump | 4 MW x 0.75 EUR/W | 3.00 |
| Gas boiler | 6 MW x 0.06 EUR/W | 0.36 |
| **Direct** | | **11.75** |
| Indirect, 15 % of direct | | 1.76 |
| Contingency, 20 % of the above | | 2.70 |
| **Total** | | **16.21** |

Check: 16.21 MEUR / 12 MW = 1.35 EUR/W, inside the whole-plant range of §2.7 (about 1.0 to
1.9 EUR2015/W). Wells are 60 % of the direct cost, so the drilling factor and the well depth are
the first sensitivities. Had the total come out at 0.4 or 4 EUR/W, a factor basis or a size
would be wrong (§18.3, §18.7) before any design conclusion is drawn.

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

### 3.7 Step by step: yearly opex, with a worked example

1. **Fixed O&M** per kind: `%/yr` x its capex, or `EUR/MW/yr` x its capacity (§3.1).
2. **Variable O&M** per MWh produced, if the source gives it (and for every producing kind, or
   for none, §19.3).
3. **Electricity** of every consumer from the simulation, times the price (§3.3). For a pump:
   `P_el = dp x V / eta`, with `dp` in Pa, `V` in m3/s, `eta` the pump-and-motor efficiency.
4. **Gas bought** on the lower heating value (§19.5), chemicals, waste (§3.4).
5. **Carbon** on the plant's own CO2e (§8.3).

Worked example (invented, the plant of §2.8):

| Item | Calculation | MEUR/yr |
|---|---|---|
| Fixed O&M, wells and site | 1 %/yr x 7.30 MEUR | 0.073 |
| Fixed O&M, surface equipment | 2 %/yr x 4.45 MEUR | 0.089 |
| Production pump electricity | `5e6 Pa x 0.0833 m3/s / 0.6 = 0.69 MW`, x 8 000 h = 5 556 MWh, x 100 EUR/MWh | 0.556 |
| Heat pump electricity | 40 000 MWh heat / COP 4 = 10 000 MWh, x 100 EUR/MWh | 1.000 |
| Gas for the boiler | 2 000 MWh heat / 0.9 = 2 222 MWh, x 40 EUR/MWh | 0.089 |
| **Total** | | **1.807** |

Electricity is 86 % of the opex: the electricity price and the heat pump's COP are this plant's
first opex sensitivities, and a design that cuts pump head or lifts the COP pays twice (opex and
CO2). gemini computes each of these from the simulated year (§16.3); the table explains its
answer and is not a substitute for it.

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

### 4.5 Worked example: an escalating price as one constant price

gemini's yearly accounting takes one price per key for every year of the analysis (§16.4; a
series varies within the simulated year, not across years). A sourced real escalation is
therefore entered as its **levelised** constant price, with the conversion in the source text.

A price `p0` that rises at a real rate `e` per year has the present value of a constant price
discounted at `r_e = (1 + r)/(1 + e) - 1`. The equivalent constant price is

`p_lev = p0 x A(r_e, n) / A(r, n)` (A from §5.2).

Invented example: electricity 100 EUR/MWh today, a published scenario with +2 %/yr real, real
discount rate 5 %, 25 years: `r_e = 1.05/1.02 - 1 = 2.94 %`, `A(2.94 %, 25) = 17.528`,
`A(5 %, 25) = 14.094`, so `p_lev = 100 x 17.528 / 14.094 = 124.4 EUR/MWh`.

A 2 %/yr real rise is worth a quarter more on the price over 25 years: enough to change a
ranking between an electric and a gas-fired design (§12.4). Without a sourced scenario use the
constant price and put the range in the uncertainty (§4.4, §18.9); never escalate by habit.

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

### 5.5 Worked example: replacements and residual value

Invented numbers; real discount rate 5 %, analysis period 25 yr. The formulas explain gemini's
results; agents quote gemini's numbers (§0.1).

**Replacements.** A downhole pump costing 0.5 MEUR lasts 5 years, so it is replaced in years 5,
10, 15 and 20. Present value of the replacements:
`0.5 x (1/1.05^5 + 1/1.05^10 + 1/1.05^15 + 1/1.05^20) = 0.5 x 2.2553 = 1.128 MEUR`.
As an equal yearly cost: `1.128 x CRF(5 %, 25) = 1.128 x 0.07095 = 0.080 MEUR/yr`, which is
16 % of the pump's price per year. A fixed O&M share of 20 %/yr for such a pump (the catalogue's
ESP replacement row, §0.4.2) is of this order; take one or the other, never both (§15 item 18).

**Residual value.** A heat pump of 6 MEUR with a 30-year life is 25 years old at the end:
straight-line residual `6 x 5/30 = 1.0 MEUR` at year 25, worth `1.0 / 1.05^25 = 0.295 MEUR` today,
5 % of its price. Ignoring it is conservative and usually small; gemini counts no residual value.

**Steps for any lifetime question**

1. List each kind's technical life (source: DEA data sheets, vendor data).
2. Lives shorter than the analysis period: replacement cash flows, or a fixed O&M row that says it
   includes them.
3. Lives longer: residual value, or state that it is ignored.
4. Report which kinds were treated how.

### 5.6 The weighted average cost of capital

An investor discounts at the project's weighted average cost of capital (Brealey, Myers and
Allen, *Principles of Corporate Finance*, chapter on the WACC):

`WACC = E/V x r_E + D/V x r_D x (1 - T)`

with `E` and `D` equity and debt, `V = E + D`, `r_E` the return equity holders require, `r_D` the
interest rate and `T` the corporate tax rate. Invented example: 30 % equity at 10 %, 70 % debt at
4 %, tax 25 %: `0.3 x 0.10 + 0.7 x 0.04 x 0.75 = 0.051`, a nominal WACC of 5.1 %. With 2 %
inflation the real rate is `1.051 / 1.02 - 1 = 3.0 %` (Fisher, §4.1).

Rules: a WACC is nominal unless its source says real; a policy rate (§5.1) is not an investor's
rate; whichever is used, `economics.discount_rate` in gemini is a **real** rate (§16.1), so a
nominal rate is converted first and the conversion is written in the source.

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

### 6.6 Worked example: an LCOH by hand, and what moves it

Invented heat-only plant: capex `I0` 20 MEUR, opex `C` 1.2 MEUR/yr, useful heat `Q` 60 000
MWh/yr, real rate 5 %, 25 yr.

1. `CRF(5 %, 25) = 0.07095`, so the annualised capex is `20 x 0.07095 = 1.419 MEUR/yr`.
2. Annualised cost `= 1.419 + 1.2 = 2.619 MEUR/yr` (gemini's `annualised_cost`).
3. `LCOH = 2.619 MEUR / 60 000 MWh = 43.65 EUR/MWh`; capex is 54 % of it.

Sensitivities that follow from the formula (check gemini's study against them):

| Change | Effect on LCOH |
|---|---|
| capex +10 % | `+0.1 x 1.419 / 60 000 = +2.37 EUR/MWh` (+5.4 %) |
| opex +10 % | `+0.12 / 60 000 = +2.00 EUR/MWh` (+4.6 %) |
| heat -10 % (same plant) | `43.65 / 0.9 = 48.50 EUR/MWh` (+11 %) |
| rate 5 % to 8 % | CRF 0.0937: `(1.874 + 1.2)/60 000 = 51.23 EUR/MWh` (+17 %) |

Lessons: energy delivered sits in the denominator, so an under-used plant is expensive however
cheap its parts; a capital-heavy plant is most sensitive to the discount rate.

**Checks on any gemini result**: `lcts x (Q_heat + Q_cold)` must give back `annualised_cost`;
`annualised_cost - opex` must equal `capex x CRF`; a heat-only plant's `lcoh` equals its `lcts`.
A failed check means a wrong reading (another result, another case), not a gemini error to fix.

### 6.7 Levelised costs in gemini and geomind

| Concept | gemini name | Tool | Needs |
|---|---|---|---|
| Annualised cost | `annualised_cost` | `estimate_costs` | capex, opex, `discount_rate`, `analysis_period` |
| LCOH, LCOC | `lcoh`, `lcoc` | `estimate_costs` | heat and cold delivered; `heat_cost_share` when both |
| LCTS | `lcts` | `estimate_costs` | as annualised cost |
| How they move | study metric | `sensitivity`, `sample_uncertainty` | an `uncertainty` on the moved keys (§18.9) |
| Lowest LCTS design | objective | `optimize` | a feasible search space (handbook-studies) |

`read_result` and `compute_kpis` do not give cost metrics (§0.8, QA-209).

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

### 7.5 Worked example: NPV, IRR and paybacks

The plant of §6.6 sells heat at 70 EUR/MWh: revenue `60 000 x 70 = 4.2 MEUR/yr`, net
`4.2 - 1.2 = 3.0 MEUR/yr`.

| Measure | Calculation | Result |
|---|---|---|
| NPV (5 %, 25 yr) | `-20 + 3.0 x A(5 %, 25) = -20 + 3.0 x 14.094` | 22.28 MEUR |
| Simple payback | `20 / 3.0` | 6.7 yr (gemini's `payback`) |
| Discounted payback | first `n` with `A(5 %, n) >= 6.667`: A(5 %, 8) = 6.463, A(5 %, 9) = 7.108 | 9 yr |
| IRR | rate where `A(r, 25) = 20 / 3.0` | 14.5 % |
| Break-even heat price | the LCOH | 43.65 EUR/MWh |

**With a sliding premium** (§7.3): base amount 60, correction amount 35 EUR/MWh, so 25 EUR/MWh
on the heat up to a cap of 6 000 full-load hours x 10 MW = 60 000 MWh/yr, for 15 years:
`25 x 60 000 = 1.5 MEUR/yr`, present value `1.5 x A(5 %, 15) = 1.5 x 10.380 = 15.57 MEUR`.
The subsidy adds to the NPV, not to the LCOH. In gemini: `revenue.subsidy.amount` 25 EUR/MWh,
`duration` 15 yr, `cap` as full-load hours times `capacity` (§16.1, §16.5).

**Reading the measures together.** NPV says how much value; IRR how robust to the rate; payback
how soon the money returns. Rank by NPV at the case's rate (or by LCTS when prices are equal,
§7.2); quote the others as context. A design with a higher IRR but lower NPV is smaller, not
better.

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
57.48 EUR2015/t (price of 2025, `carbon-price-eu-ets-esma-price-2025`) and 51.56 (price of 2024),
Dutch CO2 levy 61.10 (2026); the Instrat 2025 average above is row
`carbon-price-eu-ets-instrat-price-2025`.

### 8.2 Using a carbon price in an assessment

- In a **financial** view, price only the emissions the operator pays for (its own combustion
  under the ETS, or a national carbon tax).
- In a **social** view, a shadow price of carbon may be applied to all emissions, including those of
  grid electricity; then do not also count the carbon cost inside the electricity price.
- Future carbon prices are uncertain and politically set; use a range (chapter 13).

### 8.3 Worked example: the carbon cost of a plant

Invented plant (the same as in §9.7): scope 1 emissions 464.6 t CO2e/yr (vented CO2, flared
methane), scope 2 emissions 2 000 t CO2/yr (grid electricity). At a carbon price of 60 EUR/t:

| View | Emissions priced | Carbon cost |
|---|---|---|
| Financial, operator outside any trading system | none, unless a national tax applies | 0 |
| Financial, operator pays for its own emissions | scope 1: 464.6 t | 27.9 kEUR/yr |
| Social (shadow price on all emissions) | scope 1 + 2: 2 464.6 t | 147.9 kEUR/yr |

gemini takes the second view: `carbon.price` multiplies the plant's own CO2e (§3.6, §16.7); the
grid's carbon is already in the electricity price in a market with emissions trading, so pricing
it again would count it twice (§15 item 6). A social view is a separate study, stated as such.

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

### 9.7 Worked example: a plant's footprint and its reference

Invented heat-only plant delivering 60 000 MWh/yr of heat.

| Source | Calculation | t CO2e/yr |
|---|---|---|
| Grid electricity | 10 000 MWh x 0.200 t/MWh | 2 000.0 |
| CO2 dissolved in the brine, vented | measured mass | 300.0 |
| Methane, flared at 98 % | 50 t CH4: 49 t burnt x 2.75 | 134.8 |
| Methane, unburnt | 1 t x GWP100 29.8 (fossil, §9.3) | 29.8 |
| **Plant total** | scope 1 464.6 + scope 2 2 000 | **2 464.6** |

Reference: gas boilers at 90 % efficiency (on the lower heating value) need 66 667 MWh of gas.
The IPCC default emission factor of natural gas is 56 100 kg CO2/TJ (2006 IPCC Guidelines, Vol. 2,
ch. 2, table 2.2), 0.202 t/MWh, so the reference emits about 13 467 t CO2/yr. Avoided emissions:
`13 467 - 2 465 = 11 002 t/yr`, 82 %.

Abatement cost (§9.6): with the plant's annualised cost 2.619 MEUR/yr (§6.6) and an invented
reference annualised cost of 2.200 MEUR/yr, `(2.619 - 2.200) MEUR / 11 002 t = 38 EUR/t`.

Checks: the grid share dominates such a plant, so the grid factor (§19.2) is the first
sensitivity of its CO2; a vented gas stream can outweigh years of pump electricity, so the
gas handling choice (vent, flare, boiler, CHP, §17.7) belongs in every design comparison.

### 9.8 CO2 in gemini and geomind

| Concept | Where |
|---|---|
| Plant CO2e per year | `co2` of `estimate_costs` (and of the report) |
| Grid factor | case `utilities.electricity.co2_intensity` (g/kWh, constant or profile) |
| Methane GWP and its standard | `economics.accounting.gwp.CH4`, `.standard` |
| Carbon price | `economics.carbon.price` (on the plant's own CO2e only) |
| How CO2 moves with the grid factor | `sensitivity` on the case key, with a sourced range (handbook-studies 3.1) |

Quote gemini's `co2` digit for digit; the table of §9.7 explains it and is not for recomputing.

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

The catalogue's rows (secondary): Dutch 2024 electricity band IE 115.02 and band IF 138.02
EUR2015/MWh (`electricity-nl-eurostat-price-2024-band-*`), Dutch 2024 gas band I4 44.42 and I5
37.51 EUR2015/MWh on the gross calorific value (`gas-nl-eurostat-price-2024-band-*`), and the EU
averages above (`electricity-eu-eurostat-price-2025-band-ie`, `gas-eu-eurostat-price-2025-band-i4`).

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

The project's own catalogue, `knowledge/data-economics.csv` (157 rows at 2026-11-05: 75
verified, 82 secondary, no placeholder; notes and batches in `knowledge/data-economics.md`),
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
classes from Class 5 (concept screening, 0 to 2 % of the project defined, widest range) to Class 1
(definitive, narrowest). The ranges it gives are bands whose width depends on the technology and
the project; the outer values usually quoted for the process industries are:

| Class | Project defined | Typical use | Low side | High side |
|---|---|---|---|---|
| 5 | 0 to 2 % | concept screening | -20 to -50 % | +30 to +100 % |
| 4 | 1 to 15 % | study or feasibility | -15 to -30 % | +20 to +50 % |
| 3 | 10 to 40 % | budget, authorisation | -10 to -20 % | +10 to +30 % |

(AACE 18R-97 as summarised by secondary sources, e.g. *Products Finishing*, "Capital cost
estimate classes"; status *secondary*, read the practice itself before a contract figure rests on
it.) A plant costed from factors at the design-option stage is a Class 5 or Class 4 estimate: its
capex is a range, not a point. Report it with the class and do not quote more digits than the
class supports in prose; the tool's digits stay in tables (§0.1 rule 1).

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

How to run one with gemini and how many runs it takes: `knowledge/handbook-studies.md` §3.1 and
§0.4. This chapter is the method.

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

### 12.4 Worked example: sensitivity and a switching value

Two invented designs deliver the same 60 000 MWh/yr: A (LCTS 43.65 EUR/MWh, buys 8 000 MWh/yr of
electricity) and B (LCTS 41.00, buys 14 000 MWh/yr), both at an electricity price of
100 EUR/MWh. The electricity price enters linearly:
`dLCTS/dp = E_el / Q`: A 0.133, B 0.233 EUR/MWh per EUR/MWh.

- Over a sourced price range of 80 to 140 EUR/MWh, A moves 8.0 EUR/MWh, B 14.0.
- The switching price, where they tie:
  `43.65 + 0.133 (p - 100) = 41.00 + 0.233 (p - 100)`, so `p = 126.5 EUR/MWh`.
- Report: "B is cheaper below 126.5 EUR/MWh of electricity, A above; the sourced range reaches
  140." That sentence is worth more than either base LCTS.

**Steps** for any sensitivity request: (1) list every declared uncertainty of the case
(handbook-studies 3.1); (2) run the study with the sourced ranges; (3) rank by swing; (4) for
the top input, find the switching value against the runner-up design; (5) report base, ranges,
swings and switching values with the study key.

Global methods (variance-based indices that also catch interactions) are described in
Saltelli et al. (2008); one-at-a-time ranges suffice when the outputs are nearly linear in the
inputs, as prices are.

---

## 13. Uncertainty analysis

### 13.1 Distributions for uncertain inputs

How to run a Monte Carlo with gemini and how many draws to choose: `knowledge/handbook-studies.md`
§3.2 and §0.4. This chapter is the method.

| Distribution | Parameters | Use |
|---|---|---|
| Uniform | min, max | only the bounds are known |
| Triangular | min, mode, max | a best guess and bounds; skew allowed |
| Normal (truncated) | mean, standard deviation, cut at min and max | symmetric errors around a measured value |
| Lognormal | mean and spread of the log | positive quantities with long upper tails (permeability, drilling overruns) |
| Discrete | values and probabilities | scenarios (policy on or off, one or two wells succeed) |

Every distribution is an assumption with a source or a stated reason. Changing a value's
distribution to another kind replaces all its parameters: a uniform range set over a normal one
must not keep the old `std` (in gemini a merge patch keeps keys it is not given, so send the
whole new `uncertainty`, and check it with `read_case`). Correlated inputs (gas and
electricity prices, carbon and electricity prices) sampled independently understate or overstate
the spread; state whether correlations are modelled.

### 13.2 Monte Carlo sampling

Draw `N` sets of inputs from their distributions, run the evaluation for each, collect the outputs.

- Fix the random **seed** and report it, so the result can be reproduced. A sample count or seed
  the agent chose itself is the agent's assumption (`source: agent`, not confirmed), never the
  user's.
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

### 13.4 Worked example: how many draws

Invented study: the LCTS of a design has a standard deviation of about 5 EUR/MWh across the
uncertain inputs.

| Draws N | Standard error of the mean (`5 / sqrt(N)`) | Good for |
|---|---|---|
| 25 | 1.0 EUR/MWh | an impression of the spread |
| 100 | 0.5 | mean and median |
| 400 | 0.25 | P10 and P90 |
| 1 000+ | 0.16 | P5, P95 and the probability of a rare failure |

Tail percentiles need more draws than the mean because few draws fall in the tail: at N = 100
only about five lie below P5 (Morgan and Henrion 1990 discuss sample sizes for percentile
estimates). If the study's budget is small, report P10 to P90, say N, and say that P5/P95 would
need more draws. Each draw that re-simulates the plant costs a simulation; prices alone cost
only the accounting (§12.1), so price-only uncertainty can afford many more draws.

Reading the result: "LCTS P50 44.1, P10 39.8, P90 49.6 EUR/MWh (N 400, seed 7, 3 draws failed
the heat requirement)". A design whose failed share is large is fragile, whatever its P50.

---

## 14. Comparing configurations and deciding

### 14.1 Like-for-like comparison

How to compare and optimise families with gemini's studies, and in which order:
`knowledge/handbook-studies.md` §5.

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

### 14.4 Worked example: deciding between two designs

Invented results, both designs feasible on the same case and gemini version (§14.1):

| Measure | Design A (deep doublet + heat pump) | Design B (shallower doublet + larger boiler) |
|---|---|---|
| capex | 16.2 MEUR | 11.8 MEUR |
| LCTS | 43.7 EUR/MWh | 45.9 EUR/MWh |
| NPV at the case's prices | 22.3 MEUR | 19.0 MEUR |
| CO2 | 2 465 t/yr | 5 900 t/yr |
| LCTS P10 to P90 | 40.2 to 48.1 | 39.5 to 54.0 |
| Electricity switching price vs the other | A cheaper below 160 EUR/MWh | B cheaper above |

Reading: A is cheaper at the base case, emits 58 % less and has the narrower spread; B needs
4.4 MEUR less capital and burns more gas, so it wins on cost only if electricity rises above
160 EUR/MWh (outside a sourced range of 80 to 140). Recommendation: A, with the
condition stated ("if capital is limited to 12 MEUR, B is the feasible alternative at +2.2
EUR/MWh"). Show the whole table: the user may weigh capex or CO2 differently (§14.3).

**Steps**: (1) only feasible designs (§0.1 rule 4); (2) the same case, prices and version;
(3) LCTS or NPV for cost (§14.2); (4) CO2 and capex beside it; (5) the spread and the switching
values of the inputs that flip the ranking; (6) a recommendation with its conditions.

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
22. **The subsidy period as the analysis period** (§18.4).
23. **A row of another basis** (EUR/W heat for EUR/W shaft) (§18.3).
24. **Costing an old result after a price change** and expecting new numbers (§18.5).
25. **An unsized capacity paid at its range maximum** (§18.7).
26. **A riser and a well drilled as two short holes** instead of one path (§2.2).
27. **A user price of today written into a case in older prices unconverted** (§18.11).
28. **8 for 8 %** in a rate or share (§18.11).
29. **A national row for a case of another country, or of none** (§18.12).
30. **Costing the latest plant instead of the one discussed** (§18.13).

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
it) and `dN.injector`, each of kind `drilling`. The riser and the well carry the same whole path; each is costed on
the measured length of its segment (`above_esp`, `below_esp`, gemini `modules/wells/
productionwell.py`), so riser plus well is the producer's measured depth (§2.2).

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

## 18. Lessons from practice: economics in a running assessment

General lessons from the team's quality rounds (bug numbers QA-nnn in
`documents/project/quality-assurance/bugs/`). Each is a rule for any case. Read the one you need.

### 18.1 One source order, whatever words the user uses

The decision order of §0.2 holds for every request: "set up the economics", "fill them in
yourself", "best guesses, don't ask", "use Norwegian prices", "economics please". The words change
who approves, never where a value comes from (QA-279, QA-320, QA-327, QA-349).

- A user who names a country or region keeps the case's own assumptions document as the base.
  Only the keys for which a source **of that region** exists are replaced; the answer names
  those keys and says which keys have no regional source and stayed as they were.
- "Your best guesses" means "take the sourced values without asking", not "invent". A key no
  source gives stays `open` and is named once; it is not re-asked or re-delegated (QA-349).
- A subsidy is taken only from a scheme that applies to the site's country and technology. With
  none, the answer says that no scheme fits and the subsidy keys stay unset.
- Every value carries a source that a reader can open (a file and page, a Knowledge section or a
  catalogue row `id`). "agent" is not a source.

### 18.2 Values are numbers with units

A value is a number (or a table) and its unit goes in its own field. In `ask_economics` each item
has `key`, `value`, `unit`, `source` and, when a source gives one, `row` and `uncertainty`. A
value written as `{"value": 25, "unit": "yr"}` inside `value` is an object, not a number; it was
shown as raw text and failed only after the user approved it (QA-298). A `row` must be an `id`
that exists in the catalogue; an invented id is refused (QA-243). Unit spellings that mean the
same are the same (EUR/W/K and EUR/(W/K)); if a tool refuses one, use the spelling the refusal
names, never change the number.

### 18.3 A row must fit the key's basis

A cost factor is per something: W of heat, W of shaft power, W of electric power, m of well, m3 of
tank. A row for one basis is not a value for another (QA-192). Example on invented numbers: a
pump row gives 0.09 EUR per W of **heat moved** by a station of 20 MW heat; the key wants EUR per
W of **shaft power**, and the pump draws 0.4 MW shaft. Read as shaft price, 0.09 EUR/W x 0.4 MW
= 36 kEUR; the station row actually means 0.09 x 20 MW = 1.8 MEUR for the whole station, most of
which is not the pump. Neither is the pump's price. Either a source gives the right basis, or the
key stays open and the mismatch is named. The catalogue writes the basis in `unit_2015` ("EUR/W
heat", "EUR/W electric"): read it before choosing a row.

### 18.4 The analysis period is the economic life, not a subsidy period

`analysis_period` is the years over which costs and energy are discounted: the plant's economic
life (for example 25 yr for a geothermal plant in the Danish Energy Agency's technology data).
A subsidy duration (15 yr in some schemes) is `revenue.subsidy.duration`, a different key
(QA-314). Mixing them changes every levelised cost. Invented numbers: capex 10 MEUR, real
discount rate 5 %. The capital recovery factor `r / (1 - (1 + r)^-n)` (§5.2) is 0.0710 for
25 yr and 0.0963 for 15 yr, so the annualised capex is 0.71 or 0.96 MEUR/yr: a 36 % higher
capital share of the LCOH from the wrong key alone. (The formula explains gemini's result; agents
quote gemini's number, §0.1.)

### 18.5 A cost belongs to the case its run ran on

A stored result keeps the case it was simulated with. `estimate_costs` on it gives the costs of
that case's economics, also after a `set_case` changed the prices. Its answer says which:
`economics.same_as_case` true, or false with the `changed` keys (QA-258). When it is false,
simulate the same plant on the current case and cost the new result; costing the old result
again gives the same numbers. Price-only changes need no new design round: one `set_case`, one
`simulate`, one `estimate_costs`.

Before any costing in a new conversation, read the case (`read_case`): a value changed by hand on
the Case page is a new case version, and a remembered value may be stale (QA-284).

### 18.6 One change, one `set_case`

A single price change is one `set_case` with the new value and its source in
`economics.about.sources`, one approval, then stop and answer (QA-256). It is not a reason to
re-ask the whole economics. If the user denies the card and asks a question instead ("don't
change the case, just tell me the NPV at 30 years"), answer from a study on the current case
without changing it (QA-268; `handbook-studies`).

### 18.7 Size what you pay for

gemini prices equipment at its rated (design) capacity (§2.5). A capacity left at the maximum of
its search range is paid in full even if the plant never uses it. A rated capacity far above the
peak duty the result shows, without a stated reason (redundancy, future load), is a sizing gap,
not a cost fact (QA-324: dry coolers rated at about twice their peak). Compare rated and peak for
every costed kind before reporting capex; name any kind that was not sized. Margins for safety
are stated in the design, not hidden in an unsized maximum (handbook-design 4.9).

### 18.8 Check an optimum before calling it one

An optimiser with a small evaluation budget stops at a good point, not always the best one
(QA-285: a nearby feasible point had a lower LCTS than the reported optimum). Before reporting
"the optimum", vary the most cost-relevant variable around it (one sizing or sensitivity study)
and report whether a better feasible point appeared (`handbook-studies` 5 and 6).

### 18.9 Uncertainty travels with its value

A source that gives a range for a value (a distribution, a P10-P90, a min and max) gives it for
the studies. Carry it into the case with the value: `ask_economics` reads an uncertainty table of
the source document, rows `| \`economics.<key>\` | \`{"kind": ...}\` |`, and fills `uncertainty`
(QA-259, QA-216). Never invent a range; a key without a sourced range is held fixed and the
answer says so (`handbook-studies` 3.1).

### 18.10 Do the economics, not a survey

An economics request that names a place asks for prices of that place, not for new site physics
(ground, air). If site values would also change, ask once and wait; do not start a site survey
(QA-280). Stop searching when Knowledge has no source for the region and say so.

### 18.11 Fractions, percents and price years in a value

- A rate, share or fraction is a number without unit: 8 % is `0.08`, never `8` (QA-120). The same
  holds for `heat_cost_share` (0.87) and for gas composition given as fractions; a composition in
  mol % must add up to 100, as fractions to 1 (QA-063).
- A price the user gives is in the year the user means (usually today's money). Before it enters
  a case in 2015 prices, convert it with the HICP (§4.2) and write both numbers in the source
  ("user: 120 EUR/MWh in 2026 money, x 100/HICP(2026) = ..."); never write a 2026 number into a
  2015 case unchanged (QA-041). If the HICP of the year is not yet published, ask or use the last
  published year and say so.

### 18.12 What the user said wins over the catalogue

- A user who says "no subsidy" gets no `revenue.subsidy` keys, not a catalogue scheme (QA-084).
- Country-specific rows (a national tariff, a national subsidy) fit only a case in that country.
  A case with no site country gets general (EU) rows or the question "which country?", and every
  national row is labelled with its country (QA-085, QA-041).
- What the user approved is what is written: the values of the approved card, not a re-pick
  (QA-168). A value the user changes takes the user as its source and drops the old source
  (QA-186, QA-305).
- Case changes the user approved are the user's case; a reviewer does not reject a design because
  the case differs from the first version (QA-317).
- With auto-approve on, nothing is asked: the proposed answer is taken and said (QA-339).

### 18.13 Cost the right result

- Name the plant version and result you cost. A `simulate` without a design runs the latest
  plant, which may not be the one discussed (QA-166). A what-if run is not the chosen design
  (QA-223).
- A report on "the design" compares every plant version of the project, not only the latest
  (QA-337); the feasible one with the lowest LCTS or highest NPV is recommended (§14.2).
- A plant that leaves a demanded service unmet is infeasible, however low its LCTS (QA-239,
  §0.1 rule 4).
- Cost once and quote: one `estimate_costs` per result answers capex, opex, LCOH, LCOC, LCTS, NPV,
  payback and CO2 together; re-reading the case and the same output again adds nothing (QA-159).

### 18.14 When a tool fails or a memory disagrees

- A tool error is reported as it is ("estimate_costs failed: ..."), with the numbers that did come
  back; a missing NPV is never filled by hand (QA-275).
- The tool's answer of today beats a claim in the conversation or the project state written
  earlier (QA-346: an old "gemini returns no P10/P90" outlived the fix). When the two disagree,
  call the tool and believe it.
- A question the user already answered is not asked again in the same run (QA-079); read the
  answer from the case.

---

## 19. Finding a value the catalogue lacks

The questions agents search for most often (QA run logs, 2026-11-05) and what answers them. The
rule of §0.2 still holds: a value enters the case only with a source a reader can open and with
the user's approval. These sections say **where such a source is** and **how to bring it into
the case's currency and price year**, so that a search ends quickly with a value or with a named
gap.

### 19.1 Energy prices for a country without catalogue rows

The catalogue holds the countries its sources cover (§0.4.3). For any other country:

1. **Official statistics first.** Eurostat publishes non-household prices twice a year by
   annual consumption band: electricity `nrg_pc_205` (bands IA to IG, MWh/yr) and gas
   `nrg_pc_203` (bands I1 to I6, GJ/yr), with three tax levels (without taxes, without VAT and
   recoverable taxes, all taxes). The geo list covers the EU and several other European countries
   (check the dataset's list for the country). Choose band and tax level as in §10.2.
2. **National statistics office or regulator** when Eurostat lacks the country or the band.
3. **A contract or quote** from the user beats both (step 1 of §0.2).

If Knowledge holds none of these and no web connector is available, the key stays `open` and the
question names the dataset that would give it ("electricity: Eurostat `nrg_pc_205`, country X,
band ID, without VAT"). Do not take a neighbouring country's price as a stand-in without the
user approving it as such.

**Bring it to the case's terms** (currency and price year of the case, §4.2, §4.3):

1. Convert the currency in the **source year** at that year's average rate (Eurostat
   `ert_bil_eur_a`, or the ECB euro reference rates, annual average).
2. Deflate the euro amount to the case's price year with the euro-area HICP (§4.2).

Worked example (invented numbers): a price of 900 XCU/MWh in 2023, average rate 10.0 XCU per EUR
in 2023: 900 / 10.0 = 90 EUR(2023)/MWh; to 2015 prices: 90 x 100 / 123.15 = 73.08 EUR(2015)/MWh.
Record both steps and both sources in the value's source text. gemini converts nothing
(§16.1: `currency` is a label), so the number entered must already be in the case's terms.

### 19.2 Grid CO2 intensity for a country

The key is the case's `utilities.electricity.co2_intensity` (g/kWh), not an economics key
(§9.4). Sources, in order of preference for a location-based average:

| Source | What it gives | Note |
|---|---|---|
| A factor the client or brief prescribes | the case's value | takes precedence |
| National inventory or energy agency | official national factor | check generation or consumption basis |
| EEA, "Greenhouse gas emission intensity of electricity generation" | EU and EEA countries, yearly | generation-based |
| Ember, Yearly Electricity Data | most countries, yearly | generation-based (catalogue rows `co2-grid-eu-*`) |

A generation-based factor ignores imports: a country that imports much fossil power has a higher
consumption-based factor. The GHG Protocol Scope 2 Guidance (2015) requires the location-based
figure in every report and the market-based figure in addition when contracts are bought (§9.4).
Grids change fast: state the year, and for a plant that runs for decades give a range or a
projection as an uncertainty (§18.9), not the latest year as a fixed truth.

### 19.3 Variable O&M of chillers and the per-energy map

Many searches ask for a chiller's variable O&M in EUR/MWh of cold. The catalogue has no such row
(§0.4.2), and the main European technology catalogues used here (Danish Energy Agency, technology
data for electricity and district heating) cover heat producers, not chillers. What follows:

- A chiller's **electricity** is not O&M: gemini computes it from the chiller's COP and prices it
  with `energy.electricity`. Do not add it again as variable O&M (§15 item 6).
- Its **maintenance** is in `opex.fixed.<chiller>` (share of capex per year, rows exist).
- `opex.per_energy` is all or nothing (§16.1): once one producing kind has a price, every
  producing kind of the plant needs one. With a chiller unpriced, `ask_economics` moves the whole
  map to `open` and says so; the plant is then costed with no per-energy O&M for any kind. Report
  that as a stated simplification, and do not search further for a chiller value unless the user
  asks for one or gives one.

### 19.4 A national carbon tax next to an emissions trading system

Some countries tax CO2 on fuels in addition to, or instead of, an emissions trading system. Which
applies depends on the installation (size, sector, fuel) and the country's rules. `carbon.price`
is one price per t CO2e on the plant's own emissions (§3.6, §16.7). Add a national tax to an ETS
price only when a source says both apply to an installation of this kind; otherwise take the one
that applies and say why. Exchange and price-year steps as in §19.1.

### 19.5 Gas: gross or net heating value

Eurostat gas prices are per kWh of gross calorific value (GCV); gemini prices bought gas per
energy of its **lower** heating value (§3.3, §16.1). The net calorific value of natural gas is
about 10 % below the gross value (IEA, Energy Statistics Manual, 2005, on gross and net calorific
values), so a price per MWh(GCV) is about 1.11 times higher per MWh(NCV). The exact ratio
depends on the gas composition (ISO 6976 gives the calculation); use the ratio of the case's own
gas when it is known, and record the conversion in the source text.

---

## 20. Subsurface economics: depth, flow, doublets and exploration risk

The wells are usually the largest capex item (§2.1). This chapter shows how the subsurface
choices trade cost against heat. The physics (productivity, breakthrough, pumps) is in
`knowledge/handbook-design.md` chapter 3; here the question is what each choice costs and earns.

### 20.1 Depth: hotter water against dearer wells

The produced temperature rises with depth, `T(z) = T_s + g z` (surface temperature `T_s`,
gradient `g`), and the heat of a doublet is `Q = rho c V (T_prod - T_inj)`. Drilling cost rises
faster than depth (§2.2). The economic depth is where the cost per MW of useful heat is lowest,
counting the heat pump or boiler a shallower, cooler doublet needs to reach the network
temperature.

Worked example (invented): `T_s` 10 °C, `g` 30 K/km, injection 35 °C, flow 0.05 m3/s,
`rho c` 4.0 MJ/(m3 K), drilling 1 200 / 1 400 / 1 800 EUR/m at 2 000 / 2 500 / 3 000 m.

| Depth | T_prod | Heat | Two wells | MEUR per MW |
|---|---|---|---|---|
| 2 000 m | 70 °C | 7.0 MW | 4.8 MEUR | 0.69 |
| 2 500 m | 85 °C | 10.0 MW | 7.0 MEUR | 0.70 |
| 3 000 m | 100 °C | 13.0 MW | 10.8 MEUR | 0.83 |

On wells alone 2 000 to 2 500 m are equal. If the network needs 80 °C, the 2 000 m doublet also
needs a heat pump (capex and electricity, chapter 22) and the 2 500 m one does not: the cheaper
plant is the deeper one. Always compare whole plants (wells plus upgrade), never wells alone.

### 20.2 Flow rate: heat against pumping power

Heat grows linearly with flow; with a linear productivity and injectivity the pressure drop
grows linearly too, so pump power `P = dp V / eta` grows with the square of the flow
(Grant and Bixley 2011, productivity index). Example (invented): productivity and injectivity
10 m3/h per bar each, so `dp = 2 V / 10` bar with `V` in m3/h; efficiency 0.6; `T_prod - T_inj`
50 K.

| Flow | dp | Pump power | Heat | Heat / pump power |
|---|---|---|---|---|
| 200 m3/h | 40 bar | 0.37 MW | 11.1 MW | 30 |
| 300 m3/h | 60 bar | 0.83 MW | 16.7 MW | 20 |

The step from 200 to 300 m3/h adds 5.6 MW of heat for 0.46 MW of electricity, a marginal ratio
of 12: still far cheaper heat than a boiler. The economic flow is therefore usually set by a hard
limit (pump size, wellhead or injection pressure, sand, thermal breakthrough; handbook-design
3.3, 3.5), not by the pump's electricity. Check the limit that binds, then cost at that flow.

### 20.3 Doublet count: a step in capex

Each added doublet is a large step in capex. It pays only if its heat is used for enough hours.
Example (invented): a second doublet of 8 MEUR adds 5 000 MWh/yr that is only needed at peak.
Its heat costs `8 x CRF(5 %, 25) / 5 000 MWh = 8 x 0.0710 / 5 000 = 113.5 EUR/MWh` before any
opex, against a peak boiler at roughly gas price / efficiency (§21.2). A doublet that runs base
load all year (say 40 000 MWh/yr) costs 14.2 EUR/MWh in capital. Size the doublet count with a
study over the count (handbook-studies, `size`/`optimize`), never by adding wells "for safety".

### 20.4 Exploration risk

A first well can fail to find the expected flow or temperature. The expected cost of a project
includes that chance: with probability of success `PoS`, a failed well whose cost `C_f` is lost
adds `(1 - PoS) x C_f` to the expected capex (ESMAP 2012 discusses success rates and risk
mitigation for geothermal). Example (invented): `PoS` 0.8, a 5 MEUR well: expected loss
1.0 MEUR. Risk insurance or a guarantee scheme converts that uncertain loss into a premium.

gemini models no exploration risk. Represent it as an uncertainty on the reservoir inputs
(permeability, gradient) in a study, or as a stated, sourced contingency on the drilling capex;
never as a hidden factor.

### 20.5 In gemini and geomind

| Choice | Where |
|---|---|
| Depth and well paths | the plant's doublet wells (measured depth, §2.2, §16.2) |
| Drilling price over depth | `capex.drilling` as a depth table (§16.1) |
| Flow, pump size, limits | the plant and the case's hard limits (§0.6; handbook-design 3) |
| Doublet count, depth, flow search | `size`, `optimize` studies (handbook-studies) |
| Reservoir uncertainty | `sensitivity`, `sample_uncertainty` on the case's site keys |

---

## 21. Matching technology to the load: base, mid and peak

A plant usually combines a capital-heavy, cheap-to-run base unit (geothermal, heat pump) with a
cheap-to-build, dear-to-run peak unit (boiler). How much of each is an economic question with a
classic answer: the load duration curve and screening curves (Stoft 2002, chapter on screening
curves; Frederiksen and Werner 2013, on district heating plant mixes).

### 21.1 The load duration curve

Sort the demand of every hour of the year from highest to lowest and plot it against the hours:
the load duration curve (LDC). The area under it is the yearly energy; the height at `h` hours is
the load exceeded for `h` hours. A unit of capacity `K` placed at the bottom of the curve
delivers `integral of min(L(h), K) dh`: the first MW runs all year, the last MW of the peak runs a
few hours. Heat and cold have separate curves; a plant that serves both needs both.

The time step matters: daily means flatten the peaks of hourly data, so a unit sized on daily
data may fall short at the hourly peak. Use the step of the case's profiles and say which.

### 21.2 Screening curves

The yearly cost of 1 MW of a technology that runs `h` hours is `c(h) = F + v h`:

- `F` (EUR/MW/yr): annualised capex `I x CRF` plus fixed O&M;
- `v` (EUR/MWh): running cost: fuel / efficiency, or electricity / COP, plus variable O&M.

Two technologies cost the same at `h* = (F1 - F2) / (v2 - v1)` hours. Below `h*` the cheap-to-
build unit wins, above it the cheap-to-run one.

Worked example (invented; 5 %, 25 yr, CRF 0.07095):

| Unit | Capex | Fixed O&M | F | v |
|---|---|---|---|---|
| Geothermal with heat pump | 1.5 MEUR/MW | 30 000 EUR/MW/yr | 136 425 EUR/MW/yr | 10 EUR/MWh (pumps, compressor) |
| Gas boiler | 0.06 MEUR/MW | 2 000 EUR/MW/yr | 6 257 EUR/MW/yr | 40 / 0.9 + 1 = 45.4 EUR/MWh |

`h* = (136 425 - 6 257) / (45.4 - 10) = 3 672 h`. The base unit is the cheaper choice for every
MW of load that is present more than about 3 700 hours a year. At 8 760 h it costs 25.6 EUR/MWh;
used only 500 h it would cost 283 EUR/MWh against the boiler's 58.

### 21.3 Worked example: sizing base and peak from the curve

Invented LDC falling linearly from 20 MW (peak hour) to 2 MW (lowest hour); yearly heat
96 360 MWh. The load exceeded 3 672 h is `20 - 18 x 3 672 / 8 760 = 12.45 MW`.

| Unit | Capacity | Energy | Share |
|---|---|---|---|
| Base (geothermal + heat pump) | 12.45 MW (62 % of peak) | 82 504 MWh | 86 % |
| Peak boiler | 7.55 MW | 13 856 MWh | 14 % |

The pattern is general: a base unit sized at roughly half to two thirds of the peak covers most
of the energy, because the top of the curve is narrow. Changing prices move `h*` and with it the
split: a higher gas price lowers `h*` and enlarges the base unit (§12.4 for switching values).

Limits of the method: it ignores storage (chapter 24), minimum loads and ramping, the supply
temperature each unit can reach (chapter 22), and requirements such as a CO2 cap or a limit on
fossil heat share (§0.6), which may force a larger base unit than cost alone would choose.

### 21.4 In gemini and geomind

gemini simulates the case's demand profiles step by step and dispatches the plant's units; it
does not draw screening curves. Use them to set sensible search ranges and to explain a result:

- base-unit capacity (doublets, heat pump) and peak capacity (boiler) are searched by `size` or
  `optimize` (handbook-studies); start the range around the screening-curve split;
- after a run, compare each unit's rated capacity with its peak and its full-load hours
  (energy / capacity): a base unit with few full-load hours or a boiler with many signals a poor
  split (§18.7);
- the heat-by-source accounting (§1.4) gives each unit's energy share for the report.

---

## 22. Heat pumps against boilers: price ratio, COP and CO2

A geothermal plant often lifts its heat with an electric heat pump, or tops it up with a gas or
electric boiler. Which is cheaper and cleaner depends on three ratios: electricity to gas price,
the heat pump's COP, and the grid's CO2 factor to that of gas.

### 22.1 COP from the temperature lift

The ideal (Carnot) heating COP is `COP_C = T_sink / (T_sink - T_source)`, temperatures in K.
Real large heat pumps reach roughly half of it or somewhat more (a Carnot efficiency of about
0.4 to 0.6 is common in studies of large district heating heat pumps, e.g. David et al. 2017).
Example (invented): sink 80 °C (353 K), source 40 °C: `COP_C = 353 / 40 = 8.8`; at 0.5,
`COP = 4.4`. Sink 70 °C: `343 / 30 = 11.4`, `COP = 5.7`, 30 % more heat per kWh of electricity.

Lesson: the network supply temperature is an economic variable. Lower supply temperatures, the
idea of fourth-generation district heating (Lund et al. 2014), raise the COP, cut electricity
and CO2, and may let a shallower doublet do without a heat pump (§20.1).

### 22.2 Running-cost break-even

Per MWh of heat, a heat pump costs `p_el / COP + v_hp`, a gas boiler `p_gas / eta + v_b`
(`p_gas` per MWh of the lower heating value, §19.5). The heat pump runs cheaper when

`COP > p_el / (p_gas / eta + v_b - v_hp)`.

Invented example: electricity 100, gas 40 EUR/MWh, `eta` 0.9, variable O&M 1.7 and 1.0 EUR/MWh:
break-even COP `100 / (44.4 + 1.0 - 1.7) = 2.29`. A COP of 4.4 runs at 24.4 EUR/MWh against the
boiler's 45.4. With electricity at 200 EUR/MWh the break-even COP doubles to 4.6, and the heat
pump of COP 4.4 loses on running cost alone.

### 22.3 CO2 break-even

The heat pump emits less than a gas boiler when `EF_el / COP < EF_gas / eta`, i.e.

`COP > EF_el x eta / EF_gas`.

With `EF_gas` 0.202 t/MWh (IPCC 2006 default, §9.7), `eta` 0.9 and a grid of 0.300 t/MWh, the
break-even COP is 1.34; with a grid of 0.200 t/MWh it is 0.89, so any working heat pump wins.
An electric boiler (COP about 1) beats a gas boiler on CO2 only on grids below about
0.22 t/MWh. These ratios make the grid factor (§19.2) decisive for electric designs.

### 22.4 Including capital: the full comparison

Running cost decides only for units that already exist. For a new unit use the screening curve
(§21.2). Invented: heat pump capex 0.75 MEUR/MW, fixed O&M 2 000 EUR/MW/yr, so
`F = 0.75e6 x 0.07095 + 2 000 = 55 213 EUR/MW/yr`, `v = 24.4 EUR/MWh`; boiler `F` 6 257,
`v` 45.4. Equal cost at `(55 213 - 6 257) / (45.4 - 24.4) = 2 329 h`. A heat pump that would run
fewer than about 2 300 full-load hours a year costs more than the boiler it replaces; size it on
the base of the load curve, not on the peak.

### 22.5 Steps and checks

1. Take the COP from gemini's result, not from a rule of thumb; check it against
   `0.4 to 0.6 x COP_C` for its temperatures. A COP far outside that range means a temperature
   or a reading is wrong.
2. Compute the cost and CO2 break-even COPs with the case's prices and factors; say where the
   design's COP lies.
3. Check the heat pump's full-load hours against the screening-curve threshold.
4. Vary the electricity price and the grid factor in the sensitivity (§12.4): electric designs
   are exposed to both.

In gemini: kinds `heat_pump`, `boiler`, `electric_boiler` (§16.2); prices `energy.electricity`,
`energy.gas`; grid factor `utilities.electricity.co2_intensity` in the case.

---

## 23. Cooling economics: compression, absorption, free cooling

### 23.1 The options and their efficiencies

| Option | Driven by | Typical COP (cold / drive) | Heat rejected per unit of cold |
|---|---|---|---|
| Compression chiller, water-cooled | electricity | about 4 to 7 at district-cooling conditions | `1 + 1/COP`, about 1.2 |
| Single-effect absorption (LiBr-water) | heat, roughly 80 to 120 °C | about 0.7 | `1 + 1/COP`, about 2.4 |
| Adsorption (silica gel-water) | heat, roughly 60 to 90 °C | about 0.5 to 0.6 | about 2.7 to 3 |
| Free cooling (cold ground water, lake, cold air) | pumps and fans only | very high, limited by the source temperature | none beyond the source |

Sources: Herold, Radermacher and Klein (2016) for absorption; ASHRAE Handbook, HVAC Systems and
Equipment, for chillers and cooling towers. COPs depend strongly on the chilled-water and
heat-rejection temperatures; take the value gemini computes for the design's temperatures.

A thermally driven chiller rejects about twice as much heat as a compression chiller per unit of
cold, so its cooler (dry cooler or tower) is about twice as large: count it in its capex.

### 23.2 Running cost per MWh of cold

- Compression: `p_el / COP` plus the cooler's fan electricity.
- Absorption: `cost of the driving heat / COP` plus pump electricity and the larger cooler's fans.

The cost of the driving heat is its **opportunity cost**. Geothermal heat in summer, when the
heating demand is low and the doublet would otherwise idle, costs only its pumping electricity.
Heat taken from a gas boiler costs `p_gas / eta`: then absorption is almost never economic.

Worked example (invented; electricity 100 EUR/MWh; fans 0.02 MWh of electricity per MWh
rejected; absorption auxiliaries 0.02 MWh/MWh cold):

| | Compression, COP 5 | Absorption, COP 0.7, geothermal heat at 5 EUR/MWh |
|---|---|---|
| Drive | 100 / 5 = 20.0 | 5 / 0.7 = 7.1 |
| Auxiliaries | - | 2.0 |
| Heat rejection fans | 1.2 x 2 = 2.4 | 2.43 x 2 = 4.9 |
| **Running cost, EUR/MWh cold** | **22.4** | **14.0** |
| Same, heat from a gas boiler (40 / 0.9) | | 63.5 + 6.9 = 70.4 |

### 23.3 Including capital

Invented capex: compression 0.16, absorption 0.33 EUR/W of cold, coolers 0.07 EUR/W rejected;
fixed O&M 4 500 and 6 800 EUR/MW/yr; CRF 0.07095. Per MW of cold:

- compression `F = 11 352 + 4 500 + 1.2 x 4 967 = 21 812 EUR/MW/yr`, `v = 22.4`;
- absorption `F = 23 414 + 6 800 + 2.43 x 4 967 = 42 282 EUR/MW/yr`, `v = 14.0`.

Equal yearly cost at `(42 282 - 21 812) / (22.4 - 14.0) = 2 438` full-load hours (§21.2).
Cooling plants in temperate climates often run fewer full-load hours than that, so compression
tends to win unless the driving heat is nearly free, the cooling season is long, or a CO2
requirement favours heat over electricity. The answer is case-specific: let the study compare
both families (handbook-studies 5) and use this to explain the result.

### 23.4 CO2 and the heat source

A compression chiller emits `EF_el / COP` per MWh of cold (0.06 t/MWh at 0.3 t/MWh and COP 5);
absorption on geothermal heat emits only its pump and fan electricity; absorption on boiler heat
emits `EF_gas / (eta x COP)` (0.32 t/MWh at 0.202, 0.9, 0.7), five times the compression chiller.
"Thermally driven" is green only when the heat is.

### 23.5 In gemini and geomind

Kinds `compression_chiller`, `absorption_chiller`, `adsorption_chiller`, `cooler`, `ice_storage`
(§16.2); fixed O&M rows in §0.4.2; no chiller per-energy row (§19.3). The cost of cold is LCOC
with a stated heat-cost share, or the plant's LCTS (§6.3, §6.4). Size the cooler from the heat
it rejects, not from its range maximum (§18.7).

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

- AACE International, Recommended Practice 18R-97, Cost Estimate Classification System (read through
  the summary below; section 11.2).
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
- Lukawski, M. Z., Anderson, B. J., Augustine, C., Capuano, L. E., Beckers, K. F., Livesay, B. and
  Tester, J. W. (2014), "Cost analysis of oil, gas, and geothermal well drilling", *Journal of
  Petroleum Science and Engineering* 118, 1-14, https://doi.org/10.1016/j.petrol.2014.03.012
  (abstract and summaries read; section 2.2).
- *Products Finishing*, "Capital cost estimate classes", https://www.pfonline.com/articles/capital-cost-estimate-classes
  (summary of AACE 18R-97; section 11.2).
- GHG Protocol (2015), *Scope 2 Guidance*, World Resources Institute and WBCSD (location-based
  and market-based methods; section 19.2).
- International Energy Agency (2005), *Energy Statistics Manual*, OECD/IEA and Eurostat (gross and
  net calorific values; section 19.5).
- ISO 6976:2016, Natural gas: calculation of calorific values, density, relative density and Wobbe
  indices from composition (section 19.5).
- European Environment Agency, indicator "Greenhouse gas emission intensity of electricity
  generation" (section 19.2).
- Eurostat, `ert_bil_eur_a`, euro exchange rates, annual data; European Central Bank, euro foreign
  exchange reference rates (section 19.1).
- Brealey, R. A., Myers, S. C. and Allen, F., *Principles of Corporate Finance*, McGraw-Hill (any
  recent edition; WACC and NPV chapters; sections 5.6, 7.5).
- IPCC (2006), *2006 IPCC Guidelines for National Greenhouse Gas Inventories*, Vol. 2 Energy,
  chapter 2, table 2.2 (default CO2 emission factor of natural gas, 56 100 kg/TJ; section 9.7).
- Morgan, M. G. and Henrion, M. (1990), *Uncertainty: A Guide to Dealing with Uncertainty in
  Quantitative Risk and Policy Analysis*, Cambridge University Press (section 13.4).
- Saltelli, A. et al. (2008), *Global Sensitivity Analysis: The Primer*, Wiley (section 12.4).
- Beckers, K. F. and McCabe, K. (2019), "GEOPHIRES v2.0: updated geothermal techno-economic
  simulation tool", *Geothermal Energy* 7, 5, https://doi.org/10.1186/s40517-019-0119-6 (coupled
  reservoir, well and cost models; chapter 20).
- ESMAP (2012), *Geothermal Handbook: Planning and Financing Power Generation*, World Bank, ESMAP
  Technical Report 002/12 (exploration risk and its mitigation; section 20.4).
- Grant, M. A. and Bixley, P. F. (2011), *Geothermal Reservoir Engineering*, 2nd ed., Academic
  Press (productivity and injectivity; section 20.2).
- Frederiksen, S. and Werner, S. (2013), *District Heating and Cooling*, Studentlitteratur (plant
  mixes, load duration, heat sources; chapters 21 to 24).
- Stoft, S. (2002), *Power System Economics: Designing Markets for Electricity*, IEEE Press and
  Wiley (screening curves and load duration; chapter 21).
- David, A., Mathiesen, B. V., Averfalk, H., Werner, S. and Lund, H. (2017), "Heat Roadmap
  Europe: large-scale electric heat pumps in district heating systems", *Energies* 10(4), 578,
  https://doi.org/10.3390/en10040578 (section 22.1).
- Lund, H., Werner, S., Wiltshire, R. et al. (2014), "4th Generation District Heating (4GDH):
  integrating smart thermal grids into future sustainable energy systems", *Energy* 68, 1-11,
  https://doi.org/10.1016/j.energy.2014.02.089 (section 22.1).
- ASHRAE, *ASHRAE Handbook: HVAC Systems and Equipment*, ASHRAE, Atlanta (chillers, cooling
  towers, thermal storage; chapters 23 and 24; latest edition).
- Herold, K. E., Radermacher, R. and Klein, S. A. (2016), *Absorption Chillers and Heat Pumps*,
  2nd ed., CRC Press (section 23.1).
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
