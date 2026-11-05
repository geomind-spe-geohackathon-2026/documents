**Handbook: defining an energy-supply case** (`knowledge/handbook-case.md`)

How to turn a brief and data files into a complete, sourced case for a geothermal heating and
cooling plant in gemini. For the case lead, the geoscientists and any reviewer of a case.

- **Cite as** `knowledge/handbook-case.md §<section>` (for example `§6.5`).
- **Read by section**, never whole: `read_knowledge(name="knowledge/handbook-case.md",
  section="0")`. Chapter 0 is the short version of the whole handbook; read it first, then only
  the sections it points to.
- **Source of truth.** Keys, units, roles and quantities are gemini's (`gemini/gemini/case/`,
  `gemini/gemini/plants/roles.py`, `gemini/gemini/units/inputs.py`, gemini 0.6.34). When this
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
10. How gemini handles a case; 10.7 the case team's tools by job
11. Checklists
12. Worked example: a brief with daily demand files
13. Engineering background for checking a case: demand, load duration, ground, reservoir,
    doublet power, brine and gas, emission factors, outside air (each with a worked example)
14. Lessons from case reviews: stored = approved, nothing to start from, how the user answers,
    scope, values and digits, requirements that fail a correct plant, saying what is true, one
    question once
15. Reference ranges for the values agents search most: network temperatures, cooling and
    dew point, produced gas, sand, grid limits, initial state, salinity and net-to-gross
16. Checking a data file step by step: procedure, outliers, weather and price series
17. Requirements documents, limits, units and time in depth: modal verbs and traceability, the
    four questions from limit to requirement, tolerances, ask or take from Knowledge, units, time
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
4. **Merge.** Merge the findings into one list of values with their sources. Save nothing yet.
5. **Search the gaps.** For each missing value: Knowledge (assumptions document first), then a
   connector (§0.3, §8.1).
6. **Ask once.** ONE confirmation question with every value that did not come from the user's
   files, every flaw, and every agent choice (§8.4). Nothing that needs approval is saved before
   `approve all`.
7. **Set once.** ONE `set_case` with the file and user values and the approved values (§10).
8. **Follow-up, only if needed.** When that `set_case` returns `plants_need` paths or unit names it
   mapped (`converted`), ONE more `ask_user` with only those (§8.4, §10.4).
9. **Economics once.** ONE `ask_economics` question (skill `setting-the-case`;
   `knowledge/handbook-economics.md`).
10. **Check and hand over.** `read_case` again, then the checklist §11.2.

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
| write, ask or re-delegate after the user's `stop` | finish and report the stop | §8.7 |
| quote a value read before the last `set_case` | read the case again | §10.6 |
| ask for, or search, an optional key the case does not need | leave it unset; ask only what `set_case` reports as needed | §8.6 |

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
`missing` (only keys the case needs, §8.6) and `disagreements`. Economics are not a group: the lead sets them with
`ask_economics`.

| Group | Keys it owns | Read |
|---|---|---|
| I. Time and demand | `time.*`; `demand.heating.*`; `demand.cooling.*` (power, supply and return temperatures and pressures, indoor values) | §2.1, §2.2, §3 |
| II. Ground and reservoir | `site.ground.*`; `site.reservoir.*`; quality and range of each | §2.3, §4.1 to §4.3, §9 |
| III. Brine, gas, air and utilities | `site.fluid.*`; `site.air.*`; `utilities.electricity.*`; `utilities.gas.*` | §2.3, §2.4, §4.4, §4.5, §5 |
| IV. Requirements | every rule of the brief as a requirement; rules gemini cannot express; tolerances to propose | §6 (above all §6.7, §6.11, §6.12), §7 |

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
| `air.relative_humidity` | fraction 0 to 1, or `%` with `"unit": "%"` | file, weather connector | optional: no module reads it in gemini 0.6.34; leave it open unless a source gives it, never ask for it; never convert it yourself |
| `air.pressure` | `Pa`, `bar`; or `{"elevation": {value, unit}}` | file, connector, or the site's elevation | the elevation is the value confirmed; the ISA pressure gemini derives from it is not asked again |

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
| `sum` | the sum of the step values | a total of a per-step amount (CO2 mass of the year); a power's `sum` adds step values, not an energy: an energy cap is `over: mean` (§17.2) |
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
| "Electricity bought at most E per year" (one-year case) | `on: plant, quantity: electricity_bought, over: mean, max: E / period` as a power (§17.2) |

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
| two proposals on the same `on` and `quantity` (`min_stable_flow` 50 and `max_production_flow` 300) kept apart when merging | merge them into one requirement with `min` and `max` (§6.12) |
| an exact ratio as `min: 1, max: 1` | a narrow band from the tolerance source (§6.8): an exact 1 fails on round-off |
| a temperature difference (`brine_cooling`, `approach`, `lift`) in `degC` | `K`, the unit of a difference |
| a rule a source marks conditional ("only if the design checks it") written as a requirement | left out of the case; named in the handover for the design team |
| a requirement the brief does not state, added from a reference or a habit | only rules of the brief, the client or an assumptions document of the case |

## 6.12 The same requirements every run

The same brief must give the same requirements every time. Write them by this procedure, not
freely:

1. **One row per rule.** List each rule sentence of the brief (§1.2) with its page; one rule is
   one requirement. A geoscientist proposes, the lead decides.
2. **Merge on `on` + `quantity`.** Before `set_case`, group all proposals by `on`, `quantity`,
   `over` and `when`. Two in one group are one rule: one requirement with the `min` of one and
   the `max` of the other. Two different values for the same bound are a disagreement (§1.4).
3. **Shape from §6.9.** Take `over`, `when` and `unit` from the pattern table, never chosen anew.
4. **Names by pattern.** `<quantity>_range` (both bounds), `<quantity>_limit` (`max`),
   `<quantity>_floor` (`min`), `<quantity>_exact` (`min` = `max`); for days of operation
   `running_time_limit`; for a count `<role>_count`; for demand met `heat_delivered` and
   `cold_delivered`. Stable names keep the verdict, the comparison of designs and the report
   readable across runs.
5. **Tolerances from one source, all of them.** When an assumptions document of the case lists
   tolerances, take every one of its rows (demand met, ratios), as written; otherwise propose each
   in the one question (§6.8). Never a tolerance in one run and an exact value in the next.
6. **Count and compare.** Count the requirements against the rule list of step 1; when an
   assumptions document or a reference case of the same brief lists its requirements, compare
   name by name and name every difference with its reason in the handover.

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
Knowledge for every needed missing value (§8.6) (the case lead: `search_rag`, then `read_rag("knowledge/<name>")`;
a geoscientist: `search_knowledge`, then `read_knowledge` of the document or section) and read the cost catalogue's rows of the missing keys only. Never a typical value at
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
- It comes before the first `set_case` and holds every value not from the user's files
  (Knowledge, connector, design choice, tolerance, delegated assumption), every flaw (§1.4), and
  the time zone if assumed. Values from the files and the user are set without it.
- What only `set_case` reports cannot be in it. After the one `set_case`, ask ONE follow-up
  `ask_user` only when it returns `plants_need` paths (values the plants still lack: asked by
  path and unit, no number of yours) or a unit name it mapped in `converted`. Unit conversions
  gemini makes between units a key accepts, and derived keys (the ISA pressure from a confirmed
  elevation), are not asked.
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
the values it comes from and left to gemini; it never goes into the case. (`calculate` serves
the design and the report, not the case.)

