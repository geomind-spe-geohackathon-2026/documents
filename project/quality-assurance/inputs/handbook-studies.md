# Studies of a Geothermal Plant: Sizing, Sensitivity, Uncertainty and Optimisation

How to ask a simulator more than "does this design work": what size it should be, which inputs
matter, how sure the answer is, and which design is best. General for any case; the examples use
invented numbers. Checked against gemini 0.6.17 (`gm.study`, `gm.Study`) and geomind's study
tools on 2026-11-05.

Cite as `knowledge/handbook-studies.md` with the section (for example
`knowledge/handbook-studies.md §4.2`). Every section stands alone; chapter 0 is the short version
for agents. How to call each tool, argument by argument: skills `simulating-a-plant` (`size_plant`,
`optimize`), `comparing-designs` (`run_study`, `compare`, `evolve_structure`, `list_studies`,
`read_study`) and `economics` (`sample_uncertainty`, `sensitivity`). The design itself:
`knowledge/handbook-design.md`; costs and their meaning: `knowledge/handbook-economics.md`.

---

## 0. Quick reference for the agents

### 0.1 Rules that hold in every section

1. **gemini runs every study; agents choose and quote.** A size, a ranking, a range or a
   sensitivity is a gemini study, never a loop in `run_python` or a table built by hand.
2. **A study has a name, and its key is its evidence.** Every study is stored as `study/<name>`
   (a name is never reused). Cite the key beside every number the study gave, and say when
   `list_studies` shows it is not `current` (the case changed after it ran).
3. **Settings have no defaults.** `evaluations`, `samples` and `seed` are chosen with a reason
   (§0.4); a value the agent chose is its own assumption (`source: agent`), never the user's.
4. **Ranges and uncertainties come from the user or the case**, never invented: search ranges
   through `set_ranges` (after asking), uncertainty through the case (`set_case`).
5. **A stored plant is already a design.** Pass `design/<name>` or a project plant version
   `design/v<N>` to every study tool; never re-type a stored plant with `build_plant` (§6.2).
6. **Conclusions rest on the whole study**: on gemini's `best`, `feasible`, `trials`, `summary`
   or `rows`, never on a handful of trials read one by one (§6.1).

### 0.2 Which study answers which question

| Question | Study | Tool | gemini |
|---|---|---|---|
| What first sizes does this design need for the case? | sizing | `size_plant` | `gm.study.size` |
| Does this design work over the whole period? | one run | `simulate`, then `check_results` | `gm.simulate`, `gm.evaluate.verdict` |
| Which of these designs (families, versions) is best as they stand? | comparison | `run_study` with `method="run"`, or `compare` on stored results | `gm.Study` `run` |
| What values of this design minimise a metric within its ranges? | optimisation | `optimize` | `gm.study.minimize` |
| Which family is best after each is optimised? | comparison of optimised designs | `run_study` with `method="minimize"` (and `prepare=["size"]`) | `gm.Study` `minimize` |
| Which structure (which modules on or off) and values are best? | structure search | `evolve_structure` | `gm.study.evolve` |
| Which uncertain inputs move a metric most? | one-at-a-time sensitivity | `sensitivity` | `gm.study.sensitivity` |
| How sure is a metric, as a range? | Monte Carlo | `sample_uncertainty` | `gm.study.sample` |
| What did an earlier study find? | read it | `list_studies`, `read_study` | stored study |

### 0.3 Decision order of a design study

1. **Size** the chosen family for the case (`size_plant`): first sizes, the doublet count from its
   range, the heat pump and boiler shares (§2).
2. **Simulate** the sized design over the whole period and **check** it (§2.3). An infeasible
   start is information, not the end.
3. **Compare families** when more than one can serve the case: size each and rank them with one
   `run_study` (§5.1). Keep the best one or two.
4. **Optimise** the kept family within the ranges the user approved (§4), with the doublet count
   searchable when its range has more than one value.
5. **Check** the optimised design and compare it with the sized start (`compare`).
6. **Sensitivity**, then **uncertainty**, only when the task asks for them (§3).
7. Report: each number with its study key (`knowledge/handbook-report.md` §6, §7).

