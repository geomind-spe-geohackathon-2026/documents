# Defining an Energy-Supply Case: A Handbook for Geothermal Heating and Cooling

How to turn a client's brief and data files into a complete, sourced and checkable case for the
design of a geothermal heating and cooling plant.

Cite as `knowledge/handbook-case.md`, with the section number (for example
`knowledge/handbook-case.md §6.4`).

---

## Preface

### Who this handbook is for

For the case lead and the geoscientist of a design team, and for anyone who reviews a case: the
person (or agent) who reads what a client, an organiser or a utility hands over and writes down,
before any design starts, what the plant must serve, where it stands, what it may buy, which
rules it must keep and what is still uncertain.

### What it covers and what it does not

It covers the engineering judgement of case definition: how to read a brief, check a demand
profile, describe a site and a reservoir, choose emission factors, phrase requirements, tell a
case value from a design freedom, source every assumption and state the uncertainty. It ends
with how a case looks in gemini, checklists and a worked example.

It does not explain any agent tool. How to call `set_case`, `read_case`, `describe_case`,
`save_profile`, `list_profiles`, `read_profile`, `accept_case`, `case_changes` and
`ask_economics` is written in exactly one place, the skill `setting-the-case`
(`read_skill('setting-the-case')`); how to find a value in files and the knowledge base is the
skill `finding-sources`; values from a connected server are the skill `connectors`. Where this
handbook says "set" or "read", the skill says how. The economics of a case (prices, discounting,
levelised costs, carbon accounting) are the subject of `knowledge/handbook-economics.md`;
the design of the plant is `knowledge/handbook-design.md`; the report is
`knowledge/handbook-report.md`.

### How to read it

Every numbered section stands on its own: read only the section you need. Sections cross-refer
by number (§n.m). Chapter 0 is the case lead's split plan; chapter 12 is a worked example;
chapter 11 holds the checklists.

### Conventions

- **Sources.** Every number and rule carries its source in brackets or in the table beside it.
  A value marked **(derived)** follows from other values by the formula given; it is shown to
  explain, never to be typed into a case (gemini derives it).
- **Units.** SI and the units the source prints; gemini's unit names in `code` (`degC`, `K/km`,
  `kg/m3`, `mPa.s`, `barg`).
- **Names.** gemini's paths and names in `code` are the ones of gemini's case format
  (`gemini/gemini/case/`), checked against the source; nothing here invents a key.
- **Rule words.** "Must" states a rule of the team (`.claude/memory/` and the agent prompts);
  "should" states good practice from the references in Appendix C.

---

## Table of contents

0. Case checklist for the case lead
   0.1 How the lead uses it
   0.2 Group 1: site and subsurface
   0.3 Group 2: demand series
   0.4 Group 3: brine and gas
   0.5 Group 4: economics and requirements
   0.6 Freedoms the case never holds
1. What a case is
   1.1 The case and the plant
   1.2 Why the case comes first
   1.3 The four kinds of statement in a brief
   1.4 The reference textbooks in brief
2. Reading the brief and the files
   2.1 Inventory of the inputs
   2.2 Reading a brief: every table, every note
   2.3 Classifying each statement
   2.4 Values for checking only
   2.5 Conflicts and flaws
3. Demand profiles
   3.1 Power, energy and their units
   3.2 Resolution: hourly, daily, monthly
   3.3 The time axis
   3.4 Checks on a demand series
   3.5 Heating demand
   3.6 Cooling demand
   3.7 Supply and return temperatures
   3.8 A demand without a file
4. Site and subsurface data
   4.1 Ground: surface temperature and gradient
   4.2 Reservoir: depth, thickness, permeability, pressure
   4.3 Reservoir temperature: measured or derived
   4.4 The brine
   4.5 Dissolved gas
   4.6 Outside air
   4.7 Data quality and ranges
5. Utilities and emission factors
   5.1 Electricity grid
   5.2 Grid electricity CO2 intensity
   5.3 Bought gas
   5.4 What belongs to the economics instead
6. Requirements
   6.1 What a requirement is
   6.2 Qualities of a good requirement
   6.3 Anatomy of a requirement in gemini
   6.4 Roles and quantities
   6.5 Reading the run: `over`
   6.6 Which steps count: `when`
   6.7 Limits, ranges and exact values
   6.8 Tolerances
   6.9 Translating brief text into rules
   6.10 Rules gemini cannot express
   6.11 Common mistakes
7. Case values and design freedoms
   7.1 The test
   7.2 Typical freedoms
   7.3 Return temperatures
   7.4 A case change from the design team
8. Assumptions and their sources
   8.1 Order of sources
   8.2 What a citation holds
   8.3 Assumptions documents
   8.4 Agent assumptions
   8.5 The one confirmation question
   8.6 No computed values
9. Uncertainty
   9.1 Kinds of uncertainty
   9.2 Ranges and distributions
   9.3 Choosing a range from sources
   9.4 Uncertainty in the case
10. The case in gemini
   10.1 Sections
   10.2 Key tree
   10.3 Series and files
   10.4 Units and conversions
   10.5 Derived keys
   10.6 Validation and missing values
   10.7 The case the user gave and later changes
11. Checklists
   11.1 Before the confirmation question
   11.2 Before handing the case over
   11.3 Reviewing someone else's case
12. Worked example: the GEMINI hackathon 2026
   12.1 The inputs
   12.2 Values for checking
   12.3 Where each value goes
   12.4 Values from the assumptions document
   12.5 The requirements
   12.6 Design freedoms of this case
   12.7 Economics
   12.8 Checklist of this case

Appendix A. Glossary
Appendix B. Unit pitfalls
Appendix C. References

---

# 0. Case checklist for the case lead

The lead's split plan, readable on its own: every field gemini's case takes, in four field
groups, one per geoscientist (at most four, `knowledge/handbook-case.md` is cited by section).
Field names, units and keys are those of `gemini/gemini/case/` (`site.py`, `demand.py`,
`utilities.py`, `economics.py`, `time.py`, `requirement.py`); nothing here is a value.

## 0.1 How the lead uses it

1. Read the inputs once (§2.1) and classify every statement (§2.3); write each case field of
   the four tables below against the passage that holds it, or "none".
2. Give each geoscientist its group, the passages and the handbook sections of its table. A
   geoscientist reads Knowledge only and returns, per field: value, unit as the source prints it,
   source (file and page, Knowledge document and section, connector and origin), quality and range
   (§4.7, §9), and the flaws it saw (§2.5). It never computes a value (§8.6).
3. The lead merges the four answers, writes the case once, lists every value that did not come
   from the user's files in the one confirmation question (§8.5), then asks economics once.
4. Where the table says **user question**, the value is asked for by its path and unit with no
   number of the agent (§8.1, step 5), once, with every other gap and flaw.

Source order for every field: user request and answers, project files, Knowledge, connector, then
the question (§8.1). A field no source gives stays unset and is listed as open; the case holds no
default (`.claude/memory/feedback-no-defaults.md`).

Source key: **File** = a user input file; **Know** = a Knowledge document (assumptions document
first, §8.3); **Conn** = a connector (MCP); **Ask** = the one user question.

## 0.2 Group 1: site and subsurface (geoscientist I)

