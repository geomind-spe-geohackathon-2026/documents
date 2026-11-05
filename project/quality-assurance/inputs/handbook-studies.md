# Studies of a Plant: Sizing, Sensitivity, Uncertainty and Optimisation

A general engineering textbook on how to ask a simulator more than "does this design work": what
size it should be, which inputs matter, how sure the answer is, and which design is best. It holds
for any plant and any case; every example uses invented numbers. Each lesson names its source
(chapter 12). Checked against gemini 0.6.34 (`gm.study`, `gm.Study`) and geomind's study tools on
2026-11-05.

Cite as `knowledge/handbook-studies.md §<n.m>`. Read by section: the outline first, then only the
sections the task needs. How to call each tool argument by argument: skills `simulating-a-plant`
(`size_plant`, `optimize`), `comparing-designs` (`run_study`, `compare`, `evolve_structure`,
`list_studies`, `read_study`) and `economics` (`sample_uncertainty`, `sensitivity`). The design
itself: `knowledge/handbook-design.md`; costs: `knowledge/handbook-economics.md`; the report:
`knowledge/handbook-report.md`.

## Outline

- 0 Quick reference: 0.1 rules, 0.2 which study answers which question, 0.3 decision order,
  0.4 how many simulations, 0.5 do only what was asked, 0.6 checklist
- 1 What a study is: 1.1 in gemini, 1.2 through the tools, 1.3 metrics
- 2 Sizing: 2.1 what it does, 2.2 what it does not, 2.3 after sizing
- 3 Sensitivity: 3.1 local and global, 3.2 one at a time in gemini, 3.3 scope of the values,
  3.4 reading a tornado, 3.5 limits of one-at-a-time
- 4 Uncertainty (Monte Carlo): 4.1 method, 4.2 how many draws, 4.3 percentiles and P10/P90,
  4.4 failed and infeasible draws, 4.5 what the inputs must be
- 5 Optimisation: 5.1 what gemini searches, 5.2 feasibility, 5.3 ranges, 5.4 budget and seeds,
  5.5 reading an optimum, 5.6 an optimum that is not the optimum
- 6 Comparing designs: 6.1 compare families first, 6.2 a fair comparison, 6.3 structure search
  and several objectives
- 7 Reading a study: 7.1 the whole study, 7.2 plant versions, 7.3 stale studies, 7.4 numbers
- 8 When nothing is feasible
- 9 Worked example (invented numbers)
- 10 Common mistakes
- 11 Glossary
- 12 Sources

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
   (§0.4); a value the agent chose is its own assumption (`source: agent`), never the user's.
4. **Ranges and uncertainties come from the user or the case**, never invented: search ranges
   through `set_ranges` (after asking), uncertainty through the case (`set_case`).
5. **A stored plant is already a design.** Pass `design/<name>` or a project plant version
   `design/v<N>` to every study tool; never re-type it with `build_plant` (§7.2).
6. **Conclusions rest on the whole study**: on gemini's `best`, `feasible`, `trials`, `summary`
   or `rows`, never on trials read one by one (§7.1).
7. **Do only the study that was asked** (§0.5).

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
| What did an earlier study find? | read it | `list_studies`, `read_study` | stored study |

### 0.3 Decision order of a design study

1. **Size** the chosen family (`size_plant`) (§2).
2. **Simulate** the sized design and **check** it (§2.3). An infeasible start is information.
3. **Compare families** when more than one can serve the case: size each, rank them with one
   `run_study` (§6.1). Keep the best one or two.
4. **Optimise** the kept family within the approved ranges, the doublet count searchable when
   its range has more than one value (§5).
5. **Check** the optimum and compare it with the sized start (`compare`) (§5.5).
6. **Sensitivity**, then **uncertainty**, only when the task asks for them (§3, §4).
7. Report each number with its study key (`knowledge/handbook-report.md` §6, §7).

Stop rule: finish with the best feasible design or, when none is feasible after a real change of
approach, follow §8. A requirement of the case is never offered as the thing to change.

### 0.4 How many simulations

