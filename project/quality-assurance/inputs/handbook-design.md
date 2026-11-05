**Designing Geothermal Heating and Cooling Plants** (handbook-design)

*A handbook for the agents and engineers who design plants with gemini. Cite it as
`knowledge/handbook-design.md`, section by number (for example "0.7").*

Version 3, 2026-11-05. General, for any case and any site: a textbook of plant design and of how
to do it in gemini. It holds no data of a particular case; chapter 12 works its lessons on an
invented case. Checked against gemini 0.6.17 and the geomind design prompts.

**How to use this handbook** (front matter; the chapters start at 0)

- Read by section: `read_knowledge(name="knowledge/handbook-design.md", section="0.7")`. The name
  is always `knowledge/handbook-design.md`; the section is its **number alone** (`"0.7"`, `"4.3"`,
  `"12"`), the one key that never changes. A title also works only when spelled as in the outline
  (`"Wells and pumps"`); never invent one (there is no "3 Wells"). `outline=true` lists the
  numbers. Every section stands alone; cross-references name a section number. Read a section
  once: it does not change during a run.
- Chapters: 0 design path, 1 philosophy, 2 demand, 3 subsurface, 4 wells and pumps, 5 brine and
  gas, 6 surface heat, 7 cooling, 8 configurations, 9 control, 10 sizing and optimisation, 11
  gemini, 12 worked lessons; appendices A formulas, B rules of thumb, C glossary, D references.
- **Chapter 0 is the working chapter**: the checklist, the decision order, where each value comes
  from, a table of design values with units and how to choose them, and how a case's limits bind
  the design. Chapters 1 to 11 give the reasons; chapter 12 worked lessons; the appendices formulas,
  rules of thumb, glossary and references.
- How to call a tool is in its skill, never here (11.9).
- Prices, costs and a case's own values are not in this handbook: they come from the case, its
  assumptions document in Knowledge, and its economics (`knowledge/handbook-economics.md`,
  `knowledge/data-economics.csv`).

| Reader | Read first | Then, when the brief or a failure points there |
|---|---|---|
| Design lead | 0 (whole, once) | 8, 10, 11.7 |
| Reservoir engineer (R): reservoir, doublets, treatment and gas | 0.3, 0.7, 0.8 | 3, 5 |
| Well engineer (W): wells and pumps | 0.3, 0.7, 0.8 | 4 |
| Energy systems engineer I (H): heating | 0.3, 0.7 | 6, 8.3, 9 |
| Energy systems engineer II (C): cooling | 0.3, 0.7 | 7 |

Labels on values:

| Label | Meaning |
|---|---|
| **[textbook / paper / standard / catalogue]** | Named in Appendix D. |
| **[gemini: path]** | What a file of the gemini repository states or does. |
| **[derived]** | Computed from the values named beside it (formulas in Appendix A). |
| **[assumption]** | No verified source. It may start a design only as a recorded assumption (`confirmed: false`) with its reason; never as a fact. |

---

# 0 Design path in gemini

The design lead plans and runs a design from this chapter; each engineer reads the sections its
brief names. A value in 0.7 or 0.8 is a value with its source, to be cited, never a package
default: gemini has none (1.5).

## 0.1 Checklist for the design lead

Do the steps in order; do not start a step before its gate holds.

| # | Step | Gate to go on |
|---|---|---|
| 1 | `read_case` (whole, once), `list_plants`, `list_profiles`; read this chapter once | the case has no missing value; else hand over `case change needed: <path>: <why>` |
| 2 | Choose by 0.2 the family that fits best and at least one materially different alternative (10.7); record both in `design.families` with their reasons | two families: one superstructure, or two designs for one study |
| 3 | Build ONCE (`build_plant`): a project plant that fits, else the gemini class of the family; set `params.backup` (8.4), `params.control.dispatch` and `params.control.outages` (each the one value gemini suggests) | stored design; `issues` listed |
| 4 | Split the `issues` by the groups of 0.3, at most four; ONE `fill_parts`, one brief per group with its paths, the plant text of its modules, the case values with units, the interface values and the sections to read (0.7, 0.8 and its chapter) | every engineer answered |
| 5 | Write ONCE: all `changes` in one `patch_plant`; record every assumption in one `update_state` | `missing` is 0 |
| 6 | `size_plant` (new name); read what was sized and what was left (0.4) | no broken module |
| 7 | `simulate` a short window around the critical day (heating peak; cooling peak too when cold is made from brine heat), then `check_results` | no failed step |
| 8 | Fix from the failures by 0.5: the failure, gemini's message and the module's plant text to its owner, all owners in one `fill_parts`, one `patch_plant` | the change is applied |
| 9 | `simulate` the whole period (no `start`, `end`), `check_results` | `feasible` true |
| 10 | `optimize` few leaves with ranges from the user or the case (10.1, 10.2), always the doublets (`size.doublets`, `dN.nominal_flow`) besides the capacities; `simulate` the best for the whole period, check it | a feasible, better design; no verdict on a design whose doublets were neither sized nor searched |
| 11 | Compare the families in one `run_study`, keep the best feasible, simulate it for the whole period (how: `knowledge/handbook-studies.md` section 5.1) | ranked; a family that cannot be built is reported `blocked` with its reason |
| 12 | Record `design.reference`, `design.result`, `design.family`, `design.schematic`, the study key (`update_state`), then `finish` | recorded |

Stop rule: at most three changes aimed at one failing requirement. After the third, keep the
design that fails least, simulate it for the whole period, record it as final and name the open
requirement (its `name`, the value reached, its limit, why). Never loosen a requirement.

## 0.2 Choosing the plant family

Answer the questions in order; the first answers narrow the families, the later ones pick one.

1. **Is there a project plant that fits the services?** Start from it (`read_plant(project_plant=...)`).
2. **Which services?** Heating only: A, G or H. Heating and cooling: B, C, D, E, F or I.
3. **How hot is the brine against the heating supply?** Take the reservoir temperature at the
   design depth from the case's gradient (3.1) and compare with the heating supply T_s, the return
   T_r and an exchanger approach (6.1, 6.3):
   - T_brine ≥ T_s + approach: direct use (A, C, E);
   - T_r + approach < T_brine < T_s + approach: heat pump boost (B, D), or deeper wells (3.6);
   - T_brine ≤ T_r + approach: a heat pump on the brine only (H).
4. **How is cold made?** Brine above an absorption chiller's minimum drive temperature plus the
   approach in summer: absorption is a candidate (C, D, E). Otherwise, or with a high chilled-water
   supply (20 °C and up) and affordable electricity: compression (B) (7.8).
5. **Is there co-produced gas?** Substantial gas: burn it before you flare (F, G; 5.5). Some gas:
   degas and flare, inside the chosen family.
6. **More than one sensible answer?** One superstructure (optional modules, `choices`), or a
   `run_study` of the buildable families (10.7); never one design built by hand per variant.

| Family (8.1) | Choose when (8.2) | gemini class | Read |
|---|---|---|---|
| A. Direct use + peak boiler | brine hotter than the supply plus the approach; no cooling | `HeatingPlant`, `DoubletHeatPlant` | 6.1, 6.5 |
| B. Heat pump boost + peak boiler, compression chiller | brine somewhat colder than the supply, moderate lift, affordable electricity | `HeatingHeatPumpCoolingPlant` | 6.3, 6.4, 7.4 |
| C. Direct use + absorption cooling | brine hot enough in summer to drive the chiller | `HeatingAbsorptionCoolingPlant` | 7.2, 7.8 |
| D. Heat pump boost + all chillers | as B, and each chiller covers a distinct part of the cold load | `HeatingCoolingPlant` | 7.7, 7.8 |
| E. Direct use + all chillers | as A with D's cooling | `HeatingFullCoolingPlant` | 7.7, 7.8 |
| F. Hybrid with gas use | co-produced gas substantial: burn it for heat or power, flare only the surplus | none: built from modules and connections | 5.5, 5.6 |
| G. Boiler + CHP on the secondary side | co-produced gas substantial, no cooling | `BoilerCHPPlant` | 5.5, 6.6 |
| H. Low-temperature aquifer with heat pump | low-temperature reservoir | `ATESPlant` | 6.4, 6.7 |
| I. District energy on an aquifer store | heating and cooling networks on one store | `DistrictEnergyPlant` | 6.7, 7.7 |

A family that needs a module gemini lacks is `blocked: gemini has no module for it`.

## 0.3 Module groups for up to four engineers

Four groups, one brief each, matching the three engineer roles of `fill_parts`
(`reservoir_engineer`, `well_engineer`, `energy_systems_engineer`). The lead owns the wiring and
what the groups share. Classes are those of 11.3 and 11.5. Brief names follow the instance names
(`Reservoir engineer I`, `Well engineer I`, `Energy systems engineer I`, `II`).

| Key | Brief (role) | Owns | gemini module classes | Read |
|---|---|---|---|---|
| R | Reservoir engineer I (`reservoir_engineer`): reservoir, doublets, treatment and gas | the doublet count and spacing, the flow each doublet gives (`dN.nominal_flow`), `dN.drainage_radius`, `dN.reservoir.*`, `dN.sink.*`, the brine cooling limit, the degasser and the gas route | `ProductionReservoir`, `InjectionReservoir`, `ThermalDecline`, `BoreholeField`, `DownholeHeatExchanger`, `Formation`; `Degasser`, `Desander`, `Filter`, `InhibitorDosing`, `Flare`, `Blowdown`, `GasCompressor`, `GasMakeup`, `GasGrid`, `ChemicalGrid`, `WasteGrid` | 0.7, 0.8, 3, 5 |
| W | Well engineer I (`well_engineer`): wells and pumps | `depth`, `dN.well_diameter`, `dN.roughness`, `dN.nominal_wellhead_pressure`, `dN.pump_efficiency`, `dN.well.*`, `dN.riser.*` (with `esp_depth`), `dN.injector.*`, `dN.esp.*`, the injection pump | `ProductionWell`, `InjectionWell`, `ESP`, `LineShaftPump`, `InjectionPump`; plant classes `Doublet`, `NodalDoublet`, `MultiWellPlant` | 0.7, 0.8, 4 |
| H | Energy systems engineer I (`energy_systems_engineer`): heating | heat exchanger, heat pumps, boilers, CHP, storage, surface pipes of the heating network | `HeatExchanger`, `HeatPump` (heating), `Boiler`, `ElectricBoiler`, `CHP`, `ThermalStorage`, `HeatingGrid` | 0.7, 6, 8.3, 9 |
| C | Energy systems engineer II (`energy_systems_engineer`): cooling | chillers, coolers, cold storage, surface pipes of the cooling network | `AbsorptionUnit`, `AdsorptionChiller`, `HeatPump` (cooling: an electric chiller), `Cooler`, `IceStorage`, `CoolingGrid`, `Atmosphere` | 0.7, 7 |
| Lead | design lead | `Pipe`, `Mixer`, `Splitter`, `Valve`, `PressurizationTank`, `CirculationPump`, `CentrifugalPump`, `ElectricityGrid`, `PIDController`, `ORC`, `FlashTurbine`, `Separator`, `AquiferStorage`; the plant `type`, `size`, `params.backup`, `params.control`, `fluids`, every connection | — | 8, 9, 11.2 |

A plant without cooling needs three briefs (R, W, H); a group with no open issue gets no brief.

Interfaces the lead settles before the engineers start, and puts in every brief that needs them:
the brine temperature and flow at the wellhead (R and W to the others); the flow against the
drawdown and the pump depth (R with W); the gas stream out of the degasser (R to H for a burner);
the hot water that drives an absorption chiller (H to C); the brine order of the cascade (6.2);
the heat pump's minimum source outlet temperature, which follows from the brine cooling limit
(R to H, 0.8).

In a brief, name the sections to read by number only (`0.7`, `4.3`, `4.4`), with the document
name `knowledge/handbook-design.md`: a number always resolves, a paraphrased title does not.

## 0.4 The order: build, size, simulate, check, optimize

| Step | What | Gate | Read |
|---|---|---|---|
| 1. Build | project plant or class; every `issue` filled from a source (0.6); backup policy with its reason; both pump intake limits on every ESP | `missing` is 0 | 11.2, 11.5, 8.4, 4.4 |
| 2. Size | `size_plant` | no broken module in the notes | 8.3, 10.1 |
| 3. Short window | around the critical day | no failed step | 11.7 |
| 4. Check | `check_results`; fix owner by owner (0.5); after any change every earlier result is stale | `feasible` true | 11.7 |
| 5. Whole period | simulate and check again; read the engineering checks of 11.7 | `feasible` true | 11.7 |
| 6. Optimize | few leaves, ranges from the case or the user | feasible and better | 10.1, 10.2, 10.6 |
| 7. Compare, record | one study for the families; record design, result, study key | recorded | 10.7 |

What `size_plant` sets, and what stays yours [gemini: `gemini/study/size.py`]:

| `size_plant` sets | It leaves unchanged (you set it, from 0.7) |
|---|---|
| the doublet count: the smallest in the range of `size.doublets` whose heat at the case's flow limit and brine cooling limit covers the heating peak | exchanger UA (`thermal_conductance`) |
| each doublet's `nominal_flow`: the case's flow limit | CHP capacity |
| boiler capacity, by `params.backup` | coolers (`capacity`, `flow`, `loop_pressure`) |
| heat pump capacity: (T_s − T_reservoir) / (T_s − T_r) of the heating peak | pipes, treatment, ESP limits |
| chiller capacities: the cooling peak shared; the last chiller of the series gets the whole peak | a heat pump not needed (reservoir hotter than the supply) |
| injection pump `nominal_flow` and `nominal_head` | |

The sized plant is simulated once and every broken requirement is listed: read the notes before
step 3.

## 0.5 Failure to fix

Read the worst step of the failing reason (11.7), then the module's results around it
(`read_result`), then change one owner's values.