Stop rule: finish with the best feasible design, or, when none is feasible after a real change
of approach (another family, another doublet count, another split of base and peak), with the
best one and the list of what was tried. A requirement of the case is never offered as the thing
to change: the options are design changes.

### 0.4 How many simulations

| Study | Simulations | Choose |
|---|---|---|
| `size_plant` | 1 (the check run after sizing) | nothing |
| `simulate` | 1 | nothing |
| `run_study`, `method="run"` | one per design | nothing |
| `sensitivity` | 2 per uncertain value (its low and its high end) | which values (`values`); every declared one by default |
| `sample_uncertainty` | `samples`, one per draw | 20 to 50 for a mean and a rough range; 200 or more before quoting p5 and p95 as numbers; record the choice and its reason |
| `optimize` | up to `evaluations` for each doublet count | at least 5 per variable (gemini refuses fewer); 10 to 20 per variable for a usable optimum; the searches of the counts add up |
| `run_study`, `method="minimize"` | `evaluations` per design (per doublet count) | as for `optimize`; the same budget for every design, so the comparison is fair |
| `evolve_structure` | `evaluations` in all | a budget large enough that every structure gets several candidates |

Invented example: a design with 4 search variables and a doublet range of 1 to 3. With
`evaluations` 60, gemini runs up to 60 trials for each count: up to 180 simulations. At about
0.2 s per one-year daily run that is under a minute; at 2 s, six minutes. Ask for fewer
evaluations before a study would take more than the tool's time limit (15 minutes).

### 0.5 Checklist before a study result is reported

- [ ] The study key `study/<name>` is cited and `current` (or named as made on an older case).
- [ ] `feasible` of the best is true, or the answer says it is the least violating trial and why.
- [ ] The number of trials or draws is given, with the failed or infeasible ones counted.
- [ ] Seed and evaluations or samples given, each with who chose it.
- [ ] The comparison is fair: same case, same economics, same effort per design (§5.2).
- [ ] No conclusion drawn from part of a history (§6.1).

---

## 1. What a study is

### 1.1 Studies in gemini

A study runs a plant on a case many times with something changed, and summarises the runs.
gemini has one function per kind in `gm.study` and one file format for them, `gm.Study`
(`study.json`, `kind: study`): which `cases` and `plants`, an optional `prepare` (`["size"]`),
the `method` (`run`, `minimize`, `sample`, `sensitivity` or `evolve`), and the settings the method
needs. A setting the method needs and the file lacks is an issue; one it does not read is
refused. `gm.study.kinds()` lists the kinds with their settings; `gm.study.metrics()` the metrics
a study reads.

Every study copies the plant and the case: the originals are never changed. With
`gm.runtime.settings(processes=n)` the runs go to `n` worker processes and give the same result.

### 1.2 Studies through the agents' tools

Each geomind study tool runs one gemini study on a stored design (`design/<name>`, or a project
plant version `design/v<N>`) and the state's case, and stores it as `study/<name>`. The tool
returns the summary; `read_study` returns what ran and what came back; `list_studies` lists the
chat's and the project's studies with `current`.

### 1.3 Metrics

A study optimises or reads the metrics of `gm.study.metrics()`: `heating_coverage`,
`cooling_coverage`, `cop`, `peak_heat`, `peak_cold`, `lcoh`, `lcoc`, `lcts`, `annualised_cost`,
`co2`. A leading `-` maximises (`-cop`). Use `lcts` to rank plants that deliver both heat and cold
(`knowledge/handbook-economics.md` §6.3); `npv` and `payback` are not study metrics.

---

## 2. Sizing

### 2.1 What sizing does

`gm.study.size` (`size_plant`) gives a design its first sizes from the case, with gemini physics
only: the smallest doublet count in the plant's `size.doublets` range whose heat at the flow
limit and the brine cooling limit covers the heating peak; each doublet's nominal flow at the
flow limit; each boiler by the plant's `backup` policy; each heat pump for the part of the peak
the reservoir cannot reach, `(supply − reservoir) / (supply − return)` of it; each chiller for
the cooling peak; injection pumps for the flow and head their doublets need.

