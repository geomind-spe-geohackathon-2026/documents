**Handbook: studies of a plant: sizing, sensitivity, uncertainty and optimisation** (`knowledge/handbook-studies.md`)

A general engineering reference book on how to ask a simulator more than "does this design work":
what size it should be, which inputs matter, how sure the answer is, and which design is best. It
holds for any plant and any case; every example uses invented numbers. Each lesson names its
source (chapter 11). Checked against gemini 0.6.34 (`gm.study`, `gm.Study`) and geomind's study
tools on 2026-11-05.

Cite as `knowledge/handbook-studies.md §<n.m>`. Section numbers are stable: new material is added
as new sections, never by renumbering. Read by section: the outline first, then only the sections
the task needs. How to call each tool: chapter 12 here, and skills `simulating-a-plant`
(`size_plant`, `optimize`), `comparing-designs` (`run_study`, `compare`, `evolve_structure`,
`list_studies`, `read_study`) and `economics` (`sample_uncertainty`, `sensitivity`). The design:
`knowledge/handbook-design.md`; costs: `knowledge/handbook-economics.md`; the report:
`knowledge/handbook-report.md`.

## 0.0 Outline

- 0 Quick reference: 0.1 rules, 0.2 which study answers which question, 0.3 decision order,
  0.4 how many simulations, 0.5 checklist, 0.6 do only what was asked
- 1 What a study is: 1.1 in gemini, 1.2 through the tools, 1.3 metrics, 1.4 calibration
- 2 Sizing: 2.1 what it does, 2.2 what it does not, 2.3 after sizing
- 3 Sensitivity and uncertainty: 3.1 one-at-a-time sensitivity and its scope, 3.2 Monte Carlo,
  3.3 sensitivity first, 3.4 reading a tornado, 3.5 limits of one-at-a-time, 3.6 local and
  global methods, 3.7 percentiles and P10/P90, 3.8 failed and infeasible draws, 3.9 what the
  inputs must be
- 4 Optimisation: 4.1 what gemini searches, 4.2 feasibility, 4.3 ranges, 4.4 reading an optimum,
  4.5 budget and seeds, 4.6 an optimum that is not the optimum
- 5 Comparing designs: 5.1 families first, 5.2 a fair comparison, 5.3 structure search and
  several objectives
- 6 Reading a study: 6.1 the whole study, 6.2 plant versions, 6.3 stale studies, 6.4 digits
- 7 Common mistakes
- 8 When nothing is feasible
- 9 Worked example (invented numbers)
- 10 Glossary
- 11 Sources
- 12 The study tools argument by argument: 12.1 size_plant, 12.2 optimize and set_ranges,
  12.3 sensitivity, 12.4 sample_uncertainty, 12.5 run_study, 12.6 compare, 12.7
  evolve_structure, 12.8 list_studies and read_study
- 13 Questions agents ask, answered
- 14 Mathematics of the methods: 14.1 Monte Carlo estimators, 14.2 sensitivity measures,
  14.3 sampling plans, 14.4 differential evolution, 14.5 compass search, 14.6 constraints and
  Pareto dominance
- 15 Break-even and switching values
- 16 Robust design and margins
- 17 Verifying a study: convergence, reproducibility, plausibility

---

## 0. Quick reference for the agents

### 0.1 Rules that hold in every section

1. **gemini runs every study; agents choose and quote.** A size, a ranking, a range or a
   sensitivity is a gemini study, never a loop in `run_python` or a table built by hand
   (QA-131: 26 of 41 calls refused, nothing computed).
2. **A study has a name, and its key is its evidence.** Every study is stored as `study/<name>`
   (a name is never reused). Cite the key beside every number it gave; say when `list_studies`
   shows it is not `current` (the case changed after it ran).
3. **Settings have no defaults.** `evaluations`, `samples` and `seed` are chosen with a reason
   (§0.4); a value the agent chose is its own assumption (`source: agent`), never the user's
   (QA-195).
4. **Ranges and uncertainties come from the user or the case**, never invented: search ranges
   through `set_ranges` (after asking), uncertainty through the case (`set_case`).
5. **A stored plant is already a design.** Pass `design/<name>` or a project plant version
   `design/v<N>` to every study tool; never re-type it with `build_plant` (§6.2).
6. **Conclusions rest on the whole study**: on gemini's `best`, `feasible`, `trials`, `summary`
   or `rows`, never on trials read one by one (§6.1).
7. **Do only the study that was asked** (§0.6). **A denied card stands** for the whole request:
   never ask the same tool again in another wording (QA-288).

### 0.2 Which study answers which question

| Question | Study | Tool | gemini |
|---|---|---|---|
| What first sizes does this design need? | sizing | `size_plant` | `gm.study.size` |
| Does this design work over the whole period? | one run | `simulate`, then `check_results` | `gm.simulate`, `gm.evaluate.verdict` |
| Which of these designs is best as they stand? | comparison | `run_study` `method="run"`, or `compare` on stored results | `gm.Study` `run` |
| What values of this design minimise a metric? | optimisation | `optimize` | `gm.study.minimize` |
| Which family is best after each is optimised? | comparison of optimised designs | `run_study` `method="minimize"`, `prepare=["size"]` | `gm.Study` `minimize` |
| Which structure and values are best? | structure search | `evolve_structure` | `gm.study.evolve` |
| Which uncertain inputs move a metric most? | one-at-a-time sensitivity | `sensitivity` | `gm.study.sensitivity` |
| How sure is a metric, as a range? | Monte Carlo | `sample_uncertainty` | `gm.study.sample` |
| At what value does the answer change? | switching value | `sensitivity`, then a check run (§15) | as above |
| What did an earlier study or result find? | read it | `list_studies`, `read_study` | stored study |

### 0.3 Decision order of a design study

1. **Size** the chosen family (`size_plant`) (§2).
2. **Simulate** the sized design and **check** it (§2.3). An infeasible start is information.
3. **Compare families** when more than one can serve the case: size each, rank them with one
   `run_study` (§5.1). Keep the best one or two.
4. **Optimise** the kept family within the approved ranges, the doublet count searchable when
   its range has more than one value (§4).
5. **Check** the optimum and compare it with the sized start (`compare`) (§4.4).
6. **Sensitivity**, then **uncertainty**, only when the task asks for them (§3).
7. Report each number with its study key (`knowledge/handbook-report.md` §6, §7).

Stop rule: finish with the best feasible design or, when none is feasible after a real change of
approach, follow §8. A requirement of the case is never offered as the thing to change.