| Symptom | Engineering cause | Fix | Owner (0.3) |
|---|---|---|---|
| `missing_value` on a case path (`site`, `demand`, `utilities`, `time`, `economics`, `requirements`) | the case lacks a value | stop; hand over `case change needed: <path>: <why>`; never put it in the plant | lead (case lead decides) |
| `missing_value` on a plant path | a design value not stated | a value from 0.7 or a source, recorded with its reason; for a designed doublet the design value (`depth`, `well_diameter`), not a derived child [gemini: `docs/guide.md`] | the group's engineer (0.3) |
| `missing_value` on `params.backup` | backup policy not stated | `peak` or `none` with its reason (8.4) | lead |
| `missing_value` on `params.control.dispatch` / `params.control.outages` | plant rules not stated | `least_cost` / `lowest_demand`, the only values gemini offers [gemini: `gemini/engine/schedule/schedule.py`] | lead |
| `missing_value` on `params.dN.riser.esp_depth` | pump depth not stated | the well engineer chooses it (4.3); never the lead | W |
| Plant file refused for a case value | a site or network value written in the plant | remove it; it belongs to the case (11.1) | lead |
| Tear stream with no first guess (a closed loop) | a loop module lacks the values that let it offer its outlet; for a `Cooler`: `loop_pressure` and `flow` [gemini 0.6.17] | set those values on the module the message names | the module's group |
| `inlet 'X': <error>` | the value at that inlet is invalid [gemini 0.6.17] | fix the value the message names; an inlet is `<module>.<port>` (QA-083) | lead |
| Pipe `PhysicsError`: outlet pressure below zero | friction and static drop exceed the inlet pressure | wider pipe (2.5: 1 to 3 m/s), shorter pipe, or higher loop pressure; check the flow [gemini: `gemini/modules/piping/pipe.py`] | lead |
| `bound` on `intake_pressure` or `intake_gas_fraction` | pump too shallow for the drawdown, too much flow per well, or a deep design | set the pump deeper, lower the flow per doublet and add one, wider well, higher wellhead pressure (4.3, 4.4) | W |
| ESP `out_of_range` with a `curve` | the ESP curves do not cover the flows run | the well engineer gives sourced curves, or `pump_type` `"unspecified"` with no curves (the doublet derives them) | W |
| Doublet flow below the demand it should carry | the schedule runs a doublet at most at its `nominal_flow` [gemini 0.6.15] | raise `nominal_flow` up to the case's flow cap, or add a doublet | R |
| Heat pump: no duty, source below the minimum | brine at or below `minimum_source_outlet_temperature`, or lift below the minimum | move the heat pump upstream in the cascade, lower the exchanger duty before it, check the limit (6.4, 0.8) | H |
| Unit off below its minimum part load | machine too large for a low-demand step | smaller or two units, or accept and cover by backup (9.2) | H or C |
| Absorption chiller delivers nothing | drive water below `minimum_driving_temperature`, or cooling water too warm | hotter drive water (first in the cascade), larger cooler, or another chiller (7.2) | C |
| `heat_delivered` / `cold_delivered` fails | too little capacity on peak or outage days | read the worst step; add boiler or chiller capacity; check the backup policy covers outage days (8.4, 8.5) | H (C for cold) |
| `brine_cooling_limit` fails | brine cooled beyond the cap | heat pump `minimum_source_outlet_temperature` = production temperature less the cap, or a smaller heat pump (0.8) | H |
| `running_time_limit` fails | a doublet runs more days than allowed | `params.control.outages` `lowest_demand`, a second doublet, backup that covers the days off (8.5) | lead; H |
| `numerical` reason | a loop that does not close, or a colder return mixed into a fixed-temperature supply | plan where each stream goes (skill `designing-a-plant`, "What gemini can run") | lead |
| Supply temperature rule fails on zero-demand days | a rule with `when: always` | a case change: the rule holds only while that supply runs (9.4); never force circulation | case lead |
| `internal` error from a tool | an input gemini did not anticipate | change the input; never repeat the same call | lead |

## 0.6 Where a value comes from: case, Knowledge, your choice, or the user

| Kind of value | Examples | Comes from | Ask the user? |
|---|---|---|---|
| Case value | demand, supply temperatures, gradient, permeability, prices, requirements, the time axis | the case (`read_case`); the case lead set it from the user's files, Knowledge and the user's answers | never from design: hand over `case change needed: <path>: <why>` |
| Equipment design value | well diameter, roughness, heat transfer coefficient, efficiencies, COP model, UA, pipe size, cooler approach, treatment values | 0.7 first; then one `search_knowledge` / `search_rag`; else your engineering choice with a one-line reason; record as an assumption `{id, text, value, source, confirmed: false}` | no; never ask for a datasheet, a pump curve or stage coefficients |
| Equipment operating limit | ESP minimum intake pressure and maximum gas fraction, minimum drive temperature, minimum part load | as an equipment value; keep it on every unit (4.4, 10.4) | no |
| Plant rule | `params.control.dispatch`, `params.control.outages` | the one value gemini's `suggestions` give (0.5) | no |
| Lead's decision | backup policy, objective, number of evaluations, seed, family | the lead, as an assumption with its reason | no |
| Network length and layout | the length, diameter and elevation of the pipes to the consumers when the plant models the network | the case, its files or its assumptions document in Knowledge; never invented | yes, when none gives it: hand over `case change needed: <path>: network length not given`, so the case lead asks the user |
| Search range or option | `size.doublets` 1 to 3, `dN.nominal_flow`, `depth`, capacities | the user or the case (a range the plant file states, a requirement such as the doublet count) | yes, when missing: `ask_user` with the proposed values and a reason; `set_ranges` only after the answer |

Sources in order of preference: the user's files, Knowledge, a connector, the web, a recorded
assumption (1.5). Cite a value from this handbook as `knowledge/handbook-design.md` section 0.7
(or 0.8) with the source the row names.

## 0.7 Design values: meaning, unit, how to choose

The plant paths gemini asks for when a plant is built from a class, grouped by engineer. `dN` is
each doublet (`d0`, `d1`, ...). Write each with its unit as `{"value": 0.244, "unit": "m"}`; a
dimensionless value is a number (skill `gemini-units`). The last column gives a published value
where one exists; otherwise the value is an engineering choice: take it from the case's own
assumptions document in Knowledge when there is one (search it once by the path), else choose it
with a one-line reason and record it as an assumption (0.6).

**Doublet, wells and reservoir (R: reservoir values; W: `depth`, wells, wellhead)**

| Path | Meaning | Unit | How to choose | Published value |
|---|---|---|---|---|
| `depth` (`dN.depth` on a free plant) | true vertical depth of the reservoir midpoint | m | the case's reservoir depth, or searched within a range the user approves (3.6) | — |
| `dN.nominal_flow` | design flow per doublet; the schedule never runs a doublet above it | m3/h | the case's flow cap; `size_plant` sets it (12.5) | — |
| `dN.well_diameter` | inner diameter of the production casing | m | friction and pump size (4.1, 4.2) | 9 5/8 in or 7 in production casing is common [Stober and Bucher 2013] |
| `dN.drainage_radius` | drainage radius of the Darcy productivity; enters by a logarithm (3.3) | m | about half the spacing between doublets | doublet spacing about 1 to 2 km [Willems 2016] |
| `dN.roughness` | wall roughness of the wells | m | new steel; more with scale and corrosion | 4.5e-5 for new commercial steel [Moody 1944] |
| `dN.pump_efficiency` | production pump efficiency | 1 | the case's value when it states one, else the pump's (4.5) | — |
| `dN.nominal_wellhead_pressure` | production wellhead pressure at design flow | bar | high enough to keep gas in solution in the surface loop (5.1) and to reach the injector | — |
| `dN.reservoir.skin`, `dN.sink.skin` | near-well skin of producer and injector | 1 | 0 for a new well is optimistic for an injector (3.3) | — |
| `dN.reservoir.decline_threshold`, `dN.sink.decline_threshold` | alarm threshold of decline | 1 | the share of decline that should raise an alarm | — |
| `dN.well/riser/injector.friction_correlation`, `two_phase_friction_correlation` | friction models | text | single phase `darcy_weisbach`; two phase `BeggsBrill` where gas comes out (4.2) | — |
| `dN.well/riser/injector.heat_transfer_coefficient` | heat loss of the brine to the rock | W/m2/K | of the order of 10 for a cased well; a low value keeps the wellhead close to the reservoir temperature (3.1) | — |

**Pumps (W)**

| Path | Meaning | Unit | How to choose | Published value |
|---|---|---|---|---|
| `dN.riser.esp_depth` | ESP setting depth | m | asked only for a well split at its pump (`segment` `below_esp` / `above_esp`); a designed `Doublet` derives it. The shallowest depth that keeps the intake above its minimum at the largest flow and the lowest pressure; check with `evaluate_module` (4.3) [gemini: `gemini/engine/check.py`] | — |
| `dN.esp.pump_type` | pump curves | text | `"unspecified"` with no curves when no source gives a curve: the doublet derives them | — |
| `dN.esp.minimum_intake_pressure` | lowest intake pressure the pump may see | bar | above the bubble point when PVT data exist (4.3) | no general figure |
| `dN.esp.maximum_gas_fraction` | largest free gas share at the intake | 1 | the pump stage's limit (4.4) | 0.1875 for standard stages (one fourth of the 75 % of gas handlers) [Baker Hughes] |
| `dN.esp.motor_efficiency` | ESP motor efficiency | 1 | 1 when the case's pump efficiency already holds the whole loss | — |
| `injection_pump.efficiency` | injection pump efficiency | 1 | as the production pump | — |
| `injection_pump.nominal_flow`, `nominal_head` | injection pump rating | m3/h, bar | `size_plant` sets them (4.7) | — |

**Treatment and gas (R)**

| Path | Meaning | Unit | How to choose | Published value |
|---|---|---|---|---|
| `degasser.separation_efficiency` | share of free gas removed | 1 | vessel design (5.2) | — |
| `degasser.nominal_pressure_drop` | pressure loss of the vessel | Pa | vendor; a fraction of a bar | — |
| `filters.<f>.nominal_pressure_drop`, `nominal_mass_flow` | clean filter loss at its flow | Pa, kg/s | the flow through it; vendor loss | — |
| `filters.<f>.clogging_pressure_drop` | loss at which the filter counts as clogged | Pa | vendor; of the order of 0.5 bar | — |
| `desander.separation_efficiency`, `nominal_pressure_drop` | hydrocyclone | 1, Pa | particle size against cut size (5.4) | loss of the order of 1 bar [Svarovsky 2000] |
| `dosing.dose`, `dosing.product_concentration` | inhibitor dose, active share | ppm, 1 | geochemistry (5.3) | doses a few to tens of ppm [Gallup 2009] |
| `flare.combustion_efficiency` | share of methane burned | 1 | flare type | 0.98 [US EPA AP-42 13.5] |

**Heating (H)**

| Path | Meaning | Unit | How to choose | Published value |
|---|---|---|---|---|
| `heat_exchanger.thermal_conductance` | UA; `size_plant` does not size it | W/K | from the design duty and the chosen approach, Q = UA ΔT_lm (6.1, A.8); check with `evaluate_module` | — |
| `heat_exchanger.arrangement` | flow arrangement | text | plate exchangers are close to `counterflow` | — |
| `heat_exchanger.hot_nominal_mass_flow`, `cold_nominal_mass_flow` | design flows | kg/s | brine: the doublets' flow; network: duty / (c_p (T_s − T_r)) | — |
| `heat_exchanger.fouling_threshold` | fouling alarm | 1 | the loss of UA that should raise an alarm | — |
| `heat_pump.cop_model` | COP model | text | `carnot`; `lorenz` for large glides (6.4) | — |
| `heat_pump.carnot_fraction` | real COP over Carnot COP | 1 | the machine class | about 0.5 [Frutschi 1996]; 0.4 to 0.6 [Arpagaus et al. 2018] |
| `heat_pump.minimum_temperature_lift` | lift below which the COP is capped | K | the machine class | 10, the lowest lift of the machines reviewed [Arpagaus et al. 2018] |
| `heat_pump.minimum_source_outlet_temperature` | lowest brine temperature leaving the evaporator | degC | production temperature less the case's brine cooling cap, or a chemistry limit (0.8, 12.4) | — |
| `heat_pump.supply_margin`, `boiler.supply_margin` | heating above the supply setpoint | K | small and positive to cover losses after the unit (9.4) | — |
| `heat_pump.capacity`, `boiler.capacity` | ratings | MW | `size_plant` sets them (0.4) | — |
| `boiler.efficiency` | fuel to heat | 1 | the boiler class (6.5) | — |
| pipes `length`, `inner_diameter`, `roughness`, `elevation_change`, `heat_transfer_coefficient` | plant pipes | m, m, m, m, W/m2/K | the length of a network pipe is the site's: from the case or Knowledge, else asked (0.6), never invented; the diameter for 1 to 3 m/s at the design flow (2.5) | roughness 4.5e-5 m for new steel [Moody 1944] |

**Cooling (C)**

| Path | Meaning | Unit | How to choose | Published value |
|---|---|---|---|---|
| `compression_chiller.mode` | heat pump run as a chiller | text | `cooling` | — |
| `compression_chiller.carnot_fraction`, `minimum_temperature_lift` | as the heat pump | 1, K | as the heat pump | as the heat pump |
| `absorption_chiller.thermal_cop` | cold over drive heat | 1 | single or double effect (7.2) | about 0.7 single effect LiBr [Herold et al. 2016] |
| `absorption_chiller.minimum_driving_temperature` | drive below which it delivers nothing | K | the machine; single effect needs about 80 °C or more (7.2) | — |
| `absorption_chiller.characteristic_slope`, `minimum_driving_difference`, `rejection_coefficient`, `evaporator_coefficient`, `auxiliary_power_ratio` | characteristic equation (7.2, A.10) | W/K, K, 1, 1, 1 | the machine's data; the slope scales with capacity | [Hellmann, Schweigler and Ziegler 1999] |
| `adsorption_chiller.thermal_cop` | cold over drive heat | 1 | the machine | about 0.55 [Wang and Oliveira 2006] |
| `adsorption_chiller.minimum_driving_temperature`, `maximum_driving_temperature` | drive window | K | the machine (7.3) | — |
| `<cooler>.cooler_type`, `approach` | dry or wet; outlet above the air (dry) or wet-bulb (wet) temperature | text, K | climate and water (7.6) | dry 5 to 15 K, wet 3 to 8 K [ASHRAE] |
| `<cooler>.specific_fan_power` | fan power over duty | 1 | a small share (7.6) | — |
| `<cooler>.capacity` | heat rejected: cold plus drive | MW | compression: cold × (1 + 1/COP); absorption at COP 0.7: about 2.4 × cold (7.2) | — |
| `<cooler>.loop_pressure`, `flow`, `temperature_setpoint` | condenser loop; a closed loop needs them for its first guess (0.5) | bar, kg/s, degC | flow = capacity / (c_p ΔT of the loop); setpoint below the chiller's condensing limit | — |

## 0.8 Hard limits of a case and how they bind the design

A case states its limits as requirements (`read_case` shows each by `name`, on a role and a
quantity, 11.4). They are the case's: never loosen one; meet it by design. The common kinds, and
what each fixes in the plant:

| Kind of limit | Requirement on (role.quantity) | How it binds the design | Lesson |
|---|---|---|---|
| Number of doublets | doublet.count | the range of `size.doublets`; `size_plant` takes the smallest count that covers the heating peak | 12.3 |
| Flow per running doublet, min to max | doublet.production_flow | `dN.nominal_flow` at most the max (the schedule never exceeds it); below the min a doublet stops, so low-demand days need another unit | 12.5 |
| Brine cooling, producer to injector | doublet.brine_cooling | heat per doublet = ρ Q c_p ΔT_max (3.4); a heat pump on the brine gets `minimum_source_outlet_temperature` = production temperature − ΔT_max, which moves with the depth (3.1) | 12.3, 12.4 |
| Running days per doublet against all-year supply | the running-time rule | `params.control.outages` `lowest_demand` and a backup that covers the days off (8.4, 8.5) | 12.5 |
| Pump efficiency | doublet.pump_efficiency | `dN.pump_efficiency` (and the injection pump's) at the case's value | — |
| Reinjection of equal volumes | doublet.reinjection_ratio | every doublet reinjects its own flow (4.7) | — |
| Supply temperature, heating or cooling | heating_supply / cooling_supply.temperature | while that supply runs; above the reservoir temperature it needs a heat pump, a boiler or deeper wells (6.3) | 12.4 |
| Delivered energy (unmet share) | heating_supply / cooling_supply.unmet_share | capacity on the peak day and on outage days | 12.3 |
| Depth may change | (a case statement, not a requirement) | change the plant's `depth`, never the case's reference depth; temperature and pressure follow (3.1, 3.2) | 12.4 |
| Pump intake (an equipment limit, not the case's) | `bound` reasons on the ESP | keep `minimum_intake_pressure` and `maximum_gas_fraction` on every ESP (4.4) | — |

A case's values and the tolerances it does not state are in its own files and, when its owner
added one, its assumptions document in Knowledge: search that document once, never this handbook,
for a case's numbers.

## 0.9 Read once, search once

- Everything a tool returned stays in the conversation: read the case, a plant, a profile, a
  section of this handbook once, and again only after you wrote it.
- Do not search Knowledge for a value 0.7 or 0.8 already gives. For any other value: one search
  with the value's name and the case; if it finds nothing, choose by 0.6 and record the
  assumption. Never repeat a search in other words: a QA run spent 139 searches on the same few
  equipment values (QA-145).
- Compute nothing by hand: a number comes from the case, a gemini tool (`evaluate_module`, a short
  `simulate`), or a row of 0.7 with its source.

---

# 1 Introduction and design philosophy

Why the design is done the way chapter 0 says.

## 1.1 What a good plant is

In this order of priority: it **meets the demand** on every step (every service at its supply
temperature, within the case's tolerance); it is **robust** (it still meets the demand with one
unit out, a weaker reservoir, on the coldest and hottest day; pumps, exchangers and machines stay
in their windows); it is **efficient** (deep brine cooling, small lift, low pumping power); it is
**economic** (a low levelised cost of the thermal supply, 10.3); it **emits little** (CO2 and
methane, 5.6). The goals conflict (a deeper well is hotter, dearer and harder on the pump), so the
best compromise is found by search inside the feasible region (chapter 10).

## 1.2 Demand first

Every decision follows from the demand: peak, energy, shape, temperatures and the coincidence of
heating and cooling (chapter 2). Do not size the geothermal source on the peak alone (it idles at
part load) nor on the mean alone (it fails the peak day): peak capacity is cheap (a boiler, 6.5),
energy is what the geothermal source should supply (2.2, 8.3).

## 1.3 Design and operation are different problems

Design fixes what is built (doublets, depth, diameter, pumps, exchangers, machines, capacities);
operation decides each step which units run and how (chapter 9). A design is judged by simulating
its operation over the case's period with gemini's fixed operating rule; a design that needs a
clever rule to survive is fragile.

## 1.4 The design loop

Read, choose, complete, size, simulate a short window, check, fix, simulate the whole period,
optimise, compare (the steps of 0.1). Steps from simulate to fix repeat until the check passes.
When three changes aimed at one failing requirement make no progress, the structure is wrong, not
the numbers: change the family (8.2) or report the conflict (0.1, stop rule; QA-090 in 12.7).

## 1.5 Values, sources and the no-defaults rule

[gemini: `docs/rules.md`, "No defaults"]

- **No default values.** Nothing a user must decide has a default in gemini; a missing value is an
  error that names its path.
- **Every value has a source**: the user's files, Knowledge, a connector, the web, and only then a
  labelled assumption with its reason (0.6; skills `finding-sources`, `connectors`, `web-search`).
- **Derive, never guess**: a number that can be computed is computed with a tool (`calculator`,
  `python`, `evaluate_module`) and cited by its calculation.

The typical values in chapters 2 to 9 orient a first guess and help to recognise a wrong result;
they are inputs only through 0.7 with their label.

---

# 2 Demand analysis

This chapter turns a demand series into the numbers that drive the design: peak, energy, base/peak
split, overlap of heating and cooling, temperatures and network losses.

## 2.1 The demand series and its time step

A demand is a series of power over time, one per service (heating, cooling, sometimes domestic
hot water or process heat). Read for each:

- **Peak power** and its date: it sizes the total capacity of the service.
- **Energy over the year**: it sets the operating cost and the value of a cheap base source.
- **Minimum power**: it decides whether base units can run all year or must stop (9.2).
- **Number of days with demand**: a cooling demand present on only some days needs a plant that
  starts and stops.
- **Time step**: daily averages hide the hourly peak, which can be markedly higher than the daily
  mean. A plant sized on daily data meets the daily mean; whether it meets the hourly peak is not
  shown. State the step as a limitation, and add storage or margin if the case asks for hourly
  delivery. The size of the hourly-to-daily peak ratio depends on the network and the buildings;
  no general figure is given here: take it from measured data of the site if available.

The **full-load hours** of a service, energy divided by peak power, summarise the shape: a low
value (a peaky demand) favours cheap peak capacity; a high value favours a large base source
[textbook: Frederiksen and Werner 2013, ch. on load duration].

## 2.2 Load duration curve: base load and peak load

Sort the demand from highest to lowest step: the **load duration curve**. A base unit of capacity
B covers, in each step, the smaller of the demand and B. Its share of the yearly energy is the
area under the curve below B. Because the curve is steep at the top and flat at the bottom, a
base unit at half the peak usually covers most of the energy [textbook: Frederiksen and Werner
2013].

A worked table on an invented demand is in 12.2.

Read it as an economist: each added MW of base capacity covers less energy than the one before.
The base unit is worth adding while the energy it covers, at the difference in variable cost
between base and peak supply, pays for its annualised investment. The optimiser (Chapter 10)
finds that point; the table tells you where to start the search and whether a result is
plausible. For a typical peaky heating demand, a geothermal base that covers less than about half
the heat wastes the subsurface; one sized for the peak buys capacity that runs a few days a year
(12.2).

Compute this curve for every case with a tool (skill `python` or `calculator`), never by eye.

## 2.3 Heating and cooling together

When a site needs both heat and cold, three numbers decide the integration:

- **Coincidence**: on how many steps both are demanded, and what the heat demand is on the
  cooling peak day. A summer heat demand (domestic hot water, process) can absorb the heat a
  chiller rejects (7.7).
- **Combined peak**: the largest heat plus cold in one step. If cold is made from geothermal heat
  (an absorption chiller, 7.2), the brine must supply the heat demand plus the chiller's drive
  heat on the same step: the combined peak sizes the geothermal side.
- **Seasonal swap**: heating dominates in winter, cooling in summer. A source that serves heating
  in winter and drives cooling in summer runs more hours per year, which lowers its levelised cost.

## 2.4 Supply and return temperatures

The network's **supply temperature** is what the plant must reach; its **return temperature** is
what comes back. They decide:

- **Whether the brine can supply the heat directly.** The brine must be hotter than the supply
  temperature by at least the approach of the exchanger (6.1). If not, a heat pump, a boiler or
  deeper wells must close the gap (6.3).
- **How much heat a kilogram of brine gives.** The brine leaves the exchanger at no less than the
  return temperature plus the approach. A low return temperature lets the brine cool further and
  gives more heat per m3 produced, up to any limit on brine cooling the case states.
- **The flow in the network.** For a given power the flow is inversely proportional to the
  supply-return difference, so pumping power and pipe size fall as the difference grows.

Lower network temperatures (as in 4th-generation district heating) raise the heat taken from a
low-temperature source and lower losses [paper: Lund et al. 2014]. Where the return temperature
is a design choice of the team (not fixed by the case), choose it low enough to cool the brine
deeply, and high enough that buildings can still be heated with their existing emitters; record
the choice and its reason.

For cooling the supply temperature is the chilled-water temperature delivered (for example 6 to
20 °C) and the return is warmer. A high chilled-water supply temperature (for example for
radiant or high-temperature cooling) raises chiller COP and makes free cooling and sorption
chillers easier (Chapter 7). A supply below the dew point of the room air condenses water; a
dew-point margin is a case value.

## 2.5 Network losses and network pumping

- **Heat losses** of a buried network depend on pipe size, insulation, length and the temperature
  difference to the ground. They are a share of the delivered heat, larger in summer when the
  demand is low. If the case's demand is measured at the plant, losses are already inside it;
  if measured at the buildings, add them. Ask which, never assume.
- **Pressure losses** set the network pump. In a plant model, a pipe whose friction plus static
  drop exceeds its inlet pressure has no physical solution (in gemini, a `PhysicsError` at the
  pipe, see 0.5): give the pipe a sensible diameter for its flow, and the loop enough pressure.

A sensible pipe velocity for district heating water is of the order of 1 to 3 m/s; higher
velocities raise friction with the square of the velocity [textbook: Frederiksen and Werner 2013;
the range is orientation, verify for the pipe size].

## 2.6 Demand checklist

- Peak, energy, minimum, full-load hours, date of the peak, for each service.
- Load duration curve and the base/peak table (2.2), computed.
- Days with both services; combined peak; heat demand on the cooling peak day.
- Supply and return temperatures; which are fixed by the case and which are design choices.
- The time step and what it hides.
- Whether network losses are inside the demand.

---

# 3 The subsurface

This chapter gives the reservoir values a design needs and how they follow from depth: temperature,
pressure, productivity, drawdown, thermal breakthrough. Most of them are properties of the site
(the case) and only the depth and well design are choices.

## 3.1 Reservoir temperature from the gradient

In conductive settings the temperature rises roughly linearly with depth:

T(z) = T_surface + G · z

with T_surface the mean surface (or reference) temperature and G the geothermal gradient. Typical
continental gradients are of the order of 25 to 35 K/km; sedimentary basins with thick insulating
cover can be higher [textbook: Stober and Bucher 2013]. The gradient of a site comes from the case
(measured wells, maps), never from a typical value.

In gemini the plant states only the depth; the case holds `site.ground.gradient` and
`site.ground.surface_temperature`, and the run derives the reservoir temperature at the plant's
depth [gemini: `gemini/engine/apply.py`, `gemini/plants/doublet.py`].

The produced (wellhead) temperature is a little lower than the reservoir temperature because the
brine loses heat on the way up; the loss is larger at low flow and in thin wells. gemini computes
it with the wells' heat transfer coefficient (`heat_transfer_coefficient`, 0.7).

## 3.2 Reservoir pressure at depth

In a normally pressured aquifer the pore pressure is close to hydrostatic: p(z) ≈ ρ g z (gauge, with
the water table at the surface). From a reference pressure p_ref at depth z_ref:

p(z) = p_ref + ρ g (z − z_ref)

[gemini: `gemini/physics/ground.py`, `reservoir_pressure`]. gemini applies it: the case gives the
pressure at `site.reservoir.reference_depth`, and a doublet designed at another depth gets the
pressure at its own depth [gemini: `gemini/engine/apply.py`, `_doublets`]. Therefore **change the
plant's depth, not the case's reference depth**, to explore deeper wells: changing the reference
depth without changing the reference pressure describes a different reservoir (QA-119).

## 3.3 Productivity and injectivity

The productivity index (PI) relates the flow to the drawdown, Q = PI · (p_res − p_wf). For steady
radial Darcy flow into a well [textbook: Dake 1978]:

PI = 2π k h / ( μ · ( ln(r_e / r_w) + S ) )

with k the permeability, h the net thickness, μ the brine viscosity, r_e the drainage radius, r_w
the wellbore radius and S the skin. The injectivity index (II) has the same form for the injector.
Notes:

- **k·h (transmissivity) is the key reservoir number.** Doubling it halves the drawdown at a given
  flow. Permeability is the most uncertain of the inputs (3.7).
- **Viscosity falls with temperature**, so the injector, taking cold brine, has a lower II than the
  producer's PI at the same k·h. Design the injection pressure for the coldest injection
  temperature.
- **Skin** captures near-well damage (positive) or stimulation (negative); a new well is often
  assumed at zero skin, which is optimistic for an injector that clogs with fines over time.
- **r_e** enters only through a logarithm; the result is not sensitive to it.

gemini derives the PI and II of a `Doublet` from the case's permeability and thickness, the brine
viscosity, the plant's `drainage_radius`, `well_diameter` and `skin` [gemini: `gemini/plants/doublet.py`].

## 3.4 Drawdown and the capacity of a doublet

A **doublet** is one production well and one injection well into the same aquifer. Its thermal
capacity is

P = ṁ · c_p · ΔT_brine = ρ Q c_p (T_prod − T_inj)

limited by:

- the **flow** the pump and the reservoir allow (3.3, 4.3), and any flow cap of the case;
- the **brine cooling** ΔT_brine, limited by the return temperature of the network plus the
  exchanger approach (6.1), by a heat pump's minimum source outlet temperature (6.4), by scaling
  limits on the cold side (5.3), or by a cap of the case;
- the **pump power**: drawdown grows linearly with flow and friction with its square, so the last
  m3/h is the most expensive.

The drawdown at flow Q is Q / PI. Keep the dynamic level (the pressure at the pump) comfortably
above the pump's minimum intake pressure (4.3, 4.4).

## 3.5 Thermal breakthrough and doublet spacing

The injected cold brine forms a cooled region that grows toward the producer. After the
**breakthrough time** the produced temperature declines. For a doublet in a homogeneous confined
aquifer [paper: Gringarten and Sauty 1975]:

V_B = π L² H (ρc)_a / ( 3 (ρc)_w ),  t_B = V_B / Q

with L the well spacing at reservoir depth, H the aquifer thickness, (ρc)_a the volumetric heat
capacity of the saturated aquifer and (ρc)_w that of water. Lessons:

- breakthrough time grows with the **square of the spacing** and linearly with thickness, and falls
  with flow;
- a spacing that delays breakthrough beyond the economic lifetime of the plant is the target;
  Dutch practice places doublets with roughly 1 to 2 km between the well bottoms [paper: Willems
  2016];
- several doublets in one reservoir interfere: give each its own drainage area.

gemini models breakthrough with the `ThermalDecline` module [gemini: `gemini/modules/subsurface/
thermaldecline.py`]. A one-year simulation cannot show decline that sets in after decades: check
t_B with a calculation and state it.

## 3.6 Choosing the depth

Depth is a design choice whenever the case allows it. Deeper wells give:

- **hotter brine** (3.1): more heat per m3, a smaller temperature lift for a heat pump, possibly a
  direct supply without a heat pump;
- **higher drilling cost**: cost per metre rises with depth; the price is the case's
  (`economics.capex.drilling`, sourced in `knowledge/data-economics.csv`), never a figure of this
  handbook;
- **a deeper pump setting and more friction**, and, with dissolved gas, more gas at a given intake
  pressure if the setting does not follow (4.4).

Search depth together with the doublet count and the heat pump capacity (Chapter 10); the optimum
depends on the price of electricity against the price of drilling.

## 3.7 Subsurface uncertainty

Before drilling, permeability and the gradient are uncertain; permeability often by a factor of
two or more. A robust design:

- is checked at the pessimistic end of each range (low k·h, low gradient) and still meets the
  demand, with a backup that covers what the geothermal side may lack (8.4);
- is reported with the range of its cost (10.5);
- names the values that matter most (a sensitivity study, 10.5), so that a test of the first well
  can confirm them.

The gradient often moves the levelised cost more than any price, because it sets the brine
temperature, the heat pump lift and the number of doublets together; permeability within its usual
range often moves it much less, as long as the pump keeps its intake margin. Check this order with
a sensitivity study on the case (10.5), never assume it.

---

# 4 Wells and pumps

This chapter covers the production and injection wells and their pumps: geometry, friction, ESP
setting depth, intake pressure, free gas, pump power, and reinjection.

## 4.1 Well geometry

- **Depth**: the true vertical depth of the reservoir midpoint (3.6). Deviated wells are longer
  than their vertical depth; count measured depth for drilling cost and friction.
- **Inner diameter** of the production casing: sets friction (4.2) and the largest pump that fits.
  Geothermal production wells are commonly completed with 9 5/8" or 7" production casing [textbook:
  Stober and Bucher 2013; verify for the site]; 9 5/8 in casing has an inner diameter of about 0.22 to
  0.25 m by weight class.
- **Wall roughness**: new commercial steel about 4.5e-5 m [textbook: Moody 1944]; scaling and corrosion raise it over time.

## 4.2 Friction in the wells

Single-phase friction in a pipe follows Darcy-Weisbach:

Δp_f = f · (L / D) · ρ v² / 2

with f from the Moody chart or the Colebrook/Haaland correlation. Friction rises with the square of
the flow and the inverse fifth power of the diameter at constant flow. Example [derived, invented numbers]: brine
of 1050 kg/m3 and 0.4 mPa·s at 250 m3/h in a 0.244 m pipe flows at 1.49 m/s (Re ≈ 9.5e5, f ≈
0.0145), giving about 0.69 bar per km.

Above the bubble point the flow is single-phase; where gas comes out of solution (5.1) the flow is
two-phase and needs a two-phase correlation (gemini offers `BeggsBrill` as
`two_phase_friction_correlation`).

## 4.3 ESP setting depth and intake pressure

An electrical submersible pump (ESP) hangs in the production well below the dynamic fluid level.
Its **intake pressure** is

p_intake = p_res − Q/PI − ρ g (z_res − z_pump) − Δp_f(below the pump)

and must stay above the pump's minimum intake pressure in every running step. Set the pump deep
enough that the intake keeps its margin at the largest flow and the lowest reservoir pressure the
plant will see; deeper settings cost more cable and tubing and expose the pump to more heat.

gemini derives the setting depth of a designed `Doublet` as the shallowest that keeps the
required pressure at the intake at the nominal flow, and a pump that reaches the
`nominal_wellhead_pressure` at that flow [gemini: `gemini/plants/doublet.py`]. The plant's
`esp.minimum_intake_pressure` is then checked in every step; a breach is a verdict reason of kind
`bound` (11.7).

Published practice keeps the intake pressure above the bubble point of the produced fluid so that
no free gas reaches the pump; that needs the fluid's PVT. Without PVT data no general
minimum intake pressure is published: the value is an assumption of the case, recorded with its
reason (0.6).

## 4.4 Free gas at the pump intake

When the brine carries dissolved gas (5.1), every bar of intake pressure lost releases more free
gas. A centrifugal pump stage handles a limited gas volume fraction before its head degrades and it
gas-locks:

- standard stages: about 18.75 % free gas by volume (75 % for gas-handler stages, divided by four)
  [catalogue: Baker Hughes, Ace Plus gas handler pumps];
- a stricter rule of thumb of 10 % for a standard pump is quoted from Takacs (2009) but was not
  verified at the book.

An upper-bound estimate of the free gas fraction treats all gas as free (no solubility) and ideal
[derived, Appendix A.6]:

α ≈ GLR · (p_n / p) · (T / T_n) / (1 + GLR · (p_n / p) · (T / T_n))

With GLR 0.5 Nm3/m3 and 95 °C at the intake (invented) this gives about 6 % at 10 bar(a) and
about 12 % at 5 bar(a) [derived]. Two consequences:

- the gas limit and the intake pressure limit are linked: deeper, hotter, higher-flow designs pull
  the intake pressure down and the gas fraction up together;
- without these limits an optimiser drifts toward deep, high-flow designs that a real pump cannot
  run (a lesson in 12.7). **Keep both limits on every ESP.**

Remedies when the limits bind: set the pump deeper, lower the flow per doublet and add a doublet,
choose a larger well diameter (less friction), keep a higher wellhead pressure, or specify a
gas-handling pump (with a sourced limit).

## 4.5 Pump power and efficiency

Hydraulic power is Q · Δp; electric power is Q · Δp / (η_pump · η_motor). The pump must lift the
brine from the dynamic level to the surface and deliver it at the wellhead pressure, against
friction. Example [derived, rough, invented numbers]: at 250 m3/h with
20 bar of drawdown, 2 bar of friction and 10 bar of wellhead pressure the head is about 32 bar and
the electric power at 70 % efficiency about 0.32 MW per doublet, about 2 % of the 13.8 MW the
doublet gives at 45 K (12.3). Compute it with gemini (skill `evaluating-a-module`) for the real
design.

Pump efficiency is a property of the pump at its operating point; it falls away from the best
efficiency point. A case may fix it as a requirement (0.8).

## 4.6 ESP or line-shaft pump

| | ESP | Line-shaft pump (LSP) |
|---|---|---|
| Motor | downhole, cooled by the brine | at the surface, drives the pump through a shaft |
| Setting depth | deep settings possible | limited by shaft length and alignment |
| Temperature | motor and cable limits at high brine temperature | motor at the surface, no downhole electrics |
| Maintenance | pulling the whole string | surface motor serviceable |

Line-shaft pumps have long been used in shallow, hotter low-enthalpy wells; ESPs where the setting
must be deep [textbook: DiPippo 2016; Stober and Bucher 2013]. gemini has both: `ESP` and
`LineShaftPump`, the latter with shaft friction proportional to setting depth and speed [gemini:
`gemini/modules/pumps/lineshaftpump.py`, citing ANSI/HI 2.3].

## 4.7 Reinjection pressure and the injection pump

Cooled brine is returned to the same aquifer to maintain pressure and dispose of the fluid. The
injection wellhead pressure must overcome the injectivity (3.3) at the injected flow, less the
weight of the (cold, denser) column. Design it at the largest flow and the coldest injection
temperature, and leave margin for injectivity loss from fines and scale (5.3, 5.4).

- If the produced pressure after the surface plant is enough, no injection pump is needed.
- Otherwise an injection pump raises the pressure. gemini's `size` rates the plant's
  `InjectionPump` from the doublets it serves: their total nominal flow, and the largest pressure
  rise one asks, the wellhead pressure that injects its flow less the production wellhead pressure
  as suction, floored at zero [gemini: `gemini/study/size.py`].
- **Equal volumes.** A doublet that reinjects all produced liquid keeps the reservoir pressure; a
  case may require it (reinjection ratio 1 within a tight band).

## 4.8 Wells and pumps checklist

- Depth, diameter, roughness stated; drilling cost per metre sourced for that depth.
- Drawdown at the largest flow; intake pressure above its minimum in every running step.
- Free gas at the intake below the pump's limit in every running step.
- Pump power computed, not guessed; efficiency as the case or the pump states.
- Injection pressure at the largest flow and coldest brine; injection pump sized.
- Reinjection ratio as the case requires.

---

# 5 Brine chemistry and associated gas

This chapter covers what the brine carries besides heat: dissolved gas, salts, solids. Each can
stop a plant (scaling, gas-locked pumps, clogged injectors) or add emissions (methane, CO2).

## 5.1 Dissolved gas and why it comes out

Deep brines often carry dissolved gas, mainly CO2 and CH4 (and sometimes N2, H2S). The case
states it as a **gas-liquid ratio** (GLR, Nm3 of gas per m3 of liquid at standard conditions) and a
composition. A normal cubic metre is at 0 °C and 1.01325 bar(a) [standard: DIN 1343].

Gas stays dissolved while the pressure is above the bubble point. On the way up the pressure falls
and gas comes out: first in the well above the pump (two-phase flow, 4.2), then at the pump intake
if the intake pressure is low (4.4), then in surface equipment where the pressure is lowest.
Released CO2 raises the pH of the brine and drives carbonate scaling (5.3).

Two operating philosophies:

- **Keep it in solution**: hold the surface loop above the bubble point (pressurised loop),
  inject the gas back with the brine. Simpler, no gas to handle, but needs pressure margin
  everywhere, and the gas never earns anything.
- **Separate it**: degas at a controlled pressure (5.2), then use or dispose of the gas (5.5). Needed
  when the gas content is high or the gas has value as fuel; it produces emissions that must be
  counted (5.6).

## 5.2 Degassers and separators

A degasser (gas separator) lets the free gas leave the liquid in a vessel at a set pressure. Its
design values are the vessel pressure (or pressure drop) and the separation efficiency. In gemini
the `Degasser` removes a share `separation_efficiency` of the free gas and applies a pressure loss;
dissolved gas that does not come out at the vessel pressure stays in the liquid (Henry's law and
residence time are not modelled) [gemini: `gemini/modules/treatment/degasser.py`].

Place the degasser upstream of the heat exchanger so that the exchanger sees liquid only, and after
the production wells are joined, so that one vessel serves all doublets. A lower vessel pressure
releases more gas but makes scaling more likely; a design without PVT data cannot predict the
dissolved share and must say so.

For high-enthalpy fluids a **flash separator** splits steam from brine; it is used in power plants
and is not part of a low-temperature heating plant [textbook: DiPippo 2016]. gemini's
`Separator` (under `power`) is such a flash separator.

## 5.3 Scaling, corrosion and inhibitors

- **Carbonate scaling** (calcite) follows CO2 degassing and heating; it is worst where pressure
  falls and temperature is high (pump outlet, degasser, hot side of the exchanger).
- **Silica and sulphide scaling** follow cooling; they are worst on the cold side: the exchanger
  outlet and the injector. A low injection temperature raises heat output and raises this risk. If
  the chemistry is known, a minimum injection temperature may be a real design limit; take it from
  a geochemical study, never from a typical value.
- **Corrosion** follows CO2, H2S, oxygen ingress and chlorides; it governs material choice
  (titanium or stainless plates in exchangers, coated or alloy casing) and needs a closed, oxygen-free
  loop.

Scale and corrosion **inhibitors** are dosed continuously in proportion to the flow. Typical
geothermal scale-inhibitor doses are a few to some tens of ppm of product [paper: Gallup 2009, as
cited in gemini `gemini/modules/treatment/inhibitordosing.py`]. In gemini the `InhibitorDosing`
module computes the product mass flow from a dose; the chemical is priced through the case's
`opex.variable.chemical` and drawn from a `ChemicalGrid`.

Fouling of the exchanger lowers its UA over time; design for the fouled state and monitor it (gemini
reports a fouling diagnostic against `fouling_threshold` [gemini: `heatexchanger.py`]).

## 5.4 Sand and filters

Weakly consolidated sandstones produce fines and sand, which erode pumps and clog injectors.
Remedies, from the well outward: sand control in the completion, a **desander** (hydrocyclone) at
the surface, and **filters** before the exchanger and before the injector. A hydrocyclone's
pressure loss is of the order of 1 bar at design flow and its efficiency depends on particle size
against its cut size [textbook: Svarovsky 2000, as cited in gemini
`gemini/modules/treatment/desander.py`]; both are design-specific values to source from the
vendor. The sand load comes from the case (`site.fluid.sand_concentration`); the removed sand is
waste with a disposal price.

gemini models `Desander`, `Filter` (with a clogging pressure drop) and `WasteGrid` for the removed
solids.

## 5.5 What to do with the gas: flare, boiler, CHP

Once separated, the gas must go somewhere. The options, in rising order of value:

| Option | What it does | Gains | Costs and emissions |
|---|---|---|---|
| Vent | releases the gas | none | methane released whole: the worst option; normally not allowed |
| Flare | burns the gas | nothing but safety | CO2 from combustion plus the CO2 in the gas; the unburnt share of methane escapes (about 2 % at 98 % combustion efficiency [standard: US EPA AP-42 13.5]) |
| Boiler | burns it for heat | heat that replaces grid gas | same CO2 as a flare, but replaces bought fuel |
| CHP (gas engine) | burns it for power and heat | electricity and heat | engine cost; electricity replaces grid power |
| Reinjection | keeps it in the brine | no emissions | needs pressure everywhere (5.1) |

Rules:

- **Burn before you flare.** If a boiler or CHP needs heat anyway, the co-produced gas is free fuel.
  Size the boiler's base fuel use to the gas available, top up with grid gas, and send only the
  surplus to the flare. In gemini a `GasMakeup` offers the co-produced gas to the burner first,
  draws the shortfall from the `GasGrid` and sends the surplus to its `excess_out`, usually a
  `Flare` [gemini: `gemini/modules/piping/gasmakeup.py`; the `Boiler` and `CHP` burn the
  co-produced gas first, `boiler.py`, `chp.py`].
- **Know the fuel value.** The heating value of the co-produced gas depends on its methane share.
  For pure methane the lower heating value is about 50.0 MJ/kg, about 35.8 MJ/Nm3 [textbook: standard
  combustion tables; the per-Nm3 figure is derived with a methane density of 0.717 kg/Nm3]. CO2 in
  the gas adds no fuel value.
- **A CHP must be able to sell or use its power**, and needs enough running hours; with little
  gas the engine is small and its specific cost high (6.6).

## 5.6 Emissions: CO2, methane and electricity

Count three sources over the period:

1. **Combustion and carried CO2**: every kg of CH4 burned forms 44/16 = 2.75 kg CO2 [derived from
   stoichiometry], plus the CO2 already in the gas, whether it is burned, flared or vented.
2. **Methane released**: vented, unburnt in a flare, or slipped in an engine, counted with its
   global warming potential. IPCC AR6 gives GWP100 = 29.8 for fossil methane [paper: Forster et al.
   2021, table 7.15]. A small methane slip
   weighs much: 2 % unburnt methane at GWP 29.8 adds about 0.6 kg CO2e per kg of methane flared,
   about a fifth of the 2.75 kg from combustion [derived].
3. **Bought electricity** times the grid's CO2 intensity. The intensity is a case value (country,
   year, average or marginal); never a typical value.

gemini's `co2` metric counts all three: direct, methane and electricity [gemini:
`gemini/study/metrics.py`]. The case's CO2 price applies only to the plant's own CO2 and methane
(CO2e), not again to grid electricity, whose price already carries its CO2 [gemini 0.6.16,
`docs/CHANGELOG.md`, QA-128].

