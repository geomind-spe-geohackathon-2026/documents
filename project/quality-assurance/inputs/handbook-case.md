**Handbook: defining an energy-supply case** (`knowledge/handbook-case.md`)

How to turn a brief and data files into a complete, sourced case for a geothermal heating and
cooling plant in gemini. For the case lead, the geoscientists and any reviewer of a case.

- **Cite as** `knowledge/handbook-case.md §<section>` (for example `§6.5`).
- **Read by section**, never whole: `read_knowledge(name="knowledge/handbook-case.md",
  section="0")`. Chapter 0 is the short version of the whole handbook; read it first, then only
  the sections it points to.
- **Source of truth.** Keys, units, roles and quantities are gemini's (`gemini/gemini/case/`,
  `gemini/gemini/plants/roles.py`, `gemini/gemini/units/inputs.py`, gemini 0.6.17). When this
  handbook and `describe_case(path)` differ, `describe_case` wins.
- **Not here.** How to call a tool: skill `setting-the-case` (cases), `finding-sources`
  (files, Knowledge), `connectors` (servers), `calculator`, `gemini-units`. Economics:
  `knowledge/handbook-economics.md`. Plant design: `knowledge/handbook-design.md`. Report:
  `knowledge/handbook-report.md`.
- **Numbers in this handbook** are definitions, examples of a pattern, or values of the
  worked example (chapter 12). None is a value for another case.

---

**Contents** (read a section with its number, such as `section="6.5"`)

0. Quick start: decision order, hard rules, ask or search, field groups
1. Reading a brief
2. Key tree: every case key with unit, source and check
3. Time and demand series
4. Site and subsurface
5. Utilities and emission factors
6. Requirements
7. Case values and design freedoms
8. Sources, citations and the confirmation question
9. Uncertainty
10. How gemini handles a case
11. Checklists
12. Worked example: a brief with daily demand files
Appendix A. Unit pitfalls
Appendix B. Glossary
Appendix C. References

---

# 0. Quick start

## 0.1 Decision order

Do these in order; skip none.

1. **Inventory.** List every file (`list_files`) and the case (`read_case`); read each file once,
   whole (§1.1).
2. **Classify.** Every statement of the brief is a case value, a rule, a design freedom, a
   reading instruction or a value for checking (§1.2).
3. **Split.** Give 2 to 4 geoscientists one field group each (§0.4), with the text of the pages
   it needs, the case keys it owns and what the case already holds.
4. **Merge and set.** Merge the findings; write the case once with everything the files and the
   user state (§2, §10).
5. **Search the gaps.** For each missing value: Knowledge (assumptions document first), then a
   connector (§0.3, §8.1).
6. **Ask once.** ONE confirmation question with every value that did not come from the user's
   files, every flaw, and every agent choice (§8.4).
7. **Economics once.** ONE `ask_economics` question (skill `setting-the-case`;
   `knowledge/handbook-economics.md`).
8. **Check and hand over.** `read_case` again, then the checklist §11.2.

## 0.2 Hard rules

| Never | Instead | § |
|---|---|---|
| a typical value, a rule of thumb, a recalled number | a source, or ask the user for the value by path and unit | §8.1 |
| compute, convert, round or sum a value | copy it digit for digit in its printed unit; gemini converts and derives | §8.5 |
| set a derived key (reservoir temperature without a measurement, ISA air pressure) | leave it to gemini | §10.2 |
| put a design freedom (well depth, doublet count, flows, units) in the case | a requirement for its bound; the choice is the plant's | §7 |
| correct a flaw yourself | name both values in the one question | §1.4 |
| two requirements for the two ends of one range | one requirement with `min` and `max` | §6.7 |
| `when: always` on a supply temperature or a flow band | `when: running` | §6.6 |
| a count for days of operation | `over: duration`, unit `d` | §6.7 |
| `%` as the unit of an efficiency or a share | a fraction without unit (70 % is `0.7`) | §6.7 |
| a brief's peak or annual total as a case value | check the data with it | §1.3 |
| the produced gas in `utilities.gas` or the bought gas in `site.fluid` | `site.fluid.dissolved_gas` vs `utilities.gas.composition` | §4.4 |
| a demand series without an offset and without `time_zone` | give `time_zone` (from a source, or confirmed as an assumption) | §3.2 |
| ask the same value twice | the user's answer is final; an open value stays open | §8.4 |

## 0.3 Ask the user or use Knowledge

Take each value from the first source that has it, and keep which one.

| Order | Source | When it is enough | How it is cited |
|---|---|---|---|
| 1 | the user (request, answers) | always; needs no confirmation | `source: user`, "user message" |
| 2 | the project's files | always; a value a file states is never changed | file and page (or table) |
| 3 | Knowledge: an assumptions document of this case, then the cost catalogue, then other cited documents | goes into the one question for approval | `knowledge/<name>` with section, page or row `id` |
| 4 | a connector (MCP), such as weather or elevation | goes into the one question for approval | server, tool and time |
| 5 | the user, asked for the value itself | only after 3 and 4 found nothing | path and unit, no number of yours |

Decide by the kind of value:

| Kind of value | Do |
|---|---|
| stated by a file or the user | set it; never ask |
| missing, and Knowledge or a connector has it | propose it with its source in the one question |
| missing, no source anywhere | ask for it by path and unit, no number; with no answer it stays unset and open |
| a design choice the case still needs (a return temperature the brief leaves open) | propose it in the one question as `design choice` with a reason (§7.3) |
| a tolerance the brief implies but does not give (demand met, an exact ratio) | propose it in the one question as an assumption with a reason (§6.8) |
| the user delegates ("use reasonable assumptions") and no source exists | propose `engineering assumption, no source` with a reason, in one question (§8.3) |
| the time zone of a series no file states | propose it in the one question as an assumption (§3.2) |
| a flaw (wrong side, span mismatch, two sources disagree) | name every flaw with both values in the one question |
| a design freedom | never ask; the design team chooses it |

## 0.4 Field groups for the geoscientists

The case lead splits the case into 2 to 4 groups, one geoscientist each (prompt
`case/lead.md`, step 1). A geoscientist reads no file and sets nothing: it returns, per value,
`base`, `low`, `high`, the unit as printed, the case path, the quality (`measured`, `tested`,
`interpreted`, `estimated`, `unknown`) and the source (file, page, table, depth, quote), plus
`missing` and `disagreements`. Economics are not a group: the lead sets them with
`ask_economics`.

| Group | Keys it owns | Read |
|---|---|---|
| I. Time and demand | `time.*`; `demand.heating.*`; `demand.cooling.*` (power, supply and return temperatures and pressures, indoor values) | §2.1, §2.2, §3 |
| II. Ground and reservoir | `site.ground.*`; `site.reservoir.*`; quality and range of each | §2.3, §4.1 to §4.3, §9 |
| III. Brine, gas, air and utilities | `site.fluid.*`; `site.air.*`; `utilities.electricity.*`; `utilities.gas.*` | §2.3, §2.4, §4.4, §4.5, §5 |
| IV. Requirements | every rule of the brief as a requirement; rules gemini cannot express; tolerances to propose | §6, §7 |

With two or three geoscientists, merge neighbouring groups (I with IV, II with III).

---

# 1. Reading a brief

## 1.1 Inventory

| Input | Usually holds | Read |
|---|---|---|
| brief or requirements document | services, supply temperatures, site, rules, freedoms | every table and every note under it |
| demand data (CSV, Excel) | power per time step | header, unit, time column, `span`, rows |
| reservoir or well reports | depth, temperature, pressure, permeability, fluid | value, depth it applies to, how it was obtained |
| network data | supply and return temperatures, pressures | |
| tariffs, prices | economics (not the case) | `knowledge/handbook-economics.md` |
| organiser or client answers | clarifications; a later answer beats an older brief | date of each |

File names are case-sensitive: write each as `list_files` gives it.

## 1.2 Five kinds of statement

| Kind | Recognise by | Goes to | Example |
|---|---|---|---|
| case value | "fixed", a measured or stated value | the case key | "Supply temperature 90 °C (fixed)" -> `demand.heating.supply_temperature` |
| rule | "shall", "must", "at most", "between", "not more than" | a requirement (§6) | "Flow per well 30 to 150 m³/h" -> requirement on `doublet.production_flow` |
| design freedom | "may", "can be chosen", "allowed", "options", "1 to 3" | the plant; its bound is a rule (§7) | "The depth may be optimised" -> plant `depth` |
| reading instruction | "use ... to obtain ...", "for another depth ..." | nothing: it says what gemini derives | "Use hydrostatic pressure and the gradient for another depth" |
| value for checking | a peak, an annual total, a count of days | a check of the data only (§1.3) | "Peak demand 12 MW on 3 February" |

Examples are invented for the pattern. Keep the page of every statement: it is the citation.

## 1.3 Values for checking

A brief's peak, annual energy or day count checks the data; the case takes the series from the
data file. Use them to find:

- a unit error: a peak 1000 times off is kW for MW; 24 times off is MWh/d for MW;
- a span error: a total short by one day is a missing row or an end one step early;
- a column swap or sign error: a heating peak in summer.

When the file and the brief differ, the data are what the plant serves and the difference is a
flaw (§1.4). The annual energy and peak of a series come from gemini (`read_profile` with a
summary), never from a sum of yours.

## 1.4 Flaws

A flaw cannot be right as written: a return on the wrong side of its supply, a case span other
than the data's, a count where a duration belongs, two sources with different values. Rules
(prompt `case/lead.md`):

- never correct it yourself;
- ONE `ask_user` question names every flaw, each with both values as written;
- a flaw only listed in an answer is a check not done;
- for two sources that disagree, propose the one higher in §0.3 and name the other beside it.

---

# 2. Key tree

Every key gemini's case takes, from the `fields` of `gemini/gemini/case/`. Units in gemini's
names; write the unit the source prints when gemini takes it. `describe_case(path)` gives the
accepted units of each key.

## 2.1 `time`

| Key | Unit | Source | Check |
|---|---|---|---|
| `start` | date or ISO time (no offset = UTC) | the demand file's `span` | copied, never worked out |
| `end` | date or ISO time, **excluded** | the demand file's `span` | 2027-01-01 to 2028-01-01 at 1 d is 365 steps |
| `step` | `d`, `h` | the demand file's `span` | not finer than the data |

## 2.2 `demand.heating` and `demand.cooling`