| Study | Simulations | Choose |
|---|---|---|
| `size_plant` | 1 (the check run) | nothing |
| `simulate` | 1 | nothing |
| `run_study`, `method="run"` | one per design | nothing |
| `sensitivity` | 2 per uncertain value | which values (`values`); every declared one for a broad question (§3.3) |
| `sample_uncertainty` | `samples` | 20 to 50 for a mean; 200 or more before quoting p5/p95 or p10/p90 as numbers (§4.2) |
| `optimize` | up to `evaluations` per doublet count | at least 5 per variable (gemini refuses fewer); 10 to 20 per variable for a usable optimum (§5.4) |
| `run_study`, `method="minimize"` | `evaluations` per design and count | as for `optimize`; the same for every design |
| `evolve_structure` | the runtime's evolve settings | nothing; quote the stop reason |

Invented example: 4 search variables, a doublet range of 1 to 3, `evaluations` 60: up to 180
simulations. At 0.2 s per one-year daily run, under a minute; at 2 s, six minutes. Ask for fewer
evaluations before a study would pass the tool's time limit (15 minutes).

### 0.5 Do only what was asked

A study costs time, tokens and the user's attention. "Design and check" asks for a design and its
verdict, not a Monte Carlo; "optimise" asks for one optimisation, not a new family; "write the
report" reports the studies that exist (QA-229, QA-257, QA-276). Offer a further study in one
line; never run it unasked. An answer that is ready is given; it is not delayed by extra work.

### 0.6 Checklist before a study result is reported

- [ ] The study key `study/<name>` is cited and `current` (or named as made on an older case).
- [ ] `feasible` of the best is true, or the answer says it is the least violating trial and why.
- [ ] The number of trials or draws is given, the failed or infeasible ones counted.
- [ ] Seed and evaluations or samples given, each with who chose it.
- [ ] The comparison is fair: same case, same economics, same effort per design (§6.2).
- [ ] No conclusion from part of a history (§7.1).
- [ ] A broad question covered every declared uncertainty; a narrow one names what was held (§3.3).
- [ ] An optimum at the edge of a range names that range (§5.5).
- [ ] Percentiles named as gemini gives them (p10 = 10th percentile), not swapped (§4.3).
- [ ] Numbers rounded to what the study supports (§7.4).

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

Every study copies the plant and the case: the originals are never changed. With
`gm.runtime.settings(processes=n)` the runs go to `n` worker processes and give the same result
(gemini docstrings, `gemini/study/*.py`).

### 1.2 Studies through the agents' tools

Each geomind study tool runs one gemini study on a stored design (`design/<name>`, or a project
plant version `design/v<N>`) and the state's case, and stores it as `study/<name>`. The tool
returns the summary; `read_study` returns what ran and what came back, with a history summarised
as `trials`; `list_studies` lists the chat's and the project's studies and results with
`current`. Call `list_studies` once and keep its answer (QA-219).

### 1.3 Metrics

A study reads the metrics of `gm.study.metrics()`: `heating_coverage`, `cooling_coverage`, `cop`,
`peak_heat`, `peak_cold`, `lcoh`, `lcoc`, `lcts`, `annualised_cost`, `co2` and the KPIs of
`gm.evaluate.totals`. A leading `-` maximises (`-cop`). Rank plants that deliver both heat and
cold on `lcts` (`knowledge/handbook-economics.md` §6.3); `npv` and `payback` are not study
metrics. A metric a plant cannot have (cooling coverage of a heating-only plant) is refused by
name: pick another, do not retry (QA-240).

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
an optimum: it sizes for the peak, while the cost depends on the whole year.

### 2.3 After sizing

`size_plant` simulates the sized design once and lists every requirement it breaks: sizing never
hides an infeasible start. Read that list first. Values the size step derives (stage counts, pump
coefficients) are the size step's, not the user's: never ask the user for them (QA-287).

Invented example: a sized design meets 98.2 % of the heat against a limit of 99 %, with the
doublet count at the top of its range. The next step is a larger heat pump share or another
family (a design change), not a new requirement.

---

## 3. Sensitivity

### 3.1 Local and global sensitivity

A sensitivity analysis says how the uncertainty of an output is apportioned to its inputs
(Saltelli et al. 2008, ch 1). Two kinds:

- **Local, one-at-a-time (OAT)**: each input moved alone around a base point. Cheap (2 runs per
  input), easy to read, the tornado of decision analysis (Clemen & Reilly 2014). Blind to
  interactions and to the corners of the input space.
- **Global**: all inputs moved together over their whole ranges (Morris screening, variance-based
  Sobol indices). Sees interactions; costs tens to thousands of runs per input.

