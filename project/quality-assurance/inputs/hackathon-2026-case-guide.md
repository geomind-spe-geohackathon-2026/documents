# Case guide: GEMINI hackathon 2026

Guidance for the GEMINI hackathon 2026 case only; a starting point, the agents may depart from it
with a recorded reason.

For the case lead and the geoscientist. Cite as `knowledge/hackathon-2026-case-guide.md`. It says
how the three competition files map onto the case, so the case is set in one pass with one
confirmation question and one `ask_economics` call. The reference shape is gemini's own sample
case, `gemini/examples/hackathon_2026/case.json` (with `economics.json`); every path below is a
path of that file. Values the competition files lack: `knowledge/hackathon-2026-assumptions.md`.

## The inputs

| File | Holds |
|---|---|
| `GEMINI_Heating_Demand_Daily_2027.csv` | `date`, `heating_demand_MWth`: 365 daily averages, 2027-01-01 to 2027-12-31 |
| `GEMINI_Cooling_Demand_Daily_2027.csv` | `date`, `cooling_demand_MWcool`: 365 daily averages, same days |
| `GEMINI_Hackathon_Challenge_Requirements.pdf` | 2 pages, dated 28 October 2026: reservoir, brine and gas, constraints, supply temperatures |

The PDF states (page 1): heating peak 30.0 MWth on 28 January, 111.67 GWhth/year; cooling peak
10.0 MWcool on 19 July, 23.74 GWhcool/year. These are for checking; the case takes the series from
the CSV files, never these numbers.

## Where each value goes

| Value as the PDF writes it | Case path | Source |
|---|---|---|
| Daily heating demand | `demand.heating.power` from the heating CSV, column `heating_demand_MWth`, unit MW | CSV |
| Daily cooling demand | `demand.cooling.power` from the cooling CSV, column `cooling_demand_MWcool`, unit MW | CSV |
| Time axis | `time.start` 2027-01-01, `time.end` 2028-01-01 (excluded), `time.step` 1 d: copy from the `span` that `read_rag` gives | CSV |
| Heating supply 100 °C, "fixed" | `demand.heating.supply_temperature` 100 degC | PDF p. 2 |
| Cooling supply 20 °C, "fixed" | `demand.cooling.supply_temperature` 20 degC | PDF p. 2 |
| Reservoir midpoint depth 2,500 m TVD | `site.reservoir.reference_depth` 2500 m | PDF p. 2 |
| Gross thickness 100 m | `site.reservoir.thickness` 100 m | PDF p. 2 |
| Geothermal gradient 30 °C/km | `site.ground.gradient` 30 °C/km | PDF p. 2 |
| Reference surface temperature 12 °C | `site.ground.surface_temperature` 12 °C | PDF p. 2 |
| Reservoir pressure 250 bar(g) | `site.reservoir.pressure` 250 barg | PDF p. 2 |
| Permeability 200 mD | `site.reservoir.permeability` 200 mD | PDF p. 2 |
| Brine density 1,030 kg/m³ | `site.fluid.density` 1030 kg/m3 | PDF p. 2 |
| Dynamic viscosity 0.40 mPa·s | `site.fluid.viscosity` 0.4 mPa.s | PDF p. 2 |
| Gas-liquid ratio 0.8 Nm³/m³ | `site.fluid.gas_liquid_ratio` 0.8 Nm3/m3 | PDF p. 2 |
| 80 mol% CH₄, 20 mol% CO₂ | `site.fluid.dissolved_gas` CH4 0.8, CO2 0.2 (the produced gas, never `utilities.gas`) | PDF p. 2 |

The reservoir temperature is never set: gemini derives it from the surface temperature, the
gradient and the depth. The PDF's note "for a different well depth, use hydrostatic pressure and
the gradient" tells what gemini derives; it is no case value.