| Key | Unit | Source | Check |
|---|---|---|---|
| `power` | `MW` (`MWth`, `MWcool` are `MW`); a series `{file, column, unit, time_zone}` or a constant | data file; user values via `save_profile`; a constant from the user | §3.3 checks; a cold power, never chiller electricity |
| `supply_temperature` | `degC` | brief, network operator | a "fixed" supply is a case value |
| `return_temperature` | `degC` | network data, assumptions document, or a team design choice (§7.3) | heating: below supply; cooling: above supply |
| `minimum_return_temperature`, `maximum_return_temperature` | `degC` | network data | only when a source states them |
| `return_pressure` | `bar`, `barg` as printed | network data, assumptions document | gauge or absolute as the source says |
| `indoor_temperature` (cooling only) | `degC` | building data, brief, assumptions document | |
| `indoor_relative_humidity` (cooling only) | fraction 0 to 1, or `%` as printed | as above | within 0 to 1 after conversion |
| `dew_point_margin` (cooling only) | `K` | as above | |

## 2.3 `site.ground` and `site.reservoir`

| Key | Unit | Source | Check |
|---|---|---|---|
| `ground.surface_temperature` | `degC` | brief, well data, Knowledge, connector | a site value |
| `ground.gradient` | `degC/km` or `K/km` (equal) | brief, well data, regional study | a site value, not a continental average |
| `reservoir.reference_depth` | `m` | brief, well report | TVD; the depth the pressure and temperature hold at; not the design depth |
| `reservoir.thickness` | `m` | reservoir report | gross or net as the source says |
| `reservoir.permeability` | `mD` | reservoir report | with the thickness it rests on (transmissivity kh) |
| `reservoir.pressure` | `barg` or `bar` as printed | brief, well test | gauge (`barg`) or absolute; at `reference_depth` |
| `reservoir.temperature` | `degC` | a measurement only | unset without one: gemini derives it from the ground |

## 2.4 `site.fluid` and `site.air`

| Key | Unit | Source | Check |
|---|---|---|---|
| `fluid.density` | `kg/m3` | fluid analysis, brief | temperature and salinity it holds at |
| `fluid.viscosity` | `mPa.s` | fluid analysis, brief | temperature it holds at |
| `fluid.gas_liquid_ratio` | `Nm3/m3` | fluid analysis, brief | normal (0 °C) vs standard (15 °C) conditions |
| `fluid.dissolved_gas` | per species, a mole fraction or `mol%` | fluid analysis, brief | the produced gas; sums to one as written |
| `fluid.sand_concentration` | `mg/l` | fluid analysis, assumptions document | |
| `air.temperature` | `degC`, constant or series | file, weather connector, Knowledge | say "constant" when it is |
| `air.relative_humidity` | fraction 0 to 1, or `%` with `"unit": "%"` | file, weather connector | optional: no module reads it in gemini 0.6.17; leave it open unless a source gives it, never ask for it; never convert it yourself |
| `air.pressure` | `Pa`, `bar`; or `{"elevation": {value, unit}}` | file, connector, or the site's elevation | from an elevation `set_case` sets the ISA pressure and lists it in `converted` |

## 2.5 `utilities`

| Key | Unit | Source | Check |
|---|---|---|---|
| `electricity.co2_intensity` | `g/kWh` as printed; constant or series | brief, organiser, Knowledge, connector | location- or market-based named (§5.2) |
| `electricity.import_limit`, `export_limit` | `MW` | grid operator | unset unless a source gives one |
| `gas.composition` | per species, a mole fraction or `mol%` | supplier, assumptions document | the bought gas; digits as written; sums to one |
| `gas.heating_value` | per mass, as printed | supplier, Knowledge | optional: gemini computes it from `gas.composition`; leave it open unless a source gives it, never ask for it |

## 2.6 Other sections

| Section | Holds | § |
|---|---|---|
| `initial_state` | the starting state of stateful modules, `{module path: {state: {value, unit}}}`; no default | §10.1 |
| `economics` | prices, discount rate, accounting; set by `ask_economics` | `knowledge/handbook-economics.md` |
| `requirements` | a list of rules | §6 |

---

# 3. Time and demand series

## 3.1 Power and energy

A demand series gives **power** per step (`MW`). A daily file usually gives the mean power of
the day; a column in `MWh/d` is an energy, not a power, and is a unit to confirm. `MWth`,
`MWcool`, `MWc` are all `MW`: the suffix names the product. `MWe` is electricity, another
product. A demand derived from gas bills is fuel burnt, not heat delivered: ask which a file
holds.

## 3.2 The time axis and the time zone

- `time.start` and `time.end` without an offset are UTC; `end` is excluded
  (`gemini/gemini/case/time.py`).
- A **series** needs an offset (`2027-01-01T00:00:00Z`) on every timestamp, or a `time_zone`
  (an IANA name such as `Europe/Amsterdam`) for the file. Without both, gemini refuses the
  series: there is no default zone (`gemini/gemini/units/inputs.py`, `from_series`).
- With a `time_zone` and a step of one day or more, gemini matches the rows to the case's steps
  by local calendar date, so a 23- or 25-hour day of daylight saving does no harm.