---

# 6 Surface heat

This chapter covers how heat moves from the brine to the network: exchangers, cascades, heat pumps
for lift, boilers for peak, CHP and storage.

## 6.1 Heat exchangers: approach, UA and effectiveness

The brine almost never enters the network directly: a plate heat exchanger separates the corrosive,
gas-bearing brine from the clean network water [textbook: Stober and Bucher 2013; Frederiksen and
Werner 2013].

- **Duty**: Q = UA · ΔT_lm, with UA the thermal conductance and ΔT_lm the log-mean temperature
  difference. Equivalently Q = ε · C_min · (T_hot,in − T_cold,in) with the effectiveness ε from NTU
  = UA / C_min and the flow arrangement [textbook: Incropera et al. 2007].
- **Approach**: the smallest temperature difference between the two streams in the exchanger. In a
  counterflow exchanger with equal heat capacity rates it is the same at both ends. A smaller
  approach recovers more heat from the brine but needs a larger, more expensive exchanger: UA grows
  roughly as 1/approach for a given duty [textbook: Incropera et al. 2007]. The approach is
  therefore an economic choice, not a constant; plate exchangers can reach approaches below 1 K
  [catalogue: Tranter], at a price. Choose it by cost (Chapter 10) or by a sourced design guide.
- **What the approach costs downstream**: every kelvin of approach lowers the water temperature
  the network gets from the brine, and raises the lift of a heat pump or the duty of a boiler
  downstream by one kelvin's worth.