| Field | Comes from | Unit (gemini) | The check | Section |
|---|---|---|---|---|
| `site.ground.surface_temperature` | File (brief), Know, Conn, Ask | `degC` | a site value, not a regional average | §4.1 |
| `site.ground.gradient` | File (well data, brief), Know, Ask | `degC/km` or `K/km` (equal) | a site value; never the reservoir temperature derived by hand | §4.1, §4.3 |
| `site.reservoir.reference_depth` | File (brief, well report), Ask | `m` | TVD not MD; the depth the pressure and temperature belong to; not the design depth, which is a freedom | §4.2, §7 |
| `site.reservoir.thickness` | File (reservoir report), Know | `m` | gross or net named by the source | §4.2 |
| `site.reservoir.permeability` | File (reservoir report), Know | `mD` (gemini converts) | unit is mD not D; range kept as uncertainty | §4.2, §4.7 |
| `site.reservoir.pressure` | File, Know | `barg` or `bar`, as printed | gauge or absolute named by the source | §4.2, App. B |
| `site.reservoir.temperature` | File, only if measured | `degC` | never derived by hand: unset without a measurement | §4.3, §10.5 |
| `site.air.temperature` | File (series), Conn (weather), Know | `degC` | constant or series said; constant is a simplification | §4.6 |
| `site.air.relative_humidity` | File, Conn, Know | fraction 0 to 1, or `%` as printed | within 0 to 1 after conversion | §4.6 |
| `site.air.pressure` | File, or elevation | `Pa`, `bar` | with only an elevation, `set_case` applies the standard atmosphere: no value of the agent | §4.6 |
| `initial_state` of stateful modules | Ask (plant lead names the modules) | per module | no default state: asked, or left to the plant stage | §10.1 |
| Data quality of each value above | File, Know | text | measured on site, nearby, regional or assumed, recorded with the value | §4.7 |

## 0.3 Group 2: demand series (geoscientist II)