### 2.2 What sizing does not do

It leaves unsized what it has no rule for (a CHP, a heat exchanger, a heat pump that is not
needed) and lists it. It assumes an ideal exchanger for the heat pump share, so a plant with a
heat pump and no boiler may fall short of its supply temperature at the peak. It is a start, not
an optimum.

### 2.3 After sizing

`size_plant` simulates the sized design once and lists every requirement it breaks: sizing never
hides an infeasible start. Read that list before anything else. Invented example: a sized design
meets 98.2 % of the heat against a limit of 99 %; the doublet count is at the top of its range;
the next step is a larger heat pump share or a second family, not a new requirement.

---

## 3. Sensitivity and uncertainty

### 3.1 One-at-a-time sensitivity

`gm.study.sensitivity` (`sensitivity`) moves each value the case declares an `uncertainty` for to
its low and its high end (`min` and `max`, or value ± `std` of a normal), the others at their case
values, and returns one row per value and metric: `parameter`, `low`, `high`, `at_low`,
`at_high`, `effect`, and whether each end's run is feasible. Rows are sorted by effect, the
failed last. Plant parameters are design decisions and never move.

Economic inputs change only the cost formulas; physical inputs (permeability, gradient) change
the simulation, and an end can break a requirement: report `feasible_low` and `feasible_high`.

To test drivers the user names with ranges the user gives: put each range into the case as that
value's `uncertainty` first, then run `sensitivity` with `values` naming only those paths
(skill `economics`). A new range of another kind replaces the whole old `uncertainty`
(`knowledge/handbook-economics.md` §13.1).

### 3.2 Monte Carlo uncertainty

`gm.study.sample` (`sample_uncertainty`) draws every declared uncertain value at once, `samples`
times from `seed`, simulates each draw, and returns per metric `mean`, `p5`, `p50`, `p95`, with
each draw's values and whether its run was feasible. A draw that breaks a bound (a negative
price) is a failed draw and is left out of the summary: report how many.

How many draws: the error of a mean falls as `1/√N`; a 5th or 95th percentile needs far more
draws than a mean. Invented example: with 30 draws the mean LCTS is 52.1 EUR/MWh and its standard
error about 0.4; the p95 of 60.3 rests on one or two draws and is quoted as "about 60". With 300
draws p95 is 59.8 and can be quoted as a number.

### 3.3 Sensitivity first, then uncertainty

A sensitivity is cheap (two runs per value) and tells which inputs matter; a Monte Carlo is dear
and tells how sure the answer is. Run the sensitivity first; when two or three inputs carry most
of the effect, their ranges deserve the most care before the Monte Carlo.

---

## 4. Optimisation

### 4.1 What gemini searches

`gm.study.minimize` (`optimize`) searches the plant's own variables: every parameter with a
`range` (continuous, or integer when the parameter is), every one with `options` (a choice), and
the doublet count when `size.doublets` has a range. Parameters with the same name, role and range
are one variable (three chillers of one range are one capacity). Set the ranges with
`set_ranges`, from the user or the case.

The search is differential evolution from a Latin hypercube with the given `seed`; the plant as
given is one member, so the best is never worse than the start. The doublet count is searched
count by count, each with up to `evaluations` trials; the best of all counts wins.

### 4.2 Feasibility in a search

A trial is feasible when its verdict has no reason a design can change: no failed step, every
requirement of the case met, supply temperatures held, no operating limit breached. Feasible
trials beat infeasible ones; infeasible ones are ranked by their total relative violation, so the
search moves towards feasibility. With no feasible trial, `best` is the least violating one,
`feasible` is false and its `reason` says why: report it so, never as a solution.

### 4.3 Choosing the ranges

A range too narrow hides the optimum; one too wide wastes trials on designs that cannot work.
Take ranges from the case's limits (a flow band, a doublet count) and from engineering bounds the
user approves. Invented example: a heat pump share searched between 0 and 100 % spends half its
trials below 20 %, where the supply temperature is never reached; 30 to 80 % finds the same
optimum with half the evaluations.

### 4.4 Reading an optimum