### 0.4 How many simulations

| Study | Simulations | Choose |
|---|---|---|
| `size_plant` | 1 (the check run) | nothing |
| `simulate` | 1 | nothing |
| `run_study`, `method="run"` | one per design | nothing |
| `sensitivity` | 2 per uncertain value | which values (`values`); every declared one for a broad question (§3.1) |
| `sample_uncertainty` | `samples` | 20 to 50 for a mean; 200 or more before quoting p5/p95 or p10/p90 as numbers (§3.2) |
| `optimize` | up to `evaluations` per doublet count | at least 5 per variable (gemini refuses fewer); 10 to 20 per variable for a usable optimum (§4.5) |
| `run_study`, `method="minimize"` | `evaluations` per design and count | as for `optimize`; the same for every design |
| `evolve_structure` | the runtime's evolve settings | nothing; quote the stop reason |

Invented example: 4 search variables, a doublet range of 1 to 3, `evaluations` 60: up to 180
simulations. At 0.2 s per one-year daily run, under a minute; at 2 s, six minutes. Ask for fewer
evaluations before a study would pass the tool's time limit (15 minutes).

### 0.5 Checklist before a study result is reported

- [ ] The study key `study/<name>` is cited and `current` (or named as made on an older case).
- [ ] `feasible` of the best is true, or the answer says it is the least violating trial and why.
- [ ] The number of trials or draws is given, the failed or infeasible ones counted.
- [ ] Seed and evaluations or samples given, each with who chose it.
- [ ] The comparison is fair: same case, same economics, same effort per design (§5.2).
- [ ] No conclusion from part of a history (§6.1).
- [ ] A broad question covered every declared uncertainty; a narrow one names what was held (§3.1).
- [ ] An optimum at the edge of a range names that range (§4.4).
- [ ] Percentiles named as gemini gives them (p10 = 10th percentile), not swapped (§3.7).
- [ ] Numbers rounded to what the study supports (§6.4).

### 0.6 Do only what was asked

A study costs time, tokens and the user's attention. "Design and check" asks for a design and its
verdict, not a Monte Carlo; "optimise" asks for one optimisation, not a new family; "write the
report" reports the studies that exist (QA-229, QA-257, QA-276). Offer a further study in one
line; never run it unasked. An answer that is ready is given; it is not delayed by extra work.

---

## 1. What a study is

### 1.1 Studies in gemini

A study runs a plant on a case many times with something changed, and summarises the runs.
gemini has one function per kind in `gm.study` (`size`, `minimize`, `sample`, `sensitivity`,
`evolve`, `calibrate`) and one file format, `gm.Study` (`study.json`, `kind: study`): which
`cases` and `plants`, an optional `prepare` (`["size"]`), the `method` (`run`, `minimize`,
`sample`, `sensitivity` or `evolve`), and the settings the method needs. A missing setting is an
issue; one the method does not read is refused. `gm.study.kinds()` lists the kinds and their
settings; `gm.study.metrics()` the metrics.

Every study copies the plant and the case: the originals are never changed. `gm.check` runs first
and raises the plant's issues: a plant with missing values is sized first (`prepare=["size"]` or
`size_plant`), never run half-filled (QA-040). With `gm.runtime.settings(processes=n)` the runs go
to `n` worker processes and give the same result (gemini docstrings, `gemini/study/*.py`).

### 1.2 Studies through the agents' tools

Each geomind study tool runs one gemini study on a stored design (`design/<name>`, or a project
plant version `design/v<N>`) and the state's case, and stores it as `study/<name>`. The tool
returns the summary; `read_study` returns what ran and what came back, with a history summarised
as `trials`; `list_studies` lists the chat's and the project's studies, and the project's results
(`project_result`, newest first), with `current`. Call `list_studies` once and keep its answer
(QA-219).

### 1.3 Metrics

A study reads the metrics of `gm.study.metrics()`: `heating_coverage`, `cooling_coverage`, `cop`,
`peak_heat`, `peak_cold`, `lcoh`, `lcoc`, `lcts`, `annualised_cost`, `co2` and the KPIs of
`gm.evaluate.totals`. A leading `-` maximises (`-cop`). Rank plants that deliver both heat and
cold on `lcts` (`knowledge/handbook-economics.md` §6.3); `npv` and `payback` are not study
metrics. A metric a plant cannot have (cooling coverage of a heating-only plant) is refused by
name: pick another, do not retry (QA-240).

| Metric | Unit | Use |
|---|---|---|
| `lcoh`, `lcoc`, `lcts` | EUR/MWh | cost ranking of heat, cold, or both |
| `annualised_cost` | EUR/y | absolute yearly cost; plants of the same demand only |
| `co2` | t/y | emissions objective or constraint |
| `heating_coverage`, `cooling_coverage` | share | how much demand is met; mostly a constraint |
| `cop` | - | efficiency; maximise with `-cop` |
| `peak_heat`, `peak_cold` | MW | sizing checks |

### 1.4 Calibration

`gm.study.calibrate(plant, dataset, params, start, end)` fits plant parameters to measured
outputs by bounded least squares through gemini's replay (gemini `study/calibrate.py`). It is the
inverse problem: parameters from data, where the other studies go from parameters to outputs.
Rules from parameter estimation (Bard 1974; Tarantola 2005): fit only parameters the data can
see; keep a holdout window to test the fit; a fitted value at its bound is not identified. It has
no geomind agent tool yet: a calibration is asked of a person with gemini, not improvised.

---

## 2. Sizing

### 2.1 What sizing does

`gm.study.size` (`size_plant`) gives a design first sizes from the case, with gemini physics
only: the smallest doublet count in the plant's `size.doublets` range whose heat at the flow
limit and the brine cooling limit covers the heating peak; each doublet's nominal flow at the
flow limit; each boiler by the plant's `backup` policy; each heat pump for the part of the peak
the reservoir cannot reach, `(supply − reservoir) / (supply − return)` of it; each chiller for
the cooling peak; injection pumps for their flow and head, with efficiency and frequency.

Sizing to the peak is the classical first step of plant design: equipment is sized for the
design load, then checked over the whole load duration (ASHRAE Handbook, HVAC Systems and
Equipment, chapters on district heating and cooling; Lund & Toth 2021 for geothermal direct use).

### 2.2 What sizing does not do

It leaves unsized what it has no rule for (a CHP, a heat exchanger, a heat pump that is not
needed) and lists it. It assumes an ideal exchanger for the heat pump share, so a plant with a
heat pump and no boiler may fall short of its supply temperature at the peak. It is a start, not
an optimum: it sizes for the peak, while the cost depends on the whole year (the load duration
curve: a unit sized for the peak runs at part load most hours).