gemini's `sensitivity` is OAT; its `sample` is a global Monte Carlo that gives the spread of a
metric, not its apportionment. Use OAT to rank drivers, the Monte Carlo for the range (§4), and
say which you did.

### 3.2 One-at-a-time sensitivity in gemini

`gm.study.sensitivity` (`sensitivity`) moves each value the case declares an `uncertainty` for to
its low and its high end, the others at their case values, and returns one row per value and
metric: `parameter`, `low`, `high`, `at_low`, `at_high`, `effect`, and whether each end's run is
feasible. Rows are sorted by effect, the failed last. Plant parameters are design decisions and
never move.

The ends are `min` and `max` when declared, else `value − std` and `value + std` of a normal.
These are not alike: ±1 std covers about 68 % of a normal, a min-max band all of a uniform. Two
effects from different kinds are compared only with that said; to rank fairly, declare comparable
bands (for example each value's p5 and p95) (Saltelli & Annoni 2010).

Economic inputs change only the cost formulas; physical ones (permeability, gradient) change the
simulation, and an end can break a requirement: report `feasible_low` and `feasible_high`.

To test drivers with ranges the user gives: put each range into the case as that value's
`uncertainty` first, then run `sensitivity` with `values` naming those paths (skill `economics`).
A new range of another kind replaces the whole old `uncertainty`
(`knowledge/handbook-economics.md` §13.1).

### 3.3 Which uncertain values a study covers

The scope follows the question (QA-263):

- **A broad question** ("is this a good investment?", "how robust is this design?", "what drives
  the cost?"): cover **every** uncertainty the case declares. Run `sensitivity` without `values`
  and `sample_uncertainty` without `values`. Choosing a few decides the answer before the study.
- **A question that names values** ("how does the electricity price change the LCTS?"): move only
  those (`values` names their paths), and say the others were held at their case values (QA-248).
- **A named value the case declares no uncertainty for**: put the user's range into the case
  first, never a range of your own.

Report which values moved and which declared ones were held.

Invented example: a case declares six uncertain values. A study of electricity and gas prices
alone finds electricity dominant (LCTS 38 to 46 EUR/MWh). Over all six, permeability moves the
LCTS from 35 to 55 and the discount rate from 37 to 47: electricity is third. An answer to "is
this a good investment?" built on the two-value study names the wrong driver.

### 3.4 Reading a tornado

- The bar is `at_high − at_low`; its sign says the direction. Quote the base value beside it.
- An effect is only as wide as the range given: a narrow range makes an input look unimportant
  (Saltelli & Annoni 2010). Name each range's source.
- Bars that do not add: the sum of OAT effects is not the total spread (interactions, §3.5).
- A lopsided bar (one end moves far more) shows non-linearity or a threshold, often a
  requirement starting to fail at that end: check `feasible_low` and `feasible_high`.
- Inputs with near-zero effect over their full range can be held at their case value in later
  studies; say so.

Invented example: base LCTS 44.0 EUR/MWh. Discount rate 4 % to 10 %: 39.5 to 51.0 (effect 11.5).
Gas price ±30 %: 42.8 to 45.2 (2.4). Gradient 28 to 34 K/km: 47.9 (infeasible: heat coverage
97.6 %) to 42.1. The answer names the discount rate as the largest cost driver and the gradient
as the one that can break the design.

### 3.5 Limits of one-at-a-time

OAT explores only the axes through the base point. In 10 dimensions the points it can reach are a
vanishing share of the input box (Saltelli & Annoni 2010; Saltelli et al. 2019), so it misses
combined extremes (low permeability with high power price) and interactions (Montgomery 2017,
ch 5 on factorial designs). Use it to rank drivers, not to bound the outcome. For "how bad can it
get together", run the Monte Carlo (§4); when a requirement may fail only in a combination, run
the combination as its own case with the user's approval.

---

## 4. Uncertainty (Monte Carlo)

### 4.1 The method

A Monte Carlo propagates input distributions through the model by drawing every uncertain input
at once, many times, and running the model on each draw; the outputs form the distribution of the
result (JCGM 101:2008, the GUM Supplement 1 on propagation of distributions). It needs no
linearity and sees interactions.

`gm.study.sample` (`sample_uncertainty`) draws every declared uncertain value (or only those in
`values`) `samples` times from `seed`, simulates each draw, and returns per metric `mean`, `p5`,
`p50`, `p95`, plus any `percentiles` asked for (for example `[10, 90]`, giving `p10`, `p90`), with
each draw's values and whether its run was feasible. The same seed gives the same draws.

### 4.2 How many draws

- **A mean** converges as `σ/√N`: with σ = 4 EUR/MWh and N = 30, the standard error is about 0.7.
- **A percentile** needs more: the standard error of the p-quantile is
  `√(p(1−p)/N) / f(x_p)` (David & Nagaraja 2003). For a normal, the p95's error is about 2.1 times
  the mean's at the same N, and a tail percentile rests on few draws (at N = 30, about 1.5 draws
  lie beyond p95).
- **A standard for coverage intervals**: JCGM 101:2008 (clause 7.2) asks for M large compared with
  `1/(1−p)`, for example at least `10⁴/(1−p)`: 2×10⁵ for a 95 % interval. That is for metrology
  precision; for engineering decisions a few hundred draws give percentiles to about two
  significant figures. State N and quote accordingly.
- **Check convergence**: run a second seed. When p95 moves by more than the precision quoted,
  the draws are too few.

Invented example: 30 draws give mean LCTS 52.1 EUR/MWh (standard error about 0.7) and p95 60.3,
quoted "about 60". 300 draws give p95 59.8 and a second seed 59.5: quote "59.5 to 60".

### 4.3 Percentiles and the P10/P50/P90 convention

gemini's `p10` is the 10th percentile: 10 % of the draws lie below it. In petroleum resource
reporting P90 means the value exceeded with 90 % probability, the LOW estimate (SPE-PRMS 2018):
the opposite name for the same number. When a user asks for "P10, P50, P90", ask `percentiles`
`[10, 90]`, give the numbers, and say which convention the names follow (QA-248, QA-299). For a
cost, the high percentile is the pessimistic one; for an energy delivered, the low one.

### 4.4 Failed and infeasible draws

A draw that breaks a bound (a negative price) fails and is left out of the summary; a draw that
runs but breaks a requirement is infeasible and stays in. Report both counts. Many infeasible
draws are a finding in themselves ("the design meets the heat requirement in 82 % of the draws"),
often the most useful number of the study. Never drop them silently to tidy the percentiles.

### 4.5 What the inputs must be

- Each distribution comes from the user, the case or a cited source (`knowledge/data-*.csv`),
  never invented. Without one, ask.
- Inputs drawn independently: gemini draws each alone. When two inputs move together (gas and
  power prices), say that the correlation was not modelled and that the spread may be too narrow
  or too wide.
- The Monte Carlo describes the inputs' uncertainty, not the model's: a range is conditional on
  the model and on what was held fixed. Say so in the answer.

---

## 5. Optimisation

### 5.1 What gemini searches

`gm.study.minimize` (`optimize`) searches the plant's own variables: every parameter with a
`range` (continuous, or integer when the parameter is), every one with `options` (a choice), and
the doublet count when `size.doublets` has a range. Parameters with the same name, role and range
are one variable (three chillers of one range are one capacity). Ranges are set with
`set_ranges`, from the user or the case.

The method: differential evolution (Storn & Price 1997) from a Latin hypercube start (McKay et
al. 1979) with the given `seed`; about half of the budget is the evolution, the rest polishes its
best trial by a compass search, one variable at a time (Kolda et al. 2003). The plant as given is
one member, so the best is never worse than the start. The doublet count is searched count by
count, each with up to `evaluations` trials; the best of all counts wins. No gradient is needed:
the simulator is a black box with thresholds and integers.

### 5.2 Feasibility in a search

A trial is feasible when its verdict has no reason a design can change: no failed step, every
requirement met, supply temperatures held, no operating limit breached. gemini ranks as Deb's
feasibility rules do (Deb 2000): a feasible trial beats any infeasible one; feasible ones by the
objective; infeasible ones by their total relative violation, so the search moves towards
feasibility without a penalty weight to tune. A trial that fails to run is infeasible with the
largest violation.

With no feasible trial, `best` is the least violating one, `feasible` is false, and its `reason`
says why: report it so, never as a solution (§8).

### 5.3 Choosing the ranges

A range too narrow hides the optimum; one too wide wastes trials on designs that cannot work.
Take ranges from the case's limits (a flow band, a doublet count) and engineering bounds the user
approves. Every count the user asks about must be inside the range (QA-253); a search over one
doublet count when the case allows several is a mistake (QA-129).

Invented example: a heat pump share searched between 0 and 100 % spends half its trials below
20 %, where the supply temperature is never reached; 30 to 80 % finds the same optimum with half
the evaluations.

### 5.4 Budget and seeds

- gemini refuses fewer than 5 evaluations per variable. A stochastic search with population-based
  methods needs roughly 10 to 20 per variable to settle (Storn & Price 1997 used populations of
  5 to 10 times the dimension, over many generations); below that the result is a good design,
  not the optimum.
- The budget is per doublet count: three counts triple the runs.
- A stochastic optimiser gives a different best for another seed. When two seeds disagree by more
  than the decision needs, the budget was too small (Eiben & Smith 2015, ch 14 on experiments
  with evolutionary algorithms).
- The seed is the agent's choice and its own assumption (QA-195); give it.

### 5.5 Reading an optimum

Compare the optimum with the sized start (`compare` on both results): which variables moved, and
by how much the objective fell. Then:

- **At the edge of a range**: the range, not the plant, set it. Name that range and offer to
  widen it with the user.
- **Flat**: many trials within a small share of the best. The cheapest to build or the most
  robust of them may be the better choice; establish flatness on the whole history (§7.1) or by a
  sensitivity around the best, never from a few trials.
- **Worse than a stored design**: a fresh optimum that is worse than a design already stored
  (the project plant) is not an improvement; say so and keep the better one (QA-276).

### 5.6 An optimum that is not the optimum

An evolutionary search guarantees nothing beyond its trials (Wolpert & Macready 1997). Signs the
reported best is not the optimum: a simple design inside the ranges simulates better; a second
seed finds a better one; the best moved a lot in the last trials. Invented example: a search of
30 evaluations over 3 variables reports 41.3 EUR/MWh with a heat pump of 9.8 MW; a single
simulation at 5 MW, inside the range, gives 39.2, feasible (QA-285). Report the better design,
the budget, and that the search was too short; ask for a larger budget rather than claim an
optimum.

---

## 6. Comparing designs

### 6.1 Compare families first, then optimise

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

Invented example: four families, sized: A 47.9, B 44.6, C infeasible (cold unmet), D 45.1
EUR/MWh. B and D are close: optimise both with 60 evaluations each; B reaches 41.8, D 42.6.
Report the run study and the minimize study, both by key.

### 6.2 A fair comparison

Designs are compared on the same case and economics, with the same effort: a sized start against
an optimised rival is no comparison. Name what each design got (sized; optimised with how many
evaluations and which seed). A family that was not simulated is not ranked; it may be named as
screened out, with the reason. A difference smaller than what changing the seed or a held input
would move is a tie: say so (§4.2, §5.4).

A comparison never changes the project's current plant: studying a design is not adopting it;
adopting is its own step the user asks for (QA-237).

### 6.3 Structure search and several objectives

When the plant states optional modules or choices (a superstructure), `evolve_structure`
(`gm.study.evolve`) searches structures and values together: a genetic algorithm with one
objective, NSGA-II with two or more (Deb et al. 2002). Its settings (population, polish, stop)
come from the runtime, not from the agent; quote the stop reason.

With two or more objectives the answer is a Pareto front: designs no other beats on every
objective. No single best exists until someone states the trade-off (Miettinen 1999). Present the
front, name the extreme designs and the knee, and let the user choose; never pick one silently by
a weighting of your own. Quote gemini's explanation and front table with the study key (skill
`report`).