| Field | Comes from | Unit (gemini) | The check | Section |
|---|---|---|---|---|
| `time.start`, `time.end`, `time.step` | File (the demand file's span) | date and `d`, `h` | copy from the file's span; `end` excluded; time zone stated or asked | §3.3 |
| `demand.heating.power` | File (series), or Ask (values or constant) | `MW` (`MWth` is `MW`) | count, gaps, sign, unit against the brief's checking values, season, zero days, base load | §3.1, §3.4, §3.8 |
| `demand.heating.supply_temperature` | File (brief), Know, Ask | `degC` | a fixed supply is a case value; return on the colder side | §3.5, §3.7 |
| `demand.heating.return_temperature` | File, Know, or a team design choice with reason | `degC` | below the supply; a design choice is proposed with `source: agent` and its reason | §3.5, §7.3 |
| `demand.heating.minimum_return_temperature`, `maximum_return_temperature` | File (network data), Know | `degC` | only when a source states them | §3.5 |
| `demand.heating.return_pressure` | File (network data), Know | `bar`, `barg` as printed | gauge or absolute named | §3.5 |
| `demand.cooling.power` | File (series), or Ask | `MW` (`MWcool` is `MW`) | as heating; a cold power, not chiller electricity; zero days counted | §3.1, §3.4, §3.6 |
| `demand.cooling.supply_temperature` | File (brief), Know, Ask | `degC` | return on the warmer side | §3.6, §3.7 |
| `demand.cooling.return_temperature`, minimum, maximum, `return_pressure` | as heating | `degC`, pressure unit | return above the supply | §3.6 |
| `demand.cooling.indoor_temperature`, `indoor_relative_humidity`, `dew_point_margin` | File (building data, brief), Know | `degC`, fraction or `%`, `K` | humidity within 0 to 1; sensible against latent load named | §3.6 |

Flaws this group reports at once: a series span that differs from the brief, a unit error, a
return on the wrong side of its supply, a peak in the wrong season (§2.4, §2.5).

## 0.4 Group 3: brine and gas (geoscientist III)

| Field | Comes from | Unit (gemini) | The check | Section |
|---|---|---|---|---|
| `site.fluid.density` | File (fluid analysis, brief), Know | `kg/m3` | stated temperature and salinity noted | §4.4 |
| `site.fluid.viscosity` | File, Know | `mPa.s` | stated temperature noted | §4.4 |
| `site.fluid.gas_liquid_ratio` | File, Know | `Nm3/m3` | normal or standard conditions named by the source | §4.5, App. B |
| `site.fluid.dissolved_gas` (species) | File, Know | mole fractions or `mol%` | adds up to one as the source writes it; the produced gas, never the grid gas | §4.5 |
| `site.fluid.sand_concentration` | File (fluid analysis), Know | `mg/l` | unit as printed | §4.4 |
| `utilities.gas.composition` (species) | Know (supplier, assumptions document), Conn, Ask | mole fractions or `mol%` | adds up to one; never the dissolved gas | §5.3 |
| `utilities.gas.heating_value` | Know, Conn, Ask | per mass, unit as printed | lower or higher heating value named by the source | §5.3 |

## 0.5 Group 4: economics and requirements (geoscientist IV)

| Field | Comes from | Unit (gemini) | The check | Section |
|---|---|---|---|---|
| `utilities.electricity.co2_intensity` | File (brief), Know, Conn | `g/kWh` as printed | location or market basis named; constant is a simplification | §5.1, §5.2 |
| `utilities.electricity.import_limit`, `export_limit` | File (grid operator) | `MW` | only when a source states them; else unset | §5.1 |
| `requirements` (`name`, `on`, `quantity`, `unit`, `over`, `when`, `min`, `max`) | File (brief: every "shall", "must", "at most", "between") | the quantity's unit | one rule per requirement; a range is one; durations as durations; fractions without unit; `when: running` for supply temperatures | §6.3 to §6.11 |
| Tolerances (demand met, exact ratios) | Know, Ask (an assumption, confirmed) | fraction | named as assumptions with a reason | §6.8 |
| Rules gemini cannot express | File | text | kept in the case's `about`, named as open | §6.10 |
| `economics.currency`, `price_year`, `discount_rate`, `analysis_period` | Know (assumptions document, catalogue), Conn, Ask | currency, year, fraction, `a` | one source per key; converted values name the conversion | §5.4; economics handbook |
| `economics.capex.*`, `opex.*` (`chemical`, `waste_disposal`, `fixed`, `per_energy`) | Know (`knowledge/data-economics.md`), Ask | money per basis, as the key's unit | each equipment kind a price from a source, else `open` | §5.4; economics handbook |
| `economics.energy.*` (electricity, gas prices) | Know, Conn, File (tariff) | money per energy | price year stated | economics handbook |
| `economics.carbon.price`, `accounting.gwp`, `accounting.allocation.heat_cost_share` | Know, Ask | money per mass, none, fraction | the GWP set named; allocation asked only when heat and cold are both delivered | economics handbook |
| `economics.revenue.heat`, `cold`, `subsidy.*` | File, Know | money per energy | no subsidy unless a source states one | economics handbook |

The economics questions follow the case question and are one question (§8.5).

## 0.6 Freedoms the case never holds

Well depth, number of doublets, flows, set points, units and their sizes, backup policy, gas
handling (§7.2). A bound the brief puts on one is a requirement (group 4); the choice is the
design's. A return temperature no file gives is the one team choice that sits in the case (§7.3).

---

# 1. What a case is

## 1.1 The case and the plant

A design problem in gemini is a pair: a **plant** (what the team designs and may change) and a
**case** (the outside conditions over one period and the rules of third parties, which the
team does not change). gemini's own definition: the case holds "the outside conditions over one
period and the rules of third parties" in the sections `time`, `initial_state`, `site`,
`demand`, `utilities`, `economics` and `requirements`
(`gemini/gemini/case/case.py`, class `Case`).

| Belongs to the case | Belongs to the plant |
|---|---|
| The demand of each service over time and its supply conditions | The units, their sizes and connections |
| The ground, reservoir, brine and air of the site | The well depth, the number of doublets, their flows |
| The grids the plant buys from, their CO2 intensity | The backup policy, the controls |
| Prices, discount rate and accounting rules (economics) | The choice of heat pump, chiller, boiler, CHP |
| Rules a third party sets on the outcome (requirements) | How the rules are met |

## 1.2 Why the case comes first

A design is verified only against a case: gemini judges a result against the case's
requirements (`check_results`, skill `reading-results`). A wrong case gives a design that
passes every check and still fails the client. A missing value hidden by a guess is worse than
a missing value: gemini holds no default values (team rule, `.claude/memory/feedback-no-defaults.md`),
so a missing value is an error that names its path, and a guessed one is an error nobody sees.

## 1.3 The four kinds of statement in a brief

Every sentence of a brief is one of four kinds (team practice, from the case lead's rules in
`geomind/geomind/prompts/case/lead.md`):

1. **A case value**: a fixed input (a reservoir pressure, a supply temperature, a demand file).
2. **A rule**: a limit a third party sets on the outcome (a flow range, a cooling limit, a
   number of operating days). It becomes a requirement (chapter 6).
3. **A design freedom**: something the team may choose (a depth "may change", "1 to 3
   doublets", "several options are allowed"). It is never a case value (chapter 7); a bound on
   it may be a rule.
4. **A reading instruction**: how to obtain a value ("for another depth use the hydrostatic
   pressure and the gradient"). It says what gemini derives; it is no value.

A fifth kind, **a value for checking** (a stated peak or annual total), is used to check the
data, never put into the case (§2.4).

## 1.4 The reference textbooks in brief

The engineering behind this handbook rests on a few standard texts (full entries in
Appendix C):

- **Frederiksen and Werner, *District Heating and Cooling* (2013).** The standard textbook of
  district energy. Its lessons for case definition: heat demand is driven by outdoor
  temperature and by users' habits, so demand profiles have a strong seasonal and a daily
  pattern; the peak and the annual energy size different parts of a plant (base-load units by
  the energy, peak units by the peak); low return temperatures raise the value of every heat
  source and are a design goal of the network; cooling demand follows solar and internal gains
  and has a different, summer-centred shape.
- **Huenges (ed.), *Geothermal Energy Systems* (2010), and Stober and Bucher, *Geothermal
  Energy* (2nd ed., 2021).** The geoscience of a hydrothermal doublet: reservoir temperature
  from the surface temperature and the gradient, productivity from permeability and thickness
  (the transmissivity), brine properties and dissolved gases, scaling and degassing, and the
  uncertainty of every subsurface value before drilling.
- **ISO/IEC/IEEE 29148:2018, requirements engineering.** What makes a requirement good:
  necessary, unambiguous, complete, singular, feasible, verifiable, correct, conforming and
  traceable (§6.2).
- **JCGM 100:2008 (GUM).** How to state an uncertainty: a best estimate with a range or a
  distribution, and where it came from (chapter 9).
- **GHG Protocol Scope 2 Guidance (2015).** How to choose an emission factor for bought
  electricity: location-based or market-based (§5.2).

---

# 2. Reading the brief and the files

## 2.1 Inventory of the inputs

Start with a list of every file and what it holds, before reading any value. A typical case
has:

| Input | Typical content | Typical form |
|---|---|---|
| Brief or requirements document | services, temperatures, site, rules, deliverables | PDF, Word |
| Demand data | heating and/or cooling power over time | CSV, Excel |
| Site or reservoir reports | well tests, logs, fluid analyses | PDF |
| Network data | supply/return temperatures, pressures | PDF, table |
| Prices and tariffs | electricity, gas, heat sale prices | PDF, table, web |
| Answers to questions | clarifications of the organiser or client | email, chat, Q&A forum |

Read each file once and whole: a brief's tables and every note under them; a data file's
header, first rows, last row and span. File names are case-sensitive: quote each as it is
written.

## 2.2 Reading a brief: every table, every note

A brief packs most rules into notes, footnotes and table captions. Read in this order:

1. Title, date and version (a later answer of the organiser beats an older brief).
2. The services: heating, cooling, hot water, process heat; for each, the supply temperature,
   the return temperature if given, and the demand file.
3. The site: location, ground, reservoir, fluid, gas.
4. The rules: every "shall", "must", "at most", "between", "not more than", "fixed".
5. The freedoms: every "may", "can be chosen", "allowed", "up to the team".
6. The reading instructions: every "use ... to obtain ...", "assume ... if ...".
7. The deliverables and the judging criteria: they say what the result must show
   (`knowledge/handbook-report.md` chapter 3).

Keep the page of every value: it is the source you cite.

## 2.3 Classifying each statement

For each statement, write one line: the statement as written, its kind (§1.3), the case path
or the plant item it affects, and the page. Examples of the form (the statements are invented
for illustration):

| Statement as written | Kind | Where it goes |
|---|---|---|
| "Supply temperature 90 °C (fixed)" | case value | `demand.heating.supply_temperature` |
| "Flow per well 30 to 150 m³/h" | rule | requirement on `doublet.production_flow` |
| "The depth may be optimised" | freedom | plant `depth`, not the case |
| "Use 32 °C/km below 1 km" | case value (and a reading instruction) | `site.ground.gradient` |
| "Peak demand 12 MW on 3 February" | value for checking | check of the demand file |

## 2.4 Values for checking only

Briefs often state a peak, an annual energy or a count of days. These are written for the
reader to check the data. The case takes the series from the data file, never these numbers:
if the brief's total and the file's total differ, the data are what the plant must serve, and
the difference is a flaw to report (§2.5), not a value to choose. Use them to check:

- the file's unit (a peak ten or a thousand times off is a unit error: kW for MW, MWh/d for
  MW);
- the file's span (a total short by one day is a missing row or an end date one step early);
- the date of the peak (a peak in the wrong season is a column swap or a sign error).

The annual energy of a series is a value gemini computes (`read_profile` with a summary, skill
`setting-the-case`); never add a series by hand.

## 2.5 Conflicts and flaws

A flaw is anything that cannot be right as written: a return temperature on the wrong side of
its supply, a case span that differs from its data, a count where a duration belongs, two
pages that state different values. Rules (case lead prompt, `geomind/geomind/prompts/case/lead.md`):

- never correct a flaw yourself: ask the user, naming both values as written;
- one question names every flaw at once;
- a flaw only listed in a report is a check not done;
- when sources disagree, the order of §8.1 decides which one is proposed, and the other is
  named beside it.

---

# 3. Demand profiles

## 3.1 Power, energy and their units

A demand profile gives **power** (W, kW, MW) per time step. A daily file usually gives the
**mean power of the day** (MW), sometimes the **energy of the day** (MWh/d). Both describe the
same day; they differ by the factor 24 h/d **(derived: energy of a day in MWh = mean power in MW
× 24 h)**. A file header such as `heating_demand_MWth` says MW of heat; `MWcool` or `MWc` says
MW of cold. In gemini both are `MW` (the subscript names the product, not another unit;
`setting-the-case`).

Watch for:

- **kW vs MW**: a factor 1000;
- **energy vs power**: a "daily demand" column in MWh is not a power;
- **thermal vs electric**: `MWth` and `MWe` are different products; a cooling demand is a cold
  (thermal) power, never the electricity of the chillers that serve it today;
- **final vs useful energy**: a demand derived from gas bills is the gas burnt (final energy);
  the heat delivered is that times the old boiler's efficiency. Ask which one a file holds.

## 3.2 Resolution: hourly, daily, monthly

The step decides what the case can show:

| Step | Shows | Hides |
|---|---|---|
| Hourly | the daily pattern, the true peak, storage cycles | nothing relevant for sizing |
| Daily | the season, cold spells, which days a source runs | the hourly peak (higher than the daily mean) |
| Monthly | the season | cold spells, peaks, days with zero demand |

Consequences (Frederiksen and Werner 2013, on load duration and peak load):

- a plant sized on daily means meets the daily mean; the hourly peak above it is met only by
  the network's thermal inertia, a store or a peak unit. Say so as a limitation of the case;
- a rule written per day ("330 days of operation") fits a daily step; on an hourly step it is
  the same duration in hours;
- never build a finer series from a coarser one inside the case (no tool does, and a profile
  made by an agent is an invented value): a finer profile is asked for, or the coarse one is
  used with its limitation named.

## 3.3 The time axis

gemini's `time` has `start`, `end` and `step`; `end` is excluded, so 2027-01-01 to 2028-01-01
at one day is 365 steps (`gemini/gemini/case/time.py`). Copy the three from the file's span,
never work out a date or a count.

- **Time zone.** Times without an offset are read as UTC unless the series names a
  `time_zone` (an IANA name; `gemini/gemini/units/inputs.py`). A file in local time with
  daylight saving has a 23-hour and a 25-hour day; on a daily step this rarely matters, on an
  hourly step it shifts the peak. A zone no file states is an assumption to confirm.
- **Leap years.** A year of daily data has 365 or 366 rows; check against the calendar of the
  stated year.
- **Period length.** One year is the usual design period; an economic analysis period (often
  20 to 30 years) is an economics value, not the case's `time`
  (`knowledge/handbook-economics.md`).

## 3.4 Checks on a demand series

Run these checks before the series goes into the case, and report each failure as a flaw:

1. **Count**: the number of rows equals the span divided by the step (gemini's `span` of the
   file gives start, end and step; a gap breaks the even spacing).
2. **No gaps, no duplicates**: one row per step, each time once.
3. **Finite and not negative**: gemini refuses negative or non-finite demand (`save_profile`,
   skill `setting-the-case`); a negative heating demand is usually a sign convention.
4. **Unit**: the peak and the total match the brief's checking values (§2.4).
5. **Season**: heating peaks in winter, cooling in summer (northern hemisphere); a swap shows
   here.
6. **Zero days**: a cooling series with many zero days is normal in a temperate climate; note
   how many, since a requirement "while running" behaves differently from "always" on those
   days (§6.6).
7. **Base load**: a heating series that never falls to zero has a summer base (hot water,
   losses); it decides the minimum load a geothermal doublet must run at.
8. **Plausibility**: the ratio of annual energy to peak, the full-load hours
   **(derived: hours = annual energy / peak power)**, characterises the load (Frederiksen and
   Werner 2013, on load duration). Compare it with networks of the same kind and climate from a
   cited source; a ratio far from them is worth a question, not a correction.

## 3.5 Heating demand

What a heating service needs in the case (`demand.heating`, `gemini/gemini/case/demand.py`):

| Key | Meaning | Usual source |
|---|---|---|
| `power` | the power demanded, a series or a constant | demand file |
| `supply_temperature` | the temperature the consumer asks to be supplied at | brief, network operator |
| `return_temperature` | the temperature the water returns at | network data, or a design choice (§7.3) |
| `minimum_return_temperature`, `maximum_return_temperature` | the consumer's limits on the return | network data |
| `return_pressure` | the pressure the water returns at | network data |

Engineering notes (Frederiksen and Werner 2013):

- Supply temperatures of existing networks are often fixed by the oldest buildings and by
  domestic hot water hygiene; a newer low-temperature network runs lower. A supply temperature
  "fixed" in a brief is a case value.
- The network ΔT (supply minus return) sets the flow the network needs for a given power
  **(derived: Q = ṁ c_p ΔT)**; a lower return temperature lets a geothermal heat exchanger
  take more heat from the same brine.

## 3.6 Cooling demand

A cooling service (`demand.cooling`) has the same keys as heating plus the conditions of the
cooled space: `indoor_temperature`, `indoor_relative_humidity` and `dew_point_margin`
(`gemini/gemini/case/demand.py`).

- Chilled water returns warmer than it is supplied: the cooling return is above the cooling
  supply. A case with the opposite is a flaw (§2.5).
- The dew point of the indoor air limits how cold the supply can be without condensation on
  cooled surfaces; the margin keeps the surfaces above it. These are comfort and building
  values: take them from the brief, the building data or an assumptions document, with their
  source.
- A cooling demand in the brief is usually sensible cooling (the temperature of air or water);
  latent cooling (dehumidification) is a separate load. Say which one the file holds when the
  brief says so; when it does not, name it as an open point.

## 3.7 Supply and return temperatures

- A heating return is colder than its supply; a cooling return is warmer than its supply.
- A supply temperature the brief fixes is an operating condition of the plant: a requirement
  on it holds while that supply runs, never always (§6.6).
- A return temperature no file gives is a design choice of the team within the case's limits
  (§7.3).

## 3.8 A demand without a file

A case needs no file: a demand may be a constant power, or values the user gives
(`save_profile`, skill `setting-the-case`). No tool builds a series from a peak and an annual
energy, and an agent computes none: ask for a series file, the values, or a constant power.

---

# 4. Site and subsurface data

## 4.1 Ground: surface temperature and gradient

`site.ground.surface_temperature` is the undisturbed ground temperature at the surface;
`site.ground.gradient` the rise of the undisturbed rock temperature with depth
(`gemini/gemini/case/site.py`). Together they give the rock temperature at any depth
**(derived: T(z) = T_surface + gradient × z, for a constant gradient)** (Stober and Bucher
2021, on the geothermal gradient). gemini takes `°C/km` and `K/km` (a temperature difference of
1 °C is 1 K). The average continental gradient is commonly quoted as about 30 K/km (Stober and Bucher
2021; not checked against a page); a site value comes from well data or a regional map, never
from this average.

## 4.2 Reservoir: depth, thickness, permeability, pressure

| Key | Meaning | Pitfalls |
|---|---|---|
| `reference_depth` | the depth at which the pressure and temperature are given | TVD (true vertical depth) vs MD (measured along the well): a deviated well's MD is longer; temperatures and pressures go with TVD |
| `thickness` | the thickness of the reservoir layer | gross vs net thickness (net counts only the producing sand) |
| `permeability` | the permeability of the reservoir rock | mD (millidarcy) in reports; 1 D = 9.869233×10⁻¹³ m² by the darcy's definition; gemini converts |
| `pressure` | the reservoir pressure at the reference depth | `barg` (gauge) vs `bara`/`bar` (absolute): gemini's `barg` adds one standard atmosphere (`gemini/gemini/units/conversions.py`) |

Productivity of a doublet grows with permeability × thickness, the transmissivity kh
(Huenges 2010, on reservoir engineering); both are uncertain before drilling (§4.7).

## 4.3 Reservoir temperature: measured or derived

`site.reservoir.temperature` is set only if it was measured; without it the ground gives it
(`gemini/gemini/case/site.py`, class `Reservoir`). Never set a temperature computed from the
gradient: gemini derives it, and a hand-computed value would not follow a change of the
depth. A brief's note "for another depth, use the hydrostatic pressure and the gradient" says
exactly this: it is a reading instruction, no value.

## 4.4 The brine

`site.fluid`: `density`, `viscosity`, `gas_liquid_ratio`, `dissolved_gas`,
`sand_concentration` (`gemini/gemini/case/site.py`).

- Density and viscosity depend on temperature and salinity; a report gives them at a stated
  temperature. Write the unit as printed (`kg/m³` is `kg/m3`, `mPa·s` is `mPa.s`).
- Sand (solids) concentration drives filters and waste; it is in mg/l in fluid analyses.

## 4.5 Dissolved gas

- `gas_liquid_ratio` is the volume of gas per volume of liquid at normal or standard
  conditions, typically `Nm3/m3`. "Normal" conditions are 0 °C and 101.325 kPa (DIN 1343);
  "standard" conditions in the gas industry are 15 °C and 101.325 kPa (ISO 13443). Note which
  one a report uses.
- `dissolved_gas` is the composition of the produced gas, in mole fractions (mol% is converted
  by gemini). It is the gas that comes out of the brine, never the gas bought from a grid
  (`utilities.gas.composition`, §5.3): never put one in the other.
- Methane in the produced gas matters twice: as a fuel the plant may burn (boiler, CHP, flare)
  and as a strong greenhouse gas if vented (`knowledge/handbook-economics.md`, carbon
  accounting).

## 4.6 Outside air

`site.air`: `temperature`, `relative_humidity` (a fraction 0 to 1; a server series in `%` is
given with `"unit": "%"` and gemini converts it), `pressure` (`gemini/gemini/case/site.py`).
Air matters for air coolers, cooling towers and chillers that reject heat to air. With only the
site's elevation, the pressure comes from the ISA standard atmosphere (ISO 2533:1975), which
`set_case` applies itself (skill `setting-the-case`): never a pressure of yours. A constant air
temperature is a simplification: say it is constant.

## 4.7 Data quality and ranges

Every subsurface value has a quality: measured in a well on the site, measured nearby,
estimated from a regional study, or assumed. Record it with the value. Before drilling, the
reservoir values (permeability, thickness, temperature) are the largest uncertainty of a
geothermal project (Huenges 2010; Stober and Bucher 2021). Take the report's base case as the
case value and keep its range (P10/P90, minimum/maximum) as the value's uncertainty (§9.4). The
geoscientist proposes each value with its page, quality and range; a value it marks estimated
or unknown is named so in the confirmation question.

---

# 5. Utilities and emission factors

## 5.1 Electricity grid

`utilities.electricity`: `co2_intensity` (a constant or a series), `import_limit`,
`export_limit` (`gemini/gemini/case/utilities.py`). A limit on the grid connection is a case
value when the grid operator gives one; without one, leave it unset rather than guessing.

## 5.2 Grid electricity CO2 intensity

The CO2-equivalent emitted per energy of electricity bought. Two methods (GHG Protocol Scope 2
Guidance, 2015):

- **location-based**: the average emission intensity of the grid where the electricity is
  used;
- **market-based**: the intensity of the electricity the buyer contracts (certificates, power
  purchase agreements).

For a plant design, the location-based average of the site's grid is the usual basis, and the
method must be stated. A brief or an organiser's value comes first (§8.1). An hourly or daily
series of the grid's intensity may be given; a constant is a simplification. The value goes
into the case (`utilities.electricity.co2_intensity`), not into the economics, although the
economics price the CO2 (`knowledge/handbook-economics.md`).

## 5.3 Bought gas

`utilities.gas`: `composition` (mole fractions; gemini converts mol%) and `heating_value` (per
mass) (`gemini/gemini/case/utilities.py`). Pipeline natural gas is mostly methane with some
ethane, propane, nitrogen and CO2; the exact composition comes from the gas supplier or an
assumptions document. Keep every digit as the source writes it: a composition must sum to one.

## 5.4 What belongs to the economics instead

Prices (electricity, gas, CO2, heat sale), the discount rate, the analysis period, capital and
operating costs, the CH4 global warming potential and the cost allocation between heat and cold
are economics, set in the case's economics file (`ask_economics`, skill `setting-the-case`).
How to choose them: `knowledge/handbook-economics.md`.

---

# 6. Requirements

## 6.1 What a requirement is

A requirement is "a rule of a third party on the outcome: a quantity of a role, with its band"
(`gemini/gemini/case/requirement.py`). It applies to every unit of the role on its own. It is
what gemini's verdict judges: a design passes when every requirement holds and nothing failed
(`check_results`, skill `reading-results`).

A requirement is never a design choice ("use two doublets"), never an operating set point the
team chooses, and never a value of the site.

## 6.2 Qualities of a good requirement

ISO/IEC/IEEE 29148:2018 (section 5.2.5) lists the characteristics of an individual
requirement: necessary, appropriate, unambiguous, complete, singular, feasible, verifiable,
correct, conforming and traceable (as summarised in secondary sources; check against the
standard). For a case:

| Quality | In a case |
|---|---|
| Necessary | it comes from the brief or a third party, not from the team's preference |
| Unambiguous | one reading only: which unit, which steps, which quantity |
| Complete | both ends where the brief gives both; the steps it holds in |
| Singular | one rule per requirement; a range with two ends is one rule (§6.7) |
| Feasible | it can be met by some plant; a rule no plant can meet is a flaw to ask about |
| Verifiable | gemini can judge it: a role and a quantity of `gm.plants.roles()` |
| Traceable | its `name` and its source (page) recorded with it |

## 6.3 Anatomy of a requirement in gemini

Keys (`gemini/gemini/case/requirement.py`, `KEYS`): `name`, `on`, `quantity`, `unit`, `over`,
`when`, `min`, `max`.

| Key | Rule |
|---|---|
| `name` | unique, snake_case (`production_flow_range`) |
| `on` | a role of `gm.plants.roles()` (§6.4) |
| `quantity` | a quantity of that role |
| `over` | for a per-step quantity: how the run is read (§6.5); refused for a window quantity or a property |
| `when` | for a per-step quantity: `always` or `running`; every step when absent (§6.6) |
| `min`, `max` | numbers in `unit`; at least one; an exact rule is `min` = `max` |
| `unit` | present if and only if the bounds have a dimension; over `duration` a duration (`d`, `h`) |

## 6.4 Roles and quantities

The closed table of roles (`gemini/gemini/plants/roles.py`, `TABLE`; `gm.plants.roles()` lists
it). A role is found from the plant's wiring, never from a module name.

| Role | Quantities |
|---|---|
| `doublet` | `production_flow`, `brine_cooling`, `production_temperature`, `injection_temperature`, `pump_power`, `pump_efficiency` (property), `intake_pressure`, `intake_gas_fraction`, `reinjection_ratio`, `count` (property), `wellhead_pressure` |
| `heat_pump` | `cop`, `lift`, `heat_output` |
| `boiler` | `fuel_input`, `heat_output` |
| `chp` | `power_output`, `heat_output` |
| `chiller` (absorption, adsorption, compression) | `cop`, `cold_output` |
| `heat_exchanger` | `duty`, `approach` |
| `heating_supply` | `temperature`, `unmet`, `unmet_share` (window) |
| `cooling_supply` | `temperature`, `unmet`, `unmet_share` (window) |
| `plant` | `electricity_bought`, `gas_bought`, `heat_surplus`, `co2`, `gas_burned` |

Notes from the same file: `reinjection_ratio` is the injected over the produced liquid volume
flow; `count` is the number of doublets of the plant; `unmet_share` is the unmet energy over the
energy demanded by the service over the whole period; `co2` of `plant` is the CO2-equivalent
mass emitted in each step, so `over: sum` gives the mass of the run.

## 6.5 Reading the run: `over`

`over` (`OVERS` in `requirement.py`): `each`, `sum`, `mean`, `max`, `min`, `duration`.

| `over` | Judges | Use for |
|---|---|---|
| `each` | every step (that `when` counts) | a cap or a band per step: a flow range, a cooling limit, a temperature |
| `sum` | the sum of the step values | a total: CO2 of the year, energy bought |
| `mean` | the mean | an average limit |
| `max`, `min` | the extreme of the run | the peak only (equal to `each` with that bound, read as one figure) |
| `duration` | the total time of the steps where `when` holds; bounds are durations | days or hours of operation |

## 6.6 Which steps count: `when`

`when` (`WHENS`): `always` or `running`, the steps where the unit carries flow; every step when
absent.

- A limit that applies while equipment runs (a flow band, a brine cooling limit, a supply
  temperature) is `when: running`. On a step where the unit stands still the quantity is zero
  or meaningless (an idle loop sits at its return temperature), and `always` would fail a plant
  that is right.
- `always` is for a rule that holds on every step, running or not (rare: a pressure that must
  never exceed a rating).
- A supply temperature the brief fixes is judged while that supply runs; on a day with zero
  cooling demand no chiller runs, which is no violation (QA-091 in
  `documents/project/quality-assurance/`).

## 6.7 Limits, ranges and exact values

- A cap: `max` only. A floor: `min` only.
- A range with both ends (a flow of 50 to 300 m³/h) is ONE requirement with `min` and `max`,
  never two (QA-080).
- An exact value (a pump efficiency of 70 %) is `min` = `max` (gemini refuses the old key
  `equals`).
- A fraction, share, ratio or efficiency has no unit: 70 % is `0.7`.
- Days of operation are a duration (`over: duration`, `when: running`, unit `d`), never a
  `count`; `count` is a number of units (`{on: doublet, quantity: count, min: 1, max: 3}`, no
  `over`, `when` or `unit`).

## 6.8 Tolerances

Briefs say "the demand shall be met" or "equal volumes are reinjected" without a tolerance. A
simulation never meets a demand to the last watt on every step, and a ratio computed from two
flows is never exactly one in floating point. Write a tolerance, and name it as an assumption
with its reason:

- demand met: one `unmet_share` requirement per supply with a small `max` (for example 0.01 =
  1 % of the period's energy), no `over`, `when` or `unit`;
- an exact ratio: a narrow band around it (for example 0.99999 to 1.00001).

The tolerance is an assumption the user confirms (§8.5), never a hidden value. A tolerance that
is too loose lets a design pass that the client would reject; one that is too tight fails a
design on numerical noise.

## 6.9 Translating brief text into rules

| Brief text (pattern) | Requirement |
|---|---|
| "Flow per well between A and B m³/h" | `on: doublet, quantity: production_flow, over: each, when: running, min: A, max: B, unit: m3/h` |
| "The brine may not be cooled by more than X K" | `on: doublet, quantity: brine_cooling, over: each, when: running, max: X, unit: K` |
| "A doublet operates at most N days a year" | `on: doublet, quantity: production_flow, over: duration, when: running, max: N, unit: d` |
| "Pump efficiency E %" | `on: doublet, quantity: pump_efficiency, min: E/100, max: E/100` (no unit, no over, no when) |
| "All produced water is reinjected" | `on: doublet, quantity: reinjection_ratio, over: each, when: running, min/max` a narrow band (§6.8) |
| "Between 1 and 3 doublets" | `on: doublet, quantity: count, min: 1, max: 3` |
| "The heat demand is met" | `on: heating_supply, quantity: unmet_share, max: <tolerance>` |
| "Supply at T °C" (fixed) | case value `demand.*.supply_temperature`; a temperature requirement, if one is written, is `when: running` |
| "Annual emissions below M t" | `on: plant, quantity: co2, over: sum, max: M, unit: t` (check the unit with `describe_case('requirements')`) |

The percentages and numbers are placeholders of the pattern; the values come from the brief.

## 6.10 Rules gemini cannot express

A rule the requirement options cannot say (a noise limit, a land-use limit, a permit
condition, a rule on a role gemini does not have) is kept in the case's `about` and named as
open in the handover and the report: never dropped silently, never forced into a requirement
that means something else.

## 6.11 Common mistakes

- `when: always` on a supply temperature (fails every idle day).
- Two requirements for the two ends of one range.
- A count for days of operation, or a duration for a number of units.
- `%` as a unit of an efficiency.
- A requirement the brief does not state (a team preference); it belongs to the design brief,
  not the case.
- A limit on one source's availability (a doublet's days) read as the system's: the system
  meets the demand on every day, a doublet may stand still on others.

---

# 7. Case values and design freedoms

## 7.1 The test

Ask: **who decides it?** If a third party (client, organiser, regulator, nature) fixes it, it is
a case value or a rule. If the team may choose it, it is a design freedom: the team records its
choice as an assumption with a reason, never asks the user for it as a missing case value, and
never writes it into the case. A bound the brief puts on a freedom ("1 to 3 doublets") is a
requirement; the choice inside the bound is the design's.

## 7.2 Typical freedoms

| Freedom | Where it lives | Bound in the case, if any |
|---|---|---|
| Well depth | plant (`depth`) | a search range may be an assumption; the reservoir is a case value |
| Number of doublets | plant (`size.doublets`) | `doublet.count` requirement |
| Flows, set points, controls | plant | flow range requirement |
| Units and their sizes (heat pump, boiler, chiller, CHP, store) | plant | none |
| Backup policy | plant (`params.backup`) | demand-met requirement |
| Associated gas handling (flare, boiler, CHP) | plant | emission and safety rules, if any |
| Return temperatures (when the brief leaves them open) | case value chosen by the team (§7.3) | brine cooling limit, demand met |

## 7.3 Return temperatures

A return temperature no file gives is a design choice of the team within the case's limits,
not a value the design waits for (team rule, QA-094). The case still needs a value, so it is
proposed in the one confirmation question as a design choice with its reason (and from an
assumptions document when one covers the case), recorded with `source: agent` and its reason.
The design team may move it later with a reason (§7.4).

## 7.4 A case change from the design team

The design team never changes the case. When a design shows that a case value it chose (a
return temperature) should move, it hands over `case change needed: <path>: <why>`; the case
lead changes it and the user approves the change, because a design is verified only on the case
the user gave (`case_changes`, skill `setting-the-case`).

---

# 8. Assumptions and their sources

## 8.1 Order of sources

Take each value from the first source that has it, and keep which one
(`geomind/geomind/prompts/case/lead.md`):

1. the user: the request and every answer;
2. the project's files, and the geoscientist's findings from them;
3. the knowledge base: assumptions documents, the cost catalogue, handbooks, cited with
   document and section or page (skill `finding-sources`);
4. a connected server (MCP), with its origin (skill `connectors`);
5. only when none has it: ask the user for the value itself, naming its path and unit, with no
   number of yours.

Never a typical value, a rule of thumb or a recalled number at any step. The ranges in this
handbook (§4.1, §3.4) are for plausibility checks only.

## 8.2 What a citation holds

Enough for a reviewer to find the value again: the title, the publisher or author, the year,
the page or section (or the row id of a table, or the URL), and, for a knowledge document, its
name (`knowledge/<name>`). A value converted (unit, currency, price year) names the
conversion.

## 8.3 Assumptions documents

An assumptions document covers one case: it names the brief or the site and gives the values
the case files lack, key by key, each with its source (for the hackathon,
`knowledge/hackathon-2026-assumptions.md`). When one covers the case, it comes before the
general catalogue, so the case matches it in one question (team decision,
`.claude/memory/feedback-economics-from-knowledge-documents.md`). Such documents live in the
global knowledge base only, never in a project's files (team rule,
`.claude/memory/feedback-assumptions-in-knowledge-only.md`).

## 8.4 Agent assumptions

When the user delegates the open values ("use reasonable assumptions"), search the knowledge
base and every connected server first. For a value still without a source, propose one in one
question, each line `<path> = <value> <unit> | engineering assumption, no source | <reason>`,
and record each approved value as `source: agent` with its reason. This is the only case where
an agent's number goes into a question.

## 8.5 The one confirmation question

Every case value that did not come from the user's files goes into ONE question, one line per
value: the path, the value with its unit, its source (or, for a choice, its reason) and a short
note; options approve all, change some, stop. Economics go into the one economics question
that follows. An answer is final: a value the user leaves open stays unset and is listed as
open; it is never asked again.

## 8.6 No computed values

A case holds values as sources state them, digit for digit, in their units. Never a sum, a
product, a conversion, a count, a date or a value from a formula: gemini converts units and
derives what follows from the case. A derived number that matters to a question is named by
the values it comes from and left to gemini, or a calculation is made with `calculate`
(skill `calculator`) and cited by its id.

---

# 9. Uncertainty

## 9.1 Kinds of uncertainty

- **Aleatory**: natural variability (a mild or a cold year, the price of gas next year).
- **Epistemic**: lack of knowledge (the permeability before a well is drilled).

Both are stated the same way: a best estimate and a range or a distribution, with its source
(JCGM 100:2008, the GUM, on stating uncertainty). For a geothermal case the epistemic
uncertainty of the subsurface usually dominates before drilling (Huenges 2010).

## 9.2 Ranges and distributions

gemini's value leaf takes an `uncertainty` with `kind` `uniform`, `triangular` or `normal`
(`UNCERTAINTY_KINDS`, `gemini/gemini/units/inputs.py`), and `min`, `max`, and `std` for a
normal one (examples in `gemini/examples/hackathon_2026/case.json` and `economics.json`).

| Kind | Use when the source gives |
|---|---|
| `uniform` | only a lower and an upper bound |
| `triangular` | bounds and a most likely value (the case value is the mode) |
| `normal` (with `min`, `max` to truncate) | a mean and a standard deviation |

A P10/P50/P90 triple of a reservoir report suits a triangular or a normal distribution; name
which reading was chosen.

## 9.3 Choosing a range from sources

- Take the range from the same report as the value (well tests, regional studies, price
  forecasts).
- A range wider than the source's is an assumption with a reason; a narrower one needs a
  source.
- Do not give ranges to values no study varies: uncertainty and sensitivity studies run only
  when the task asks for them (skill `economics`).

## 9.4 Uncertainty in the case

The uncertainty sits on the value leaf; a run, sizing and optimisation use only the value
itself, and only uncertainty studies draw from the range. The report states which values were
uncertain and which study used them (`knowledge/handbook-report.md` §8).

---

# 10. The case in gemini

How to set and read the case with the tools: skill `setting-the-case`. What each key means:
`describe_case(path)`. The exact schema: `read_case(section="schema")`, also in
`gemini/docs/schemas/case.schema.json`. This chapter is the map, not the tool manual.

## 10.1 Sections

Order of `case.json`: header (`format`, `kind`, `name`), `time`, `initial_state`, `site`,
`demand`, `utilities`, `economics` (a file name or an object), `requirements` (a list)
(`gemini/gemini/case/case.py`). `initial_state` holds the starting state of stateful modules
(the charge of a store) as `{module path: {state name: {value, unit}}}`: a module with states
has no default state.

## 10.2 Key tree

| Section | Keys |
|---|---|
| `time` | `start`, `end` (excluded), `step` |
| `site.ground` | `surface_temperature`, `gradient` |
| `site.reservoir` | `reference_depth`, `thickness`, `permeability`, `pressure`, `temperature` (only if measured) |
| `site.fluid` | `density`, `viscosity`, `gas_liquid_ratio`, `dissolved_gas` (species), `sand_concentration` |
| `site.air` | `temperature`, `relative_humidity`, `pressure` (or `{elevation}`) |
| `demand.heating` | `power`, `supply_temperature`, `return_temperature`, `minimum_return_temperature`, `maximum_return_temperature`, `return_pressure` |
| `demand.cooling` | as heating, plus `indoor_temperature`, `indoor_relative_humidity`, `dew_point_margin` |
| `utilities.electricity` | `co2_intensity`, `import_limit`, `export_limit` |
| `utilities.gas` | `composition` (species), `heating_value` |

Source: the `fields` of `gemini/gemini/case/site.py`, `demand.py` and `utilities.py`.

## 10.3 Series and files

A series is a leaf with `file`, `column`, `unit` and, optionally, `range` and `time_zone`
(`SERIES_KEYS`, `gemini/gemini/units/inputs.py`). The data file is given to the case, never
retyped; gemini reads a series' times from a column named `time` (a header of another name is
renamed when the file is given). Values a user types become a case file through
`save_profile`.