## 8.6 Only what the case needs

Many keys of the key tree (§2) are optional: gemini needs them only for some plants or some
studies. Searching and asking for them costs the user a question and may move the case away from
what the brief meant.

- **Needed** is what gemini says is needed: a path in `case_incomplete`, `missing_value` or
  `plants_need`, or a key the brief itself gives. Search the gaps (§8.1) and ask (§8.4) only for
  those, plus the values that need confirmation because they came from Knowledge or a connector.
- **Optional and not given:** leave it unset, say nothing to the user, and do not list it as
  "missing" in a geoscientist's findings. Typical ones:

| Key | Needed only when | Otherwise |
|---|---|---|
| `site.air.relative_humidity` | the plant rejects heat to air by evaporation (a cooling tower) or a study needs it | unset |
| `utilities.gas.heating_value` | no `utilities.gas.composition` is given | unset: gemini computes the heating value from the composition |
| `utilities.electricity.import_limit`, `export_limit` | the grid operator states a limit | unset |
| `demand.*.minimum_return_temperature`, `maximum_return_temperature` | the network data state them | unset |
| extra gas species (`O2`, `H2S`) | the analysis lists them | not added |

- A reason given to the user must be true: never "needed to price the gas" for a key gemini does
  not need. When unsure whether a key is needed, `describe_case(path)` and the `set_case` result
  decide, not a habit.

## 8.7 What each answer means

The user answers a question (`ask_user`) or an approval card for a write (`set_case`). Each answer
has one meaning, and it holds for the rest of the request.

| Answer | Means | Do | Never |
|---|---|---|---|
| `approve all` | every listed value is approved | set them all in the one `set_case`; record each with its source (§8.3) | ask any of them again |
| `change some` | some values change | ask which and to what, without options; set them; confirm the changed lines once | treat the unchanged lines as open |
| values typed instead of an option | the typed values are the answer | set them as the user's (`source: user`) | ask to confirm what the user typed |
| `stop` | the user ends the case work for this request | finish at once: report what is set, what is open, and that the user stopped; the whole team stops (the project lead does not send the case lead again) | another `set_case`, another question, or a final answer that blames anything but the stop |
| card approved | the call may run | nothing more to confirm | a question that repeats the card |
| card denied **with a change** (text in the reason box) | "change this and propose again" | apply the change, and propose the same call once more with it | read it as a plain no; ask "shall I write it with the change?" |
| card denied **without a reason** | "no" to this call | do not send that call again in this request; report what is not saved and why | retry the same call, or route it through another agent |

When a tool refuses a call because the user denied it earlier, do not loop: one refusal is the
answer. Report it, with what the user asked to change, and stop that path.

## 8.8 What an approval card must say

A card is the user's only view of a write. It must let the user approve without opening JSON:

- **One sentence of what is saved:** "Set the case: time, demand, site, 8 requirements from
  brief.pdf and demand.csv, 11 approved values" or "Load the project's case, version 4".
- **What changes:** each path that differs from the case before, `before -> after`, with its
  source (file and page, `user`, Knowledge document). A load of the user's saved case names the
  values the user changed.
- **Nothing the user already decided.** A value the user typed or saved needs no second approval.

The card's text is built from the call's arguments, so a call that carries the values it changes
(not only `{"source": "project"}`) shows them. The handover after the write repeats the same
sentence and changes.

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
| P10/P50/P90 | `triangular` or `normal`; name the reading chosen; check the convention (PRMS and finance: P90 is the value exceeded with 90 % probability, the LOW end; some sources mean the opposite), `knowledge/handbook-studies.md §4.3` |

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
in `converted`: a mapped unit name goes into the follow-up question (§8.4); a conversion between
units the key accepts is gemini's and is not asked.

## 10.4 Validation

- A rejected `set_case` stores nothing and names each path; fix them all and resend the SAME full
  call, never a files-only call.
- `case_incomplete` lists every missing path at once.
- `missing_value` (or `missing_assumption` under `economics`) names the path a run needs.
- `plants_need` lists case values the project's plants still lack: each goes into the follow-up
  question (§8.4) before the case is called complete.

## 10.5 The user's case and later changes

The project's case, or a chat's first case, is the case the user gave. Every later change,
economics included, waits for the user's approval (`case_changes`, `accept_case`).


## 10.6 A case changed by hand

The user may save the case in the app (a form, an upload) while a chat runs. Then:

- **The saved case is the user's.** Its values are `source: user`: never ask the user for a value
  they saved, and never ask them to approve it again (§8.7).
- **Every earlier read is stale.** After a load (`set_case(source="project")`) or any `set_case`,
  results of `read_case`, `case_changes` and briefs written before it no longer hold. Read the case
  again (`read_case`) before a brief, a question or a claim, and quote values only from that read.
- **The case beats the brief.** When a brief says one value and `read_case` shows another, the case
  is right: report the difference to whoever wrote the brief; do not ask the user.
- **What changed** is the difference between the case before the load and the case after it
  (path, `before -> after`), named in the handover and on the card (§8.8). `case_changes` compares
  with the case the user gave, so after a load of the user's own case it may be empty: that means
  "nothing to approve", not "nothing changed".
- The next step is the design team's: simulate and check the current design on the new case. A
  case lead step is needed only when gemini names a missing value.

---

## 10.7 Tools of the case team, by job

Which tool does which job (geomind `agents/case/lead.py`, `agents/case/geoscientist.py`).
How to call each: the skills named in the front matter.

| Job | Case lead | Geoscientist |
|---|---|---|
| list and read the user's files | `list_files`, `read_rag` | (gets the text in its brief) |
| search and read Knowledge | `search_rag`, `read_rag` | `search_knowledge`, `read_knowledge` |
| keys, units, bounds, what is missing | `describe_case` | `describe_case` |
| read the case | `read_case` (only once a case exists) | none |
| write the case | `set_case` (once, after the one question) | none |
| economics | `ask_economics` (once) | none |
| series the user types | `save_profile` | none |
| fix a few steps of a series | `repair_series` | none |
| look at saved series | `list_profiles`, `read_profile` | none |
| a big earlier tool result | `read_stored` | none |
| the web | `web_search`, `read_web_page` | none |
| connectors (when on) | `list_mcp`, `read_mcp`, `call_mcp`, `save_mcp_table` | none |
| arithmetic for a check | `calculate` (never for a case value, §8.5) | none |
| the user | `ask_user` (the one question, §8.4) | none |
| split the work | the `geoscientists` team, one field group each (§0.4) | none |
| lessons and user facts | `search_memory`, `read_memory` | `search_memory`, `read_memory` |
| a skill's text | `read_skill` | none |
| record progress, end | `update_state`, `finish` | `finish` |

**Rules.** A geoscientist never writes or asks; it returns findings with sources. Knowledge is
read by section after its outline (front matter). A source found on the web is a candidate
like any other: it goes in the one question with its URL and date (§8.3). A connector table
becomes a case file with `save_mcp_table`, then is passed to `set_case` by its file name.

# 11. Checklists

## 11.1 Before the confirmation question

- [ ] Every file read once, whole; every statement classified (§1.2).
- [ ] Demand series checked (§3.3); time zone given or proposed (§3.2).
- [ ] Every missing value searched in Knowledge and connectors (§8.1).
- [ ] Every flaw collected (§1.4).
- [ ] No design freedom in the case (§7).