Invented example: cost against CO2. Design P: 40 EUR/MWh, 900 t/y; Q: 43, 400; R: 52, 350. Q is
the knee: 3 EUR/MWh more than P saves 500 t/y; R pays 9 more for 50 t/y.

---

## 7. Reading a study

### 7.1 Read the whole study, not a sample of it

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
  than re-reading it step by step (QA-179).

### 7.2 Plant versions are designs

A project's stored plant versions are designs: `design/v<N>` is version N. To rank six versions,
pass `design/v1` to `design/v6` to one `run_study`; never rebuild them with `build_plant`
(re-typing drops values and costs a confirmation each, QA-221). `v<N>` is reserved for versions:
give a new design another name.

### 7.3 Current and stale studies

A study ran on the case of its time. `list_studies` says whether it is `current`; one that is not
is quoted as "made on an older case" or run again. A study is never edited: a new run is a new
study with a new name. After a case change, a result's verdict may differ: re-check before
quoting it as feasible.

### 7.4 How many digits

Quote a number to what the study supports, never gemini's 15 digits (QA-099, QA-299). A Monte
Carlo of 30 draws supports two significant figures of a mean and one of a tail percentile; an
optimum supports the digits by which a second seed agrees. Costs: 0.1 EUR/MWh at most; shares:
0.1 %; capacities: 0.1 MW. The study record keeps the full numbers.