Values from `knowledge/hackathon-2026-assumptions.md` (all in the ONE confirmation question, each
with that file as its source): return temperatures and pressures
(`demand.heating.return_temperature` 60 degC, `return_pressure` 6 bar;
`demand.cooling.return_temperature` 25 degC, `return_pressure` 4 bar), `demand.cooling` dew point
margin 1 K, indoor 26 degC and relative humidity 0.5, `site.air` 10 degC and 101325 Pa,
`site.fluid.sand_concentration` 20 mg/l, `utilities.gas.composition` (bought gas),
`utilities.electricity.co2_intensity` 300 g/kWh (the organisers' value, QA-095).

## The requirements

Write them as gemini's sample does (`case.json`, `requirements`), each ONE requirement:

| `name` | Rule | From |
|---|---|---|
| `production_flow_range` | `on: doublet`, `quantity: production_flow`, `over: each`, `when: running`, `min` 50, `max` 300, `unit` m3/h | PDF p. 2 (ONE rule with both ends, QA-080) |
| `brine_cooling_limit` | `on: doublet`, `quantity: brine_cooling`, `over: each`, `when: running`, `max` 40, `unit` K | PDF p. 2 |
| `running_time_limit` | `on: doublet`, `quantity: production_flow`, `over: duration`, `when: running`, `max` 330, `unit` d | PDF p. 2 ("330 daily steps") |
| `pump_efficiency` | `on: doublet`, `quantity: pump_efficiency`, `min` 0.7, `max` 0.7 (no unit, no over, no when) | PDF p. 2 (70 %) |
| `full_reinjection` | `on: doublet`, `quantity: reinjection_ratio`, `over: each`, `when: running`, `min` 0.99999, `max` 1.00001 | PDF p. 2 says "equal liquid volumes"; the band is gemini's sample's |
| `doublet_count` | `on: doublet`, `quantity: count`, `min` 1, `max` 3 (no over, when, unit) | PDF p. 2 |
| `heat_delivered` | `on: heating_supply`, `quantity: unmet_share`, `max` 0.01 | Organisers: the whole system meets the demand on all 365 days; 1 % is the sample's tolerance |
| `cold_delivered` | `on: cooling_supply`, `quantity: unmet_share`, `max` 0.01 | as above |

Supply temperatures (QA-091): 100 °C and 20 °C are fixed operating conditions in `demand.*`. The
sample judges them through `heat_delivered` and `cold_delivered`, with no temperature
requirement. If a temperature requirement is written anyway, it holds only while that supply runs
(`when: running`), never `when: always`: on the 146 days with zero cooling demand no chiller runs
and the idle loop sits at its return temperature, which is no violation.

The 330 days limit only the doublet (organisers, QA-091): the plant as a whole meets the demand on
all 365 days.

## Design freedoms: never a case question

These are the design team's choices, recorded as assumptions with a reason, never asked of the
user as missing case values:

- well depth (the plant's `depth`; the sample searches 2000 to 3500 m), PDF p. 2 and organisers;
- the number of doublets (`size.doublets`, 1 to 3, the case only bounds it);
- the return temperatures (QA-094: organisers, "as long as the return temperature does not violate
  the constraints, then it is fine"). The case still needs a value: take 60 degC and 25 degC from
  the assumptions file, labelled "team design choice", in the one question. A design team that
  wants another value hands over `case change needed: demand.heating.return_temperature: <why>`;
- the backup policy (`params.backup`), the number and kind of units, how the associated gas is
  handled (flare, boiler, CHP: organisers allow several).

## Economics: one `ask_economics` call

Name in `values` each key the assumptions file gives, as `{key, value, unit, source}` with source
`knowledge/hackathon-2026-assumptions.md` (the keys are written in that file, as in gemini's
`economics.json`). This gives the same economics as gemini's sample, so its rankings
(`knowledge/hackathon-2026-design-guide.md`) can be compared. Put in `open` every
`opex.per_energy.*` key and every `revenue.subsidy.*` key: the sample has neither, there is no
subsidy, and a per-energy map would need a price for each chiller that no source gives.

## Checklist before `finish`

- 8 requirements as above; no `when: always`; flow as one rule.
- No reservoir temperature, no depth and no doublet count in the case.
- Return temperatures set from the assumptions file, confirmed in the one question.
- `set_case`'s `plants_need` empty; economics set with `currency` EUR, `price_year` 2015.
- Only the three competition files are project files; this guide and the assumptions are in the
  global Knowledge, never copied into the project.