## 11.2 Before handing over

- [ ] gemini accepts the case; `plants_need` empty or each path asked in the follow-up (§8.4).
- [ ] Every value a file states is in, with file and page; none computed.
- [ ] No derived key set (§10.2).
- [ ] Units as printed; heating return below supply, cooling return above.
- [ ] Case span equals data span.
- [ ] Every hard rule of the brief is a requirement or named open in `about` (§6.10).
- [ ] Durations as durations, counts as counts, one rule per range, fractions without unit.
- [ ] `when: running` on supply temperatures and per-step doublet limits.
- [ ] Tolerances proposed and confirmed (§6.8).
- [ ] Requirements written by §6.12: proposals merged on `on` + `quantity`, names by pattern, count equals the brief's rules.
- [ ] No optional key asked for or listed as missing (§8.6).
- [ ] Every claim and question quotes the case as read after the last `set_case` (§10.6).
- [ ] Each answer handled as §8.7 says; after `stop`, no further write.
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

# 13. Engineering background for checking a case

What a case value means physically, how to check it for plausibility, and how gemini uses it.
These are checks, never values: a number here never enters a case (§8.5, §0.2). Every example
uses invented numbers.

## 13.1 Heat demand: power, energy and the degree-day check

**Lesson.** A demand series is power over time; its energy is the sum of power times step
length, `E = Σ P_i · Δt_i`. Space-heating demand follows the outside temperature roughly
linearly below a balance (base) temperature; hot-water demand is nearly constant over the year.
The degree-day method (CIBSE TM41; EN ISO 15927-6) states this:
`E_space ≈ UA · HDD · 24 h`, with `HDD = Σ max(0, T_base − T_out,day)` in K·d and `UA` the
building's heat loss coefficient. The design (peak) load of EN 12831-1 is
`P_design ≈ UA · (T_inside − T_design,out)`.

**How to use it.** When a brief gives both a series and a yearly energy, the two must agree
within the rounding of the brief (§1.3). When a brief gives a peak and an energy, the ratio
`E / (P_peak · 8760 h)` is the load factor: typical space heating gives a low load factor,
process heat a high one (Frederiksen and Werner 2013, ch. 4). A load factor far outside the
pattern of the stated use is a flaw to name in the confirmation question, not to fix.

**Worked example (invented).** A daily series has 365 values in MW. Mean 4.2 MW, peak 11.0 MW.
Energy `4.2 MW × 8760 h = 36 792 MWh ≈ 36.8 GWh`. Load factor `4.2 / 11.0 = 0.38`. The brief
says "about 37 GWh a year": consistent. Had the brief said 3.7 GWh, the file is likely in
MWh/d or the brief in another unit: ask, never rescale (Appendix A).

**Traps.** A daily series in MW is the day's mean power, not its peak: the hourly peak inside
the day is higher. Keep the series as given and name the resolution in the handover so the
design team knows peaks are smoothed (§3.4).

## 13.2 Load duration curve, base and peak

**Lesson.** Sorting a year of demand from highest to lowest gives the load duration curve. The
area under it is the energy; its left end is the peak. A base-load source (geothermal, a heat
pump on a steady source) that covers a fraction of the peak power usually covers a much larger
fraction of the energy, because high loads last few hours (Frederiksen and Werner 2013, ch. 4;
Huenges 2010, ch. 9).

**How to use it.** In the case: give the series as it is; the split into base and peak is a
design freedom (§7.2), never a case value. In the handover: name the peak, the mean and the
duration of high loads, so the design team can size the base source from the curve.

**Worked example (invented).** Sorted daily means: 60 days above 8 MW, 120 days between 4 and
8 MW, 185 days below 4 MW. A base source of 6 MW is the full demand on most days below 6 MW and
6 MW on the rest. With a mean of 4.2 MW, it covers on the order of 80 to 90 % of the energy
while holding only 55 % of the 11 MW peak. The design team computes the exact share with gemini;
the case lead only checks that the series supports such a split.

**Cooling.** The same curve applies to cooling demand. Heating and cooling at the same time
(spring, autumn, process loads) matter for a plant that recovers heat between them: say in the
handover whether the series overlap.

## 13.3 Ground temperature and the reservoir temperature

**Lesson.** In conductive crust the temperature rises about linearly with depth:
`T(z) = T_surface + G · z`. The geothermal gradient `G` depends on the rock's thermal
conductivity and the heat flow `q`: `G = q / λ` (Fourier's law; Stober and Bucher 2021, ch. 2).
Sediments with low conductivity (shale) give higher gradients than crystalline rock. A regional
average is a prior; a measured well temperature at depth beats it.

**In gemini.** `gemini.physics.ground.geotherm_temperature(surface_temperature, gradient,
depth)` and `reservoir_temperature(...)`: with a measured reference temperature, gemini uses
`T = T_ref + G (z − z_ref)`; without one, it starts from the surface. That is why the case
holds `reservoir.temperature` only when it is a measurement (§2.3): a computed value would hide
the gradient's uncertainty and is a computed value (§8.5).

**Worked example (invented).** Surface 9 °C, gradient 31 K/km, reservoir top at 2 400 m TVD:
`9 + 31 × 2.4 = 83.4 °C`. A drill-stem test at 2 400 m gave 79 °C. Keep the measurement; the
mismatch (4 K) is a value for checking that says the gradient overstates this site.

**Traps.** Depth must be true vertical depth (TVD), not measured depth along a deviated well
(Appendix B). Gradients printed as °C/km and K/km are equal; °F/100 ft is not (1 °F/100 ft ≈
18.2 K/km).

## 13.4 Reservoir pressure and deliverability

**Lesson.** At hydrostatic conditions the pore pressure is `p(z) ≈ p_surface + ρ g z`
(`gemini.physics.hydraulics.hydrostatic_pressure`). Overpressure or underpressure is what a well
test shows against that line. How much water a well delivers per unit of drawdown is its
productivity index `PI = Q / (p_res − p_wf)`; for injection the injectivity index `II`
(`productivity_index`, `injectivity_index` in the same module). For steady radial flow (Thiem;
Dake 1978, ch. 6) `PI` scales with the transmissivity `k h`: double the thickness or the
permeability, double the PI. The case holds `permeability` and `thickness`; gemini derives the
indices (`radial_index`).

**How to use it.** Keep the permeability with the thickness it was measured over (gross or net,
as the source says), since the product is what matters. A core-plug permeability is often far
from the well-test value at reservoir scale; prefer the well test and say which it is.

**Worked example (invented).** `k = 400 mD`, `h = 60 m`: `kh = 24 000 mD·m = 24 D·m`. A second
source gives 300 mD over a net 80 m: also 24 D·m. The two agree on the product; record the pair
from the better source, never mix one source's k with the other's h.

**Units.** 1 D = 9.869233×10⁻¹³ m² (Appendix A); `barg` is gauge, add one standard atmosphere for
absolute (§2.3). A pressure without its reference depth is incomplete.

## 13.5 Thermal power of a doublet and thermal breakthrough

**Lesson.** Heat taken from produced water is `P = ṁ · c_p · (T_prod − T_inj)` with
`ṁ = ρ · Q` (`gemini.physics.energy.circuit_flow` solves it for the flow). The injection
temperature is a design choice bounded by the users' return temperature and any scaling limit
(§7.3); the production temperature falls once the cold front from the injector arrives.
Gringarten and Sauty (1975) give the breakthrough time of a doublet in a confined aquifer;
gemini implements it (`gemini.physics.ground.doublet_breakthrough_volume`,
`doublet_breakthrough_time`, `doublet_cold_fraction`). The well spacing is a design freedom,
never a case value.

**How to use it.** The case gives what the ground is (temperature, pressure, permeability,
thickness, fluid); flow, spacing and injection temperature are design. When a brief states a
flow or a spacing as a site "fact", classify it: if it is a licence limit it is a rule (§6.10);
if it is a suggestion it is a freedom (§7.2).

**Worked example (invented).** `Q = 150 m³/h = 0.0417 m³/s`, `ρ = 1 050 kg/m³`,
`c_p = 3.9 kJ/(kg·K)`, `T_prod = 80 °C`, `T_inj = 40 °C`:
`P = 0.0417 × 1 050 × 3.9 × 40 = 6 830 kW ≈ 6.8 MW`. Halving the temperature drop halves the
power: the injection temperature matters as much as the flow.

**Traps.** Brine heat capacity is lower than that of pure water (salt lowers it); never use
4.18 kJ/(kg·K) for a brine without a source.

## 13.6 Brine, dissolved gas and their effect on the case

**Lesson.** Formation water in sedimentary basins is often saline. Salinity raises density and
viscosity and lowers heat capacity; temperature lowers density and viscosity (Batzle and Wang
1992; Kestin et al. 1981). Dissolved gas (CO₂, CH₄, N₂) comes out of solution when the
pressure falls below the bubble point, in the well or the surface plant; it changes the
mixture density and the pump's work and may be a fuel (CH₄) or an emission (CO₂) (Huenges 2010,
ch. 5).