- A zone that no file and no user message states is an assumption: propose it in the one
  question with its reason (the site's location), `source: agent`, never "the user chose it".
- The time column is read as `time`; a column of another name (`date`) is named in `columns`
  when the file is given (skill `setting-the-case`).
- A year has 365 or 366 daily rows; check against the calendar.
- The economic analysis period (often decades) is an economics value, not `time`.

## 3.3 Checks on a demand series

Report each failure as a flaw (§1.4); correct none.

| Check | Fails when |
|---|---|
| count | rows differ from the span over the step |
| gaps, duplicates | a missing or repeated time |
| sign, finite | a negative or non-finite value (gemini refuses them) |
| unit | the peak or total is far from the brief's values for checking (§1.3) |
| season | heating peaks in summer or cooling in winter (northern hemisphere) |
| span | the case's span differs from the file's: the span is wrong, never the data |
| zero days | many zero days of cooling are normal; note how many (they matter for `when`, §6.6) |
| base load | a heating series that never reaches zero has a summer base: say so |

## 3.4 Resolution

| Step | Shows | Hides |
|---|---|---|
| hourly | daily pattern, true peak, storage cycles | nothing relevant for sizing |
| daily | season, cold spells, days a source runs | the hourly peak, which is higher than the daily mean |
| monthly | season only | peaks, cold spells, zero days |

A daily case sizes on daily means: name the hidden hourly peak as a limitation. Never build a
finer series from a coarser one, nor a series from a peak and an annual energy: ask for a
series file, the values, or a constant power.

---

# 4. Site and subsurface

## 4.1 Ground temperature

The rock temperature at depth follows from `surface_temperature` and `gradient`; gemini
derives it (reservoir temperature, §10.2). A site value comes from well data or a regional
study, never from a continental average.

## 4.2 Reservoir

- **Depth.** TVD (true vertical depth), not MD (measured along a deviated well). The
  `reference_depth` is where the stated pressure and temperature hold; it changes only together
  with them, from a source. A depth the user wants for the wells is the plant's `params.depth`
  (§7); when `set_case` returns `check`, ask which is meant.
- **Flow capacity** is transmissivity: permeability × thickness (kh). Report the permeability
  with the thickness it rests on; gross vs net thickness as the source says.
- **Pressure.** `barg` is gauge; gemini's `barg` adds one standard atmosphere. `bar` or `bara`
  is absolute.
- **Temperature.** Set only a measured reservoir temperature. A brief's "for another depth use
  the hydrostatic pressure and the gradient" is a reading instruction: no value.

## 4.3 Data quality

Each subsurface value carries its quality: `measured` (logs, cores, samples), `tested` (well
tests), `interpreted` (model, map), `estimated` (the report's own assumption), `unknown`. Take
the report's base case as the value; keep its range (P10/P90, min/max) as uncertainty (§9). A
value of quality `estimated` or `unknown` is named so in the one question. Before drilling,
permeability, thickness and temperature are the largest uncertainties of the project.

## 4.4 Brine and dissolved gas

- Density and viscosity hold at a stated temperature and salinity: keep the note.
- `gas_liquid_ratio`: gas volume per liquid volume. "Normal" is 0 °C and 101.325 kPa
  (DIN 1343); "standard" is 15 °C and 101.325 kPa (ISO 13443). Name which the source uses.
- `site.fluid.dissolved_gas` is the **produced** gas; `utilities.gas.composition` is gas
  **bought** from a grid. Never put one in the other.
- Methane in the produced gas is both a possible fuel (boiler, CHP, flare) and a strong
  greenhouse gas when vented: name it for the design and economics teams.

## 4.5 Outside air

Air matters for air coolers, cooling towers and chillers. Search files and Knowledge first; a
connected weather or elevation server comes before any question. When only the location is
missing, ask for the location, never for values a server gives. Relative humidity is a
fraction; a server series in `%` goes in with `"unit": "%"` and gemini converts it. With no
source, ask the user for the air pressure or the site's elevation, with no number of yours.

---

# 5. Utilities and emission factors

## 5.1 Electricity grid

`co2_intensity` goes in the case, not the economics; the economics price it. A constant is a
simplification of an hourly or daily series: say so. `import_limit` and `export_limit` come only
from a grid operator; otherwise unset.

## 5.2 Choosing a CO2 intensity

| Method (GHG Protocol Scope 2, 2015) | Means | Use |
|---|---|---|
| location-based | the average intensity of the grid at the site | the usual basis for a plant design |
| market-based | the intensity of the contracted electricity | only when a contract is given |

A value from the brief or the client comes first; name the method.

## 5.3 Bought gas

`utilities.gas.composition` (mole fractions; gemini converts `mol%`) and `heating_value` come
from the supplier or an assumptions document. Keep every digit; never round a composition.

## 5.4 Not the case

Prices, discount rate, analysis period, capital and operating costs, carbon price, GWP and
heat/cold cost allocation are economics: `ask_economics` and `knowledge/handbook-economics.md`.

---

# 6. Requirements

## 6.1 What a requirement is

A rule of a third party on the outcome: a quantity of a role, with its band
(`gemini/gemini/case/requirement.py`). It applies to every unit of the role on its own, and
gemini's verdict judges it (`check_results`). Never a design choice ("use two doublets"), a set
point the team chooses, or a site value.

## 6.2 Qualities of a good requirement

| Quality (ISO/IEC/IEEE 29148:2018) | In a case |
|---|---|
| necessary | it comes from the brief or a third party, not from the team's preference |
| unambiguous | one reading: which unit, which steps, which quantity |
| complete | both ends where the brief gives both; the steps it holds in |
| singular | one rule per requirement; a range with two ends is one rule |
| feasible | some plant can meet it; one no plant can meet is a flaw to ask about |
| verifiable | gemini can judge it: a role and quantity of §6.4 |
| traceable | its `name` and its source page recorded with it |

## 6.3 Keys

`{name, on, quantity, unit, over, when, min, max}` (`KEYS`).

| Key | Rule |
|---|---|
| `name` | unique, snake_case (`production_flow_range`) |
| `on` | a role (§6.4) |
| `quantity` | a quantity of that role |
| `over` | per-step quantities only: how the run is read (§6.5); refused on a property or window quantity |
| `when` | per-step quantities only: `always` or `running`; every step when absent (§6.6) |
| `min`, `max` | at least one; exact rule: `min` = `max` (`equals` is refused) |
| `unit` | present only when the bounds have a dimension; over `duration`, a duration (`d`, `h`) |

## 6.4 Roles and quantities

From `gemini/gemini/plants/roles.py` (`TABLE`; `gm.plants.roles()`). A role is read from the
plant's wiring, never from a module name. *Property* and *window* quantities take no `over` and
no `when`.

| Role | Quantities |
|---|---|
| `doublet` | `production_flow`, `brine_cooling`, `production_temperature`, `injection_temperature`, `pump_power`, `pump_efficiency` (property), `intake_pressure`, `intake_gas_fraction`, `reinjection_ratio`, `count` (property), `wellhead_pressure` |
| `heat_pump` | `cop`, `lift`, `heat_output` |
| `boiler` | `fuel_input`, `heat_output` |
| `chp` | `power_output`, `heat_output` |
| `chiller` | `cop`, `cold_output` |
| `heat_exchanger` | `duty`, `approach` |
| `heating_supply` | `temperature`, `unmet`, `unmet_share` (window) |
| `cooling_supply` | `temperature`, `unmet`, `unmet_share` (window) |
| `plant` | `electricity_bought`, `gas_bought`, `heat_surplus`, `co2`, `gas_burned` |

`reinjection_ratio`: injected over produced liquid volume flow. `count`: number of doublets.
`unmet_share`: unmet over demanded energy of the service over the whole period. `co2` of `plant`:
CO2-equivalent mass per step, so `over: sum` is the run's mass.

## 6.5 `over`: how the run is read

| `over` | Judges | Use for |
|---|---|---|
| `each` | every counted step | a cap or band per step (flow range, brine cooling, temperature) |
| `sum` | the sum | a total (CO2 of the year, energy bought) |
| `mean` | the mean | an average limit |
| `max`, `min` | the extreme | a peak as one figure |
| `duration` | total time of the steps where `when` holds; bounds are durations | days or hours of operation |

## 6.6 `when`: which steps count

- `running`: steps where the unit carries flow. Use for anything that holds while equipment
  runs: flow bands, brine cooling, a fixed supply temperature. An idle loop sits at its return
  temperature; `always` would fail a correct plant.
- `always`: every step, running or not; rare (a rating that may never be exceeded).

## 6.7 Bounds

- cap: `max`; floor: `min`; a range with both ends: ONE requirement with both;
- exact: `min` = `max`;
- fraction, share, ratio, efficiency: no unit (70 % is `0.7`);
- days of operation: `over: duration`, `when: running`, unit `d`;
- number of units: `{on: doublet, quantity: count, min, max}`, no `over`, `when`, `unit`.

## 6.8 Tolerances

A brief that says "the demand shall be met" or "equal volumes are reinjected" gives no
tolerance, and a simulation never meets them exactly. Propose one in the one question, named as
an assumption with its reason:

- demand met: one `unmet_share` requirement per supply, a small `max` such as a percent of the period's energy;
- an exact ratio: a narrow band around it (such as ± 0.001 % of the ratio).

Too loose passes a design the client rejects; too tight fails one on numerical noise.

## 6.9 Brief text to requirement

Placeholders A, B, X, N, E, M come from the brief.

| Brief says | Requirement |
|---|---|
| "Flow per well between A and B m³/h" | `on: doublet, quantity: production_flow, over: each, when: running, min: A, max: B, unit: m3/h` |
| "Brine cooled by at most X K" | `on: doublet, quantity: brine_cooling, over: each, when: running, max: X, unit: K` |
| "A doublet operates at most N days a year" | `on: doublet, quantity: production_flow, over: duration, when: running, max: N, unit: d` |
| "Pump efficiency E %" | `on: doublet, quantity: pump_efficiency, min: E/100, max: E/100` (written as the fraction) |
| "All produced water is reinjected" | `on: doublet, quantity: reinjection_ratio, over: each, when: running`, narrow band (§6.8) |
| "1 to 3 doublets" | `on: doublet, quantity: count, min: 1, max: 3` |
| "The heat demand is met" | `on: heating_supply, quantity: unmet_share, max: <tolerance>` |
| "Supply at T °C, fixed" | case value `demand.*.supply_temperature`; a temperature requirement, if written, is `when: running` |
| "Annual emissions below M t" | `on: plant, quantity: co2, over: sum, max: M, unit: t` |

A limit on one source's availability (a doublet's days) is that source's, never the system's:
the system meets the demand on every day.

## 6.10 Rules gemini cannot express

A noise, land-use or permit rule, or one on a role gemini lacks, goes in the case's `about` and
is named as open in the handover and the report. Never dropped, never forced into a requirement
that means something else.

## 6.11 Common mistakes

| Mistake | Fix |
|---|---|
| `when: always` on a supply temperature | `when: running` |
| two requirements for one range | one with `min` and `max` |
| `count` for days, or `duration` for units | duration for time, count for units |
| `unit: "%"` on an efficiency | a fraction, no unit |
| a team preference as a requirement | it belongs to the design brief |
| a doublet's availability read as the system's | system demand met every day |

---

# 7. Case values and design freedoms

## 7.1 The test

**Who decides it?** A third party (client, organiser, regulator, nature): a case value or a
rule. The team: a design freedom. A freedom is never asked of the user as a missing value and
never written into the case; a bound on it is a requirement.

## 7.2 Typical freedoms

| Freedom | Lives in | Bound in the case |
|---|---|---|
| well depth | plant `params.depth` | none; the reservoir stays a case value |
| number of doublets | plant `size.doublets` | `doublet.count` requirement |
| flows, set points, controls | plant | flow range requirement |
| units and sizes (heat pump, boiler, chiller, CHP, store) | plant | none |
| backup policy | plant `params.backup` | demand-met requirement |
| associated gas handling (flare, boiler, CHP) | plant | emission rules, if any |

## 7.3 Return temperatures

The one team choice that sits in the case. A return temperature no file gives is a design
choice within the case's limits, not a value the design waits for: never ask the user
to supply it and never stop for it. Propose it in the one question:
`<path> = <value> <unit> | design choice, the brief leaves it to the team | <reason>`, taking
the value of an assumptions document of the case when one gives it. On approval record it with
`source: "agent"`, `confirmed: true`, `citation: {"origin": "design choice"}`.

## 7.4 A case change from the design team

The design team never changes the case. It hands over `case change needed: <path>: <why>`; the
case lead changes it and the user approves (`case_changes`, skill `setting-the-case`).

---

# 8. Sources, citations and the confirmation question

## 8.1 Order of sources

The table in §0.3. Before the one question, ALWAYS, also when the files look complete: search
Knowledge for every missing value (`search_knowledge`, then `read_knowledge` of the document or
section) and read the cost catalogue's rows of the missing keys only. Never a typical value at
any step.

## 8.2 Assumptions documents

A Knowledge document that names this case's brief or site, or gives its values key by key, is
an assumptions document (for a competition, its own document such as
`knowledge/<competition>-assumptions.md`). It comes before
the cost catalogue, so the case matches it in one question. It lives in global Knowledge only,
never in a project's files.

## 8.3 What each source records

| Source | `source` | `citation` | `confirmed` |
|---|---|---|---|
| user typed it | `user` | `{"origin": "user message"}` | `true`, no question |
| file | the file | file and page or table | needs no question |
| Knowledge, connector | `knowledge`, `connector` | document and section or row `id`; server, tool, time | after the one question |
| design choice (§7.3) | `agent` | `{"origin": "design choice"}`, reason | after the one question |
| delegated engineering assumption | `agent` | `{"origin": "agent assumption"}`, reason `engineering assumption, no source, approved by the user: <reason>` | after the one question |

A citation lets a reviewer find the value again: title, author or publisher, year, page or
section, row id or URL, and `knowledge/<name>` for a Knowledge document. A converted value names
the conversion.

## 8.4 The one confirmation question

- ONE `ask_user` question, one line per value: path, value with unit, source (or reason for a
  choice), short note. Options exactly `approve all`, `change some`, `stop`.
- It holds every value not from the user's files, every flaw (§1.4), every unit `set_case` listed
  in `converted`, every path in `plants_need`, and the time zone if assumed.
- `change some`: ask which values and to what, without options; set them; ask again.
- `stop`: finish without a final case and say so.
- The answer is final: a value left open, `unknown` or `leave open` stays unset, is listed as
  open, and is never asked again. An answer naming a source ("use the town's weather data") gives
  no value: fetch it there and confirm it.
- Economics follow in their own ONE question (`ask_economics`).

## 8.5 No computed values

Every number in the case, a question, a note or an answer is one a file, the user, a tool or
Knowledge gave, digit for digit, in its unit. Never a sum, product, conversion, count, date or a
value from a formula; never a constant from memory. A derived number that matters is named by
the values it comes from and left to gemini, or computed with `calculate` (skill `calculator`)
and cited by its id.

---

# 9. Uncertainty

## 9.1 Stating it

A best estimate with a range or a distribution, and its source (JCGM 100:2008, GUM). Before
drilling the subsurface (epistemic) uncertainty usually dominates.

## 9.2 In gemini

A value leaf takes `uncertainty` with `kind` `uniform`, `triangular` or `normal` and `min`,
`max` (plus `std` for normal) (`UNCERTAINTY_KINDS`, `gemini/gemini/units/inputs.py`). Runs,
sizing and optimisation use only the value; only uncertainty studies draw from the range.

| Source gives | Kind |
|---|---|
| lower and upper bounds only | `uniform` |
| bounds and a most likely value (the value is the mode) | `triangular` |
| mean and standard deviation | `normal`, truncated by `min`, `max` |
| P10/P50/P90 | `triangular` or `normal`; name the reading chosen |

## 9.3 Choosing a range

Take the range from the same source as the value. A wider range is an assumption with a reason;
a narrower one needs a source. Give ranges only when a study asks for them.

---

# 10. How gemini handles a case

## 10.1 Sections and files

Order of `case.json`: header (`format`, `kind`, `name`), `time`, `initial_state`, `site`,
`demand`, `utilities`, `economics`, `requirements` (`gemini/gemini/case/case.py`). A series is
`{file, column, unit}` plus optional `range` and `time_zone`; the data file is given to the case
by name, never retyped. Values the user types become a file through `save_profile`. A stateful
module (a store) has no default `initial_state`.

## 10.2 Derived keys: never set by hand

| Key | gemini derives it from |
|---|---|
| `site.reservoir.temperature` (when not measured) | ground surface temperature, gradient, depth |
| pressure at another depth | reservoir pressure, hydrostatic column |
| `site.air.pressure` from `{elevation}` | ISA standard atmosphere (ISO 2533:1975), set by `set_case` |

## 10.3 Units

gemini stores SI and writes each value back as given. Write the unit the source prints, in
gemini's names (Appendix A); gemini converts. Every value `set_case` maps or converts is listed
in `converted` and goes into the one question.

## 10.4 Validation

- A rejected `set_case` stores nothing and names each path; fix them all and resend the SAME full
  call, never a files-only call.
- `case_incomplete` lists every missing path at once.
- `missing_value` (or `missing_assumption` under `economics`) names the path a run needs.
- `plants_need` lists case values the project's plants still lack: each goes into the one
  question before the case is called complete.

## 10.5 The user's case and later changes

The project's case, or a chat's first case, is the case the user gave. Every later change,
economics included, waits for the user's approval (`case_changes`, `accept_case`).

---

# 11. Checklists

## 11.1 Before the confirmation question

- [ ] Every file read once, whole; every statement classified (§1.2).
- [ ] Demand series checked (§3.3); time zone given or proposed (§3.2).
- [ ] Every missing value searched in Knowledge and connectors (§8.1).
- [ ] Every flaw collected (§1.4).
- [ ] No design freedom in the case (§7).

## 11.2 Before handing over

- [ ] gemini accepts the case; `plants_need` empty or each path asked.
- [ ] Every value a file states is in, with file and page; none computed.
- [ ] No derived key set (§10.2).
- [ ] Units as printed; heating return below supply, cooling return above.
- [ ] Case span equals data span.
- [ ] Every hard rule of the brief is a requirement or named open in `about` (§6.10).
- [ ] Durations as durations, counts as counts, one rule per range, fractions without unit.
- [ ] `when: running` on supply temperatures and per-step doublet limits.
- [ ] Tolerances proposed and confirmed (§6.8).
- [ ] Every value not from the files confirmed and recorded with its source (§8.3).
- [ ] Economics set in the one `ask_economics` question.

## 11.3 Reviewing a case

- [ ] Trace three values at random to their page.
- [ ] Compare gemini's annual energies and peaks with the brief's values for checking.
- [ ] Read each requirement aloud: does it say what the brief says?
- [ ] List the `source: agent` values and their reasons.
- [ ] `case_changes` empty, or every change approved.

---

# 12. Worked example: a brief with daily demand files

A general pattern with **invented numbers** (a fictional town, "Northbay"). It shows the method
of chapters 0 to 11 end to end; no number here is a value for any real case. A competition or a
client case keeps its own values in its own assumptions document in Knowledge (§8.2).

## 12.1 Inputs

| File | Holds |
|---|---|
| `Northbay_Heat_Daily.csv` | `day`, `heat_MWth`: one row per day of one year, dates without offset |
| `Northbay_Cold_Daily.csv` | `day`, `cold_MWc`: same days |
| `Northbay_Brief.pdf` | 3 pages: supply temperatures, reservoir, brine, rules, freedoms |

Lessons:
- the time column is `day`: name it in `columns` when the files are given (§3.2);
- the dates have no offset: each series needs a `time_zone`. The brief names the site but no
  zone, so the zone is an assumption with its reason (the site's location) in the one question
  (§3.2, §0.3);
- the brief is the only source of rules; read every note under its tables (§1.1).

## 12.2 Values for checking

The brief says (p. 1): "heating peak 18 MW in January, 70 GWh per year; cooling peak 6 MW in
July". These check the CSV files (§1.3): a peak of 18,000 in the file would be kW; a cooling
peak in January a column swap. The case takes the series, never these numbers. gemini's
`read_profile` summary gives the file's own peak and total for the comparison.

## 12.3 Classifying the brief

| Brief says (invented) | Kind (§1.2) | Goes to |
|---|---|---|
| "Heating is supplied at 85 °C (fixed)" | case value | `demand.heating.supply_temperature` 85 degC |
| "Chilled water at 8 °C (fixed)" | case value | `demand.cooling.supply_temperature` 8 degC |
| "Reservoir top 1,900 m TVD, 60 m net sand, 150 mD" | case values | `site.reservoir.reference_depth`, `thickness`, `permeability` |
| "Gradient 32 °C/km; mean surface temperature 9 °C" | case values | `site.ground.gradient`, `surface_temperature` |
| "Reservoir pressure 190 bar(g)" | case value | `site.reservoir.pressure` 190 barg |
| "Expected reservoir temperature about 70 °C" | not a measurement | not set: gemini derives it (§4.2, §10.2) |
| "Flow per well 40 to 200 m³/h" | rule | one requirement, `min` 40, `max` 200 (§6.7) |
| "Reinjection temperature not below 30 °C" | rule | `doublet`, `injection_temperature`, `each`, `running`, `min` 30, `degC` |
| "The heat and cold demand shall be met" | rule without tolerance | `unmet_share` per supply; tolerance proposed (§6.8) |
| "Up to 2 doublets; depth may be chosen" | freedoms with a bound | `doublet.count` `max` 2; depth stays in the plant (§7) |
| "Noise at the fence below 40 dB(A)" | rule gemini cannot express | case `about`, named open (§6.10) |

## 12.4 Filling the gaps

The brief gives no return temperatures, no air values and no grid CO2 intensity. In order (§0.3):

1. search Knowledge for an assumptions document of this site; none is found;
2. search Knowledge for a cited grid CO2 intensity of the country: one document gives it with
   its year and method (location-based): propose it with that source (§5.2);
3. a weather connector is offered: read the site's air temperature from it, cited with server,
   tool and time (§4.5);
4. return temperatures: design choices with a reason, heating below 85 °C, cooling above 8 °C
   (§7.3);
5. what still has no source is asked for by path and unit, with no number of yours.

All of 2 to 5, the time zone, the tolerances and any flaw go into the ONE confirmation question
(§8.4); economics follow in one `ask_economics` question.

## 12.5 Requirements

| `name` | Rule |
|---|---|
| `production_flow_range` | `doublet`, `production_flow`, `over: each`, `when: running`, `min` 40, `max` 200, `unit` m3/h |
| `injection_temperature_floor` | `doublet`, `injection_temperature`, `over: each`, `when: running`, `min` 30, `unit` degC |
| `doublet_count` | `doublet`, `count`, `max` 2 (no over, when, unit) |
| `heat_delivered` | `heating_supply`, `unmet_share`, `max` <tolerance, confirmed> |
| `cold_delivered` | `cooling_supply`, `unmet_share`, `max` <tolerance, confirmed> |

The noise rule is in `about`, named open. The fixed supply temperatures are case values; a
temperature requirement, if written, is `when: running` (§6.6).

## 12.6 Design freedoms

Never asked as missing case values (§7): the well depth, the number of doublets within the
bound, flows, unit kinds and sizes, backup policy, gas handling. The return temperatures are
the team's choice inside the case, confirmed once and changed later only through
`case change needed` (§7.4).

## 12.7 Common traps of this pattern

| Trap | Right reading |
|---|---|
| set the "about 70 °C" reservoir temperature | an expectation, not a measurement: leave it to gemini |
| two requirements for "40 to 200 m³/h" | one requirement with both ends |
| `when: always` on the injection floor | `running`: an idle doublet injects nothing |
| use the brief's 70 GWh as a value | a check of the file only |
| ask the user for the well depth | a design freedom |
| series refused for a missing zone | add `time_zone` from a source or a confirmed assumption |

## 12.8 Done when

- gemini accepts the case; `plants_need` empty or each path asked (§10.4);
- every brief value in, with its page; nothing derived set by hand;
- every rule a requirement or named open; tolerances confirmed;
- both series with a `time_zone` or offsets;
- every value not from the files confirmed once and recorded with its source (§8.3);
- economics set in one question.

---

# Appendix A. Unit pitfalls

| Source writes | gemini reads | Note |
|---|---|---|
| `MWth`, `MWcool`, `MWc` | `MW` | the suffix names the product |
| MWh/d in a "power" column | an energy per day | not a power; confirm |
| `bar(g)`, `barg` | `barg` | gauge; gemini adds one standard atmosphere |
| `bar`, `bara` | `bar` | absolute |
| `°C/km` | `degC/km` or `K/km` | equal |
| `%` efficiency or share | `0.7` (no unit) | requirements and fractions |
| `mol%` | `mol%` | gemini converts to a fraction |
| `Nm³` vs `Sm³` | `Nm3` | 0 °C (DIN 1343) vs 15 °C (ISO 13443) |
| relative humidity `%` | `"unit": "%"` | gemini converts; never convert yourself |
| `mD` | `mD` | gemini converts to m² (1 D = 9.869233×10⁻¹³ m²) |
| `kg/m³`, `mPa·s` | `kg/m3`, `mPa.s` | |
| `2027-01-01` in a series | refused without `time_zone` | give `time_zone` or offsets (§3.2) |

# Appendix B. Glossary

| Term | Meaning |
|---|---|
| case | the outside conditions over one period and the rules of third parties |
| design freedom | a choice of the team, bounded at most by a requirement |
| doublet | a production and an injection well |
| GLR | gas-liquid ratio, normal m³ of gas per m³ of liquid |
| requirement | a rule on a quantity of a role, with its band |
| role | what a unit is for, read from the plant's wiring |
| TVD / MD | true vertical depth / measured depth along the well |
| transmissivity | permeability × thickness (kh) |
| unmet share | unmet over demanded energy of a service over the period |
| value for checking | a brief's number used only to check the data |

# Appendix C. References

- Frederiksen, S. and Werner, S. (2013). *District Heating and Cooling*. Studentlitteratur.
- Huenges, E. (ed.) (2010). *Geothermal Energy Systems*. Wiley-VCH.
- Stober, I. and Bucher, K. (2021). *Geothermal Energy*, 2nd ed. Springer.
- ISO/IEC/IEEE 29148:2018. *Requirements engineering* (characteristics from secondary summaries
  of section 5.2.5).
- JCGM 100:2008. *Guide to the expression of uncertainty in measurement* (GUM).
- WRI and WBCSD (2015). *GHG Protocol Scope 2 Guidance*.
- ISO 2533:1975 *Standard Atmosphere*; DIN 1343 *Normal conditions*; ISO 13443:1996 *Natural gas
  standard reference conditions*.
- gemini 0.6.17: `gemini/gemini/case/`, `gemini/gemini/plants/roles.py`,
  `gemini/gemini/units/inputs.py`.
- geomind: prompts `case/lead.md`, `case/geoscientist.md`; skills `setting-the-case`,
  `finding-sources`, `connectors`, `gemini-units`, `calculator`.