---

## 8. When nothing is feasible

A design problem with no feasible trial needs a diagnosis, not more of the same search.

1. **Read the reasons** of the least violating trial: which requirement, by how much, when.
2. **Name the binding cause**: capacity (peak not met), temperature (supply not reached), a
   limit (flow, pressure, drawdown), or a failed step (the model refused the operating point).
3. **Change the approach, one at a time**: another family, another doublet count, another split
   of base and peak load, a wider range the user approves. Re-size after each structural change.
4. **Stop** after real changes of approach fail, and report the best design, its violations and
   the list of what was tried, with each study key.

A requirement of the case is never offered as the thing to change: it is the user's to change.
Options offered are design changes. When the user asks what would make it feasible, the answer
may name the requirement that binds and by how much, as information.

Invented example: three families all miss heat coverage by 0.5 to 2 % in the coldest week.
Diagnosis: peak capacity. Options: a peak boiler, a larger heat pump, one more doublet; not "lower
the coverage requirement".

---

## 9. Worked example (invented numbers)

A district of 40 GWh/y heat (peak 14 MW) and 6 GWh/y cold; requirements: 99 % heat coverage,
supply 75 °C. The user asks: "Find the cheapest design and tell me how sure the cost is."

1. **Size** three families: direct use with a boiler (D), direct use with a heat pump (H),
   direct use with heat pump and absorption chiller (HA). `run_study` `method="run"`
   `prepare=["size"]` → `study/families_sized`: D 51.0 EUR/MWh feasible; H 46.2 feasible;
   HA 45.8 infeasible (cold supply 9.4 °C against 8 °C).