- **Arrangement**: counterflow gives the highest effectiveness for a given UA; plate exchangers are
  close to counterflow.
- **Fouling**: design UA for the fouled state (5.3).

In gemini the `HeatExchanger` takes `thermal_conductance` (UA), `arrangement`, nominal pressure
drops and flows; its role quantities are `duty` and `approach` [gemini: `gemini/plants/roles.py`].
Note that gemini's `size` does not size the exchanger: it keeps the plant's UA and lists it as
unchanged [gemini: `gemini/study/size.py`], so check the approach in the results (11.7) and set UA
yourself.

## 6.2 Cascading: using the brine more than once

A cascade passes the brine through several users in order of falling temperature: the hottest
service first, then lower-temperature services on the cooler brine. The Lindal diagram classifies
direct uses by the temperature they need [textbook: Lindal 1973, reproduced in Stober and Bucher
2013]. In a heating and cooling plant common cascades are:

- **Exchanger, then heat pump on the brine**: the exchanger takes the heat the brine gives directly;
  the heat pump then cools the brine further (its evaporator on the brine) and lifts that heat to the
  supply temperature. This raises the heat per m3 and keeps the brine cooling within its limit.
- **Absorption chiller drive, then heating**: the hottest water drives the chiller (it needs a high
  drive temperature, 7.2) and its outlet still heats a lower-temperature service.
- **Series of exchangers on the network**: the coolest return water meets the coolest brine first.

Order users so each takes the brine at the temperature it needs and no higher.

## 6.3 Temperature reach and temperature lift

Compare three temperatures: the brine at the wellhead T_b, the supply T_s and the return T_r.

- **T_b > T_s + approach**: direct supply is possible; the brine heats the network up to the supply
  temperature and is cooled toward T_r + approach.
- **T_r + approach < T_b < T_s + approach**: the brine can preheat the return water; the remaining
  lift to T_s comes from a heat pump or a boiler. The share of the heat the brine cannot reach is
  about (T_s − T_b) / (T_s − T_r) for an ideal exchanger [gemini: `gemini/study/size.py`, the share
  by which `size` rates the heat pump].
- **T_b < T_r + approach**: the brine cannot heat the network at all directly; only a heat pump can
  use it.

Ways to close a gap: deeper wells (3.6), a heat pump (6.4), a boiler (6.5), or a lower supply
temperature (if the case allows it). They differ in cost and emissions: deeper wells cost capital;
a heat pump costs capital and electricity; a boiler is cheap to build but burns fuel all the hours
it closes the gap. Use a boiler for hours and peaks, not for a gap that exists all year, unless gas
is free (5.5).

## 6.4 Heat pumps

An electric heat pump moves heat from a source (the brine, or the network return) to a sink (the
supply). Its coefficient of performance:

COP_heating = η_C · T_sink / (T_sink − T_source)

with temperatures in kelvin and η_C the Carnot fraction. Real water-to-water machines reach about
0.4 to 0.6 of Carnot over a lift of about 10 to 80 K [paper: Arpagaus et al. 2018]; "close to 50
percent of the Carnot value" [paper: Frutschi 1996] Consequences:

- **COP falls fast with lift.** At 100 °C supply and 0.5 of Carnot: a 40 K lift gives about 4.7, a
  60 K lift about 3.1 [derived]. Every kelvin of lift saved (deeper wells, smaller approach, lower
  supply) raises the COP.
- **Lorenz form**: with large glides on both sides (water heated by 40 K, brine cooled by 30 K), the
  log-mean temperatures of the glides describe the machine better than the outlet temperatures;
  gemini offers `cop_model` `lorenz` for heating [gemini: `gemini/modules/heating/heatpump.py`].
- **Staging**: two machines in series, each with a smaller lift, reach a higher overall COP than one
  machine with the whole lift, at higher capital cost; worth it for large lifts.
- **Source outlet limit**: the evaporator must not cool the brine below a limit (freezing, scaling,
  or the case's brine cooling cap). gemini states it as `minimum_source_outlet_temperature`: the
  production temperature less the brine cooling cap (12.4).
- **Minimum lift and minimum part load**: below a minimum lift the formula overstates the COP
  (gemini caps it with `minimum_temperature_lift`, 10 K being the lowest lift in
  Arpagaus et al. 2018); below a minimum part load the machine stops (`minimum_part_load`).
- **High supply temperatures** (above about 90 to 100 °C) need high-temperature refrigerants and
  machines; check availability and source a cost for that class [paper: Arpagaus et al. 2018].

Size the heat pump to the heat the brine cannot reach (6.3), not to the whole peak; let a boiler
carry the peak (8.3). A heat pump costs about ten times a gas boiler per MW of capacity
[catalogue: Danish Energy Agency, Technology Data, sheets 40 and 44]; the prices are the case's
economics.

## 6.5 Peak and backup boilers

A boiler is the cheapest capacity per MW, an order of magnitude below a heat pump [catalogue: DEA
Technology Data, sheets 40 and 44], and expensive per MWh (fuel and CO2). Its two jobs:

- **Peak**: cover the top of the load duration curve, the few hundred hours above the base
  capacity (2.2).
- **Backup**: cover the load when a geothermal unit is out (8.4).

Boiler efficiency is a property of the boiler; source it for the boiler class. An **electric boiler** does the same with electricity at an
efficiency near 1; it pays where electricity is cheap or low-carbon, and needs no gas connection
(gemini `ElectricBoiler`, counted as backup in coverage since gemini 0.6.13 [gemini:
`docs/CHANGELOG.md`]).

## 6.6 Combined heat and power

A gas engine CHP gives electricity and heat from one fuel. In gemini's `CHP` the fuel use follows
the Willans line, fuel = F_full · (f0 + (1 − f0) · L), where L is the electric load fraction [textbook:
Heywood 1988, as cited in gemini `gemini/modules/heating/chp.py`]. A CHP pays when:

- there is a use for its heat for many hours (otherwise its heat is dumped);
- its electricity is worth more than the gas it burns, or the fuel is free co-produced gas (5.5).

Its capital cost per W of electricity is far above a boiler's per W of heat [catalogue: DEA sheet
06]; the price is the case's economics.

## 6.7 Thermal storage

Storage decouples production from demand:

- **Short-term (hours to days)**: a hot water tank shaves daily peaks, lets a base unit run at full
  load and avoids boiler starts. In a daily-step simulation its value is invisible: only intra-day
  dynamics show it.
- **Seasonal**: aquifer thermal energy storage (ATES), boreholes or pits store summer heat (for
  example chiller reject heat) for winter, or winter cold for summer.
- **Cold storage**: chilled water or ice shifts chiller operation to cheap hours.

gemini has `ThermalStorage` (fully mixed tank), `IceStorage` and `AquiferStorage`, and a plant
class `ATESPlant` [gemini: `gemini/modules/storage/`, `gemini/plants/atesplant.py`]. Add storage
only when the time step lets the model show its benefit.

---

# 7 Cooling

This chapter covers how a geothermal plant makes cold: sorption chillers driven by brine heat,
compression chillers, free cooling, heat rejection, and how heating and cooling share one plant.

## 7.1 The cooling service

A cooling demand is a chilled-water flow delivered at a supply temperature and returned warmer.
Every chiller **moves** heat: it takes the cold load from the chilled water and **rejects** that heat
plus its drive energy at a higher temperature, to a cooler, a cooling tower, the ground or a heat
user. A cooling design therefore has three parts: the cold source, the drive (heat or electricity),
and the heat sink. Forgetting the sink is a common error.

## 7.2 Absorption chillers

An absorption chiller (water/lithium bromide for chilled water) is driven by heat:

- **Single effect**: drive about 80 to 95 °C or more; thermal COP (cold out / heat in) about 0.7
  [textbook: Herold, Radermacher and Klein 2016, a summary gives
  0.7 to 0.8 at a 95 °C source, Techniques de l'Ingénieur BE9735].
- **Double effect**: drive about 150 to 180 °C; COP about 1.0 to 1.3 [textbook: Herold et al. 2016,
  as quoted in a LiBr/H2O thermoeconomic study published by UNICAMP (nipe.unicamp.br); Techniques de l'Ingénieur BE9735]; needs
  brine hotter than most low-enthalpy reservoirs.
- **Minimum drive temperature**: below it the machine delivers nothing; for a single-effect LiBr chiller it is of
  the order of 80 °C; take it from the machine's data.
- **Characteristic equation**: the available cold falls as the drive temperature falls or the
  cooling water warms. gemini's `AbsorptionUnit` uses the characteristic equation of Hellmann,
  Schweigler and Ziegler (1999), Q_E = s · (ΔΔt − ΔΔt_min), with ΔΔt = t_G − a · t_AC + r · t_E
  [gemini: `gemini/modules/cooling/absorptionunit.py`].
- **Heat rejection** = cold + drive heat (+ small pump power), about 2.4 times the cold at COP 0.7
  [derived]: the cooler or tower must be sized for that.

The drive heat is heat used inside the plant, not heat delivered: account it by source as
`knowledge/handbook-economics.md` section 1.4 says.

Why it fits geothermal: the drive heat comes from brine that is otherwise idle in summer, so the
geothermal source runs more hours (2.3). Why it may not: the brine at the chiller must be above the
drive minimum, and its heat is then not available for heating that day; the brine leaving the
generator must still satisfy the brine cooling limits. Check that the combined heat plus drive peak
(2.3) fits the doublets.

## 7.3 Adsorption chillers

Silica-gel/water adsorption chillers run on lower drive temperatures (about 55 to 90 °C in gemini's
model), with a thermal COP about 0.55 [paper: Wang and Oliveira 2006]. They are larger and dearer per kW than absorption chillers [gemini: catalogue rows
`adsorption-chiller-edinburgh-2023`, `-bigee-100-150kw` in `knowledge/data-economics.csv`]. Use
them where the drive water is too cool for absorption.

## 7.4 Compression chillers

An electric vapour-compression chiller is a heat pump in cooling mode:

COP_cooling = η_C · T_evap / (T_cond − T_evap)

A high chilled-water supply and a low condensing (rejection) temperature give a high COP; with a 20
°C chilled-water supply the COP is high [derived from the formula]. Compression chillers are cheap
and compact (price: the case's `economics.capex`, row `compression-chiller-ecos-2023` in
`knowledge/data-economics.csv`). Their electricity costs money and CO2 at the case's grid
intensity. A compression chiller can also run as a **heat recovery chiller**: its condenser heat
goes to a heating network instead of a cooler (7.7).

## 7.5 Free cooling

When the ambient air (dry cooler) or a cold source (ground, lake, sea, the cold side of an aquifer
store) is colder than the chilled-water return by more than an approach, it can cool the water
directly, with only fan or pump power. With a high chilled-water supply temperature (such as 20 °C)
free cooling covers much of the year in a cool climate. Model it as a cooler on the chilled-water
loop before the chiller, or as an ATES cold well.

## 7.6 Heat rejection: dry and wet coolers

- **Dry cooler**: rejects heat to air, no water use; the outlet cannot fall below the air
  temperature plus an approach, typically 5 to 15 K [standard: ASHRAE Handbook, HVAC Systems and
  Equipment, as cited in gemini `gemini/modules/exchangers/cooler.py`].
- **Wet (evaporative) cooler or tower**: rejects to the wet-bulb temperature with an approach
  typically 3 to 8 K [same source]; uses water (evaporation about duty / latent heat).
- Fan power is a small share of the duty (gemini states it as `specific_fan_power`).

The rejection temperature sets the chiller's condensing temperature and its COP (compression) or
capacity (sorption). Size coolers for the hottest air of the case, not the mean.

## 7.7 Heating and cooling in one plant

Integration ideas, in rising order of coupling:

- **Separate**: geothermal heating, electric chillers with their own coolers. Simple; no shared
  risk.
- **Geothermal-driven cooling**: an absorption chiller on the hot water in summer (7.2). Uses the
  doublets in summer; ties the cold to the brine temperature.
- **Heat recovery**: a heat pump or chiller whose cold side serves the cooling network and whose
  warm side serves the heating network at the same time. Both outputs are useful, so the
  combined COP (heat + cold over electricity) is high. Needs simultaneous demand (2.3).
- **Seasonal storage**: chiller reject heat stored underground for winter, winter cold stored for
  summer (6.7).

## 7.8 Choosing the cold source

| Condition | Favoured cold source |
|---|---|
| Brine well above about 80 °C in summer, doublets idle in summer | Absorption (single effect) |
| Brine 55 to 80 °C, cold demand small | Adsorption, or compression |
| Cheap or low-carbon electricity | Compression (with free cooling) |
| High chilled-water temperature and cool climate | Free cooling plus a compression trim |
| Simultaneous heat demand | Heat recovery chiller |
| A jury, client or policy that values geothermal cooling | Absorption, if the economics allow |

The temperature limits in this table restate 7.2 and 7.3; the economic choice must be made by
simulation on the case (Chapter 10). With a high chilled-water supply temperature a compression
chiller often beats absorption on cost, because its COP is high and absorption needs drive water
well above its minimum.

---

# 8 System configurations

This chapter catalogues the plant archetypes, says when each wins, how to split base and peak, and
how to provide redundancy.

## 8.1 A catalogue of archetypes

| # | Archetype | Heating chain | Cooling chain | gemini plant class (closest) |
|---|---|---|---|---|
| A | Direct use + peak boiler | doublets → exchanger → boiler → network | none | `HeatingPlant`, `DoubletHeatPlant` |
| B | Heat pump boost + peak boiler | doublets → exchanger → heat pump (on brine) → boiler | compression chiller | `HeatingHeatPumpCoolingPlant` |
| C | Direct use + absorption cooling | doublets → exchanger → boiler; hot water drives absorption chiller | absorption | `HeatingAbsorptionCoolingPlant` |
| D | Heat pump boost + all chillers | as B | absorption + adsorption + compression | `HeatingCoolingPlant` |
| E | Direct use + all chillers | as A | absorption + adsorption + compression | `HeatingFullCoolingPlant` |
| F | Hybrid with gas use | as B or C, boiler/CHP burns co-produced gas first, surplus flared, desander and inhibitor | absorption | none: a plant built from modules and connections  |
| G | Boiler + CHP on the secondary side | doublet → exchanger → boiler + CHP | none | `BoilerCHPPlant` |
| H | Low-temperature aquifer with heat pump | well pair → exchanger → heat pump | cooling exchanger | `ATESPlant` |
| I | District energy on an aquifer store | heating and cooling networks on one store | store | `DistrictEnergyPlant` |

Class summaries are from the gemini plant modules [gemini: `gemini/plants/*.py`, first line of
each]. 

## 8.2 When each archetype wins

- **Direct use (A)** wins when the brine is hotter than the supply temperature plus the approach:
  no heat pump, lowest electricity. With a large gap it needs a boiler most of the year, which
  becomes expensive and emitting; then go deeper or add a heat pump.
- **Heat pump boost (B, D)** wins when the brine is somewhat colder than the supply, electricity is
  affordable, and the lift is moderate. It also lets the brine be cooled further, so fewer doublets
  give the same heat.
- **Absorption cooling (C, D, E, F)** wins when the brine is hot enough in summer to drive it and
  the doublets would otherwise be idle; it loses when the brine is barely above the drive minimum,
  when electricity is cheap, or when its heat rejection is expensive.
- **Gas use (F, G)** wins when the co-produced gas is substantial: burning it for heat or power
  replaces bought fuel; flaring alone only adds cost and emissions.
- **Multiple chillers of different kinds** (D, E) add flexibility and capital; they pay only if each
  covers a distinct part of the cold load duration curve.

Always compare at least two materially different families on the same case (10.7).

## 8.3 Sizing ratios and the base/peak split

Start from these first sizes, then let the optimiser refine them:

- **Doublets**: the smallest number whose heat at the flow cap and the brine cooling cap covers
  the part of the heating peak they are meant to carry; gemini's `size` takes the smallest count in
  the plant's range that covers the heating peak [gemini: `gemini/study/size.py`]. Then test one
  fewer doublet with a larger heat pump and boiler: the base/peak table (2.2) often shows that a
  base of about half the peak covers about four fifths of the energy.
- **Heat pump**: the share of the heating peak the brine cannot reach, (T_s − T_b) / (T_s − T_r)
  of the peak (6.3) [gemini: same file]; with a finite exchanger approach the real share is
  somewhat larger, which a boiler downstream makes up.
- **Boiler**: by the backup policy (8.4): the whole peak, or only what the doublets cannot reach.
- **Chillers**: the cooling peak shared among them; the last chiller of a series gets the whole
  peak because a sorption unit may deliver less than its rating at peak conditions [gemini: same
  file].
- **Exchanger UA**: from the duty and the chosen approach (6.1); not sized by gemini's `size`.
- **Injection pump**: from the doublets it serves (4.7).

## 8.4 Redundancy, backup and N-1

A heating plant serves people in winter: the loss of one unit must not stop the supply.

- **N-1 rule**: with the largest single unit out, the rest still meet the design peak (or a stated
  share of it). It is common practice in district heating to provide peak and reserve boilers for
  this [textbook: Frederiksen and Werner 2013].
- **Backup policy in gemini**: `params.backup` states it and has no default [gemini:
  `gemini/study/size.py`]:
  - `peak`: the boilers cover the whole heating plus the sorption chillers' drive heat at the step
    where they peak together, **with the doublets off**, so they carry the peak when a doublet is
    out;
  - `none`: the boilers cover only what the doublets cannot reach at their limits.
- `peak` costs more boiler capacity (cheap, 6.5) and buys robustness against a doublet outage and
  against a weaker reservoir (3.7). Choose `none` only with a stated reason (for example several
  doublets where one outage leaves enough), and test the outage case.
- Redundancy of the cold side: two chillers rather than one, or a backup chiller, when the cold
  service is critical (data centres, hospitals).

## 8.5 Availability: running days of a doublet against all-year supply

A doublet needs maintenance (pump changes, cleaning, inspections), so it runs fewer days than the
year has; a case may cap its running days (12.5). The plant as a
whole must still supply every day. Design so that:

- the **days off** fall where the demand is lowest (in summer for a heating plant, unless the
  doublets drive absorption cooling, then in the shoulder seasons); gemini's `control.outages`
  `lowest_demand` places them there [gemini: `gemini/engine/schedule/schedule.py`];
- on those days another unit (boiler, heat pump on another source, a second doublet) covers the
  demand: the backup policy (8.4) must cover the lowest-demand days with the doublet off;
- the running-time limit is counted per doublet, the supply over the whole plant.

---

# 9 Control and operation

This chapter covers how a built plant runs each step: which unit loads first, part load, minimum
loads, seasons and outages, setpoints. Design is judged through this operation (1.3).

## 9.1 Dispatch: the merit order

Each step, the plant meets the demand by loading its units in order of rising marginal cost per
MWh delivered (the **merit order**):

1. geothermal heat through the exchanger (the pump power only);
2. heat pumps on the brine (electricity / COP);
3. CHP, when its electricity is worth more than its extra fuel;
4. boilers on co-produced gas, then on bought gas or electricity.

For cooling: free cooling, then sorption chillers on otherwise unused brine heat, then compression
chillers. The order changes with prices: with expensive electricity a gas boiler may come before a
heat pump at a high lift. The CO2 price belongs in the marginal cost.

In gemini the plant states `control.dispatch`; the only rule is `least_cost`, and the schedule
loads the sources from the cheapest to the dearest [gemini: `gemini/engine/schedule/schedule.py`;
skill `designing-a-plant`, "What gemini can run"]. A case without economics cannot be dispatched
by cost [gemini: `gemini/engine/check.py`].

## 9.2 Part load and minimum loads

- **Doublet**: a production pump has a minimum stable flow (a case may state it as the low end of a flow
  range, 12.5). Below it the doublet must stop, not crawl. On low-demand
  days a doublet either runs at its minimum and the surplus heat must go somewhere (it cannot), or it
  stops and another unit covers the day. Several doublets give finer steps.
- **Heat pump and chiller**: below a minimum part load the compressor stops or cycles [gemini:
  `heatpump.py`, `minimum_part_load`]. A machine sized for the peak runs below its minimum on mild
  days; two smaller machines cover a wider range.
- **Boiler**: modulates over a wide range but loses efficiency with frequent starts; not modelled
  in daily steps.
- **Sorption chillers** need their drive temperature at every load (7.2).

Check minimum loads against the lowest demand of each service (2.1). When the lowest heat demand
is below one doublet's minimum heat (minimum flow times c_p times brine cooling), the doublet will
cycle off on those days; that is fine if the backup covers them (8.5).

## 9.3 Seasonal operation, outages and maintenance

- **Heating season**: doublets at full flow, heat pumps at high load, boilers on peaks.
- **Summer**: heating at its minimum; doublets either drive absorption chillers or run at minimum
  flow or stop. Plan maintenance (the doublet's days off) here, unless the doublets drive cooling.
- **Outages**: the schedule places a doublet's days off; in gemini `control.outages`
  `lowest_demand` [gemini: `gemini/engine/schedule/schedule.py`].
- **Reservoir decline** over years (3.5) lowers the brine temperature; a design that is just
  feasible in year one fails later. Keep margin, or check a later year.

## 9.4 Setpoints and margins

- Each unit on the supply line heats (or cools) to the supply temperature of the case plus (or
  minus) a `supply_margin` the plant states [gemini: `gemini/engine/apply.py`, docstrings of
  `HeatPump`, `Boiler`, `AbsorptionUnit`]. A small positive margin covers losses after the unit.
- A supply temperature requirement applies only while that supply runs: on a day with zero cooling
  demand the idle loop sits at its return temperature, which is no violation (QA-091, see 12.7).
- Do not force circulation through an idle loop to satisfy a rule: it breaks the mass balance and
  the energy accounting (QA-090).

---

# 10 Sizing and optimisation

This chapter says which values to fix and which to search, how to set the search, which objective
to use, and how to avoid wasting a search on infeasible designs.

## 10.1 What to fix and what to search

Fix (state with a source, do not search):

- everything the case owns: demand, temperatures fixed by the case, site, brine, prices;
- properties of equipment classes: Carnot fraction, boiler efficiency, chiller COP, pump
  efficiency, roughness, approach of a cooler type;
- operating limits of equipment: minimum intake pressure, maximum gas fraction, minimum drive
  temperature, minimum part load;
- the backup policy (8.4) and the operating rules (9.1).

Search (design variables), few at a time:

- the number of doublets and their depth;
- the nominal flow per doublet;
- the capacities of heat pumps, chillers and, if not set by the backup policy, boilers;
- where it matters, exchanger UA and network return temperature (a design choice where the case
  allows).

Size first (8.3), then search around the sized design: a search that starts from a feasible design
finds better designs faster.

## 10.2 Search ranges

- A range must contain only designs that are buildable and allowed by the case: doublet count
  within the case's bounds, depth within what the site and drilling allow, flow within the case's
  caps.
- Ranges come from the user, the case or the plant file; never fill a missing range with a typical
  value (skill `designing-a-plant`, `set_ranges`). Propose a range with its reason and get it
  approved.
- Keep ranges and leaves few: gemini refuses fewer than 5 evaluations per search variable, and a
  usable optimum needs about 10 to 20 per variable (`knowledge/handbook-studies.md` section 0.4);
  a search over six leaves therefore needs 60 to 120 evaluations per doublet count.
- A capacity range should reach from the share the geothermal side cannot cover (lower bound) to
  the full peak (upper bound).

## 10.3 Objectives: LCOH, LCOC, LCTS, annualised cost, CO2

- **Annualised cost**: investment spread over the analysis period at the discount rate (the annuity
  or capital recovery factor, Appendix A.9), plus fixed and variable operating cost, energy and
  carbon [gemini: `gemini/study/metrics.py`].
- **LCOH / LCOC**: discounted cost over discounted heat (cold) delivered; for a plant that makes both
  they need an allocation of the cost between heat and cold (a `heat_cost_share` in gemini's
  economics) [gemini: same file].
- **LCTS** (levelised cost of thermal supply): annualised cost over the heat **plus** the cold
  delivered in a year; one figure for both products, no allocation needed [gemini:
  `gemini/evaluate/costs.py`, `lcts`]. Use it to compare heating and cooling plants.
- **CO2**: direct, methane and electricity emissions over the period (5.6).

Minimise one cost objective, report CO2 alongside, and look at the Pareto front when cost and
emissions trade off: a design that is slightly dearer and much cleaner may be the better
recommendation. A cost objective already includes the plant's own CO2 and methane at the case's
carbon price (5.6).

## 10.4 Constraints

A design is feasible only if every requirement of the case passes and no unit leaves its operating
window (11.7). Distinguish:

- **requirements of the case** (third-party limits: flow caps, brine cooling, reinjection, delivered
  energy): never loosened by the designer;
- **operating limits of equipment** (intake pressure, gas fraction, drive temperature): properties
  of the equipment chosen; change the equipment (and source its new limit) rather than delete the
  limit.

## 10.5 Sensitivity and uncertainty

Run them on the chosen design, sensitivity first, uncertainty only when the task asks: how, and how
many runs, in `knowledge/handbook-studies.md` section 3 (skill `economics`).

## 10.6 Staying out of infeasible regions

Most wasted searches come from ranges that include designs that cannot run. Before searching:

- Check the extremes by engineering: at the deepest depth and the highest flow, is the pump intake
  above its minimum and the gas fraction below its limit (4.3, 4.4)? At the shallowest depth, can
  the heat pump reach the supply with its lift (6.4)?
- Keep operating limits on every unit (4.4): without them the optimiser exploits unphysical
  designs.
- Prefer integer-plus-continuous searches with few leaves; fix what does not matter.
- When the search returns `feasible: false`, read the reason (11.7) and change ranges, options or
  the structure, not the requirement.

## 10.7 Comparing families

Compare at least two materially different families (8.1), each sized first, on the same case,
objective, evaluations and seed; report a family that fails by structure with its reason, never
drop it. How to run and read the comparison: `knowledge/handbook-studies.md` sections 5.1 to 5.3
(skill `comparing-designs`).

---

# 11 Designing in gemini

This chapter maps the engineering of Chapters 1 to 10 onto gemini: what the case and the plant
file hold, which modules represent which equipment, how roles and requirements judge a run, the
template plants, the good path from template to compared designs, and how to read and fix
failures. It names modules and fields as they exist in gemini 0.6.17 [gemini: `docs/CHANGELOG.md`]. For
how to call each GeoMind tool, read its skill (11.9).

## 11.1 The case and the plant

gemini separates what is asked from what is built [gemini: `docs/guide.md`]:

- **The case** (`case.json` with CSV files, `economics.json`): the time axis (`time.start`,
  `time.end` excluded, `time.step`), the site (`site.ground`, `site.reservoir`, `site.fluid`,
  `site.air`), the demand per service with its supply and return temperatures, the utilities
  (`utilities.electricity`, `utilities.gas`), the requirements of third parties, the economics, and
  uncertainty ranges. `gm.Case.schema()` describes every key.
- **The plant file**: only the plant: modules, connections, parameters, fluids, sizes, search
  ranges. A plant file that states a case value (gradient, surface temperature, permeability,
  thickness, reservoir pressure, network temperatures) is refused [skill `designing-a-plant`; QA-082].

So one design runs on several cases, and one case judges any plant. The reservoir temperature and
pressure at the plant's depth are derived by the run (3.1, 3.2).

## 11.2 Anatomy of a plant file

A plant file (format 1, kind `plant`) has [gemini: `docs/guide.md`, the plant files under `examples/`]:

- `type`: a plant class (`HeatingHeatPumpCoolingPlant`), which declares the modules and
  connections; or no `type` and explicit `modules` and `connections` (a free plant);
- `size`: structural sizes, such as `size.doublets` with its `value` and `range`;
- `params`: every module's parameters by path (`params.heat_pump.capacity`,
  `params.d0.nominal_flow`, `params.d1.esp.maximum_gas_fraction`, `params.peak_boiler.efficiency`),
  plus the plant's own options: `params.backup`, `params.control.dispatch`,
  `params.control.outages`;
- `fluids`: the fluid of every stream source (a grid, a user, an air module), keyed by module name.

Conventions:

- **Every value with a dimension** is `{"value": 300, "unit": "m3/h"}`; a dimensionless one is a
  number or `{"value": 0.7}`; a text such as `"300 m3/h"` is refused [gemini: `docs/rules.md`].
  Skill `gemini-units`.
- **Design value with a range**: a leaf with `range: {min, max}` is searchable (`depth`,
  `heat_pump.capacity`, `d0.nominal_flow`); a search changes only leaves with a range.
- **Parameters vs controls**: parameters are fixed for the run (capacity, UA); controls vary per
  step and are written by the schedule (an ESP's `frequency`, a doublet's production rate) [gemini:
  `gemini/plants/doublet.py`]. A control stated in the plant file is the stored design's control
  (`params.peak_boiler.temperature_setpoint`) [gemini: `docs/guide.md`].
- **Ports**: every port of every module is connected or named as a plant port; an inlet or outlet
  is `<module>.<port>` (for example `hx.hot_in`), never a bare name (QA-083) [gemini:
  `docs/rules.md`].
- **Doublets** are `d0`, `d1`, ...; a designed `Doublet` needs `depth` (plant level),
  `well_diameter`, `drainage_radius`, `roughness`, `nominal_flow`, `pump_efficiency`,
  `nominal_wellhead_pressure`, and derives its reservoir, wells and pump from them with the case
  [gemini: `gemini/plants/doublet.py`]. `gm.check` names the design value missing, never the
  derived children.
- **No defaults**: a missing value is an issue with its path (`missing_value`); fill it from a
  source (1.5).

## 11.3 Module classes by engineering function

All under `gm.modules.<Name>` [gemini: `gemini/modules/<category>/`]:

| Function (chapter) | Module classes |
|---|---|
| Subsurface (3) | `ProductionReservoir`, `InjectionReservoir`, `ThermalDecline`, `BoreholeField`, `DownholeHeatExchanger` |
| Wells (4) | `ProductionWell`, `InjectionWell` (plant `Doublet`, `NodalDoublet`, `MultiWellPlant` combine them) |
| Pumps (4) | `ESP`, `LineShaftPump`, `InjectionPump`, `CentrifugalPump`, `CirculationPump`, `GasCompressor` |
| Treatment (5) | `Degasser`, `Desander`, `Filter`, `InhibitorDosing`, `Flare`, `Blowdown` |
| Exchangers (6, 7) | `HeatExchanger`, `Cooler` (dry or wet) |
| Heating (6) | `HeatPump` (mode `heating`, or `cooling` as an electric chiller), `Boiler`, `ElectricBoiler`, `CHP` |
| Cooling (7) | `AbsorptionUnit` (chiller or absorption heat pump), `AdsorptionChiller` |
| Storage (6.7) | `ThermalStorage`, `IceStorage`, `AquiferStorage` |
| Piping | `Pipe`, `Mixer`, `Splitter`, `Valve`, `PressurizationTank`, `GasMakeup` |
| Power | `ORC`, `FlashTurbine`, `Separator` |
| Control | `PIDController` |
| Edges of the plant | `ElectricityGrid`, `GasGrid`, `HeatingGrid`, `CoolingGrid`, `WasteGrid`, `ChemicalGrid`, `Atmosphere`, `Formation` |

Totals of a plant are read at its edge modules; mass and energy close on them [gemini:
`docs/guide.md`]. Skill `evaluating-a-module` lists a module's parameters (`describe_module`) and
runs one module at one operating point (`evaluate_module`), which is the way to check a number
(a pump power, a COP at a lift, an exchanger approach) before a whole run.

## 11.4 Roles, quantities and requirements

A requirement of the case names a **role** and a **quantity** of it, never a module name, so one case
judges any plant [gemini: `gemini/plants/roles.py`]. Roles are found from the class or the wiring
(a `HeatPump` whose sink reaches a `HeatingGrid` is a `heat_pump`; one whose source reaches a
`CoolingGrid` is a `chiller`). The table of roles and quantities:

| Role | Quantities |
|---|---|
| `doublet` | `production_flow`, `brine_cooling`, `production_temperature`, `injection_temperature`, `pump_power`, `pump_efficiency`, `intake_pressure`, `intake_gas_fraction`, `reinjection_ratio`, `count`, `wellhead_pressure` |
| `heat_pump` | `cop`, `lift`, `heat_output` |
| `boiler` | `fuel_input`, `heat_output` |
| `chp` | `power_output`, `heat_output` |
| `chiller` | `cop`, `cold_output` |
| `heat_exchanger` | `duty`, `approach` |
| `heating_supply` | `temperature`, `unmet`, `unmet_share` |
| `cooling_supply` | `temperature`, `unmet`, `unmet_share` |

(First rows of the closed table in `roles.py`; `list_plants(plant_class=...)` gives the roles of a
class with their quantities.)

A requirement states `name`, `on` (role), `quantity`, `min` and/or `max` with `unit`, and for a
per-step quantity `over` (`each`, `duration`, ...) and `when` (`running`, ...) [gemini: `docs/guide.md`]. A limit the case does not state is not checked; do not invent
one [skill `designing-a-plant`].

## 11.5 Plant classes: the templates

`gm.plants.names()` lists the classes; `list_plants` shows them with the project's own plant files
[skill `designing-a-plant`]. The classes in gemini 0.6.17 [gemini: `gemini/plants/*.py`]:

| Class | What it is |
|---|---|
| `HeatingPlant` | doublet, exchanger, peak boiler and the heating consumer |
| `HeatingHeatPumpCoolingPlant` | heat pump heating with a peak boiler, and a compression chiller |
| `HeatingAbsorptionCoolingPlant` | heating with a peak boiler and an absorption chiller on the hot water |
| `HeatingCoolingPlant` | integrated heating and cooling on a geothermal doublet (heat pump, three chillers) |
| `HeatingFullCoolingPlant` | heating with all three chillers: every unit but the heat pump |
| `DoubletHeatPlant` | the measured doublet and its surface equipment: filters, degasser, exchanger, pump |
| `BoilerCHPPlant` | nodal doublet with an exchanger, a boiler and a CHP on the secondary network |
| `ParallelExchangerPlant` | nodal doublet with three parallel exchangers on one secondary network |
| `ATESPlant` | low-temperature ATES: well pair, well pump, cooling exchanger and heat pump |
| `DistrictEnergyPlant` | a district heating and a district cooling network on an aquifer store |
| `DistrictNetwork`, `HeatingSubstation`, `CoolingSubstation` | networks and building substations |
| `Doublet`, `NodalDoublet`, `MultiWellPlant` | building blocks for the subsurface side |

A class is read without values: every parameter it needs is an `issue` until filled. Fill them
from 0.7 and the engineers' proposals (0.1, steps 3 to 5); a project's own plant file, when one
fits, starts with its values. gemini's example plant files are not templates for a design (IMP-023): a design is built from a
class and the values of 0.7. A module can be added to a class (for example `thermal_storage`) through `build_plant`
with `from_class` [skill `designing-a-plant`].

## 11.6 The good path

The good path is the checklist of 0.1 with the gates of 0.4: read the case once; choose one family
(0.2); build once from a project plant or a class; one round of engineers' proposals and one
patch; size; simulate a short window, check; fix by 0.5; simulate the whole period, check;
optimise; compare; record design, result, alternatives and study key in the shared state (skill
`working-in-a-team`): a result kept only in a note is lost. Get every number from gemini (a module
evaluation, a short simulation), never by hand [skill `designing-a-plant`].

## 11.7 Reading results and violations

`check_results` (skill `reading-results`) returns gemini's verdict [gemini:
`gemini/evaluate/verdict.py`]:

- `feasible`: true when there is no reason.
- `reasons`, each with a `kind`:
  - `requirement`: a requirement of the case failed (or could not be judged);
  - `failed_step`: steps of the run that failed or were skipped: a simulation problem in the plant;
  - `numerical`: a mass or energy residual above tolerance, or a loop that did not converge;
  - `bound`: an output outside a module's declared limits or past an operating limit (an ESP's
    intake pressure or gas fraction).
  Each reason has a `name`, a `message`, and when known `path`, `value`, `limit`, `worst_step`.