## 10.4 Units and conversions

gemini stores SI and writes back each value as it was read. Write units as the source prints
them in gemini's names (`°C/km`, `mol%`, `kg/m3`, `mPa.s`, `barg`, `Nm3/m3`, `MW`); gemini
converts. Every value `set_case` maps or converts is listed in its result's `converted` and goes
into the confirmation question. More: skill `gemini-units` and Appendix B.

## 10.5 Derived keys

Never set by hand: the reservoir temperature without a measurement (from the ground), a
hydrostatic pressure at another depth, the ISA air pressure from an elevation (set by
`set_case` itself).

## 10.6 Validation and missing values

gemini validates the whole case: a rejected case names each path and message and stores
nothing; a case with values missing is `case_incomplete` with every missing path at once; a
call that needs an absent value raises `missing_value` (`missing_assumption` under
`economics`) naming its path (`gemini/gemini/case/case.py`). `set_case`'s `plants_need` lists
case values the project's plants still lack.

## 10.7 The case the user gave and later changes

The project's case, or the first case of a chat, is the case the user gave. A design is
verified only on it: every later change, economics included, waits for the user's approval
(`case_changes`, `accept_case`; skill `setting-the-case`).

---

# 11. Checklists

## 11.1 Before the confirmation question

- [ ] Every file read once and whole; every statement classified (§2.3).
- [ ] Demand series checked: count, gaps, sign, unit, season, zero days (§3.4).
- [ ] Every missing value searched in the knowledge base and connected servers (§8.1).
- [ ] Every flaw collected for one question (§2.5).
- [ ] Design freedoms kept out of the case (§7).

