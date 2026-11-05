# Designing Geothermal Heating and Cooling Plants

*A reference handbook for engineers and agents who design plants with gemini*

Version 1, 2026-11-05. Written for the GeoMind project; general, for any case and any site.

---

## Preface

### Who this handbook is for

This handbook is for anyone who designs a geothermal heating and cooling plant: a human
engineer, or an agent of GeoMind (design lead, reservoir, well, process, integration and energy
systems engineers, analysts). It assumes the reader knows basic thermodynamics and hydraulics.
It does not assume the reader knows geothermal practice or gemini.

The aim is a **good** plant: one that meets every demand on every day, uses the reservoir well,
keeps its pumps and exchangers inside their safe windows, costs little per MWh delivered and emits
little. A plant that merely runs in a simulation is not yet a good plant.

### How to read it

- Every chapter starts with what it is for, and every section (`##`) stands on its own: an agent
  may read only the section it needs. Cross-references name the section number (for example
  "see 4.4").
- Chapters 1 to 10 are engineering and hold for any tool. Chapter 11 maps that engineering onto
  gemini: its plant files, modules, roles and the GeoMind skills that drive it. Chapter 12 is one
  worked example (the GEMINI hackathon 2026 case). The appendices hold the formulas, the rules of
  thumb with their sources, a glossary and the references.
- How to call a GeoMind tool is written in exactly one place: that tool's skill. This handbook names
  the skill (`designing-a-plant`, `simulating-a-plant`, `reading-results`, ...) and never re-explains
  a tool's arguments.

### How values are labelled

No number in this handbook is a default. Each carries its source in brackets:

| Label | Meaning |
|---|---|
| **[textbook / paper / standard / catalogue]** | Named in Appendix D, with author and year. |
| **[gemini: path]** | A file of the gemini repository (code, sample plant, README). The value is what gemini states or does; a sample's value is a sample assumption unless the file cites a source. |
| **[derived]** | Computed in this handbook from the values named next to it; the formula is in Appendix A. |
| **[assumption]** | A placeholder with no verified source. It may orient a first guess; it must never enter a design as a fact. A design that uses it records it as an assumption with its reason and gets it approved. |

Where no reliable figure could be confirmed, the handbook says so and tells you how to obtain the
value (from the case, from Knowledge, from a connector, from a gemini calculation) instead of
giving one.

---

## Table of contents

1. Introduction and design philosophy
   - 1.1 What a good plant is
   - 1.2 Demand first
   - 1.3 Design and operation are different problems
   - 1.4 The design loop
   - 1.5 Values, sources and the no-defaults rule
2. Demand analysis
   - 2.1 The demand series and its time step
   - 2.2 Load duration curve: base load and peak load
   - 2.3 Heating and cooling together
   - 2.4 Supply and return temperatures
   - 2.5 Network losses and network pumping
   - 2.6 Demand checklist
3. The subsurface
   - 3.1 Reservoir temperature from the gradient
   - 3.2 Reservoir pressure at depth
   - 3.3 Productivity and injectivity
   - 3.4 Drawdown and the capacity of a doublet
   - 3.5 Thermal breakthrough and doublet spacing
   - 3.6 Choosing the depth
   - 3.7 Subsurface uncertainty
4. Wells and pumps
   - 4.1 Well geometry
   - 4.2 Friction in the wells
   - 4.3 ESP setting depth and intake pressure
   - 4.4 Free gas at the pump intake
   - 4.5 Pump power and efficiency
   - 4.6 ESP or line-shaft pump
   - 4.7 Reinjection pressure and the injection pump
   - 4.8 Wells and pumps checklist
5. Brine chemistry and associated gas
   - 5.1 Dissolved gas and why it comes out
   - 5.2 Degassers and separators
   - 5.3 Scaling, corrosion and inhibitors
   - 5.4 Sand and filters
   - 5.5 What to do with the gas: flare, boiler, CHP
   - 5.6 Emissions: CO2, methane and electricity
6. Surface heat
   - 6.1 Heat exchangers: approach, UA and effectiveness
   - 6.2 Cascading: using the brine more than once
   - 6.3 Temperature reach and temperature lift
   - 6.4 Heat pumps
   - 6.5 Peak and backup boilers
   - 6.6 Combined heat and power
   - 6.7 Thermal storage
7. Cooling
   - 7.1 The cooling service
   - 7.2 Absorption chillers
   - 7.3 Adsorption chillers
   - 7.4 Compression chillers
   - 7.5 Free cooling
   - 7.6 Heat rejection: dry and wet coolers
   - 7.7 Heating and cooling in one plant
   - 7.8 Choosing the cold source
