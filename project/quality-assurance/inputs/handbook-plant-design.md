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

---

# 5 Brine chemistry and associated gas

This chapter covers what the brine carries besides heat: dissolved gas, salts, solids. Each can
stop a plant (scaling, gas-locked pumps, clogged injectors) or add emissions (methane, CO2).

## 5.1 Dissolved gas and why it comes out

Deep brines often carry dissolved gas, mainly CO2 and CH4 (and sometimes N2, H2S). The case
states it as a **gas-liquid ratio** (GLR, Nm3 of gas per m3 of liquid at standard conditions) and a
composition. A normal cubic metre is at 0 °C and 1.01325 bar(a) [gemini:
`examples/hackathon_2026/README.md`].

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
   2021, table 7.15, as quoted in gemini `examples/hackathon_2026/README.md`]. A small methane slip
   weighs much: 2 % unburnt methane at GWP 29.8 adds about 0.6 kg CO2e per kg of methane flared,
   about a fifth of the 2.75 kg from combustion [derived].
3. **Bought electricity** times the grid's CO2 intensity. The intensity is a case value (country,
   year, average or marginal); never a typical value.

gemini's `co2` metric counts all three: direct, methane and electricity [gemini:
`gemini/study/metrics.py`]. The CO2 price of the case (for example an emissions trading price)
turns emissions into cost.

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
percent of the Carnot value" [paper: Frutschi 1996] is the figure the gemini samples use [gemini:
sample plant files]. Consequences:

- **COP falls fast with lift.** At 100 °C supply and 0.5 of Carnot: a 40 K lift gives about 4.7, a
  60 K lift about 3.1 [derived]. Every kelvin of lift saved (deeper wells, smaller approach, lower
  supply) raises the COP.
- **Lorenz form**: with large glides on both sides (water heated by 40 K, brine cooled by 30 K), the
  log-mean temperatures of the glides describe the machine better than the outlet temperatures;
  gemini offers `cop_model` `lorenz` for heating [gemini: `gemini/modules/heating/heatpump.py`].
- **Staging**: two machines in series, each with a smaller lift, reach a higher overall COP than one
  machine with the whole lift, at higher capital cost; worth it for large lifts.