- `requirements`: one check per unit of each requirement; `failures`: failed steps by module and
  code.

Read the worst step: it tells when (the peak day, a zero-demand day) and where (which module). Then
read the module's results around that step (`read_result`) before changing anything. An
`unmet_share` of a run with failed steps is undecided (`passed` null), not failed: fix the failed
steps first [gemini: `docs/CHANGELOG.md` 0.6.13, QA-104].

Engineering checks beyond the verdict (read them in every full-period result):

- brine cooling and injection temperature against chemistry limits (5.3);
- exchanger approach: a very small approach means UA is huge (cost); a large one wastes brine heat
  (6.1);
- heat pump COP and lift over the year (6.4); a heat pump at its minimum lift most of the year is
  oversized or misplaced;
- boiler share of the heat: high means the geothermal side is undersized or the gap is too large
  (6.3); count the heat by source as `knowledge/handbook-economics.md` section 1.4 says, so heat
  that drives a chiller or a heat pump is not counted twice;
- doublet running days against the cap, and where the days off fall (8.5);
- flared gas and methane emissions (5.5, 5.6).

## 11.8 Common failures and their engineering fixes

The table is section 0.5 (symptom, cause, fix, owner); the stop rule after three changes on one
failing requirement is in 0.1.

## 11.9 Which skill to read

| Task | Skill |
|---|---|
| Read or set the case, economics, profiles | `setting-the-case` |
| Build, read, patch, range a plant; families; `optimize`, `run_study` | `designing-a-plant` |
| Simulate, size, optimise a stored design | `simulating-a-plant` |
| Check results, read large results | `reading-results` |
| Superstructure, compare studies | `comparing-designs`, `report` |
| One module at one point; module parameters | `evaluating-a-module` |
| Uncertainty, sensitivity, costs | `economics` |
| Derive a number; a loop or a table | `calculator`, `python` |
| Find a value: files, Knowledge, connectors, web | `finding-sources`, `connectors`, `web-search` |
| Units | `gemini-units` |
| Record work, ask the user, hand back | `working-in-a-team` |
| Lessons from earlier runs | `memory` |

All are in `geomind/geomind/skills/<name>/SKILL.md`.


---

# 12 Worked lessons on an invented case

Each section is one lesson a real case needs, worked on invented numbers so that the method, not
the numbers, carries over. Every number below is **[invented]** or **[derived]** from them; none
belongs to a real site. In a real design every number comes from a tool (0.9).

## 12.1 The invented case

| Item | Value |
|---|---|
| Heating demand | daily, peak 24.0 MW, 102.3 GWh/yr, minimum 2.0 MW |
| Cooling demand | summer only, peak 6 MW |
| Heating supply / return | 110 °C / 55 °C |
| Cooling supply | 16 °C |
| Reservoir | midpoint 2800 m; gradient 32 K/km; surface 10 °C |
| Brine | 1050 kg/m3, c_p 4.2 kJ/kg/K, GLR 0.5 Nm3/m3, gas 70 mol% CH4 and 30 mol% CO2 |
| Limits | 1 to 3 doublets; 60 to 250 m3/h per running doublet; brine cooling at most 45 K; at most 320 running days per doublet; supply on all 365 days |
| Prices (for 12.6) | gas 40 EUR/MWh; CO2 80 EUR/t |

## 12.2 Lesson: the load duration curve and the base/peak split

Sort the daily heating demand and compute, for a base unit of capacity B, the share of the yearly
heat it covers (A.15) and its full-load hours [derived, with a tool]:

| Base (share of the 24 MW peak) | Heat covered | Full-load hours of the base |
|---|---|---|
| 4.8 MW (20 %) | 33.9 % | 7224 h |
| 7.2 MW (30 %) | 46.8 % | 6644 h |
| 9.6 MW (40 %) | 58.4 % | 6218 h |
| 12.0 MW (50 %) | 68.7 % | 5859 h |
| 14.4 MW (60 %) | 77.9 % | 5534 h |
| 19.2 MW (80 %) | 92.4 % | 4920 h |

Read it as 2.2 says: each added MW of base covers less heat than the one before. A geothermal base
of half to two thirds of the peak carries most of the energy; the top of the curve belongs to a
cheap peak unit (6.5). The optimiser finds the exact point (chapter 10); the table says where to
start and whether a result is plausible.

## 12.3 Lesson: sizing doublets for a given peak

1. Reservoir temperature at the depth (3.1): 10 + 32 × 2.8 = 99.6 °C.
2. Heat of one doublet at the caps (3.4, A.5): ṁ = 1050 × 250 / 3600 = 72.9 kg/s;
   P = 72.9 × 4.2 × 45 = 13.8 MW.
3. Doublets to cover the peak: 24.0 / 13.8 = 1.74, so **2 doublets** carry the whole peak at the
   caps. This is the count `size_plant` takes (0.4).
4. Then test one doublet fewer with a larger peak unit: by 12.2 one doublet (13.8 MW, 58 % of the
   peak) still covers about three quarters of the heat. Which wins depends on drilling against
   fuel and carbon: one study decides (10.7).
5. With `backup` `peak` the boiler carries the whole 24 MW with the doublets off (8.4); with
   `none` only what the doublets cannot reach.

The general rule: count = ceil(peak share the geothermal side should carry / heat per doublet at
the caps), checked against the doublet range of the case.

## 12.4 Lesson: a supply temperature above the reservoir temperature

The 110 °C supply is above the 99.6 °C brine (6.3).

- **Direct use is impossible** at this depth: with an approach of 3 K the brine heats the 55 °C
  return to about 96.6 °C at most.
- **Heat pump share** (ideal exchanger, the rule of `size_plant`): (110 − 99.6) / (110 − 55) =
  0.189 of the peak, about 4.5 MW; a finite approach makes it somewhat larger, which a boiler
  downstream makes up.
- **Brine cooling cap on the evaporator**: `minimum_source_outlet_temperature` = 99.6 − 45 =
  54.6 °C. At another depth it moves: compute it again from 3.1 for every depth searched.
- **COP** at 0.5 of Carnot on the outlet temperatures (A.9), sink 110 °C, source 54.6 °C: 0.5 ×
  383.15 / 55.4 = 3.46.
- **Deeper wells** reach the supply plus the approach directly at (110 + 3 − 10) / 32 = 3.22 km:
  a third option, dearer to drill, with no heat pump electricity (3.6).

Three families follow (0.2): heat pump boost (B or D), deeper direct use (A, C or E at about
3.2 km), or a large boiler share. A boiler for a gap that exists all year is the dear one (6.3).

## 12.5 Lesson: a flow range limit and low-demand days

- **Upper bound**: `dN.nominal_flow` at most 250 m3/h; the schedule never runs a doublet above its
  `nominal_flow` [gemini 0.6.15], so a doublet set lower carries less on the peak.
- **Lower bound**: below 60 m3/h a doublet must stop. Its least heat while running is 1050 × 60 /
  3600 × 4.2 × 45 = 3.3 MW, above the 2.0 MW summer minimum: on the lowest days a running doublet
  would make heat nobody takes, so it stops and another unit (a boiler, a heat pump on another
  source, or absorption cooling that uses the brine) covers those days (9.2).
- **Running days**: with at most 320 days per doublet, `params.control.outages` `lowest_demand`
  puts the 45 days off where the demand is lowest, and the backup must cover them (8.5). Several
  doublets give finer steps between the bounds.

## 12.6 Lesson: costing the use of co-produced gas

Per doublet at 250 m3/h and 8000 h/yr [derived]:

| Quantity | Value |
|---|---|
| Gas | 0.5 × 250 = 125 Nm3/h: 87.5 Nm3/h CH4 (62.7 kg/h) and 37.5 Nm3/h CO2 (74.1 kg/h) |
| Fuel value | 87.5 × 35.8 MJ/Nm3 = 0.87 MW, about 7000 MWh/yr |
| Methane | about 502 t/yr |

Flare it (5.5, 5.6): combustion CO2 0.98 × 2.75 × 502 = 1353 t, carried CO2 593 t, unburnt methane
2 % × 502 × 29.8 = 299 t CO2e; about 2245 t CO2e/yr, at 80 EUR/t about 180 kEUR/yr, and no heat.

Burn it in the peak boiler first (`GasMakeup` offers it to the burner, the grid gas tops up, the
flare takes the surplus): the same combustion and carried CO2, little methane slip, and about 7000
MWh of bought gas avoided, worth 7000 × 40 = 280 kEUR/yr, plus the CO2 of that bought gas. So the
rule "burn before you flare" holds whenever the burner needs heat on the days the gas flows; the
surplus in summer still goes to the flare. Price it with gemini (`simulate`, the cost metrics),
not by hand: these numbers only show the order of magnitude.

## 12.7 Lessons from agent runs

From GeoMind's QA of design runs (`documents/project/quality-assurance/BUGS.md`), each a general
rule:

- QA-090: one failing rule chased through 15 variants: stop after three changes aimed at it (0.1).
- QA-091: a supply temperature rule `when: always` fails on days with no demand for that supply;
  the rule holds only while it runs; never force circulation (9.4).
- QA-082: case values written into a plant are refused (11.1).
- QA-083: an inlet is `<module>.<port>`; after an internal error change the input (0.5).
- QA-104: `unmet_share` with failed steps is undecided; fix the steps first (11.7).
- QA-119: change the plant's depth, not the case's reference depth (3.2).
- QA-145: 139 knowledge searches for a few equipment values, 27 hand patches and no simulation in
  70 minutes: read 0.7 once, write once, simulate as soon as nothing is missing (0.1, 0.9).
- Operating limits change the answer: in gemini's own example study a search without the pump
  intake limits ranked first a design whose pumps ran at 2 bar intake and 36 % free gas, which no
  standard pump survives; with the limits it fell to fifth [gemini: `examples/` README, "Pump
  intake limits"]. Keep the limits on every unit (4.4, 10.6).

---

# Appendix A: Formulas

Symbols: SI units unless stated; temperatures in K inside ratios.

**A.1 Geotherm.** T(z) = T_s + G · z; with a reference: T(z) = T_ref + G (z − z_ref)
[gemini: `gemini/physics/ground.py`].

**A.2 Hydrostatic pressure.** p(z) = p_ref + ρ g (z − z_ref), g = 9.80665 m/s2 [gemini: same file].

**A.3 Productivity index (steady radial Darcy).** PI = 2π k h / (μ (ln(r_e / r_w) + S)); drawdown
Δp = Q / PI [textbook: Dake 1978]. 1 mD = 9.869e-16 m2.

**A.4 Darcy-Weisbach.** Δp_f = f (L / D) ρ v² / 2; Haaland: 1/√f = −1.8 log10[(ε/D / 3.7)^1.11 +
6.9 / Re]; Re = ρ v D / μ [textbook: Incropera et al. 2007; Haaland 1983, J. Fluids Eng. 105].

**A.5 Thermal power of a doublet.** P = ρ Q c_p (T_prod − T_inj).

**A.6 Free gas fraction, upper bound (all gas free, ideal gas).** With R = GLR · (p_n / p) · (T / T_n),
p_n = 1.01325 bar(a), T_n = 273.15 K: α = R / (1 + R) [derived; ignores solubility, so it
overestimates].

**A.7 Pump power.** P_el = Q Δp / (η_pump η_motor).

**A.8 Heat exchanger.** Q = UA ΔT_lm; ΔT_lm = (ΔT_1 − ΔT_2) / ln(ΔT_1 / ΔT_2); NTU = UA / C_min;
counterflow ε = (1 − exp(−NTU (1 − C_r))) / (1 − C_r exp(−NTU (1 − C_r))), C_r = C_min / C_max;
for C_r = 1, ε = NTU / (1 + NTU) [textbook: Incropera et al. 2007].

**A.9 Heat pump and chiller COP (Carnot fraction).** COP_h = η_C T_sink / (T_sink − T_source);
COP_c = η_C T_source / (T_sink − T_source); gemini uses the outlet temperatures and a minimum lift
[gemini: `gemini/modules/heating/heatpump.py`]. Lorenz: replace T by the log-mean temperatures of the
glides.

**A.10 Sorption chiller characteristic equation.** Q_E = s (ΔΔt − ΔΔt_min), ΔΔt = t_G − a t_AC + r
t_E (mean circuit temperatures, °C); Q_G = Q_E / COP_th; Q_reject = Q_G + Q_E + P_el [gemini:
`absorptionunit.py`, after Hellmann, Schweigler and Ziegler 1999].

**A.11 Doublet breakthrough.** V_B = π L² H (ρc)_a / (3 (ρc)_w); t_B = V_B / Q; (ρc)_a = φ (ρc)_w +
(1 − φ)(ρc)_r [paper: Gringarten and Sauty 1975].

**A.12 Willans line (CHP).** F = F_full (f0 + (1 − f0) L) [textbook: Heywood 1988].

**A.13 Capital recovery factor.** CRF = r (1 + r)^n / ((1 + r)^n − 1); annualised cost = CRF · capex +
fixed opex + variable opex + energy + carbon. LCTS = annualised cost / (heat + cold delivered per
year) [gemini: `gemini/evaluate/costs.py`; the annuity form as in its `npv`].

**A.14 Combustion CO2.** CH4 + 2 O2 → CO2 + 2 H2O: 44/16 = 2.75 kg CO2 per kg CH4; CO2e of methane
released = m_CH4 · GWP.

**A.15 Base load coverage.** Share covered by base B = Σ min(D_t, B) / Σ D_t over the steps.

---

# Appendix B: Rules of thumb and their sources

Orientation only: never an input without its source and the user's approval (1.5).

| Rule | Value | Source |
|---|---|---|
| Continental geothermal gradient | about 25 to 35 K/km | Stober and Bucher 2013 |
| Dutch doublet spacing | about 1 to 2 km | Willems 2016, cited in gemini README |
| Steel pipe roughness (new) | 4.5e-5 m | Moody 1944 |
| Heat pump Carnot fraction | about 0.4 to 0.6; "close to 50 %" | Arpagaus et al. 2018; Frutschi 1996 |
| Heat pump lift range of water-to-water machines | about 10 to 80 K | Arpagaus et al. 2018 |
| Single-effect LiBr absorption | thermal COP about 0.7 (0.7 to 0.8 at 95 °C) | Herold et al. 2016; Techniques de l'Ingénieur BE9735 |
| Double-effect LiBr absorption | COP about 1.0 to 1.3, drive about 150 to 180 °C | Herold et al. 2016 as quoted; Techniques de l'Ingénieur BE9735 |
| Absorption minimum drive temperature | 80 °C | GEMINI operating limit, **[assumption]** |
| Silica-gel adsorption chiller | COP about 0.55, drive about 55 to 90 °C | Wang and Oliveira 2006; gemini model |
| Dry cooler approach | 5 to 15 K | ASHRAE Handbook, HVAC Systems and Equipment |
| Wet cooler approach | 3 to 8 K | same |
| Flare combustion efficiency | 98 % | US EPA AP-42, 13.5 |
| Methane GWP100 (fossil) | 29.8 | IPCC AR6 WG1, table 7.15 |
| Methane LHV | about 50.0 MJ/kg, about 35.8 MJ/Nm3 | combustion tables; per Nm3 derived |
| ESP free gas, standard stages | 18.75 % (75 % / 4) | Baker Hughes Ace Plus page, cited in gemini README |
| ESP free gas, stricter rule | 10 % | Takacs 2009 as quoted, not verified at the book |
| Geothermal scale inhibitor dose | a few to some tens of ppm | Gallup 2009 |
| Hydrocyclone pressure loss | of the order of 1 bar at design flow | Svarovsky 2000, cited in gemini |
| Base at half the peak covers | most of the energy (69 % in the invented case of 12.2) | Frederiksen and Werner 2013 |
| Capital cost: heat pump against gas boiler per MW | about ten times | DEA Technology Data, sheets 40 and 44 (prices: the case's economics) |
| Plate exchanger approach | no general figure confirmed; below 1 K is achievable at a cost | Tranter (vendor); choose by cost |

---

# Appendix C: Glossary

- **Approach**: the smallest temperature difference between the two streams of an exchanger.
- **Backup policy**: the rule that sizes boilers: whole peak with doublets off (`peak`) or only what
  doublets cannot reach (`none`).
- **Base load / peak load**: the steady lower part of the demand / the short high part.
- **Breakthrough**: arrival of injected cold water at the producer.
- **Brine cooling**: production temperature less injection temperature.
- **Bubble point**: pressure below which dissolved gas comes out of solution.
- **Carnot fraction**: real COP over the ideal (Carnot) COP at the same temperatures.
- **Case**: in gemini, everything a plant is asked to do and its surroundings (demand, site,
  utilities, requirements, economics).
- **Cascade**: use of one heat stream by several users in order of falling temperature.
- **COP**: coefficient of performance: useful heat or cold over the energy driving it.
- **Doublet**: a production well and an injection well into one aquifer.
- **Drawdown**: pressure drop from reservoir to well bottom needed for a flow.
- **ESP**: electrical submersible pump.
- **Family**: one plant configuration (structure), searched over its design values.
- **Free cooling**: cooling by a cold ambient source without a chiller.
- **GLR**: gas-liquid ratio, Nm3 of gas per m3 of liquid.
- **GWP**: global warming potential relative to CO2 over 100 years.
- **Intake pressure**: pressure at the pump inlet.
- **LCOH / LCOC / LCTS**: levelised cost of heat / cold / thermal supply.
- **Lift**: temperature difference a heat pump or chiller makes between sink and source.
- **Load duration curve**: demand sorted from highest to lowest.
- **Merit order**: units loaded from the cheapest marginal cost upward.
- **N-1**: supply still met with the largest unit out.
- **Plant file**: gemini's JSON description of a plant: modules, connections, parameters, fluids,
  sizes, ranges.
- **Productivity / injectivity index**: flow per unit drawdown (production / injection).
- **Requirement**: a named limit of the case on a role's quantity.
- **Role**: the function of a unit in a plant (`doublet`, `heat_pump`, `boiler`, `chiller`, ...).
- **Skin**: dimensionless extra pressure loss near the wellbore.
- **Transmissivity**: permeability times thickness (k·h).
- **Verdict**: gemini's judgement of a run: feasible, or the reasons it is not.

---

# Appendix D: References

Textbooks and papers (cited as named; figures quoted through gemini were checked there, not
always in the original):

- Arpagaus, C., Bless, F., Uhlmann, M., Schiffmann, J., Bertsch, S. S. (2018). High temperature heat
  pumps: market overview, state of the art, research status, refrigerants, and application
  potentials. *Energy* 152, 985-1010.
- ASHRAE. *ASHRAE Handbook: HVAC Systems and Equipment* (chapter on cooling towers and fluid coolers).
- Dake, L. P. (1978). *Fundamentals of Reservoir Engineering*. Elsevier.
- DiPippo, R. (2016). *Geothermal Power Plants*, 4th ed. Butterworth-Heinemann.
- Danish Energy Agency. *Technology Data for Generation of Electricity and District Heating*,
  version 0019 (August 2026), data sheets 06, 40, 44, 45.
- Forster, P., et al. (2021). The Earth's energy budget, climate feedbacks and climate sensitivity.
  IPCC AR6 WG1, chapter 7 (table 7.15).
- Frederiksen, S., Werner, S. (2013). *District Heating and Cooling*. Studentlitteratur.
- Frutschi, H. U. (1996). ABB Review 5/1996, pp. 33-34.
- Gallup, D. L. (2009). Production engineering in geothermal technology: a review. *Geothermics* 38,
  326-334.
- Gringarten, A. C., Sauty, J. P. (1975). A theoretical study of heat extraction from aquifers with
  uniform regional flow. *J. Geophys. Res.* 80(35), 4956-4962.
- Hellmann, H.-M., Schweigler, C., Ziegler, F. (1999). The characteristic equations of absorption
  chillers. International Sorption Heat Pump Conference.
- Herold, K. E., Radermacher, R., Klein, S. A. (2016). *Absorption Chillers and Heat Pumps*, 2nd ed.
  CRC Press.
- Heywood, J. B. (1988). *Internal Combustion Engine Fundamentals*. McGraw-Hill.
- Incropera, F. P., DeWitt, D. P., Bergman, T. L., Lavine, A. S. (2007). *Fundamentals of Heat and Mass
  Transfer*, 6th ed. Wiley.
- Lindal, B. (1973). Industrial and other applications of geothermal energy. UNESCO, Geothermal
  Energy, Earth Sciences 12.
- Lund, H., et al. (2014). 4th Generation District Heating (4GDH). *Energy* 68, 1-11.
- Mijnlieff, H., et al. (2013). SDE+ reference case, European Geothermal Congress (as cited in gemini).
- Moody, L. F. (1944). Friction factors for pipe flow. *Trans. ASME* 66.
- Stober, I., Bucher, K. (2013). *Geothermal Energy: From Theoretical Models to Exploration and
  Development*. Springer.
- Svarovsky, L. (2000). *Solid-Liquid Separation*, 4th ed. Butterworth-Heinemann.
- Takacs, G. (2009). *Electrical Submersible Pumps Manual*. Gulf Professional (quoted, not verified).
- US EPA. AP-42, 5th ed., section 13.5, Industrial Flares (2018).
- Wang, R. Z., Oliveira, R. G. (2006). Adsorption refrigeration: an efficient way to make good use of
  waste heat and solar energy. *Prog. Energy Combust. Sci.* 32.
- Willems, C. (2016), Dutch doublet spacing.

Catalogues and web pages:

- Baker Hughes, Ace Plus gas handler pumps (opened 2026-11-01 by gemini's authors).
- Techniques de l'Ingénieur, BE9735, Absorption chillers: water-lithium bromide systems.
- Thermoeconomic analysis of a single and double effect LiBr/H2O chiller, UNICAMP
  (nipe.unicamp.br).
- Tranter, plate heat exchangers (vendor page).

gemini files (repository `gemini`, version 0.6.17): `docs/guide.md`, `docs/rules.md`,
`docs/CHANGELOG.md`, `docs/cost-sources/`, `gemini/plants/*.py`, `gemini/plants/roles.py`,
`gemini/plants/doublet.py`, `gemini/study/size.py`, `gemini/study/metrics.py`,
`gemini/evaluate/costs.py`, `gemini/evaluate/verdict.py`, `gemini/engine/apply.py`,
`gemini/engine/schedule/schedule.py`, `gemini/physics/ground.py`, the module files under
`gemini/modules/`, `examples/` (README files).

GeoMind skills: `geomind/geomind/skills/<name>/SKILL.md`.