## 11.2 Before handing the case over

- [ ] gemini accepts the case; `plants_need` empty or each path asked.
- [ ] Every value a file states is in it, with its file and page; none computed.
- [ ] No derived key set by hand (§10.5).
- [ ] Units as the sources print them; supply and return on the right sides.
- [ ] The case span equals the data span.
- [ ] Every hard rule of the brief is a requirement, or named as open in `about` (§6.10).
- [ ] Durations as durations, counts as counts, ranges as one rule, fractions without unit.
- [ ] No `when: always` on a supply temperature.
- [ ] Tolerances written and named as assumptions (§6.8).
- [ ] Every value not from the files confirmed in the one question, recorded with its source.
- [ ] Economics set in the one economics question.

## 11.3 Reviewing someone else's case

- [ ] Trace three values at random back to their page.
- [ ] Recompute nothing; ask gemini for the annual energies and peaks and compare with the
      brief's checking values (§2.4).
- [ ] Read each requirement aloud as a sentence: does it say what the brief says?
- [ ] List the assumptions with `source: agent` and their reasons.
- [ ] Check `case_changes` is empty or every change approved.

---

# 12. Worked example: the GEMINI hackathon 2026

This chapter is one example of the method; it holds the values of one competition case only.
The reference shape is gemini's sample case, `gemini/examples/hackathon_2026/case.json` (with
`economics.json`); every path below is a path of that file. Values the competition files lack:
`knowledge/hackathon-2026-assumptions.md`.