- **Source outlet limit**: the evaporator must not cool the brine below a limit (freezing, scaling,
  or the case's brine cooling cap). gemini states it as `minimum_source_outlet_temperature`; in the
  hackathon sample it is 47 °C, which is 87 °C less the 40 K cap [gemini: sample
  `HeatingHeatPumpCoolingPlant.json`].
- **Minimum lift and minimum part load**: below a minimum lift the formula overstates the COP
  (gemini caps it with `minimum_temperature_lift`, 10 K in the samples, from the lowest lift in
  Arpagaus et al. 2018); below a minimum part load the machine stops (`minimum_part_load`).
- **High supply temperatures** (above about 90 to 100 °C) need high-temperature refrigerants and
  machines; check availability and source a cost for that class [paper: Arpagaus et al. 2018].

Size the heat pump to the heat the brine cannot reach (6.3), not to the whole peak; let a boiler
carry the peak (8.3). Capital cost of large heat pumps in district heating is of the order of 0.74
EUR2015 per W of heat [catalogue: Danish Energy Agency, Technology Data, sheet 40, as cited in
gemini `examples/hackathon_2026/README.md`].

## 6.5 Peak and backup boilers

A boiler is the cheapest capacity per MW: about 0.061 EUR2015/W for a natural gas district heating
boiler [catalogue: DEA Technology Data sheet 44, as cited in gemini
`examples/hackathon_2026/README.md`], an order of magnitude below a heat pump. It is expensive per
MWh (fuel and CO2). Its two jobs:

- **Peak**: cover the top of the load duration curve, the few hundred hours above the base
  capacity (2.2).
- **Backup**: cover the load when a geothermal unit is out (8.4).

Boiler efficiency is a property of the boiler (the samples state 0.9 [gemini: sample plant files]);
source it for the boiler class. An **electric boiler** does the same with electricity at an
efficiency near 1; it pays where electricity is cheap or low-carbon, and needs no gas connection
(gemini `ElectricBoiler`, counted as backup in coverage since gemini 0.6.13 [gemini:
`CHANGELOG.md`]).

## 6.6 Combined heat and power

A gas engine CHP gives electricity and heat from one fuel. In gemini's `CHP` the fuel use follows
the Willans line, fuel = F_full · (f0 + (1 − f0) · L), where L is the electric load fraction [textbook:
Heywood 1988, as cited in gemini `gemini/modules/heating/chp.py`]. A CHP pays when:

- there is a use for its heat for many hours (otherwise its heat is dumped);
- its electricity is worth more than the gas it burns, or the fuel is free co-produced gas (5.5).

Capital cost of a small natural gas engine is of the order of 0.96 EUR2015 per W of electricity
[catalogue: DEA sheet 06, as cited in gemini README].

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
  [textbook: Herold, Radermacher and Klein 2016, as cited in gemini sample files; a summary gives
  0.7 to 0.8 at a 95 °C source, Techniques de l'Ingénieur BE9735].
- **Double effect**: drive about 150 to 180 °C; COP about 1.0 to 1.3 [textbook: Herold et al. 2016,
  as quoted in a LiBr/H2O thermoeconomic study published by UNICAMP (nipe.unicamp.br); Techniques de l'Ingénieur BE9735]; needs
  brine hotter than most low-enthalpy reservoirs.
- **Minimum drive temperature**: below it the machine delivers nothing; the gemini samples state
  80 °C (353.15 K) for a LiBr chiller **[assumption**, a GEMINI operating limit, gemini sample
  files**]**.
- **Characteristic equation**: the available cold falls as the drive temperature falls or the
  cooling water warms. gemini's `AbsorptionUnit` uses the characteristic equation of Hellmann,
  Schweigler and Ziegler (1999), Q_E = s · (ΔΔt − ΔΔt_min), with ΔΔt = t_G − a · t_AC + r · t_E
  [gemini: `gemini/modules/cooling/absorptionunit.py`].
- **Heat rejection** = cold + drive heat (+ small pump power), about 2.4 times the cold at COP 0.7
  [derived]: the cooler or tower must be sized for that.

Why it fits geothermal: the drive heat comes from brine that is otherwise idle in summer, so the
geothermal source runs more hours (2.3). Why it may not: the brine at the chiller must be above the
drive minimum, and its heat is then not available for heating that day; the brine leaving the
generator must still satisfy the brine cooling limits. Check that the combined heat plus drive peak
(2.3) fits the doublets.

## 7.3 Adsorption chillers

Silica-gel/water adsorption chillers run on lower drive temperatures (about 55 to 90 °C in gemini's
model), with a thermal COP about 0.55 [paper: Wang and Oliveira 2006, as cited in gemini sample
files]. They are larger and more expensive per kW than absorption chillers: the gemini catalogue
rows give 0.83 to 0.86 EUR2015/W, nearly three times the absorption rows [gemini:
`examples/hackathon_2026/README.md`, catalogue ids `adsorption-chiller-edinburgh-2023`,
`-bigee-100-150kw`]. Use them where the drive water is too cool for absorption.

## 7.4 Compression chillers

An electric vapour-compression chiller is a heat pump in cooling mode:

COP_cooling = η_C · T_evap / (T_cond − T_evap)

A high chilled-water supply and a low condensing (rejection) temperature give a high COP; with a 20
°C chilled-water supply the COP is high [derived from the formula]. Compression chillers are cheap
and compact; their cost per W of cold in the gemini catalogue is about 0.16 EUR2015/W [gemini:
catalogue row `compression-chiller-ecos-2023`]. Their electricity costs money and CO2 at the case's
grid intensity. A compression chiller can also run as a **heat recovery chiller**: its condenser heat
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
- Fan power is a small share of the duty (gemini states `specific_fan_power`; the samples use 0.02
  **[assumption]**).

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
simulation on the case (Chapter 10). In the hackathon sample, a compression chiller beat
absorption on cost (12.5).

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
| F | Hybrid with gas use | as B or C, boiler/CHP burns co-produced gas first, surplus flared, desander and inhibitor | absorption | `HackathonPlant` (sample plant file, built from modules) |
| G | Boiler + CHP on the secondary side | doublet → exchanger → boiler + CHP | none | `BoilerCHPPlant` |
| H | Low-temperature aquifer with heat pump | well pair → exchanger → heat pump | cooling exchanger | `ATESPlant` |
| I | District energy on an aquifer store | heating and cooling networks on one store | store | `DistrictEnergyPlant` |

Class summaries are from the gemini plant modules [gemini: `gemini/plants/*.py`, first line of
each]. Archetype rows A to F are the six candidates of gemini's hackathon sample; the cooling
column states what each sample plant holds [gemini: `examples/hackathon_2026/plants/`].

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

## 8.5 Availability: 330 days of a doublet against 365 days of supply

A doublet needs maintenance (pump changes, cleaning, inspections), so it runs fewer days than the
year has; a case may cap it (the hackathon: 330 days [competition PDF, p. 2]). The plant as a
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

- **Doublet**: a production pump has a minimum stable flow (the hackathon: 50 m3/h per doublet
  while running [competition PDF, p. 2]). Below it the doublet must stop, not crawl. On low-demand
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
- Keep ranges no wider than needed: each continuous leaf needs about five evaluations [skill
  `designing-a-plant`, `optimize`], so a search over six leaves needs about thirty evaluations just
  to start.
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
recommendation. A cost objective already includes CO2 at the case's carbon price.

## 10.4 Constraints

A design is feasible only if every requirement of the case passes and no unit leaves its operating
window (11.7). Distinguish:

- **requirements of the case** (third-party limits: flow caps, brine cooling, reinjection, delivered
  energy): never loosened by the designer;
- **operating limits of equipment** (intake pressure, gas fraction, drive temperature): properties
  of the equipment chosen; change the equipment (and source its new limit) rather than delete the
  limit.

## 10.5 Sensitivity and uncertainty

- **One-at-a-time sensitivity**: run the chosen design at the low and high end of each uncertain
  value (prices, gradient, permeability, discount rate) and rank the effects (a tornado). It tells
  which values to investigate further.
- **Monte Carlo sampling**: draw the uncertain values from their distributions and report the mean
  and the 5 % and 95 % values of cost and CO2; note draws that fail.
- Sensitivity is of the **chosen** design. Whether the choice itself is robust (would another family
  win at other prices?) needs the comparison run again at those prices.

Skill `economics` runs both; uncertainty runs only when the task asks for it.

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

Compare two to six materially different families (8.1) on the same case, objective, number of
evaluations and seed, each sized first. Report for each: objective value, CO2, feasibility and its
reason, rank, Pareto membership. A family that fails by structure (no cooling unit for a cooling
demand) is reported as infeasible with that reason, not dropped silently. Skill
`comparing-designs` (and `run_study` in `designing-a-plant`) describe the tools; a superstructure
search (`evolve_structure`) explores structures beyond the hand-picked families.

---

# 11 Designing in gemini

This chapter maps the engineering of Chapters 1 to 10 onto gemini: what the case and the plant
file hold, which modules represent which equipment, how roles and requirements judge a run, the
template plants, the good path from template to compared designs, and how to read and fix
failures. It names modules and fields as they exist in gemini 0.6.13 [gemini: `CHANGELOG.md`]. For
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

A plant file (format 1, kind `plant`) has [gemini: `examples/hackathon_2026/plants/*.json`]:

- `type`: a plant class (`HeatingHeatPumpCoolingPlant`), which declares the modules and
  connections; or no `type` and explicit `modules` and `connections` (the `HackathonPlant` sample is
  written this way);
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
per-step quantity `over` (`each`, `duration`, ...) and `when` (`running`, ...) [gemini:
`examples/hackathon_2026/case.json`]. A limit the case does not state is not checked; do not invent
one [skill `designing-a-plant`].

## 11.5 Plant classes: the templates

`gm.plants.names()` lists the classes; `list_plants` shows them with the project's own plant files
[skill `designing-a-plant`]. The classes in gemini 0.6.13 [gemini: `gemini/plants/*.py`]:

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

A class is read without values: every parameter it needs is missing until filled. A **complete
plant file** (a project's plant, or a sample such as `examples/hackathon_2026/plants/<Class>.json`)
is a far better start than a bare class: it holds a coherent set of design values. A module can be
added to a class (for example `thermal_storage`) through `build_plant` with `from_class` [skill
`designing-a-plant`].

## 11.6 The good path

1. **Read the case** (skill `setting-the-case` for the tools, `designing-a-plant` for what to read):
   demand peaks, energy, overlap (Chapter 2), site, requirements, economics.
2. **Pick families** (8.1, 8.2): one, or two to six for a comparison; mark a family gemini cannot run
   `blocked` with the reason.
3. **Start from a complete plant file**: the project's plant if it has one, else a class whose
   sample file exists; fill the `issues` it lists, each from a source (1.5). Set `params.backup` with
   its reason (8.4). Keep the pump intake limits on every `esp` (4.4).
4. **Build** the plant; continue only when its `missing` count is 0.
5. **Size** (`size_plant`): read the notes: what was sized, what stayed unchanged (exchanger UA,
   CHP), what is broken.
6. **Simulate a short window** around the critical day (the heating peak; also the cooling peak if
   cold is made from brine heat), check, fix; then **simulate the whole period** and check.
7. **Fix** what the check names (11.8), owner by owner. After any change every earlier result of
   that design is stale.
8. **Optimise** few leaves with ranges that come from the case or the user (10.1, 10.2).
9. **Compare** families with one study (10.7); simulate the best for the whole period and check it
   again.
10. **Record** the reference design, its result, the alternatives and the study key in the shared
    state (skill `working-in-a-team`): a result kept only in a note is lost.

Get every number from gemini (a module evaluation, a short simulation), never by hand [skill
`designing-a-plant`].

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
steps first [gemini: `CHANGELOG.md` 0.6.13, QA-104].

Engineering checks beyond the verdict (read them in every full-period result):

- brine cooling and injection temperature against chemistry limits (5.3);
- exchanger approach: a very small approach means UA is huge (cost); a large one wastes brine heat
  (6.1);
- heat pump COP and lift over the year (6.4); a heat pump at its minimum lift most of the year is
  oversized or misplaced;
- boiler share of the heat: high means the geothermal side is undersized or the gap is too large
  (6.3);
- doublet running days against the cap, and where the days off fall (8.5);
- flared gas and methane emissions (5.5, 5.6).

## 11.8 Common failures and their engineering fixes

| Symptom | Engineering cause | Fix |
|---|---|---|
| `missing_value` naming a path | a design value or a case value not stated | give the value from a source; for a designed doublet give the design value (`depth`, `well_diameter`), not the derived child [gemini: `docs/guide.md`] |
| `missing_value` on `params.backup` | backup policy not stated | state `peak` or `none` with its reason (8.4) |
| Plant file refused for a case value | a site or network value written in the plant | remove it; it belongs to the case (11.1) |
| Pipe `PhysicsError`: outlet pressure below zero | friction and static drop exceed the inlet pressure: pipe too narrow or too long for its flow, or the loop pressure too low [gemini: `gemini/modules/piping/pipe.py`] | enlarge the diameter, shorten the pipe, or raise the loop pressure; check the flow is the intended one |
| `bound` on `intake_pressure` or `intake_gas_fraction` | pump set too shallow for the drawdown, or too much flow per well, or too deep a design | set deeper, lower the flow per doublet and add one, wider well, higher wellhead pressure (4.3, 4.4) |
| Heat pump: no duty, source below the minimum | brine already at or below `minimum_source_outlet_temperature` at the evaporator, or a lift below the minimum | move the heat pump upstream in the cascade, lower the exchanger duty before it, or check the limit (6.4) |
| Unit off: below minimum part load | machine too large for a low-demand step | smaller units, or two units, or accept and cover by backup (9.2) |
| Absorption chiller delivers nothing | drive water below `minimum_driving_temperature`, or cooling water too warm | drive from hotter water (first in the cascade), larger cooler, or another chiller (7.2) |
| `heat_delivered` / `cold_delivered` fails | not enough capacity on peak days or outage days, or a unit capped | read the worst step; add boiler/chiller capacity, or check the backup policy covers outage days (8.4, 8.5) |
| `brine_cooling_limit` fails | brine cooled beyond the cap (heat pump on brine too large or its source limit missing) | set the heat pump's `minimum_source_outlet_temperature` to the production temperature less the cap, or lower its capacity |
| `running_time_limit` fails | a doublet runs more days than allowed | outages policy `lowest_demand`, a second doublet, backup that covers the days off (8.5) |
| `numerical` reason | a loop that does not close, or water returned into a fixed-temperature supply | plan where each stream goes; do not mix a colder return into a fixed supply (skill `designing-a-plant`, "What gemini can run") |
| Supply temperature rule fails on zero-demand days | a rule with `when: always` | a case change: the rule holds only while that supply runs (9.4, QA-091); never force circulation |
| `internal` error from a tool | an input gemini did not anticipate | change the input; never repeat the same call (QA-083) |

Three rounds on the same failing requirement without progress: stop, record the best variant and
the conflict with its owner (1.4).

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

# 12 Worked example: the GEMINI hackathon 2026 case

This chapter applies Chapters 2 to 11 to one case: the SPE Europe Energy GeoHackathon 2026 (GEMINI
digital twin). It is an example, not a template: its numbers belong to this case only. Sources: the
three competition files (`GEMINI_Heating_Demand_Daily_2027.csv`,
`GEMINI_Cooling_Demand_Daily_2027.csv`, `GEMINI_Hackathon_Challenge_Requirements.pdf`, dated 28
October 2026) and gemini's sample [gemini: `examples/hackathon_2026/README.md`, `case.json`,
`plants/`, `tests/e2e/expected/hackathon.txt`, `evolve.txt`]. Values the competition files do not
give are in the global Knowledge document `hackathon-2026-assumptions.md`, each labelled.

## 12.1 The case

| Item | Value | Source |
|---|---|---|
| Heating demand | 365 daily values; peak 30.0 MW on 28 January; 111.67 GWh/yr | CSV, PDF p. 1 |
| Cooling demand | 365 daily values; peak 10.0 MW on 19 July; 23.74 GWh/yr | CSV, PDF p. 1 |
| Supply temperatures | heating 100 °C, cooling 20 °C, fixed | PDF p. 2 |
| Return temperatures | a design choice of the team; the sample uses 60 °C and 25 °C | organisers; sample **[assumption]** |
| Reservoir | midpoint 2500 m TVD, 100 m thick, 200 mD, 250 bar(g) | PDF p. 2 |
| Ground | gradient 30 °C/km, surface 12 °C | PDF p. 2 |
| Brine | 1030 kg/m3, 0.40 mPa·s, GLR 0.8 Nm3/m3, gas 80 mol% CH4 and 20 mol% CO2 | PDF p. 2 |
| Doublets | 1 to 3 | PDF p. 2 |
| Flow per doublet | 50 to 300 m3/h while running | PDF p. 2 |
| Brine cooling | at most 40 K, producer to injector | PDF p. 2 |
| Pump efficiency | 70 % | PDF p. 2 |
| Reinjection | equal liquid volumes | PDF p. 2 |
| Doublet operation | at most 330 days; the whole system meets demand on all 365 days | PDF p. 2; organisers |
| Depth | may change; hydrostatic pressure and the gradient for another depth | PDF p. 2; organisers |
| Grid CO2 intensity | 300 g/kWh | organisers |

The sample's case states the requirements as eight named rules: `doublet_count`,
`production_flow_range`, `brine_cooling_limit`, `running_time_limit`, `pump_efficiency`,
`full_reinjection` (ratio 0.99999 to 1.00001, a band of the sample), `heat_delivered` and
`cold_delivered` (unmet share at most 1 %, a tolerance of the sample) [gemini:
`examples/hackathon_2026/README.md`].

## 12.2 Demand analysis

**[derived** from the two CSVs**]**:

- Heating: mean 12.75 MW, minimum 2.673 MW (heat demand on all 365 days), full-load hours about
  3720 h. More than 14 MW on 161 days; more than 28 MW on 4 days.
- Cooling: demand on 219 days, full-load hours about 2370 h.
- Heat plus cold in one day: at most 30.0 MW. On cooling days the heat demand ranges from 2.673 to
  18.9 MW.
- Base/peak: a heating base of 15 MW (half the peak) covers 78.4 % of the heat; 21 MW covers 93.4 %
  (table in 2.2).

Reading: a peaky heating demand with a long low summer tail. A base of one to two doublets plus a
cheap peak unit fits; the summer tail is far below one doublet's capacity, so either the doublets
also drive cooling in summer or they take their days off then.

## 12.3 Subsurface and one doublet

**[derived**, formulas in Appendix A**]**:

| Quantity | Value |
|---|---|
| Reservoir temperature at 2500 / 3000 / 3500 m | 87 / 102 / 117 °C |
| Reservoir pressure at 3000 / 3500 m (from 250 bar(g) at 2500 m, hydrostatic) | about 300.5 / 351.0 bar(g) |
| Productivity index (radial Darcy, r_e 1000 m, r_w 0.122 m, zero skin) | about 12.4 m3/h/bar |
| Drawdown at 300 m3/h | about 24 bar |
| Friction in a 0.244 m well at 300 m3/h | about 0.96 bar/km |
| Mass flow at 300 m3/h | 85.8 kg/s |
| Heat at 300 m3/h and 40 K (c_p about 4.2 kJ/kg/K, an assumption: the PDF gives none) | about 14.4 MW |
| Brine leaving at 87 °C less 40 K | 47 °C, the sample heat pump's `minimum_source_outlet_temperature` |

Consequences (6.3, 8.3):

- 87 °C brine cannot give a 100 °C supply directly. Brine at 87 °C can preheat 60 °C return water
  to about 87 °C less the approach; the remaining lift to 100 °C needs a heat pump, a boiler, or
  wells deeper than about 3000 m (102 °C less the approach) [derived].
- The share of the peak the brine cannot reach (ideal exchanger) is (100 − 87) / (100 − 60) =
  0.325, about 9.75 MW of the 30 MW peak [derived, the rule of `gm.study.size`].
- One doublet (about 14 MW at the caps) cannot carry the 30 MW peak; two or three doublets, or one
  or two plus a heat pump and a boiler.
- Sensitivity: the gradient (25 to 35 K/km) moves the LCTS of the best design from 47.16 to 33.76
  EUR/MWh, more than any price [gemini: `tests/e2e/expected/hackathon.txt`].

## 12.4 Gas

Per doublet at 300 m3/h **[derived]**:

- 240 Nm3/h of gas, of which 192 Nm3/h CH4 (137.7 kg/h) and 48 Nm3/h CO2.
- Fuel value about 1.9 MW (methane LHV about 35.8 MJ/Nm3): a useful fuel for a peak boiler, small
  against the 30 MW peak.
- Over 330 days at full flow about 1090 t CH4 per doublet. Flared at 98 %, about 22 t of methane
  escape, about 650 t CO2e at GWP 29.8, besides the combustion CO2.

Free gas at the pump: the stored sample designs at 300 m3/h have intake pressures of at least 7.7
bar and at most 12.1 % free gas over the first 32 days [gemini: README, "Pump intake limits"]; the
upper-bound estimate of 4.4 gives about 12 % at 7.7 bar, consistent. Deep searched designs without
intake limits reach 35.7 % at 2.0 bar: keep the limits.

Design rule for this case: degas after joining the doublets, burn the gas in the peak boiler first
through a `GasMakeup`, flare only the surplus (5.5).

## 12.5 Configurations and what gemini found

Gemini's six sample plants are archetypes A to F of 8.1. Common sample values: 2 doublets (range 1 to
3), depth 2500 m (range 2000 to 3500 m), 300 m3/h per doublet (range 50 to 300), well diameter
0.244 m, pump efficiency 0.7, wellhead pressure 10 bar, drainage radius 1000 m, `backup` `peak`,
`dispatch` `least_cost`, `outages` `lowest_demand`, peak boiler 30 MW (efficiency 0.9), heat pumps
and chillers at 0.5 of Carnot; the heat pump plants state a 15 MW heat pump [gemini:
`examples/hackathon_2026/plants/*.json`].

Search: size, then minimise LCTS, 20 evaluations, seed 0, with the pump intake limits [gemini:
`tests/e2e/expected/hackathon.txt`]:

| Plant | LCTS [EUR/MWh] | CO2 [kt] | Rank | Feasible |
|---|---|---|---|---|
| `HeatingHeatPumpCoolingPlant` (heat pump, boiler, compression chiller) | 40.34 | 12.9 | 1 | yes, Pareto |
| `HeatingCoolingPlant` (heat pump, boiler, three chillers) | 42.54 | 10.34 | 2 | yes, Pareto |
| `HackathonPlant` (free plant: gas use, desander, inhibitor, absorption) | 44.25 | 13.05 | 3 | yes |
| `HeatingAbsorptionCoolingPlant` | 50.5 | 20.96 | 4 | yes |
| `HeatingFullCoolingPlant` | 55.57 | 22.16 | 5 | yes |
| `HeatingPlant` (no cooling) | 29.79 | 7.827 | 6 | no: `cold_delivered` |

Without the pump intake limits `HeatingFullCoolingPlant` ranks first at 40.29 EUR/MWh, but its
design (3 doublets at 3319 m) runs its pumps at 2.0 bar intake and 35.7 % free gas: unbuildable
with standard stages (4.4). With the limits it falls to 55.57 [gemini: README and
`hackathon.txt`]. This is the clearest example in this handbook of why operating limits belong on
every unit (10.6).

A structure search over 32 valid structures (small budget) found heat pump + boiler + compression
chiller best: 34.58 EUR/MWh, 8.70 kt CO2 [gemini: `tests/e2e/expected/evolve.txt`]. Monte Carlo of
the best ranked design (5 draws): LCTS mean 44.56, p5 40.85, p95 49.41 EUR/MWh; CO2 mean 13.83 kt
[gemini: `hackathon.txt`] (five draws are a demonstration, not a converged estimate).

Engineering reading:

- Heat pump boost wins: at 87 °C brine and 100 °C supply the lift is moderate, and cooling the brine
  further (down to 47 °C) gets more heat per doublet.
- Compression cooling beats absorption on cost in this case: the 20 °C chilled-water supply gives a
  compression chiller a high COP, and absorption needs drive water above its 80 °C minimum, which
  87 °C brine only just reaches after an approach.
- `HeatingCoolingPlant` (with absorption) has lower CO2: a candidate for a recommendation that
  weighs emissions or values geothermal cooling.
- `HeatingPlant` is cheapest only because it delivers no cold: it is infeasible by structure (10.7).

## 12.6 A recommended path

1. Read the case and the demand (12.1, 12.2).
2. Families: A = `HeatingHeatPumpCoolingPlant`, B = `HeatingCoolingPlant` (absorption cooling);
   optionally the free `HackathonPlant` for gas use.
3. Start from the sample plant files; keep `backup` `peak` (a doublet outage must not cut heat);
   keep both pump intake limits.
4. Size, simulate a window around 28 January, check; then the whole year, check.
5. Compare A and B in one study (minimise LCTS, the same evaluations and seed, size first); simulate
   the best for the whole year; report LCTS, CO2, coverage, the Pareto front and the sensitivity.
6. Record design, result, alternatives and study in the state.

## 12.7 Lessons from QA

From GeoMind's QA of agent runs on this case [documents: `project/quality-assurance/BUGS.md` and
the hackathon design guide in Knowledge]:

- QA-090: one failing rule chased through 15 variants for 2 h 40 min: stop after three rounds
  without progress (1.4).
- QA-091: a supply temperature rule `when: always` fails on the 146 days without cooling demand;
  the rule holds only while the supply runs; never force circulation (9.4).
- QA-082: case values written into a plant are refused (11.1).
- QA-083: an inlet is `<module>.<port>`; after an internal error change the input (11.8).
- QA-104: `unmet_share` with failed steps is undecided; fix the steps first (11.7).
- QA-119: change the plant's depth, not the case's reference depth (3.2).

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
| ESP minimum intake pressure | 5 bar | **[assumption]**, gemini sample |
| Geothermal scale inhibitor dose | a few to some tens of ppm | Gallup 2009 |
| Hydrocyclone pressure loss | of the order of 1 bar at design flow | Svarovsky 2000, cited in gemini |
| Base at half the peak covers | most of the energy (78 % in the hackathon case) | Frederiksen and Werner 2013; derived for the case |
| Large heat pump capex | about 0.74 EUR2015/W | DEA Technology Data, sheet 40 |
| Gas DH boiler capex | about 0.061 EUR2015/W | DEA sheet 44 |
| Gas engine CHP capex | about 0.96 EUR2015/W_e | DEA sheet 06 |
| Drilling cost | 1247 / 1845 / 2075 EUR2015/m at about 2300 / 3000 / 4000 m | gemini `docs/cost-sources` (Dutch rows, secondary source) |
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
- Willems, C. (2016), Dutch doublet spacing, as cited in gemini `examples/hackathon_2026/README.md`.

Catalogues and web pages:

- Baker Hughes, Ace Plus gas handler pumps (opened 2026-11-01 by gemini's authors).
- Techniques de l'Ingénieur, BE9735, Absorption chillers: water-lithium bromide systems.
- Thermoeconomic analysis of a single and double effect LiBr/H2O chiller, UNICAMP
  (nipe.unicamp.br).
- Tranter, plate heat exchangers (vendor page).
- Eurostat `nrg_pc_203`, `nrg_pc_205`, `prc_hicp_aind`; Instrat EU ETS 2025 summary (economics of
  the hackathon sample).

gemini files (repository `gemini`, version 0.6.13): `docs/guide.md`, `docs/rules.md`,
`CHANGELOG.md`, `docs/cost-sources/`, `gemini/plants/*.py`, `gemini/plants/roles.py`,
`gemini/plants/doublet.py`, `gemini/study/size.py`, `gemini/study/metrics.py`,
`gemini/evaluate/costs.py`, `gemini/evaluate/verdict.py`, `gemini/engine/apply.py`,
`gemini/engine/schedule/schedule.py`, `gemini/physics/ground.py`, the module files under
`gemini/modules/`, `examples/hackathon_2026/` (README, case, plants), `tests/e2e/expected/`.

GeoMind skills: `geomind/geomind/skills/<name>/SKILL.md`.