8. System configurations
   - 8.1 A catalogue of archetypes
   - 8.2 When each archetype wins
   - 8.3 Sizing ratios and the base/peak split
   - 8.4 Redundancy, backup and N-1
   - 8.5 Availability: 330 days of a doublet against 365 days of supply
9. Control and operation
   - 9.1 Dispatch: the merit order
   - 9.2 Part load and minimum loads
   - 9.3 Seasonal operation, outages and maintenance
   - 9.4 Setpoints and margins
10. Sizing and optimisation
    - 10.1 What to fix and what to search
    - 10.2 Search ranges
    - 10.3 Objectives: LCOH, LCOC, LCTS, annualised cost, CO2
    - 10.4 Constraints
    - 10.5 Sensitivity and uncertainty
    - 10.6 Staying out of infeasible regions
    - 10.7 Comparing families
11. Designing in gemini
    - 11.1 The case and the plant
    - 11.2 Anatomy of a plant file
    - 11.3 Module classes by engineering function
    - 11.4 Roles, quantities and requirements
    - 11.5 Plant classes: the templates
    - 11.6 The good path
    - 11.7 Reading results and violations
    - 11.8 Common failures and their engineering fixes
    - 11.9 Which skill to read
12. Worked example: the GEMINI hackathon 2026 case
    - 12.1 The case
    - 12.2 Demand analysis
    - 12.3 Subsurface and one doublet
    - 12.4 Gas
    - 12.5 Configurations and what gemini found
    - 12.6 A recommended path
    - 12.7 Lessons from QA
- Appendix A: Formulas
- Appendix B: Rules of thumb and their sources
- Appendix C: Glossary
- Appendix D: References

---

# 1 Introduction and design philosophy

This chapter says what the designer optimises and in what order: demand, then reliability, then
efficiency, then cost and emissions. It also says how design differs from operation, and gives the
loop every design follows.

## 1.1 What a good plant is

A good geothermal heating and cooling plant meets five goals, in this order of priority:

1. **It meets the demand.** Every service (heat at its supply temperature, cold at its supply
   temperature) is delivered on every step of the year, within the tolerance the case states. A
   plant that leaves demand unmet is infeasible, however cheap.
2. **It is robust.** It keeps meeting the demand when one unit is out (a doublet in maintenance, a
   heat pump tripped), when the reservoir turns out somewhat worse than expected, and on the coldest
   and the hottest day. Pumps stay inside their intake pressure and gas windows; exchangers stay
   inside their approach; machines stay above their minimum loads.
3. **It is efficient.** It takes as much heat as it can from the brine (deep brine cooling), at
   the smallest temperature lift a machine must make, with low pumping power. Efficiency is
   measured by delivered energy per unit of bought energy (COP of the plant), not by the efficiency
   of one machine.
4. **It is economic.** The levelised cost of the thermal supply (Chapter 10.3) is low over the
   whole analysis period: investment, fixed and variable operation, energy, carbon.
5. **It emits little.** CO2 from burned gas and bought electricity, and methane from the
   co-produced gas, counted with its global warming potential (5.6).

These goals conflict. A deeper well raises the brine temperature (efficiency) and the drilling
cost (economics) and lowers the pump intake margin (robustness, 4.4). The designer's job is the
best compromise, found by search (Chapter 10) inside the feasible region.

## 1.2 Demand first

Every design decision follows from the demand: its peak, its energy, its shape over the year, its
temperatures, and the coincidence of heating and cooling. Read the demand before choosing
anything (Chapter 2). Two errors are common:

- **Sizing on the peak alone.** A plant sized so the geothermal source covers the peak runs at
  part load most of the year and costs too much. The base/peak split (2.2, 8.3) decides how much of
  the peak the geothermal source should carry.
- **Sizing on the energy alone.** A plant sized on the mean power cannot deliver on the peak day.
  Peak capacity is usually cheap (a boiler, 6.5); energy is what the geothermal source should
  supply.

## 1.3 Design and operation are different problems

- **Design** fixes what is built: the number and depth of doublets, the well diameter, the pump,
  the exchangers, the heat pumps, chillers, boilers and their capacities, the network temperatures.
  These are decided once and are expensive to change.
- **Operation** decides, each step, how the built plant meets that step's demand: which units run,
  at what load, at what setpoint (Chapter 9).