## 12.1 The inputs

| File | Holds |
|---|---|
| `GEMINI_Heating_Demand_Daily_2027.csv` | `date`, `heating_demand_MWth`: 365 daily averages, 2027-01-01 to 2027-12-31 |
| `GEMINI_Cooling_Demand_Daily_2027.csv` | `date`, `cooling_demand_MWcool`: 365 daily averages, same days |
| `GEMINI_Hackathon_Challenge_Requirements.pdf` | 2 pages, dated 28 October 2026: reservoir, brine and gas, constraints, supply temperatures |

The time column is named `date`, so it is renamed to `time` when the files are given to the
case (§10.3).

## 12.2 Values for checking

The PDF states (page 1): heating peak 30.0 MWth on 28 January, 111.67 GWhth/year; cooling peak
10.0 MWcool on 19 July, 23.74 GWhcool/year. These are for checking (§2.4); the case takes the
series from the CSV files, never these numbers.

## 12.3 Where each value goes

| Value as the PDF writes it | Case path | Source |
|---|---|---|
| Daily heating demand | `demand.heating.power` from the heating CSV, column `heating_demand_MWth`, unit MW | CSV |
| Daily cooling demand | `demand.cooling.power` from the cooling CSV, column `cooling_demand_MWcool`, unit MW | CSV |
| Time axis | `time.start` 2027-01-01, `time.end` 2028-01-01 (excluded), `time.step` 1 d, from the file's span | CSV |
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
gradient and the depth (§4.3). The PDF's note "for a different well depth, use hydrostatic
pressure and the gradient" is a reading instruction (§1.3), no case value.