### 2.3 After sizing

`size_plant` simulates the sized design once and lists every requirement it breaks: sizing never
hides an infeasible start. Read that list first. Values the size step derives (stage counts, pump
coefficients) are the size step's, not the user's: never ask the user for them (QA-287).

Invented example: a sized design meets 98.2 % of the heat against a limit of 99 %, with the
doublet count at the top of its range. The next step is a larger heat pump share or another
family (a design change), not a new requirement.

---

## 3. Sensitivity and uncertainty

### 3.1 One-at-a-time sensitivity

`gm.study.sensitivity` (`sensitivity`) moves each value the case declares an `uncertainty` for to
its low and its high end, the others at their case values, and returns one row per value and
metric: `parameter`, `low`, `high`, `at_low`, `at_high`, `effect`, and whether each end's run is
feasible. Rows are sorted by effect, the failed last. Plant parameters are design decisions and
never move. A case with no declared uncertainty gives `missing_value`: see §13.

The ends are `min` and `max` when declared, else `value − std` and `value + std` of a normal.
These are not alike: ±1 std covers about 68 % of a normal, a min-max band all of a uniform. Two
effects from different kinds are compared only with that said (Saltelli & Annoni 2010).

Economic inputs change only the cost formulas; physical ones (permeability, gradient) change the
simulation, and an end can break a requirement: report `feasible_low` and `feasible_high`. To
test values the user names with ranges the user gives: put each range into the case as that
value's `uncertainty` first, then run `sensitivity` with `values` naming those paths (skill
`economics`). A new range of another kind replaces the whole old `uncertainty` (QA-154;
`knowledge/handbook-economics.md` §13.1).

**Which uncertain values a study covers (all of them for a broad question)**