**In gemini.** The liquid properties are constant snapshots (`gemini/physics/fluid.py`,
`FluidProperties`): gemini does not correct a density or viscosity for temperature or salinity.
So the case must hold the value at the conditions the plant sees, and the source must say those
conditions (§2.4). A density "at 20 °C, surface" for an 80 °C brine is a flaw to name.
The gas-liquid ratio and the gas composition feed `gemini.physics.gas` (`gas_mass_fraction`,
`combustion_co2`, `emission_per_energy`).

**Worked example (invented).** A fluid report gives salinity 120 g/l, density 1 080 kg/m³ at
20 °C, viscosity 1.3 mPa·s at 20 °C, and GLR 0.9 Nm³/m³ with 75 mol% CO₂, 20 mol% CH₄,
5 mol% N₂. The composition sums to 100 % (check). Density and viscosity are at 20 °C, not at the
production temperature: put them in the confirmation question as "file values at 20 °C;
reservoir values unknown", and let the user approve or give better ones. Never correct them
yourself with a correlation: that is a computed value (§8.5).

**Normal vs standard.** `Nm³` is at 0 °C, `Sm³` at 15 °C (DIN 1343, ISO 13443): the same gas
volume differs by about 5.5 %. Keep the unit the source prints (Appendix A).

## 13.7 Grid electricity and emission factors

**Lesson.** The GHG Protocol Scope 2 Guidance (WRI and WBCSD 2015) defines two methods: the
**location-based** factor (the average intensity of the grid where power is used) and the
**market-based** factor (the contracts the user buys: guarantees of origin, supplier mix,
residual mix). An **average** factor describes the grid's mean; a **marginal** factor describes
the plant that changes when demand changes. They answer different questions and can differ by a
factor of two or more.

**How to use it.** The case holds the factor the brief or the user names, with its method and
year (§5.2). When the brief names none, the confirmation question offers the candidates with
their method and source; the user picks (§8.4). A factor in g/kWh and one in kg/MWh are equal;
t/MWh is 1 000 times larger.

**Worked example (invented).** A plant uses 9 GWh of electricity a year. Location-based
0.35 kg/kWh gives `9×10⁶ × 0.35 = 3.15×10⁶ kg = 3 150 t CO₂`. Market-based with a renewable
contract 0.02 kg/kWh gives 180 t. Both are right for their method; the report must say which.

**Gas.** For bought gas the factor per energy needs the heating value basis: lower (LHV) or
higher (HHV); for natural gas HHV is about 10 % above LHV. Keep the basis the source states.

## 13.8 Outside air and weather series

**Lesson.** Air temperature drives air-source heat pumps, dry coolers and cooling towers. A
constant air temperature hides the season: the plant's worst hours are the cold heating hours
and the hot cooling hours. Air pressure falls with elevation (ISO 2533 standard atmosphere),
which matters for air density in fans and coolers; gemini derives it from the elevation
(§2.4).

**How to use it.** Prefer a series of the same span and step as the demand, from a file or a
weather connector, with its time zone (§3.2). A connector that prints `GMT` means `UTC`. A
typical-year or reanalysis series is an assumption: name it as such in the confirmation
question. Say "constant" in the case when a single value is used.

**Worked example (invented).** Demand is daily for one year; the connector gives hourly air
temperature. The case keeps the connector's series as a saved file with its own step and time zone
(§3.4); `describe_case` says whether gemini accepts the mixed steps. Never average it by hand
into a new series (§8.5). If the connector covers only part of the year, the
gap is a flaw to name, not to fill with a guess.

# 14. Lessons from case reviews

General lessons from reviewed case runs. Each names the mistake, the rule and the section that
holds the rule. They apply to any case.

## 14.1 What is stored must be what was approved

- **Stored differs from approved.** The user approved one value and the case holds another
  (a candidate from an earlier search, a rounded value, a second source). Rule: the `set_case`
  call carries exactly the approved values, digit for digit; after it, `read_case` and compare
  every approved path (§11.2).
- **Approved but left out.** A value the user approved is dropped because "no module needs it".
  Rule: what the user approved is stored; only values never asked may stay unset (§8.6).
- **Computed and stored.** A value derived by a formula (a standard-atmosphere pressure, a
  corrected density, an averaged series) is written into the case. Rule: store the input the
  source gives (the elevation, the measured density, the series) and let gemini derive the rest
  (§8.5, §10.2).
- **Retyped series.** A user's fix to a few values of a long series is sent by retyping the
  whole series. Rule: repair only the named steps with `repair_series` (it inserts missing rows and
  shows the neighbours) and pass the result by file name; a series is never retyped (§10.6).

## 14.2 When there is nothing to start from

- **No case yet.** Reading the case before one exists returns an error; it is not a fault to
  retry. Rule: start from `list_files`; call `read_case` once a case exists (§0.1).
- **No files at all.** With no brief and no data, every value is an assumption: offer the
  candidates with sources in the one confirmation question; never claim an example case or
  files exist that are not in the project (§8.1, §8.4).
- **Connector series.** A series saved from a connector is a project file like any other; pass
  it by the saved name and with its time zone (`GMT` is `UTC`) (§3.2, §13.8).

## 14.3 How the user answers

- **Auto-approve is on.** Ask the user nothing: no confirmation question, no follow-up. Use the
  same sources in the same order and record each choice with its source in the case, so the
  user can review it later (§8.1, §8.3).
- **"Best guesses, don't ask".** The same: one search per gap, the best-sourced candidate, its
  source recorded; no retries of a refused call with the same arguments.
- **Deny.** A deny with a reason stops the change it denies; a deny with a change means propose
  again with that change, once (§8.7). A refusal by the user is never overridden by a later
  step of another agent.