## 12.4 Values from the assumptions document

From `knowledge/hackathon-2026-assumptions.md`, all in the ONE confirmation question, each with
that file as its source: return temperatures and pressures (`demand.heating.return_temperature`
60 degC, `return_pressure` 6 bar; `demand.cooling.return_temperature` 25 degC,
`return_pressure` 4 bar), `demand.cooling` dew point margin 1 K, indoor 26 degC and relative
humidity 0.5, `site.air` 10 degC and 101325 Pa, `site.fluid.sand_concentration` 20 mg/l,
`utilities.gas.composition` (bought gas), `utilities.electricity.co2_intensity` 300 g/kWh (the
organisers' value, QA-095).

## 12.5 The requirements

As gemini's sample writes them (`case.json`, `requirements`), each ONE requirement:

| `name` | Rule | From |
|---|---|---|
| `production_flow_range` | `on: doublet`, `quantity: production_flow`, `over: each`, `when: running`, `min` 50, `max` 300, `unit` m3/h | PDF p. 2 (one rule with both ends, QA-080) |
| `brine_cooling_limit` | `on: doublet`, `quantity: brine_cooling`, `over: each`, `when: running`, `max` 40, `unit` K | PDF p. 2 |
| `running_time_limit` | `on: doublet`, `quantity: production_flow`, `over: duration`, `when: running`, `max` 330, `unit` d | PDF p. 2 ("330 daily steps") |
| `pump_efficiency` | `on: doublet`, `quantity: pump_efficiency`, `min` 0.7, `max` 0.7 (no unit, over, when) | PDF p. 2 (70 %) |
| `full_reinjection` | `on: doublet`, `quantity: reinjection_ratio`, `over: each`, `when: running`, `min` 0.99999, `max` 1.00001 | PDF p. 2 ("equal liquid volumes"); the band is the sample's tolerance (§6.8) |
| `doublet_count` | `on: doublet`, `quantity: count`, `min` 1, `max` 3 (no over, when, unit) | PDF p. 2 |
| `heat_delivered` | `on: heating_supply`, `quantity: unmet_share`, `max` 0.01 | Organisers: the whole system meets the demand on all 365 days; 1 % is the sample's tolerance |
| `cold_delivered` | `on: cooling_supply`, `quantity: unmet_share`, `max` 0.01 | as above |

Supply temperatures (QA-091): 100 °C and 20 °C are fixed operating conditions in `demand.*`; the
sample judges them through `heat_delivered` and `cold_delivered`, with no temperature
requirement. A temperature requirement, if written, is `when: running`: on the days with zero
cooling demand no chiller runs and the idle loop sits at its return temperature, which is no
violation (§6.6). The 330 days limit only the doublet (organisers, QA-091): the plant meets the
demand on all 365 days (§6.11).

## 12.6 Design freedoms of this case

Recorded as assumptions with a reason, never asked as missing case values (§7):

- the well depth (the sample searches 2000 to 3500 m; PDF p. 2 and organisers);
- the number of doublets (`size.doublets`, 1 to 3, bounded by `doublet_count`);
- the return temperatures (QA-094; organisers: "as long as the return temperature does not
  violate the constraints, then it is fine"): 60 degC and 25 degC from the assumptions file,
  labelled "team design choice"; another value comes as `case change needed: ...` (§7.4);
- the backup policy (`params.backup`), the number and kind of units, how the associated gas is
  handled (flare, boiler, CHP: organisers allow several).

## 12.7 Economics

One economics question: each key the assumptions file gives as `{key, value, unit, source}`
with source `knowledge/hackathon-2026-assumptions.md` (keys as in gemini's `economics.json`),
so the economics match gemini's sample and its rankings can be compared. Every
`opex.per_energy.*` and `revenue.subsidy.*` key goes to `open`: the sample has neither, there is
no subsidy, and a per-energy map would need a price for each chiller no source gives. Method:
`knowledge/handbook-economics.md`.

## 12.8 Checklist of this case

- 8 requirements as above; no `when: always`; flow as one rule.
- No reservoir temperature, no depth and no doublet count in the case.
- Return temperatures from the assumptions file, confirmed in the one question.
- `plants_need` empty; economics set with currency EUR, price year 2015.
- Only the three competition files are project files; handbooks and the assumptions are in the
  global knowledge base, never copied into the project.

---

# Appendix A. Glossary

| Term | Meaning |
|---|---|
| Case | the outside conditions over one period and the rules of third parties (§1.1) |
| Design freedom | a choice of the team, bounded at most by a requirement (§7) |
| Doublet | a production and an injection well pair |
| GLR | gas-liquid ratio: gas volume (normal conditions) per liquid volume (§4.5) |
| Requirement | a rule on a quantity of a role, with its band (§6) |
| Role | what a unit is for, read from the plant's wiring (§6.4) |
| TVD / MD | true vertical depth / measured depth along the well (§4.2) |
| Transmissivity | permeability × thickness, kh (§4.2) |
| Unmet share | unmet energy over demanded energy of a service over the period (§6.4) |
| Value for checking | a number a brief states so the data can be checked (§2.4) |

# Appendix B. Unit pitfalls

| Pitfall | Correct reading |
|---|---|
| `MWth`, `MWcool`, `MWc` | all `MW`; the suffix names the product |
| MWh/d in a "power" column | an energy per day, not a power (§3.1) |
| `bar(g)` vs `bar` | gauge vs absolute; gemini's `barg` adds one standard atmosphere |
| `°C/km` vs `K/km` | equal; a temperature difference |
| `%` efficiency | a fraction without unit (0.7) |
| mol% | a mole fraction; gemini converts |
| `Nm³` vs `Sm³` | 0 °C vs 15 °C reference (DIN 1343, ISO 13443) |
| relative humidity `%` | a fraction 0 to 1; a series in `%` keeps its unit and gemini converts |
| mD | millidarcy; gemini converts to m² |
| kg/m³, mPa·s | `kg/m3`, `mPa.s` in gemini |

# Appendix C. References

- Frederiksen, S. and Werner, S. (2013). *District Heating and Cooling*. Lund:
  Studentlitteratur. ISBN 978-91-44-08530-2.
- Huenges, E. (ed.) (2010). *Geothermal Energy Systems: Exploration, Development, and
  Utilization*. Weinheim: Wiley-VCH.
- Stober, I. and Bucher, K. (2021). *Geothermal Energy: From Theoretical Models to Exploration
  and Development*, 2nd ed. Cham: Springer.
- ISO/IEC/IEEE 29148:2018. *Systems and software engineering — Life cycle processes —
  Requirements engineering*. (The list of characteristics in §6.2 is taken from secondary
  summaries of section 5.2.5.)
- JCGM 100:2008. *Evaluation of measurement data — Guide to the expression of uncertainty in
  measurement* (GUM). BIPM.
- World Resources Institute and WBCSD (2015). *GHG Protocol Scope 2 Guidance*.
- ISO 2533:1975. *Standard Atmosphere*.
- DIN 1343. *Reference conditions, normal conditions, normal volume*.
- ISO 13443:1996. *Natural gas — Standard reference conditions*.
- BIPM (2019). *The International System of Units (SI)*, 9th ed.
- EN 12831-1:2017. *Energy performance of buildings — Method for calculation of the design
  heat load*. (For a demand that must be built from buildings rather than given.)
- gemini source: `gemini/gemini/case/` (case, site, demand, utilities, time, requirement),
  `gemini/gemini/plants/roles.py`, `gemini/gemini/units/inputs.py`,
  `gemini/examples/hackathon_2026/`.
- geomind: skill `setting-the-case`, `finding-sources`, `connectors`, `gemini-units`,
  `calculator`; prompt `geomind/geomind/prompts/case/lead.md`.
- Team decisions: `.claude/memory/feedback-no-defaults.md`,
  `feedback-assumptions-in-knowledge-only.md`, `feedback-economics-from-knowledge-documents.md`;
  bug files QA-080, QA-091, QA-094, QA-095 in `documents/project/quality-assurance/`.