- **A broad question** ("is this a good investment?", "how robust is this design?", "what drives
  the cost?"): cover **every** uncertainty the case declares. Run `sensitivity` and
  `sample_uncertainty` without `values`. Choosing a few decides the answer before the study
  (QA-263).
- **A question that names values** ("how does the electricity price change the LCTS?"): move only
  those (`values` names their paths), and say the others were held at their case values (QA-248).
- **A named value the case declares no uncertainty for**: put the user's range into the case
  first, never a range of your own.

Invented example: a case declares six uncertain values. A study of two prices alone finds
electricity dominant (LCTS 38 to 46 EUR/MWh). Over all six, permeability moves the LCTS from 35
to 55 and the discount rate from 37 to 47: electricity is third.

### 3.2 Monte Carlo uncertainty

A Monte Carlo propagates input distributions through the model by drawing every uncertain input
at once, many times, and running the model on each draw (JCGM 101:2008, GUM Supplement 1). It
needs no linearity and sees interactions. `gm.study.sample` (`sample_uncertainty`) draws every
declared uncertain value (or those in `values`) `samples` times from `seed`, simulates each draw,
and returns per metric `mean`, `p5`, `p50`, `p95`, plus any `percentiles` asked for (`[10, 90]`
gives `p10`, `p90`), with each draw's values and feasibility. The same seed gives the same draws.

How many draws (equations in §14.1):
- A mean's standard error is `σ/√N`: σ = 4 EUR/MWh, N = 30 gives about 0.7.
- A tail percentile's error is about 2.1 times the mean's at the same N for a normal, and at
  N = 30 only about 1.5 draws lie beyond p95 (David & Nagaraja 2003).
- JCGM 101:2008 (clause 7.2) asks, for metrology, M ≥ 10⁴/(1−p): 2×10⁵ for a 95 % interval. For
  engineering decisions a few hundred draws give percentiles to about two significant figures.
- Check convergence with a second seed (§17).

Invented example: 30 draws give mean LCTS 52.1 EUR/MWh and p95 60.3, quoted "about 60". 300
draws give p95 59.8, a second seed 59.5: quote "59.5 to 60".

### 3.3 Sensitivity first, then uncertainty

A sensitivity is cheap (two runs per value) and tells which inputs matter; a Monte Carlo is dear
and tells how sure the answer is. Run the sensitivity first; when two or three inputs carry most
of the effect, their ranges deserve the most care before the Monte Carlo. Inputs whose whole
range moves the metric by less than its reporting precision may be named as negligible.

### 3.4 Reading a tornado

- The bar is `at_high − at_low`; its sign gives the direction. Quote the base value beside it
  (Clemen & Reilly 2014, ch 5).
- An effect is only as wide as the range given: a narrow range makes an input look unimportant
  (Saltelli & Annoni 2010). Name each range's source.
- The sum of OAT effects is not the total spread (interactions, §3.5).
- A lopsided bar (one end moves far more) shows non-linearity or a threshold, often a requirement
  starting to fail at that end: check `feasible_low` and `feasible_high`.
- Compare inputs of different units by elasticity (§14.2), not by raw bars of different kinds.

Invented example: base LCTS 44.0 EUR/MWh. Discount rate 4 % to 10 %: 39.5 to 51.0 (effect 11.5).
Gas price ±30 %: 42.8 to 45.2 (2.4). Gradient 28 to 34 K/km: 47.9 (infeasible: heat coverage
97.6 %) to 42.1. The discount rate drives cost most; the gradient can break the design.

### 3.5 Limits of one-at-a-time

OAT explores only the axes through the base point. In 10 dimensions the points it can reach are a
vanishing share of the input box (Saltelli & Annoni 2010; Saltelli et al. 2019), so it misses
combined extremes (low permeability with high power price) and interactions (Montgomery 2017,
ch 5 on factorial designs). Use it to rank drivers, not to bound the outcome. For "how bad can it
get together", run the Monte Carlo (§3.2); when a requirement may fail only in a combination,
run the combination as its own case with the user's approval.

### 3.6 Local and global methods

| Method | Runs | Gives | Sees interactions | In gemini |
|---|---|---|---|---|
| OAT / tornado | 2k | ranking at a base point | no | `sensitivity` |
| Morris elementary effects | r(k+1), r ≈ 10 to 20 | screening: μ*, σ | flags them (σ) | no |
| Regression on Monte Carlo (SRC) | N ≥ 10k | linear shares of variance | no | from `sample` draws, by a person |
| Sobol indices | N(k+2), N ≈ 10³ | first and total order shares | yes | no |
| Monte Carlo | N | output distribution | yes | `sample_uncertainty` |

k = number of uncertain inputs (Saltelli et al. 2008; Morris 1991; Sobol 2001). With gemini's
tools, say what OAT plus Monte Carlo can and cannot claim; a variance apportionment is not one of
them.

### 3.7 Percentiles and the P10/P90 convention

gemini's `p10` is the 10th percentile: 10 % of the draws lie below it. In petroleum resource
reporting P90 means the value exceeded with 90 % probability, the LOW estimate (SPE-PRMS 2018):
the opposite name for the same number. When a user asks for "P10, P50, P90", ask `percentiles`
`[10, 90]`, give the numbers, and say which convention the names follow (QA-248, QA-299). For a
cost, the high percentile is the pessimistic one; for energy delivered, the low one. The mean
and p50 differ when the distribution is skewed: quote both when they differ by more than the
precision.

### 3.8 Failed and infeasible draws

A draw that breaks a bound (a negative price) fails and is left out of the summary; a draw that
runs but breaks a requirement is infeasible and stays in. Report both counts. Many infeasible
draws are a finding ("the design meets the heat requirement in 82 % of the draws"), often the
most useful number of the study (§16). Never drop them silently to tidy the percentiles. The
share has its own error: `√(q(1−q)/N)`, about ±2 % at q = 0.82 and N = 300 (binomial).

### 3.9 What the inputs must be

- Each distribution comes from the user, the case or a cited source (`knowledge/data-*.csv`),
  never invented. Without one, ask (§13).
- Shape follows knowledge: uniform when only bounds are known; triangular with a most likely
  value; normal for a measured value with a standard error; lognormal for permeability and other
  positive quantities spanning orders of magnitude (Vose 2008, ch 9-10).
- gemini draws each input alone. When two inputs move together (gas and power prices), say that
  the correlation was not modelled and that the spread may be wrong.
- The Monte Carlo describes the inputs' uncertainty, not the model's: a range is conditional on
  the model and on what was held fixed. Say so.

---

## 4. Optimisation

### 4.1 What gemini searches

`gm.study.minimize` (`optimize`) searches the plant's own variables: every parameter with a
`range` (continuous, or integer when the parameter is), every one with `options` (a choice), and
the doublet count when `size.doublets` has a range. Parameters with the same name, role and range
are one variable (three chillers of one range are one capacity). Ranges are set with
`set_ranges`, from the user or the case.

The method (gemini `study/minimize.py`): about half of the budget is differential evolution
(Storn & Price 1997) from a Latin hypercube start (McKay et al. 1979) with the given `seed`, a
population of 5 per variable (at least 5); the rest polishes the best trial by a compass search,
one variable at a time, from a step of 25 % of the range halved to 0.01 % (Kolda et al. 2003;
§14.4, §14.5). The plant as given is one member, so the best is never worse than the start. The
doublet count is searched count by count, each with up to `evaluations` trials; the best of all
counts wins. No gradient is needed: the simulator is a black box with thresholds and integers.

### 4.2 Feasibility in a search

A trial is feasible when its verdict has no reason a design can change: no failed step, every
requirement met, supply temperatures held, no operating limit breached. gemini ranks as Deb's
feasibility rules do (Deb 2000): a feasible trial beats any infeasible one; feasible ones by the
objective; infeasible ones by their total relative violation, so the search moves towards
feasibility without a penalty weight to tune (§14.6). A trial that fails to run is infeasible
with the largest violation.

With no feasible trial, `best` is the least violating one, `feasible` is false, and its `reason`
says why: report it so, never as a solution (§8).

### 4.3 Choosing the ranges

A range too narrow hides the optimum; one too wide wastes trials on designs that cannot work.
Take ranges from the case's limits (a flow band, a doublet count) and engineering bounds the user
approves. Every count the user asks about must be inside the range (QA-253); a search over one
doublet count when the case allows several is a mistake (QA-129).

| Variable kind | Lower bound from | Upper bound from |
|---|---|---|
| Doublet count | demand / heat per doublet at the flow limit | the user's limit, land, budget |
| Flow per doublet | the smallest flow worth a well | the case's flow or drawdown limit |
| Heat pump capacity | peak minus what the reservoir gives | the peak heat |
| Boiler / peak unit | 0 (if the backup policy allows) | the peak heat |
| Chiller capacity | peak cold minus free cooling | the peak cold with margin |

Invented example: a heat pump share searched between 0 and 100 % spends half its trials below
20 %, where the supply temperature is never reached; 30 to 80 % finds the same optimum with half
the evaluations.

### 4.4 Reading an optimum

Compare the optimum with the sized start (`compare` on both results): which variables moved, and
by how much the objective fell. Then:

- **At the edge of a range**: the range, not the plant, set it. Name that range and offer to
  widen it with the user.
- **Flat**: many trials within a small share of the best. The cheapest to build or the most
  robust of them may be the better choice (§16); establish flatness on the whole history (§6.1)
  or by a sensitivity around the best, never from a few trials.
- **Worse than a stored design**: a fresh optimum worse than a design already stored is not an
  improvement; say so and keep the better one (QA-276).
- **Active constraint**: an optimum often sits where a requirement is just met (coverage at its
  limit). That is normal, but it leaves no margin: see §16.

### 4.5 Budget and seeds

- gemini refuses fewer than 5 evaluations per variable. Below 10 to 20 per variable the result is
  a good design, not the optimum (Storn & Price 1997 used populations of 5 to 10 times the
  dimension over many generations; gemini's small budgets trade that for the polish).
- The budget is per doublet count: three counts triple the runs.
- A stochastic optimiser gives a different best for another seed. When two seeds disagree by more
  than the decision needs, the budget was too small (Eiben & Smith 2015, ch 14).
- The seed is the agent's choice and its own assumption (QA-195); give it.

| Variables | Screening budget | Decision budget |
|---|---|---|
| 1-2 | 10-20 | 30-40 |
| 3-4 | 20-40 | 60-80 |
| 5-8 | 40-80 | 100-160 |

### 4.6 An optimum that is not the optimum

An evolutionary search guarantees nothing beyond its trials (Wolpert & Macready 1997). Signs the
reported best is not the optimum: a simple design inside the ranges simulates better; a second
seed finds a better one; the best moved a lot in the last trials. Invented example: a search of
30 evaluations over 3 variables reports 41.3 EUR/MWh with a heat pump of 9.8 MW; a single
simulation at 5 MW, inside the range, gives 39.2, feasible (QA-285). Report the better design,
the budget, and that the search was too short; ask for a larger budget rather than claim an
optimum.

---

## 5. Comparing families, and when to optimise

### 5.1 Compare first, then optimise

A family (a plant structure: how the supply temperature is reached, how cold is made, how a
co-produced gas is used) decides more than any size within it. So:

1. When more than one family can serve the case, size each and rank them with ONE `run_study`
   (`method="run"`, `prepare=["size"]`): one row per family, feasible first, then by objective.
2. Optimise the best one or two (`optimize`), not every family.
3. When the sized ranking is close (within a few per cent), or the best sized family is
   infeasible, optimise each close one with the same budget (`run_study`, `method="minimize"`)
   before choosing (QA-211).
4. When every family fails at the sized start, repair before ranking: a sized start that fails
   all steps is not yet a design (QA-251; §8).
5. A variant the analysis team needs (another cooling option, say) is built and simulated by the
   design team; the analysis team compares the results (QA-347).

Invented example: four families, sized: A 47.9, B 44.6, C infeasible (cold unmet), D 45.1
EUR/MWh. B and D are close: optimise both with 60 evaluations each; B reaches 41.8, D 42.6.
Report the run study and the minimize study, both by key.

### 5.2 A fair comparison

Designs are compared on the same case and economics, with the same effort: a sized start against
an optimised rival is no comparison. Name what each design got (sized; optimised with how many
evaluations and which seed). A family that was not simulated is not ranked; it may be named as
screened out, with the reason. A difference smaller than what changing the seed or a held input
would move is a tie: say so (§3.2, §4.5).

A comparison never changes the project's current plant: studying a design is not adopting it;
adopting is its own step the user asks for (QA-237).

### 5.3 Searching the structure, and several objectives

When the plant states optional modules or choices (a superstructure), `evolve_structure`
(`gm.study.evolve`) searches structures and values together: a genetic algorithm with one
objective, NSGA-II with two or more (Deb et al. 2002), with local compass steps (gemini
`study/evolve.py`). Its settings (population, polish, stop) come from the runtime, not from the
agent; quote the stop reason.

With two or more objectives the answer is a Pareto front: designs no other beats on every
objective. No single best exists until someone states the trade-off (Miettinen 1999). Present the
front, name the extreme designs and the knee, and let the user choose; never pick one silently by
weights of your own. Quote gemini's explanation and front table with the study key (skill
`report`).

Invented example: cost against CO2. P: 40 EUR/MWh, 900 t/y; Q: 43, 400; R: 52, 350. Q is the
knee: 3 EUR/MWh more than P saves 500 t/y; R pays 9 more for 50 t/y. The implied carbon price of
P→Q is 3 EUR/MWh × annual heat / 500 t: compare it with the carbon price in the economics.

---

## 6. Reading a study

### 6.1 Read the whole study, not a sample of it

An optimisation's `history` holds every trial: its values, its objective, its violation (0 when
feasible) and the reason of an infeasible one. A conclusion about the search ("the optimum is
flat", "most designs are infeasible", "two doublets always win") must rest on all trials.

- Quote gemini's summary first: `best`, `feasible`, `trials`, and for a sample or sensitivity its
  `summary` or `rows`. `read_study` summarises a history as `trials`.
- Never page through a history one trial at a time. When the tools cannot summarise what is
  asked, say what is known (best, trials, feasible or not) and that the shape of the search was
  not assessed; a sensitivity around the best answers "how flat" properly (§3).
- Invented example of the mistake: a search of 240 trials; 27 are read, 3 feasible; the answer
  says "only 3 of 27 feasible, the optimum is flat". Nothing in 27 trials says anything about the
  other 213 (QA-205).
- Read a study once and keep its numbers; reviewers and explainers quote the same key rather
  than re-reading it step by step (QA-179). No `run_python` to slice a history (QA-296).

### 6.2 Plant versions are designs

A project's stored plant versions are designs: `design/v<N>` is version N. To rank six versions,
pass `design/v1` to `design/v6` to one `run_study`; never rebuild them with `build_plant`
(re-typing drops values and costs a confirmation each, QA-221). `v<N>` is reserved for versions:
give a new design another name.

### 6.3 Current and stale studies

A study ran on the case of its time. `list_studies` says whether it is `current`; one that is not
is quoted as "made on an older case" or run again. A study is never edited: a new run is a new
study with a new name. After a case change, a result's verdict may differ: re-check before
quoting it as feasible.

### 6.4 How many digits

Quote a number to what the study supports, never gemini's 15 digits (QA-099, QA-299). A Monte
Carlo of 30 draws supports two significant figures of a mean and one of a tail percentile; an
optimum supports the digits by which a second seed agrees. Costs: 0.1 EUR/MWh at most; shares:
0.1 %; capacities: 0.1 MW. The study record keeps the full numbers.

---

## 7. Common mistakes

1. Ranking families sized against one family optimised (§5.2).
2. Optimising before any family comparison, or not optimising close sized families (§5.1).
3. A search over a single doublet count when the case allows several (§4.3).
4. Ranges invented, or so wide most trials cannot work (§4.3).
5. Too few draws for a percentile, or too few evaluations for the variables (§3.2, §4.5).
6. A conclusion from part of a history (§6.1).
7. Rebuilding stored plant versions instead of passing `design/v<N>` (§6.2).
8. A least-violating trial reported as a solution (§4.2, §8).
9. A sensitivity or Monte Carlo written in `run_python` (§0.1).
10. A requirement offered as the thing to change (§8).
11. A study without its key, or a stale one quoted as current (§6.3).
12. A few agent-picked values answering a broad question (§3.1).
13. P10 and P90 swapped between conventions, or said not to exist (§3.7).
14. OAT effects of ±1 std and of min-max ranked together without saying so (§3.1).
15. OAT taken as the bounds of the outcome (§3.5).
16. Infeasible draws dropped silently (§3.8).
17. An optimum at a range edge reported as the plant's optimum (§4.4).
18. A one-seed, short-budget best called "the optimum" (§4.6).
19. A Pareto front collapsed to one design by the agent's own weights (§5.3).
20. Studies nobody asked for (§0.6); 15-digit numbers (§6.4).
21. The agent's own seed or sample count recorded as the user's (§0.1, QA-195).
22. A denied card asked again in other words (§0.1, QA-288).
23. Earlier results searched in Knowledge instead of `list_studies` (§13, QA-294).

---

## 8. When nothing is feasible

A design problem with no feasible trial needs a diagnosis, not more of the same search.

1. **Read the reasons** of the least violating trial: which requirement, by how much, when.
2. **Name the binding cause**: capacity (peak not met), temperature (supply not reached), a limit
   (flow, pressure, drawdown), or a failed step (the model refused the operating point).
3. **Change the approach, one at a time**: another family, another doublet count, another split
   of base and peak load, a wider range the user approves. Re-size after each structural change.
4. **Stop** after real changes of approach fail, and report the best design, its violations and
   the list of what was tried, with each study key.

| Binding cause | Typical design change |
|---|---|
| Peak heat not met | peak unit, larger heat pump, one more doublet |
| Supply temperature not reached | heat pump lift, a boiler in series, lower return |
| Cold not met | larger chiller, another cooling technology |
| Flow or drawdown limit | more doublets at lower flow each |
| Every step fails | a value outside the model's range: read the first failed step |

A requirement of the case is never offered as the thing to change: it is the user's. When the user
asks what would make it feasible, the answer may name the binding requirement and by how much.

---

## 9. Worked example (invented numbers)

A district of 40 GWh/y heat (peak 14 MW) and 6 GWh/y cold; requirements: 99 % heat coverage,
supply 75 °C. The user asks: "Find the cheapest design and tell me how sure the cost is."

1. **Size** three families: direct use with a boiler (D), with a heat pump (H), with heat pump and
   absorption chiller (HA). `run_study` `method="run"` `prepare=["size"]` →
   `study/families_sized`: D 51.0 EUR/MWh feasible; H 46.2 feasible; HA 45.8 infeasible (cold
   supply 9.4 °C against 8 °C).
2. **Close and one infeasible**: optimise H and HA with the same budget, 3 variables, doublets 1
   to 2, 45 evaluations each, seed 1 → `study/families_opt`: H 43.9, HA 42.7, both feasible.
   Seed 2 gives HA 42.9: a gap of 1.2 against a seed spread of 0.2 is real.
3. **Edge check**: the HA heat pump sits at 6.0 MW, the top of its range. The user widens it to
   9 MW; a new search gives 42.4 at 7.1 MW, inside the range.
4. **Sensitivity**, every declared uncertainty (broad question): discount rate first (38.9 to
   47.6), permeability second, its low end infeasible (coverage 98.4 %).
5. **Monte Carlo**, 300 draws, seed 7, percentiles 10 and 90: mean 42.8, p10 39.6, p50 42.5,
   p90 46.9; 21 draws infeasible (7 %). Seed 8: p90 47.1.
6. **Answer**: HA at 42.4 EUR/MWh (keys given). Cost 39.6 to 46.9 between the 10th and 90th
   percentiles, driven by the discount rate; in 7 % of draws low permeability breaks heat
   coverage: a margin or a peak unit is the remedy if that risk matters (§16).

---

## 10. Glossary

- **Design variable**: a plant value the search may change (a range or options).
- **Uncertain input**: a case value with a declared `uncertainty`; never a design variable.
- **Feasible**: every requirement and limit met (gemini's verdict); not the report's `passed`.
- **Violation**: the total relative amount by which requirements are missed.
- **Tornado**: OAT effects sorted by size.
- **Elasticity**: relative change of output per relative change of input (§14.2).
- **Percentile p<n>**: n % of the draws lie below it.
- **Pareto front**: designs no other beats on every objective.
- **Switching value**: the input value at which a decision changes (§15).
- **Budget**: `evaluations` (per doublet count) or `samples`.
- **Seed**: makes a stochastic study repeatable.
- **Current**: a study made on the case as it is now.

---

## 11. Sources

- Saltelli A., Ratto M., Andres T. et al. (2008). *Global Sensitivity Analysis. The Primer*.
  Wiley. (§3.5, §3.6, §14.2)
- Saltelli A., Annoni P. (2010). How to avoid a perfunctory sensitivity analysis. *Environmental
  Modelling & Software* 25, 1508-1517. (§3.1, §3.4, §3.5)
- Saltelli A. et al. (2019). Why so many published sensitivity analyses are false. *Environmental
  Modelling & Software* 114, 29-39; arXiv:1711.11359. (§3.5)
- Morris M.D. (1991). Factorial sampling plans for preliminary computational experiments.
  *Technometrics* 33, 161-174. (§3.6, §14.2)
- Sobol I.M. (2001). Global sensitivity indices for nonlinear mathematical models and their Monte
  Carlo estimates. *Mathematics and Computers in Simulation* 55, 271-280. (§3.6, §14.2)
- Montgomery D.C. (2017). *Design and Analysis of Experiments*, 9th ed. Wiley. (§3.5)
- Clemen R.T., Reilly T. (2014). *Making Hard Decisions with DecisionTools*, 3rd ed. Cengage.
  (§3.4, §15)
- JCGM 101:2008. *Evaluation of measurement data, Supplement 1 to the GUM: Propagation of
  distributions using a Monte Carlo method*. BIPM, doi:10.59161/JCGM101-2008. (§3.2, §14.1)
- David H.A., Nagaraja H.N. (2003). *Order Statistics*, 3rd ed. Wiley. (§3.2, §14.1)
- Vose D. (2008). *Risk Analysis: A Quantitative Guide*, 3rd ed. Wiley. (§3.9)
- SPE, WPC, AAPG, SPEE, SEG, SPWLA, EAGE (2018). *Petroleum Resources Management System
  (PRMS)*. (§3.7)
- Storn R., Price K. (1997). Differential evolution. *J. Global Optimization* 11, 341-359.
  (§4.1, §4.5, §14.4)
- McKay M.D., Beckman R.J., Conover W.J. (1979). A comparison of three methods for selecting
  values of input variables. *Technometrics* 21, 239-245. (§4.1, §14.3)
- Kolda T.G., Lewis R.M., Torczon V. (2003). Optimization by direct search. *SIAM Review* 45,
  385-482. (§4.1, §14.5)
- Deb K. (2000). An efficient constraint handling method for genetic algorithms. *Comput. Methods
  Appl. Mech. Engrg.* 186, 311-338. (§4.2, §14.6)
- Deb K., Pratap A., Agarwal S., Meyarivan T. (2002). NSGA-II. *IEEE Trans. Evol. Comput.* 6,
  182-197. (§5.3, §14.6)
- Miettinen K. (1999). *Nonlinear Multiobjective Optimization*. Kluwer. (§5.3)
- Wolpert D.H., Macready W.G. (1997). No free lunch theorems for optimization. *IEEE Trans. Evol.
  Comput.* 1, 67-82. (§4.6)
- Eiben A.E., Smith J.E. (2015). *Introduction to Evolutionary Computing*, 2nd ed. Springer.
  (§4.5, §17)
- Beyer H.-G., Sendhoff B. (2007). Robust optimization: a comprehensive survey. *Comput. Methods
  Appl. Mech. Engrg.* 196, 3190-3218. (§16)
- Bard Y. (1974). *Nonlinear Parameter Estimation*. Academic Press; Tarantola A. (2005). *Inverse
  Problem Theory*. SIAM. (§1.4)
- ASHRAE (2020). *ASHRAE Handbook, HVAC Systems and Equipment*. (§2.1)
- Lund J.W., Toth A.N. (2021). Direct utilization of geothermal energy 2020 worldwide review.
  *Geothermics* 90, 101915. (§2.1)
- Oberkampf W.L., Roy C.J. (2010). *Verification and Validation in Scientific Computing*.
  Cambridge. (§17)
- gemini 0.6.34 docstrings: `gemini/study/size.py`, `minimize.py`, `sample.py`,
  `sensitivity.py`, `evolve.py`, `calibrate.py`; geomind `geomind/tools/gemini/study.py`,
  `studies.py`.
- QA lessons: `documents/project/quality-assurance/bugs` (numbers given in the sections).

---

## 12. The study tools argument by argument

### 12.1 size_plant

`size_plant(design, name)`. `design`: a stored design reference. `name`: the new design's name
(it is stored as `design/<name>`; not `v<N>`). Choose nothing else: sizing reads the case. Read
the returned `sizing` and the list of broken requirements (§2.3). Typical mistake: re-sizing an
already optimised design, which throws the optimum away.

### 12.2 optimize and set_ranges

`set_ranges(design, ranges, name)` writes the search ranges onto a copy of a design, after the
user approves them (§4.3). `optimize(design, objective, evaluations, seed, name)`:

| Argument | How to choose |
|---|---|
| `design` | the ranged design from `set_ranges` |
| `objective` | the metric the user named; `lcts` for heat and cold, `lcoh` heat only, `-cop` to maximise |
| `evaluations` | per doublet count; table §4.5; at least 5 per variable |
| `seed` | any integer, recorded as the agent's assumption |
| `name` | new and descriptive (`lcts_opt_hp_flow`) |

Mistakes: ranges not set (the search has no variables), the doublet range dropped (QA-129), one
seed taken as final (§4.6). A denied `set_ranges` card ends the search for the request (QA-288).

### 12.3 sensitivity

`sensitivity(design, metrics, name, values=None)`. `metrics`: the asked metrics, at most a few.
`values`: omit for a broad question; the named paths for a narrow one (§3.1). Prerequisite: the
case declares an `uncertainty` for each value moved. Runs 2 per value.

### 12.4 sample_uncertainty

`sample_uncertainty(design, metrics, samples, seed, name, values=None, percentiles=None)`.
`samples`: §0.4 and §3.2. `seed`: the agent's assumption. `percentiles`: extra ones the user asked
for, each 0 to 100, for example `[10, 90]` (§3.7); p5, p50, p95 always come. `values`: as for
`sensitivity`.

### 12.5 run_study

`run_study(designs, method, name, objective, metrics, evaluations, seed, samples, prepare,
values)`: one gemini study over several designs. `method="run"` needs nothing more;
`"minimize"` needs `objective`, `evaluations`, `seed`; `"sample"` needs `metrics`, `samples`,
`seed`; `"sensitivity"` needs `metrics`. `prepare=["size"]` sizes each design first: use it for
unsized families, not for versions already sized and tuned. Same settings for every design (§5.2).

### 12.6 compare

`compare(references, by)`: gemini's ranking of stored results (`result/...`) by the metrics in
`by`, with each run's report. Use it for results that already exist (an optimum against its sized
start, or the newest project result against this chat's); it simulates nothing.

### 12.7 evolve_structure

`evolve_structure(design, objectives, name)`: a superstructure design (optional modules,
choices). One objective gives one best; two or more give a front (§5.3). Settings come from the
runtime; an unset one is refused by name: report that, do not invent it.

### 12.8 list_studies and read_study

`list_studies()`: once per request; gives every chat and project study and the project's results,
with `current`. `read_study(study)`: one study by its key; its history comes summarised as
`trials`. Never read a study again to re-derive numbers already quoted (QA-179).

---

## 13. Questions agents ask, answered

**Where is an earlier result or study of this project?** `list_studies`: project studies and
`project_result` entries, newest first; never `search_rag` for a result id (QA-294).

**The user asked for P10/P90 but gemini gives p5/p95.** Pass `percentiles=[10, 90]` (§3.7).

**How many samples, which seed?** §0.4 and §3.2; the agent chooses, records it as its own.

**The case has no uncertainty for the values to move (`missing_value`).** Uncertainty enters
through the case. Use ranges the user gave, or ranges from a cited Knowledge source the user
approves (the case lead asks once, with the source); never your own (QA-216, QA-259).

**I set a new range and the old `std` is still there.** A new kind replaces the whole
`uncertainty` object; write it whole (QA-154).

**The study fails with a missing plant value.** Size first (`prepare=["size"]`); a value only
the user can give is asked once with its meaning (QA-040).

**Can the analysis team simulate a variant?** No: the design team builds and simulates it; the
analysis team compares (QA-347).

**The user denied the search.** Answer with what is known; do not re-ask (QA-288).

**Is the optimum good enough?** §4.4-§4.6 and §17.

**Which metric for a plant with heat and cold?** `lcts` (§1.3).

---

## 14. Mathematics of the methods

### 14.1 Monte Carlo estimators

For N draws `y_1..y_N` of a metric (unit of the metric, for example EUR/MWh):

- Mean `ȳ = (1/N) Σ y_i`; standard deviation `s = √(Σ(y_i − ȳ)²/(N−1))`; standard error of the
  mean `s/√N`; a 95 % confidence interval for the mean `ȳ ± 1.96 s/√N`.
- The p-quantile `x_p` is estimated by the sorted draw at rank about `pN`. Its standard error is
  `√(p(1−p)/N) / f(x_p)`, with f the density at `x_p` (David & Nagaraja 2003). For a normal,
  `f(x_0.95) = 0.103/σ`, so `SE(p95) ≈ 2.11 σ/√N`, against `σ/√N` for the mean.
- A share q of infeasible draws has standard error `√(q(1−q)/N)`.
- Draws needed for a target error e of the mean: `N = (1.96 s / e)²`.

Invented example: s = 4.0 EUR/MWh, target ±0.5 on the mean: N = (1.96·4/0.5)² ≈ 246. For p95 to
±0.5: about 4.4 times as many, ≈ 1,100.

### 14.2 Sensitivity measures

- OAT effect `Δy = y(x_high) − y(x_low)` (unit of y).
- Elasticity `E = (Δy/y₀)/(Δx/x₀)` (dimensionless): a 1 % change of x moves y by E %. Use it to
  rank inputs of different units. Invented: discount rate 6 % → 8 % (+33 %) moves LCTS 44 → 48
  (+9 %): E ≈ 0.27.
- Morris elementary effect `EE_i = [y(x + Δe_i) − y(x)]/Δ` at r random points; μ* (mean of |EE|)
  ranks importance, σ (spread) flags non-linearity or interaction (Morris 1991).
- Sobol first-order index `S_i = Var(E[y|x_i])/Var(y)`, total index `S_Ti = 1 −
  Var(E[y|x_~i])/Var(y)`; `S_Ti − S_i` is the part of x_i in interactions (Sobol 2001;
  Saltelli et al. 2008, ch 4).

gemini gives Δy per input; elasticities follow from the row (`low`, `high`, `at_low`, `at_high`,
and the base case value) by plain arithmetic, done with `calculate`, never by guess.

### 14.3 Sampling plans

- Simple random sampling: each draw independent; errors as §14.1.
- Latin hypercube (McKay et al. 1979): each input's range cut into N equal-probability strata,
  one draw per stratum, paired at random. It covers each input evenly with few points and lowers
  the variance of the mean for monotone models; gemini's optimiser starts from one.
- A seed fixes either plan: the same seed gives the same draws, so two designs sampled with one
  seed are compared on the same inputs (common random numbers), which sharpens differences.

### 14.4 Differential evolution

A population of NP vectors x. For each target x_i, a mutant `v = x_r1 + F (x_r2 − x_r3)` (three
other members, F ≈ 0.5 to 1), a trial `u` taking each coordinate from v with probability CR (≈ 0.7
to 0.9) and else from x_i, and selection: u replaces x_i if it is not worse (Storn & Price 1997).
Integer and choice variables are rounded. Strengths: no gradient, robust to noise and thresholds.
Weakness: needs many generations; with a small budget it explores more than it converges, which
is why gemini adds the polish (§14.5).

### 14.5 Compass search

From the best point x, try `x ± s·range_i` for each variable i in turn; move to the first
improvement; when no direction improves, halve s. gemini starts at s = 0.25 and stops at 1e-4 or
at the budget (gemini `study/minimize.py`). It converges to a local optimum near a good start
(Kolda et al. 2003): the evolution finds the basin, the compass search its bottom.

### 14.6 Constraints and Pareto dominance

Deb's rules (Deb 2000): (1) feasible beats infeasible; (2) of two feasible, the better objective
wins; (3) of two infeasible, the smaller total violation wins. gemini's violation is the sum of
relative misses, `Σ max(0, g_j)/|limit_j|`, so misses of different units add.

Pareto dominance: a dominates b when a is no worse on every objective and better on one. The
first front is the set no member dominates. NSGA-II sorts fronts and, within a front, prefers
designs with a large crowding distance (the gap to their neighbours), keeping the front spread
(Deb et al. 2002).

---

## 15. Break-even and switching values

A switching value is the value of an input at which the decision changes: two designs cost the
same, or a design stops being feasible (Clemen & Reilly 2014, ch 5). It answers "how wrong can
this input be before my choice is wrong?", often more useful than a range.

Procedure:
1. Run `sensitivity` on both designs with the same `values` (§12.5, `run_study`
   `method="sensitivity"`).
2. For the input in question, the two lines `y_A(x)`, `y_B(x)` between the ends cross where
   `y_A = y_B`; by linear interpolation `x* = x_low + (x_high − x_low)·d_low/(d_low − d_high)`,
   with `d = y_A − y_B` at each end (`calculate`).
3. Check x* with one run of each design on a case with that value (user's approval to change
   the case, or a copy). Interpolation is only a guide where the response bends or a requirement
   fails between the ends.
4. Report x* against the input's range: inside the plausible range means the ranking is fragile.

Invented example: design A (heat pump) and B (boiler). Electricity at 60 EUR/MWh: A 40, B 45;
at 140: A 49, B 46. d = −5 and +3: x* = 60 + 80·(−5)/(−5 − 3) = 110 EUR/MWh. The case's range
is 80 to 140: the choice depends on the power price, and the answer says so.

---

## 16. Robust design and margins

An optimum often sits exactly on a requirement (§4.4). Under uncertainty it then fails in many
draws. Robust design trades a little expected cost for a lower chance of failing (Beyer &
Sendhoff 2007).

Ways to get it with gemini's tools:
1. **Check the optimum under uncertainty**: `sample_uncertainty` on it; read the share of
   infeasible draws (§3.8).
2. **Compare with margin variants**: a design with one size step more (a larger peak unit, one
   more doublet) run through the same Monte Carlo, same seed (§14.3). Report the cost of the
   margin against the drop in failure share.
3. **Let the user choose** the trade-off: "+0.8 EUR/MWh cuts the failure share from 12 % to 2 %".

Rules: a margin is a design change, never a changed requirement; a margin is stated, never hidden
in a size; the same seed for every variant. Margins below hard limits:
`knowledge/handbook-design.md` §4.9.

Invented example: optimum 42.4 EUR/MWh, 7 % of draws miss heat coverage. With a 2 MW peak
boiler: 42.9, 0.7 % miss. With one more doublet: 44.1, 0 % miss. The boiler variant is offered as
the robust choice.

---

## 17. Verifying a study: convergence, reproducibility, plausibility

Verification asks "is the study solved right?" before anyone asks "is it the right study?"
(Oberkampf & Roy 2010).

| Check | How | Pass when |
|---|---|---|
| Reproducible | same seed, same settings | identical numbers |
| Seed stability | a second seed | change below the quoted precision |
| Budget convergence | double `evaluations` or `samples` | best or percentile moves less than the precision |
| Start included | best vs the start design | best ≤ start (always true in gemini) |
| Plausibility | best vs a hand-picked design inside the ranges | best is not worse (§4.6) |
| Edges | each optimal variable vs its range | none at an edge, or the edge named |
| Units and scale | LCTS in EUR/MWh, shares 0 to 1 | magnitudes plausible against `knowledge/handbook-economics.md` |
| Failures | failed and infeasible counts | named, explained |

A study that fails a check is reported with the failed check, not silently re-run until it
passes. Two runs that disagree are both reported, with the reason the second one was run.