A design is judged by simulating its operation over a representative year (or the case's period)
with a fixed operating rule. The design is good only if a sensible operating rule makes it meet
every requirement. A design that needs a clever operating rule to survive is fragile.

## 1.4 The design loop

Every design, by hand or by agent, follows the same loop:

1. **Read** the case: demand, site, utilities, requirements, economics (Chapter 2, 3).
2. **Choose** one or a few configurations (families) that can meet the services (Chapter 8).
3. **Complete** the plant: every design value stated, from a sourced value or a labelled
   assumption (1.5).
4. **Size** it: first capacities from the demand peaks and the subsurface (8.3, 10.1).
5. **Simulate** a short window around the critical day, then the whole period.
6. **Check** the results against the requirements and the safe windows of each unit (11.7).
7. **Fix** what the check names, owner by owner; never loosen a requirement (11.8).
8. **Optimise** the few values that matter, inside sensible ranges (Chapter 10).
9. **Compare** the families on the same case and objective, and pick one with its reasons.

Steps 5 to 7 repeat until the check passes. A loop that makes no progress on the same failing
requirement after three rounds is a sign that the configuration is wrong, not the numbers: change
the structure (8.2) or report the conflict [gemini-hackathon design guide, QA-090 lesson: see 12.7].

## 1.5 Values, sources and the no-defaults rule

A design is only as good as its inputs. Three rules hold in GeoMind and in gemini [gemini:
`docs/rules.md`, "No defaults"]:

- **No default values.** Nothing a user must decide (a price, a temperature, a limit, an
  efficiency) has a default. A missing value is an error that names its path, never silently
  filled.
- **Every value has a source.** In order of preference: the user's files; the Knowledge base
  (RAG); a connected server (MCP); a published source found on the web; and only then a labelled
  engineering assumption that the user approves with its reason (skills `finding-sources`,
  `connectors`, `web-search`).
- **Derive, never guess.** A number that can be computed (a heat duty from a flow and a
  temperature difference, a pressure at depth) is computed with a tool (skills `calculator`,
  `python`, `evaluating-a-module`) and cited by its calculation, never worked out in the head.

The typical values in this handbook orient a first guess and help to recognise a wrong result.
They are not inputs.

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

Example, on the GEMINI hackathon heating demand (peak 30.0 MW, 111.67 GWh/yr) **[derived** from
the case's CSV**]**:

| Base capacity (share of peak) | Share of yearly heat covered | Equivalent full-load hours of the base unit |
|---|---|---|
| 6 MW (20 %) | 40.8 % | 7600 h |
| 9 MW (30 %) | 55.3 % | 6863 h |
| 12 MW (40 %) | 67.8 % | 6312 h |
| 15 MW (50 %) | 78.4 % | 5840 h |
| 18 MW (60 %) | 87.1 % | 5406 h |
| 21 MW (70 %) | 93.4 % | 4965 h |
| 24 MW (80 %) | 98.1 % | 4563 h |

Read it as an economist: each added MW of base capacity covers less energy than the one before.
The base unit is worth adding while the energy it covers, at the difference in variable cost
between base and peak supply, pays for its annualised investment. The optimiser (Chapter 10)
finds that point; the table tells you where to start the search and whether a result is
plausible. A design whose geothermal base covers less than about half the heat of a demand like
this one wastes the subsurface; one whose base is sized for the peak buys capacity that runs a few
days a year [derived from the table].

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
  pipe, see 11.8): give the pipe a sensible diameter for its flow, and the loop enough pressure.

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
it with the wells' heat transfer coefficient [gemini: sample plant files, `heat_transfer_coefficient`
10 W/m2/K, an assumption].

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
  2016, as cited in gemini: `examples/hackathon_2026/README.md`];
- several doublets in one reservoir interfere: give each its own drainage area.

gemini models breakthrough with the `ThermalDecline` module [gemini: `gemini/modules/subsurface/
thermaldecline.py`]. A one-year simulation cannot show decline that sets in after decades: check
t_B with a calculation and state it.

## 3.6 Choosing the depth

Depth is a design choice whenever the case allows it. Deeper wells give:

- **hotter brine** (3.1): more heat per m3, a smaller temperature lift for a heat pump, possibly a
  direct supply without a heat pump;
- **higher drilling cost**: cost per metre rises with depth [catalogue: gemini
  `docs/cost-sources`, rows `drilling-nl-2013-2300m`, `-3000m`, `-4000m`: 1246.83, 1844.74 and
  2075.37 EUR2015/m];
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

In the hackathon example the gradient moved the LCTS more than any price: 47.16 EUR/MWh at 25 K/km
against 33.76 at 35 K/km, while permeability from 100 to 400 mD moved it by 2.3 EUR/MWh [gemini:
`tests/e2e/expected/hackathon.txt`, one-at-a-time sensitivity of the best design].