- **Changed by hand.** When the user edits the case on the Case page, the next `read_case` is
  the truth; compare with what you held and name what changed (§10.6).

## 14.4 Scope of the case lead

- **Only the case.** A request about economics, a design or a report does not reopen the site
  survey; read the case and pass on. Site values are re-surveyed only when the user asks or a
  value is missing (§0.3).
- **One assumptions document per case.** When the case names an assumptions document, its
  values come first for every key it covers; a source for another place or country replaces it
  only for the keys the user names (§8.1, §8.2).
- **Read by section.** Knowledge is read by section after its outline, never whole; a search
  result is a pointer to a section, not a value to paste (front matter of this handbook).

## 14.5 Values and digits

- **Retyped digits.** A number shown in a question or a card with other digits than the source
  (rounded, a digit dropped, a float tail). Rule: copy every value from the source text or the
  tool result exactly; show it as the source prints it, and store the same digits (§8.8).
- **Units gemini refuses.** A value approved in a unit gemini does not read (`mg/L` in another
  spelling, a bare percent) means a second approval. Rule: before the question, check each
  key's accepted units with `describe_case` and write the value in one of them, converting
  nothing; the unit the source prints goes in the source note (Appendix A).
- **Dependent values.** When one value changes, values the source tied to it may no longer
  hold: a pressure given "at" a depth holds at that `reference_depth`, not at a new design
  depth; a density given at one temperature does not follow a new one. Rule: when the user
  changes a value, list the values its source tied to it and say whether they still hold
  (§2.3, §13.4).
- **A series from two numbers.** A peak power and a yearly energy do not define a series:
  the shape is missing. Rule: ask for a series or a cited profile; never build one, and never
  fall back to a constant without the user's approval (§3.3, §8.5).

## 14.6 Requirements that fail a correct plant

- **Exact and always.** A supply temperature written as an exact value checked `always` fails
  on every step where the service is idle (no demand). Rule: a temperature the plant must give
  while serving is checked `when: running`, with the tolerance from one source (§6.6, §6.8).
- **Half a range.** A flow band given as "between A and B" is ONE requirement with `min` and
  `max`; written as two, or with one end only, gemini cannot read it as a range for the units
  that need one (§6.7).
- **Rules not in the case.** A rule of the brief that gemini cannot express stays out of the
  case and is named in the handover (§6.10). No agent may later say "the case fixes" it.

## 14.7 Saying what is true

- **Claimed but not done.** Never say "the case is set" or "complete" when the last `set_case`
  was refused or `describe_case` still lists missing keys; say what is missing (§11.2).
- **Words put in the user's mouth.** Never write "the user said" or "the user chose" for a value
  the user did not state; an agent choice is `source: agent` with its reason (§3.2, §8.3).
- **Delegated values.** When the user says "you choose" or "use your best judgement", that is
  not a reason to leave the values open: propose each with the best source found, mark it as
  the agent's choice, and ask the one question unless approval is waived (§14.3).

## 14.8 One question, once

- **The same question again.** A question the user answered is never asked again in the run;
  read the answer from the conversation and the case (§8.4, §8.7).
- **Questions in rounds.** Asking site, then demand, then air in separate rounds triples the
  user's work. Rule: one question with every open value grouped by section; a second only for
  what `set_case` itself reports (`plants_need`, mapped units) (§0.1 steps 6 to 8).
- **Values nobody needs.** Keys no module of the case reads, and that no source gives, are not
  asked (§8.6); keys the plant needs that are missing are asked once, before the design starts,
  never discovered by the design team later.

# 15. Reference ranges for the values agents search most

Answers to the questions case agents ask Knowledge most often. Each section says what the key
is, where its value comes from, the typical range in the literature (to check a source, never to
fill a gap) and common mistakes. A typical range is never a case value: a gap is filled only by
a source the user approves (§8.1, §8.4). Examples use invented numbers.

## 15.1 Supply and return temperatures of heating networks

**What.** `demand.heating.supply_temperature` is what the consumers ask for; `return_temperature`
what they give back; `minimum_return_temperature` and `maximum_return_temperature` the limits
the network operator states. They are the consumer's, not the plant's: the plant must meet them.

**Typical ranges.** Lund et al. (2014) describe the generations of district heating:
third-generation networks run supply temperatures mostly below 100 °C with returns of about
40 to 50 °C; fourth-generation (low-temperature) networks aim at supply 50 to 60 °C and return
about 25 °C. Frederiksen and Werner (2013, ch. 6) show that return temperature is set by the
consumers' substations: a poor substation raises it. Building heating systems designed to
EN 12831-1 with radiators often run 70/50 °C or 55/35 °C; floor heating lower.

**Why it matters.** The heat taken from geothermal brine is limited by how cold the injection can
be, which is bounded below by the network return (§13.5, §7.3). A return temperature 10 K too
high can cut the usable temperature drop by a fifth or more.

**Mistakes.** Taking a supply temperature from a design table and writing it as the case value;
mixing a network's design temperature with its yearly mean; writing a return temperature that a
source gives only as a target as if it were a limit (§6.10).

**Example (invented).** A brief gives supply 85 °C and "return about 45 °C". Case: supply 85,
return 45, both cited to the brief. No minimum or maximum return: the brief gives none (§8.6).

## 15.2 Cooling networks, indoor air and the dew point margin

**What.** `demand.cooling.supply_temperature` and `return_temperature` are the chilled water;
`indoor_temperature` and `indoor_relative_humidity` the room; `dew_point_margin` [K] how far the
chilled water must stay above the room's dew point so that no condensation (latent load) occurs.

**Typical ranges.** The ASHRAE District Cooling Guide (2013) describes conventional chilled-water
networks with supply about 4 to 7 °C and a design temperature difference of about 8 to 10 K.
High-temperature cooling (chilled ceilings, active beams) uses supply 14 to 18 °C and needs a
dew-point margin of about 1 to 2 K (REHVA Guidebook No. 7, Babiak et al. 2007). Indoor design
conditions for comfort are in EN 16798-1 (operative temperature about 23 to 26 °C in summer
for category II) and ASHRAE 55.

**Dew point.** Magnus formula (Alduchov and Eskridge 1996):
`γ = ln(RH) + 17.625·T/(243.04 + T)`, `T_dew = 243.04·γ/(17.625 − γ)`, T in °C.

**Example (invented).** Room 24 °C at 50 % RH: `γ = −0.693 + 1.584 = 0.891`,
`T_dew = 243.04 × 0.891 / 16.734 = 12.9 °C`. With a margin of 2 K the chilled water must stay
at or above 14.9 °C to take no latent load. This is a check on the source's numbers; gemini
computes it itself from the case (`gemini.physics.psychrometrics`), so store the three inputs,
never the dew point (§8.5).

**Mistakes.** Asking the user for `dew_point_margin` on a case with no cooling; writing the
indoor humidity in % without `"unit": "%"`; confusing the site's outside humidity
(`site.air.relative_humidity`) with the room's.

## 15.3 Produced gas: composition, heating value, bubble point

**What.** `site.fluid.gas_liquid_ratio` (GLR, `Nm3/m3`) and `site.fluid.dissolved_gas` (mole
fractions per species) describe the gas that leaves the brine at surface pressure.