Compare the optimised design with the sized start (`compare` on both results): which variables
moved, and by how much the objective fell. An optimum at the edge of a range says the range, not
the plant, set it: name that range. A flat optimum (many trials within a small share of the best)
is a result too: the cheapest-to-build of them may be the better choice; establish it on the whole
history (§6.1).

---

## 5. Comparing families, and when to optimise

### 5.1 Compare first, then optimise

A family (a plant structure: how the supply temperature is reached, how cold is made, how the gas
is used) decides more than any size within it. So:

1. When more than one family can serve the case, size each and rank them with ONE `run_study`
   (`method="run"`, `prepare=["size"]`): one row per family, feasible first, then by the
   objective.
2. Optimise the best one or two (`optimize`), not every family.
3. When the ranking of the sized families is close (within a few per cent on the objective), or
   when the best sized family is infeasible, optimise each of the close ones with the same
   budget (`run_study`, `method="minimize"`) before choosing.

Invented example: four families, sized: A 47.9, B 44.6, C infeasible (cold unmet), D 45.1
EUR/MWh. B and D are close: optimise both with 60 evaluations each; B reaches 41.8 and D 42.6.
Report the run study and the minimize study, both by key.

### 5.2 A fair comparison

Designs are compared on the same case and economics, with the same effort: a sized start
against an optimised rival is no comparison. Name what each design got (sized, optimised with
how many evaluations). A family that was not simulated is not ranked; it may be named as screened
out, with the reason.

### 5.3 Searching the structure itself

When the plant states optional modules or choices (a superstructure), `evolve_structure`
(`gm.study.evolve`) searches structures and values together: a genetic algorithm with one
objective, NSGA-II with two or more (a front of designs no other beats on every objective).
Quote gemini's own explanation and front table with the study key (skill `report`).

---

## 6. Reading a study

### 6.1 Read the whole study, not a sample of it

An optimisation's `history` holds every trial: its values, its objective, its violation (0 when
feasible) and the reason of an infeasible one. A conclusion about the search ("the optimum is
flat", "most designs are infeasible", "two doublets always win") must rest on all trials.

- Quote gemini's summary first: `best`, `feasible`, the number of trials (`trials`), and for a
  sample or sensitivity its `summary` or `rows`.
- Never page through a history one trial at a time and draw a conclusion from the part read.
  When the tools cannot summarise the whole history, say what is known (best, trials, feasible
  or not) and that the shape of the search was not assessed; a sensitivity around the best
  answers "how flat" properly (§3.1).
- Invented example of the mistake: a search of 240 trials; 27 are read one by one, 3 of them
  feasible; the answer says "only 3 of 27 feasible, the optimum is flat". Nothing in 27 trials
  says anything about the other 213.

### 6.2 Plant versions are designs

A project's stored plant versions are already designs: `design/v<N>` is version N. To rank six
versions, pass `design/v1` to `design/v6` to one `run_study`; never rebuild them with
`build_plant` (re-typing a plant drops values and costs a confirmation each). `v<N>` is reserved
for versions: give a new design another name.

### 6.3 Current and stale studies

A study ran on the case of its time. `list_studies` says whether it is `current`; one that is not
is quoted as "made on an older case" or run again. A study is never edited: a new run is a new
study with a new name.

---

## 7. Common mistakes

1. Ranking families sized against one family optimised (§5.2).
2. Optimising before any family comparison, or comparing families never optimised when the
   sized ranking is close (§5.1).
3. A search over a single doublet count when the case allows several (§4.1).
4. Ranges invented by the agent, or so wide most trials cannot work (§4.3).
5. Too few draws for a percentile, or too few evaluations for the number of variables (§0.4).
6. A conclusion from part of a history (§6.1).
7. Rebuilding stored plant versions instead of passing `design/v<N>` (§6.2).
8. A least-violating trial reported as a solution (§4.2).
9. A sensitivity or Monte Carlo written in `run_python` (§0.1).
10. A requirement of the case offered as the thing to change when a design stays infeasible
    (§0.3).
11. A study quoted without its key, or a stale study quoted as current (§6.3).