2. **Close and one infeasible**: optimise H and HA with the same budget, 3 variables, doublets 1
   to 2, 45 evaluations each, seed 1 → `study/families_opt`: H 43.9 feasible, HA 42.7 feasible
   (chiller enlarged). Seed 2 gives HA 42.9: a gap of 1.2 against a seed spread of 0.2 is real.
3. **Edge check**: the HA heat pump sits at 6.0 MW, the top of its range. Name it; the user widens
   to 9 MW; a new search gives 42.4 at 7.1 MW, inside the range.
4. **Sensitivity**, every declared uncertainty (broad question): discount rate first (38.9 to
   47.6), permeability second, the low end infeasible (coverage 98.4 %).
5. **Monte Carlo**, 300 draws, seed 7, every declared uncertainty, percentiles 10 and 90: mean
   42.8, p10 39.6, p50 42.5, p90 46.9; 21 draws infeasible (7 %). Seed 8: p90 47.1.
6. **Answer**: HA at 42.4 EUR/MWh (`study/...` keys). Cost 39.6 to 46.9 between the 10th and 90th
   percentiles, driven by the discount rate; in 7 % of draws, low permeability breaks heat
   coverage: a design margin or a peak unit is the remedy if that risk matters.

---

## 10. Common mistakes

1. Ranking families sized against one family optimised (§6.2).
2. Optimising before any family comparison, or not optimising close sized families (§6.1).
3. A search over a single doublet count when the case allows several (§5.3).
4. Ranges invented, or so wide most trials cannot work (§5.3).
5. Too few draws for a percentile, or too few evaluations for the variables (§4.2, §5.4).
6. A conclusion from part of a history (§7.1).
7. Rebuilding stored plant versions instead of passing `design/v<N>` (§7.2).
8. A least-violating trial reported as a solution (§5.2, §8).
9. A sensitivity or Monte Carlo written in `run_python` (§0.1).
10. A requirement offered as the thing to change (§8).
11. A study without its key, or a stale one quoted as current (§7.3).
12. A few agent-picked values answering a broad question (§3.3).
13. P10 and P90 swapped between conventions, or said not to exist (§4.3).
14. OAT effects of ±1 std and of min-max ranked together without saying so (§3.2).
15. OAT taken as the bounds of the outcome (§3.5).
16. Infeasible draws dropped silently (§4.4).
17. An optimum at a range edge reported as the plant's optimum (§5.5).
18. A one-seed, short-budget best called "the optimum" (§5.6).
19. A Pareto front collapsed to one design by the agent's own weights (§6.3).
20. Studies nobody asked for (§0.5); 15-digit numbers (§7.4).