---

# 4 Wells and pumps

This chapter covers the production and injection wells and their pumps: geometry, friction, ESP
setting depth, intake pressure, free gas, pump power, and reinjection.

## 4.1 Well geometry

- **Depth**: the true vertical depth of the reservoir midpoint (3.6). Deviated wells are longer
  than their vertical depth; count measured depth for drilling cost and friction.
- **Inner diameter** of the production casing: sets friction (4.2) and the largest pump that fits.
  Geothermal production wells are commonly completed with 9 5/8" or 7" production casing [textbook:
  Stober and Bucher 2013; verify for the site]; the gemini samples use 0.244 m [gemini: sample plant
  files, an assumption of the sample].
- **Wall roughness**: new commercial steel about 4.5e-5 m [textbook: Moody 1944, as cited in gemini
  sample files]; scaling and corrosion raise it over time.

## 4.2 Friction in the wells

Single-phase friction in a pipe follows Darcy-Weisbach:

Δp_f = f · (L / D) · ρ v² / 2

with f from the Moody chart or the Colebrook/Haaland correlation. Friction rises with the square of
the flow and the inverse fifth power of the diameter at constant flow. Example [derived]: brine of
1030 kg/m3 and 0.4 mPa·s at 300 m3/h in a 0.244 m pipe flows at 1.78 m/s (Re ≈ 1.1e6, f ≈ 0.0143),
giving about 0.96 bar per km.

Above the bubble point the flow is single-phase; where gas comes out of solution (5.1) the flow is
two-phase and needs a two-phase correlation (gemini states `BeggsBrill` in the samples [gemini:
sample plant files]).

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
no free gas reaches the pump; that needs the fluid's PVT. Without it, the gemini samples use 5 bar
as a minimum intake pressure, explicitly **[assumption]** with no verified source [gemini:
`examples/hackathon_2026/README.md`, "Pump intake limits"].

## 4.4 Free gas at the pump intake

When the brine carries dissolved gas (5.1), every bar of intake pressure lost releases more free
gas. A centrifugal pump stage handles a limited gas volume fraction before its head degrades and it
gas-locks:

- standard stages: about 18.75 % free gas by volume (75 % for gas-handler stages, divided by four)
  [catalogue: Baker Hughes, Ace Plus gas handler pumps, as quoted in gemini
  `examples/hackathon_2026/README.md`];
- a stricter rule of thumb of 10 % for a standard pump is quoted from Takacs (2009) but was not
  verified at the book [gemini: same README].

An upper-bound estimate of the free gas fraction treats all gas as free (no solubility) and ideal
[derived, Appendix A.6]:

α ≈ GLR · (p_n / p) · (T / T_n) / (1 + GLR · (p_n / p) · (T / T_n))

With GLR 0.8 Nm3/m3 and 87 °C at the intake this gives about 10 % at 10 bar(a) and about 18 % at
5 bar(a) [derived]. Two consequences:

- the gas limit and the intake pressure limit are linked: deeper, hotter, higher-flow designs pull
  the intake pressure down and the gas fraction up together;
- without these limits an optimiser drifts toward deep, high-flow designs that a real pump cannot
  run. In the hackathon sample, searches without the limits reached 35.7 % free gas at 2.0 bar
  intake (3 doublets at 3319 m) [gemini: `examples/hackathon_2026/README.md`]. **Keep both limits on
  every ESP.**

Remedies when the limits bind: set the pump deeper, lower the flow per doublet and add a doublet,
choose a larger well diameter (less friction), keep a higher wellhead pressure, or specify a
gas-handling pump (with a sourced limit).

## 4.5 Pump power and efficiency

Hydraulic power is Q · Δp; electric power is Q · Δp / (η_pump · η_motor). The pump must lift the
brine from the dynamic level to the surface and deliver it at the wellhead pressure, against
friction. Example [derived, rough]: at 300 m3/h with about 24 bar of drawdown (Chapter 12.3), 2.4 bar
of friction and 10 bar of wellhead pressure, the head is of the order of 37 to 40 bar and the
electric power at 70 % efficiency about 0.47 MW per doublet, about 3 % of the 14 MW of
heat the doublet gives at 40 K. Compute it with gemini (skill `evaluating-a-module`) for the real
design.

Pump efficiency is a property of the pump at its operating point; it falls away from the best
efficiency point. A case may fix it (the hackathon fixes 70 % [competition PDF, p. 2]).

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