**Typical ranges.** Sedimentary-basin brines often carry CO₂ and CH₄ with some N₂; H₂S occurs
in some basins (Huenges 2010, ch. 5; Stober and Bucher 2021, ch. 7). GLR varies by orders of
magnitude between basins, so only a fluid analysis of the site or its basin is a source.

**Heating value.** Only combustible species (CH₄, C₂H₆, H₂S, H₂) add heat; CO₂ and N₂ are inert.
ISO 6976:2016 gives the values; methane's LHV is about 50.0 MJ/kg (35.8 MJ/Nm³), HHV about
55.5 MJ/kg. gemini computes the mixture's value (`gemini.physics.gas.lower_heating_value`,
`combustion_co2`): store the composition, never a computed heating value.

**Bubble point.** Gas stays dissolved while the pressure stays above the bubble point
(Henry's law). Below it, gas comes out in the well or the plant; operators often keep surface
pressure above it to avoid degassing and scaling (Huenges 2010). A bubble point the fluid
report gives is a value for checking or a rule (§6.10), not a case key unless gemini lists one
(`describe_case`).

**Example (invented).** Report: GLR 1.1 Nm³/m³; gas 80 mol% CO₂, 15 mol% CH₄, 5 mol% N₂.
Check: sums to 100 %. Case: both keys as printed. No H₂S given: leave it out; do not ask for a
species the report does not name (§8.6). A search for "nitrogen fraction" across Knowledge
finds no site value: say so in the confirmation question.

## 15.4 Sand and solids in produced brine

**What.** `site.fluid.sand_concentration` (`mg/l` or `kg/m3`) is the mass of solids per volume
of produced brine; it feeds erosion and filtration in gemini (`gemini.physics.erosion`,
`separation`).

**Typical ranges.** Well-completed geothermal wells produce low solids; a sand screen or gravel
pack keeps it down; higher values point to a completion problem. Erosion limits for pipe flow
are set from the solids load and velocity (API RP 14E, 1991; DNV RP O501, 2015).

**Mistakes.** Writing `mg/l` as `kg/m3` (factor 1 000); taking a filter's rating (µm) for a
concentration; filling the key with a guess when the case's modules do not need it: leave it
unset unless a source gives it (§8.6).

## 15.5 Grid connection limits

**What.** `utilities.electricity.import_limit` and `export_limit` [power] are the largest power
the grid connection can take in or give out. They are the grid operator's contract or the
connection's rating, not the plant's choice.

**How to choose.** Only a source sets them: the connection agreement, the operator's offer, or
the brief. Without one, leave both unset: gemini then puts no limit on the exchange
(`gemini.physics.energy.net_exchange`). Never take a transformer size or a typical connection
class as a limit. When a brief says "the grid can supply at most X", that is the import limit;
"no export allowed" is an export limit of zero only if gemini accepts zero (`describe_case`
states the bound), else a requirement on the exported power (§6.10).

**Check.** The plant's peak electricity (heat pumps, pumps, chillers) must stay under the import
limit; the design team checks it, the case lead only records the limit.

**Example (invented).** The operator's offer: 4 MW firm import, export not permitted. Case:
`import_limit = 4 MW` (source: the offer, page). Export: `export_limit = 0 MW` when
`describe_case` shows the bound admits zero (gemini 0.6.34: `min=0`); otherwise a requirement
"exported electricity = 0" proposed in the confirmation question.

## 15.6 Initial state of stores

**What.** `initial_state` gives the starting state of each stateful module, as
`{module path: {state: {value, unit}}}`. In gemini 0.6.34 the stateful modules are the stores
(`gemini/modules/storage/`): a tank (`temperature`), an ice store (`ice_fraction`,
`temperature`) and an aquifer store (`warm_volume`, `cold_volume`, their temperature changes,
`charged_heat`, `recovered_heat`). There is no default.

**How to choose.** A plant without a store needs no `initial_state`: leave it out and never ask
for it. A plant with a store needs one per state. The start state is a modelling choice of the
design team, not a site value: a new store starts empty or at the surrounding temperature
(a cold start); a long simulation should start from the state the store reaches after a year of
operation (a periodic start), which the design team finds by running one year and taking its
end state. Record which one was used.

**Mistakes.** Asking the user for the initial state before the plant is known; giving a store's
state when the plant has no store; leaving it unset on a plant with a store (there is no default; gemini reports it
missing).

**Example (invented).** The design team adds a 2 000 m³ hot-water tank. The case gets
`initial_state: {"plant.storage.tank": {"temperature": {"value": 60, "unit": "degC"}}}`, the
supply temperature at start, named as the design team's choice, not the user's.

## 15.7 Brine salinity, net-to-gross and transmissivity

**Salinity.** Total dissolved solids (TDS), mostly NaCl, in g/l or mg/kg. It is not a gemini
case key; it is the reason a brine's density, viscosity and heat capacity differ from water's
(§13.6). Use it to check the fluid values a report gives: a TDS of a few tens of g/l raises
density a few percent above water's at the same temperature (Batzle and Wang 1992).

**Net-to-gross (N/G).** The share of the gross reservoir thickness that is permeable sand.
`net thickness = N/G × gross thickness`. A source that gives a permeability for the net sand
must be paired with the net thickness; for the gross, with the gross (§13.4). Mixing them is
the most common transmissivity error.

**Transmissivity.** `kh` in D·m or mD·m. Some reports give only kh: then record kh's source and
split it into the permeability and thickness the same report gives; never invent one of the
two to recover the other.

**Example (invented).** Gross 90 m, N/G 0.6, net-sand permeability 350 mD: net 54 m,
`kh = 18.9 D·m`. Case: thickness 54 m, permeability 350 mD, both cited, with "net" in the source
note.

# 16. Checking a data file step by step

A procedure for any time-series file (demand, weather, prices), with the statistics behind each
step. It extends the table of §3.3. Every finding is a flaw to report (§1.4), never a fix.

## 16.1 Procedure

1. **Shape.** Columns, header, delimiter, decimal mark (`,` vs `.`), units in the header or a
   separate row. A decimal comma read as a thousands separator turns 4,2 MW into 42 MW.
2. **Time axis.** First and last stamp, step, count. Expected count = span / step: 365 or 366
   daily rows a year, 8 760 or 8 784 hourly; an hourly local-time year has 8 759 or 8 761 rows
   in the spring and autumn DST weeks unless it is in UTC or has offsets (§3.2).
3. **Gaps and duplicates.** Every expected stamp once. A repeated hour in autumn is DST, not
   an error, when the file is local time without offsets: name the zone (§3.2).
4. **Values.** Finite, non-negative for a demand; no text in a number column; no sentinel
   values (`-999`, `9999`, `0` in a column that is never zero).
5. **Units and totals.** Sum the energy (`Σ P·Δt`, §13.1) and compare it with the brief's
   values for checking (§1.3). A factor of 24, 1 000 or 3.6 points to a unit slip
   (MWh/d vs MW, kW vs MW, GJ vs MWh; Appendix A).
6. **Pattern.** Season, weekday and holiday pattern as the stated use implies (§13.1, §13.2).
7. **Outliers.** §16.2.
8. **Report.** One line per flaw: what, where (rows), how large, and what the user must decide.

Use `read_profile` and `list_profiles` to look at a saved series; never paste a whole series
into the context (§14.1).

## 16.2 Outliers and suspicious values

**Lesson.** A value far from its neighbours is either a real event (a cold snap, a plant trip)
or a data error. Tukey's fences (Tukey 1977) flag values outside
`[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`, with `IQR = Q3 − Q1`, as candidates; on a seasonal series apply
them to the deviation from a smooth seasonal curve, not to the raw values, else every winter
day is an "outlier" (Hyndman and Athanasopoulos 2021, ch. 3 and 13). A run of identical values
(a flat line) usually means a frozen meter or a gap filled by copying.

**Rule.** Flag, describe and ask; never remove, smooth or replace a value yourself (§8.5). When
the user asks for a repair, use `repair_series` on the named steps only (§14.1).

**Example (invented).** A daily heating series has a typical January value of 9 to 11 MW and one
day of 0.0 MW between two 10 MW days, and one of 104 MW. The 104 MW day is ten times its
neighbours: a likely decimal or unit slip. The 0.0 MW day in mid-winter is a likely gap. Both go
into the one question: "rows 15 and 22: 104 MW and 0.0 MW against neighbours of about 10 MW;
please confirm or give the right values".

## 16.3 Weather and price series

- **Weather.** Air temperature by hour has a daily cycle; a daily file gives the daily mean.
  Check the span and the zone; a reanalysis or typical-year file is named as such (§13.8).
  Physical bounds (ISO 2533, local records) catch unit slips: °F written as °C, K as °C.
- **Prices and emission factors as series.** Check the unit and its reference year; a series
  with a step finer than the demand is accepted when gemini resamples it (`describe_case`), else
  it is a flaw to name. The economics side is in `knowledge/handbook-economics.md`.
- **Consistency between files.** Demand and weather of the same site must cover the same span
  in the same zone; a one-day shift between them is a time-zone error (§3.2).

# 17. Requirements documents, limits, units and time in depth

Deeper lessons for the four places a case goes wrong most: reading a requirements document,
turning limits into requirements, deciding what to ask, and units and time. Every example is an
invented text with invented numbers.

## 17.1 Reading a requirements document

**Modal verbs.** Requirements writing (ISO/IEC/IEEE 29148:2018; RFC 2119 for the keywords) gives
each verb a strength: **shall / must** = a binding requirement; **should** = a recommendation
(not checked as pass or fail; a design preference to report); **may** = a permission (a design
freedom, §7.2); **will** = a statement of fact or intent (often a case value). "Is expected to",
"typically", "about" mark an estimate, not a bound.

**Per sentence, record.** The text (quoted), page, the kind (§1.2: case value, rule, freedom,
reading instruction, value for checking), the quantity and its owner (which unit or service),
the bound and its unit, and the condition ("while operating", "on average over the year").
This is a traceability matrix: every requirement in the case points back to one sentence, and
every binding sentence ends in a requirement, a case value, or a named rule gemini cannot
express (§6.10). Nothing binding is lost; nothing is added that no sentence states.

**Watch for.** Two sentences on one quantity (merge into one requirement, §6.12); a number in a
table caption or footnote that changes a bound; "per well" vs "in total"; "net" vs "gross"
(power, thickness); "at the wellhead" vs "at the pump intake"; a unit only in a column header.

**Example (invented).** "The operator *shall* keep the production flow of each well between
40 and 220 m³/h. Wells *should* run at least 300 days a year. The client *will* supply return
water at about 45 °C. Additional wells *may* be drilled." Kinds: a rule (one flow-range
requirement per §6.9); a recommendation (report it; no requirement unless the user makes it
binding); a case value (`return_temperature`, with "about" in the source note); a freedom (the
doublet count, bounded only if a sentence bounds it).