---

## 11. Glossary

- **Design variable**: a plant value the search may change (a range or options).
- **Uncertain input**: a case value with a declared `uncertainty`; never a design variable.
- **Feasible**: every requirement and limit met (gemini's verdict); not the report's `passed`.
- **Violation**: the total relative amount by which requirements are missed.
- **Tornado**: OAT effects sorted by size.
- **Percentile p<n>**: n % of the draws lie below it.
- **Pareto front**: designs no other beats on every objective.
- **Budget**: `evaluations` (per doublet count) or `samples`.
- **Seed**: makes a stochastic study repeatable; the same seed gives the same trials.
- **Current**: a study made on the case as it is now.

---

## 12. Sources

- Saltelli A., Ratto M., Andres T. et al. (2008). *Global Sensitivity Analysis. The Primer*.
  Wiley. (§3.1, §3.5)
- Saltelli A., Annoni P. (2010). How to avoid a perfunctory sensitivity analysis. *Environmental
  Modelling & Software* 25, 1508-1517. (§3.2, §3.4, §3.5)
- Saltelli A., Aleksankina K., Becker W. et al. (2019). Why so many published sensitivity
  analyses are false. *Environmental Modelling & Software* 114, 29-39; arXiv:1711.11359. (§3.5)
- Morris M.D. (1991). Factorial sampling plans for preliminary computational experiments.
  *Technometrics* 33, 161-174. (§3.1)
- Montgomery D.C. (2017). *Design and Analysis of Experiments*, 9th ed. Wiley. (§3.5)
- Clemen R.T., Reilly T. (2014). *Making Hard Decisions with DecisionTools*, 3rd ed. Cengage.
  (§3.1, tornado)
- JCGM 101:2008. *Evaluation of measurement data, Supplement 1 to the GUM: Propagation of
  distributions using a Monte Carlo method*. BIPM, doi:10.59161/JCGM101-2008. (§4.1, §4.2)
- David H.A., Nagaraja H.N. (2003). *Order Statistics*, 3rd ed. Wiley. (§4.2, quantile error)
- SPE, WPC, AAPG, SPEE, SEG, SPWLA, EAGE (2018). *Petroleum Resources Management System
  (PRMS)*, rev. 2018. (§4.3, P90 convention)
- Storn R., Price K. (1997). Differential evolution: a simple and efficient heuristic for global
  optimization over continuous spaces. *J. Global Optimization* 11, 341-359. (§5.1, §5.4)
- McKay M.D., Beckman R.J., Conover W.J. (1979). A comparison of three methods for selecting
  values of input variables. *Technometrics* 21, 239-245. (§5.1)
- Kolda T.G., Lewis R.M., Torczon V. (2003). Optimization by direct search. *SIAM Review* 45,
  385-482. (§5.1, compass search)
- Deb K. (2000). An efficient constraint handling method for genetic algorithms. *Computer
  Methods in Applied Mechanics and Engineering* 186, 311-338. (§5.2)
- Deb K., Pratap A., Agarwal S., Meyarivan T. (2002). A fast and elitist multiobjective genetic
  algorithm: NSGA-II. *IEEE Trans. Evolutionary Computation* 6, 182-197. (§6.3)
- Miettinen K. (1999). *Nonlinear Multiobjective Optimization*. Kluwer. (§6.3)
- Wolpert D.H., Macready W.G. (1997). No free lunch theorems for optimization. *IEEE Trans.
  Evolutionary Computation* 1, 67-82. (§5.6)
- Eiben A.E., Smith J.E. (2015). *Introduction to Evolutionary Computing*, 2nd ed. Springer.
  (§5.4)
- ASHRAE (2020). *ASHRAE Handbook, HVAC Systems and Equipment*. (§2.1)
- Lund J.W., Toth A.N. (2021). Direct utilization of geothermal energy 2020 worldwide review.
  *Geothermics* 90, 101915. (§2.1)
- gemini 0.6.34 docstrings: `gemini/study/size.py`, `minimize.py`, `sample.py`,
  `sensitivity.py`, `evolve.py`; geomind tools `geomind/tools/gemini/study.py`, `studies.py`.
- QA lessons: documents/project/quality-assurance/bugs (QA numbers given in the sections).