## 17.2 From a limit to a requirement: the four questions

For each binding limit, answer four questions; each answer is one key of the requirement (§6.3).

| Question | Key | Typical answer in text |
|---|---|---|
| Whose quantity? | `on` + `quantity` | "each well's flow" -> `doublet` / `production_flow` |
| Judged how over the run? | `over` | "at any time" -> `each`; "per year" total -> `sum`; "on average" -> `mean`; "peak" -> `max`; "days of" -> `duration` |
| On which steps? | `when` | "while operating" -> `running`; "at all times, also idle" -> `always` |
| Which bound? | `min`, `max`, `unit` | "at most" -> `max`; "at least" -> `min`; "between" -> both; "equal to" -> both equal, with a tolerance (§17.3) |

**Worked examples (invented).**
- "No well may produce more than 180 m³/h at any time": doublet, production_flow, each,
  running, max 180 m3/h.
- "Electricity bought shall not exceed 25 GWh per year" over a one-year case: plant,
  electricity_bought, `over: mean`, no `when`, max `25 GWh / 8 760 h = 2.854 MW`. Not
  `over: sum`: in gemini `sum` of a power adds the step values, not an energy
  (`gemini/plants/roles.py`); the mean of a power over every step of equal length is the
  energy over the period. Show the arithmetic in the one question so the user approves the
  bound in gemini's form, next to the text it restates.
- "The heat pump's COP shall average at least 3.2": heat_pump, cop, mean, running, min 3.2.
- "Brine shall be cooled by no more than 50 K": doublet, brine_cooling, each, running, max 50 K.
- "Between one and four doublets": doublet, count, min 1, max 4 (property: no over, no when).
- "Emissions of 400 t at most" with no period named: ask whether per year or over the analysis
  period; never guess the period.

**Not a requirement.** A limit on something gemini has no quantity for (noise, land use, a
permit date) is a rule gemini cannot express (§6.10). A target ("aim for", "ideally") is a
design preference for the handover.

## 17.3 Tolerances in depth

**Why.** A simulation is a numerical solution: a balance closes to a solver tolerance, not to
zero. A measurement-based acceptance test always allows for uncertainty: JCGM 106:2012 treats
conformity with a limit as a decision with a stated risk, and sets an acceptance band (guard
band) on purpose. An "exact" rule without a band fails a correct design on noise.

**How to set one.** (1) Use a tolerance a source gives (the requirements document, a standard,
the assumptions document). (2) Else propose one in the one question, as an assumption with its
reason, from the size of the quantity and the solver's noise, and name its effect. (3) Use one
source for all tolerances of a case (§6.12). Never tighten or loosen a tolerance after seeing a
result: that is fitting the rule to the design.

| Text | Band | Note |
|---|---|---|
| "equal to X" | `min = X − t`, `max = X + t` | t from a source, or proposed |
| "all demand met" | `unmet_share` `max = t` | t a small share of the period's energy |
| "100 % reinjection" | `reinjection_ratio` in `[1 − t, 1 + t]` | t relative, small |
| "at least X" | `min = X` | no band needed: a one-sided limit |

**Example (invented).** "All produced brine is reinjected." No tolerance in the text. Proposal:
`reinjection_ratio` in [0.9999, 1.0001] ("relative 1×10⁻⁴, numerical noise only; a real
loss of brine would be far larger"), for the user to approve.

## 17.4 Ask the user or take from Knowledge

| The value is ... | Source | Approval |
|---|---|---|
| stated in the user's files or messages | the file, page or message | none: set as given (§8.1) |
| in the case's assumptions document | that document, its section | in the one question |
| in another Knowledge file (catalogue, handbook data) | that file, row or section | in the one question |
| from a connector or the web | server or URL, with date | in the one question |
| a choice of the team (tolerance, zone, start state) | `source: agent`, with reason | in the one question |
| in no source | none | asked in the one question as "unknown" |

**Rules.** Knowledge and connectors are searched BEFORE the question so it offers candidates,
not blanks (§0.1 step 5). A site value never comes from a generic default. When the user has
waived approval (auto-approve, "best guesses"), the same order applies and nothing is asked
(§14.3). A value the user gave beats every other source, even a "better" one; name the
conflict in the handover instead of overriding it.

**Example (invented).** Open: air temperature, a grid CO₂ factor, a reinjection tolerance.
Search finds an hourly air series from a weather connector, and a national grid factor in a
catalogue row (2024, location-based). Question: three numbered items, each with value, unit,
source and date; the tolerance marked as the agent's proposal.

## 17.5 Units in depth

**Method.** Dimensional analysis (NIST SP 811, 2008; BIPM SI Brochure, 9th ed., 2019): every
value has a number and a unit; a sum needs one dimension; a conversion is a factor of one
(`1 h / 3 600 s`). Write the unit the source prints and let gemini convert (`describe_case`
names the accepted units); the agent never converts a case value (§8.5).

**Power, energy and their mix-ups.**

| Printed | Is | Factor to check |
|---|---|---|
| MW in a daily file | mean power of the day | energy of the day = MW × 24 h |
| MWh per day | energy per day | mean power = MWh/d ÷ 24 h |
| GJ | energy | 1 GJ = 0.2778 MWh |
| kW vs MW | power | factor 1 000 |
| toe, Btu, therm | energy | 1 toe = 11.63 MWh; 1 therm = 29.31 kWh (IEA, NIST) |

**Pressure.** Gauge vs absolute (`barg` vs `bar`, `psig` vs `psia`); 1 bar = 10⁵ Pa;
1 psi = 6 894.76 Pa; a head in metres of water is a pressure only with a density
(`p = ρ g h`).

**Temperature.** A temperature (°C, K) and a temperature difference (K) are different
quantities: 10 °C is 283.15 K, a difference of 10 °C is 10 K. °F to °C: `(F − 32) × 5/9`; a
difference: `× 5/9`.

**Flow.** m³/h vs m³/s (factor 3 600); L/s; volume vs mass flow (`ṁ = ρ Q`); a flow in
`Sm³`/`Nm³` is a gas volume at reference conditions (§13.6).

**Example (invented).** A table titled "Heat demand [MWh]" with daily rows: 96, 120, 84. These
are energies per day, mean power 4.0, 5.0 and 3.5 MW. Give the file with unit `MWh` per day only
if `describe_case` accepts an energy per step; otherwise name it as a flaw and ask the user to
confirm the reading; never divide by 24 yourself.

## 17.6 Time in depth

**Standards.** ISO 8601 for timestamps (`2030-01-01T00:00:00+01:00`); the IANA time zone
database for zone names (`Europe/Oslo`, never `CET` or `+01:00` for a zone with daylight
saving time); UTC for the clock without seasons.

**What a stamp marks.** A row's time is the start of its interval (interval-beginning) or its
end (interval-ending, common in meter and market data: "00:00-01:00" stamped 01:00). A one-step
shift moves a whole day of demand at a daily step. Read the file's description or the headers
("period ending", "hour ending", `HE`); if nothing says, it is an open reading instruction for
the one question.

**Daylight saving.** A local-time hourly file has one 23-hour day in spring and one 25-hour day
in autumn: one hour missing and one repeated. With offsets on every stamp, nothing is
ambiguous; without, the zone is needed (§3.2). Daily files with a zone are matched by local
date (§3.2).

**Leap years.** A calendar year has 366 days when the year is divisible by 4, except century
years not divisible by 400. A 365-row file for a leap year misses a day.

**Example (invented).** An hourly file stamped `01:00 ... 24:00` local, with no offsets, for a
site in a zone with daylight saving. Readings: interval-ending ("24:00" is the end of the
day), local time. Ask once: "the file's hours look interval-ending in local time
(Europe/<city>); confirm, or give the convention". The zone name comes from the site's
location, as the agent's choice with its reason (§3.2).

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
- Tukey, J.W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
- WRI and WBCSD (2015). *GHG Protocol Scope 2 Guidance*.
- ISO 2533:1975 *Standard Atmosphere*; DIN 1343 *Normal conditions*; ISO 13443:1996 *Natural gas
  standard reference conditions*.
- Alduchov, O.A. and Eskridge, R.E. (1996). Improved Magnus form approximation of saturation
  vapor pressure. *Journal of Applied Meteorology* 35(4), 601-609.
- API RP 14E (1991). *Design and installation of offshore production platform piping systems*.
- ASHRAE (2013). *District Cooling Guide*. ASHRAE 55: *Thermal environmental conditions for
  human occupancy*.
- Babiak, J., Olesen, B.W. and Petras, D. (2007). *Low temperature heating and high temperature
  cooling*. REHVA Guidebook No. 7.
- BIPM (2019). *The International System of Units (SI)*, 9th ed.
- Batzle, M. and Wang, Z. (1992). Seismic properties of pore fluids. *Geophysics* 57(11),
  1396-1408.
- CIBSE (2006). *TM41 Degree-days: theory and application*. CIBSE, London.
- DNV RP O501 (2015). *Managing sand production and erosion*.
- Dake, L.P. (1978). *Fundamentals of Reservoir Engineering*. Elsevier.
- IANA. *Time Zone Database* (tz). ISO 8601-1:2019. *Date and time: representations*.
- EN 12831-1:2017. *Energy performance of buildings: method for calculation of the design heat
  load*. EN ISO 15927-6:2007. *Hygrothermal performance of buildings: accumulated temperature
  differences (degree-days)*.
- EN 16798-1:2019. *Energy performance of buildings: indoor environmental input parameters*.
- Gringarten, A.C. and Sauty, J.P. (1975). A theoretical study of heat extraction from aquifers
  with uniform regional flow. *Journal of Geophysical Research* 80(35), 4956-4962.
- Hyndman, R.J. and Athanasopoulos, G. (2021). *Forecasting: Principles and Practice*, 3rd ed.
  OTexts.
- ISO 6976:2016. *Natural gas: calculation of calorific values, density, relative density and
  Wobbe indices from composition*.
- JCGM 106:2012. *Evaluation of measurement data: the role of measurement uncertainty in
  conformity assessment*.
- Kestin, J., Khalifa, H.E. and Correia, R.J. (1981). Tables of the dynamic and kinematic
  viscosity of aqueous NaCl solutions. *J. Phys. Chem. Ref. Data* 10(1), 71-87.
- Lund, H. et al. (2014). 4th Generation District Heating (4GDH). *Energy* 68, 1-11.
- NIST SP 811 (2008). *Guide for the Use of the International System of Units*.
- RFC 2119 (1997). *Key words for use in RFCs to indicate requirement levels*.
- Ramey, H.J. (1962). Wellbore heat transmission. *Journal of Petroleum Technology* 14(4),
  427-435.
- gemini physics: `gemini/gemini/physics/ground.py` (geotherm, Gringarten-Sauty doublet, Ramey),
  `hydraulics.py` (hydrostatic, productivity and injectivity indices), `energy.py`, `fluid.py`
  (constant property snapshots), `gas.py`.
- gemini 0.6.34: `gemini/gemini/case/`, `gemini/gemini/plants/roles.py`,
  `gemini/gemini/units/inputs.py`.
- geomind: prompts `case/lead.md`, `case/geoscientist.md`; skills `setting-the-case`,
  `finding-sources`, `connectors`, `gemini-units`, `calculator`.
