# Writing an Engineering Design Report: A Handbook for Geothermal Heating and Cooling

How to report a plant design so that a reviewer can follow every decision back to its reason and
its source, and check every number. For the explainer, the reviewer and the project lead, and for
anyone who writes a feasibility study, concept design, competition entry or design memo.

Cite as `knowledge/handbook-report.md`, with the section number (for example
`knowledge/handbook-report.md §7.2`). Every numbered section stands alone. Chapter 0 is the short
version for agents; chapter 15 the review checklist; chapter 16 a worked example for a scored
brief; Appendix A templates.

This handbook explains no tool. Reading results: skill `reading-results`; quoting a study:
`comparing-designs` and `report`; uncertainty and sensitivity: `economics`; derived numbers:
`calculator` and `python`. The case: `knowledge/handbook-case.md`; the design:
`knowledge/handbook-design.md`; the costs and CO2 behind the numbers:
`knowledge/handbook-economics.md`. A value marked **(derived)** is explained by its formula; in a
report it is a number a tool gave, never one the writer computed. "Must" is a team rule, "should"
good practice (Appendix B).

---

# 0. Quick reference for the agents

## 0.1 Rules that hold in every section

1. **Every number from the state or a tool, digit for digit**, with the unit the tool returns.
   Never estimate, compute, round or convert one; a sum, share or difference is a tool's, or it
   is left out (§8.6).
2. **Every reference from the state or a tool**: `design.reference`, `design.result`,
   `verification.result`, `study/<name>`. Never a made-up one.
3. **Feasible means gemini's verdict**: `feasible` true with no reason, from the reviewer's
   `check_results` (state `verification`). Not the report's `passed`, which only tallies the
   checks that ran. A check with `passed` `None` is "not judged", never "passed" (§9).
4. **Every decision with its reason and source** (§7); every choice the agents made themselves
   and every case change the user approved is listed so the user can overrule it (§7.3).
5. **What gemini did not judge is open**, never compliant (§9.3, §11).
6. **No internal version numbers** to the user: say the case or the design was saved.

## 0.2 The explainer's headings: what goes under each

The explainer finishes with Markdown under exactly these headings, in this order:

| Heading | Holds | From | Section |
|---|---|---|---|
| `Design` | family, doublets (number, depth, flow), every unit, how the supply temperature is reached, how cold is made, where the gas goes | `read_plant`, state `design` | §8.1 |
| `Schematic` | the flow of brine, heating water, chilled water, gas and electricity, units labelled | state `design.schematic` | §8.1 |
| `Capacities` | each unit's capacity, peak use and share, against `peak_heat` and `peak_cold` | `compute_kpis` `capacities` | §8.2 |
| `Delivered` | heat and cold delivered beside the case's demand; surplus named; heat by source; electricity and gas bought | `compute_kpis` | §8.3 |
| `Costs` | capex, opex, LCOH, LCOC, LCTS, NPV, CO2 with units; the economic basis once; missing or unconfirmed economics | `estimate_costs`, state `results` | §8.4, §8.5 |
| `Checks` | gemini's verdict, then one line per requirement by `name`: worst value, limit, passed or "not judged" with the reason | state `verification` and the reviewer's report (its `check_results`) | §9 |
| `Open points` | what gemini did not judge, what the case does not constrain, unconfirmed assumptions, limitations | state `assumptions`, `verification` | §9.3, §11 |
| `Decisions` | each major decision with reason and source; the study's ranked table; agent choices and approved case changes | `list_studies`, `read_study`, `case_changes` | §6, §7 |

## 0.3 Order of work

1. Read once, in one step: `read_case`, `read_plant`, `compute_kpis` (no `names`),
   `estimate_costs`, `list_studies` on `design.result` and `design.reference`; `case_changes`.
   Never call them again for the same thing.
2. When a study's `tool` is `evolve_structure`, read `read_skill('report')` before `Decisions`.
3. Write the eight headings of §0.2, every number copied from step 1.
4. Check the answer against §0.4 before `finish`.

## 0.4 Short checklist (the full one is §15)

- [ ] Verdict first in `Checks`; `feasible` only when gemini says so; "not judged" named.
- [ ] Heat and cold delivered beside the demand; surplus said plainly.
- [ ] LCOH and LCOC with the `heat_cost_share` they rest on; LCTS for the ranking.
- [ ] Currency and price year stated once (`read_case` section `economics`).
- [ ] Every study cited by `study/<name>`; a study on an older case named so.
- [ ] Every `source: agent` assumption and approved case change listed under `Decisions`.
- [ ] No number that a tool did not give; no unit conversion.

## 0.5 When the job is done: stop rules

A review or an explanation is short when it reads only what it quotes. Every extra read makes
each later step slower and dearer, because the conversation grows.

**Reviewer.** In one step: `check_results`, `case_changes`, `compute_kpis` on the result. Then
record and finish. Read a module result (`read_result`) only for a failure of kind `requirement`
or `failed_step`, on that module and those days. A feasible verdict needs no module result. Never
read a case section you already hold from a whole `read_case`. The reviewer judges the verdict,
the case changes, a stale result and unconfirmed assumptions; an engineering review of the
structure, the dispatch or the backup is the analysis lead's, even when a brief asks for it.

**Explainer.** Read once, in one step (§0.3), and write. Quote no module result the answer does
not use. When the question is not the explanation of the verified design (another family, a
concept, a why), answer that question only, under headings that fit it, not the eight headings
of §0.2.

**Finding a section.** Open a handbook section by its number with `read_knowledge`
(§0.6). Search (`search_rag`) only to find which document holds a topic, a few times per answer
at most, never to fish for a section whose number you already know: a search returns snippets,
not the section.

Invented example: a reviewer gets a feasible verdict at step 2 and then reads twelve module
results and the case section by section until step 15. The verdict never changes; the thirteen
extra steps cost about four times the tokens of the whole review.

## 0.6 Which section answers which question

| Question | Read |
|---|---|
| What goes under each heading of the explanation | `knowledge/handbook-report.md` §0.2 |
| Is the design feasible; how to show the checks | §9 (feasible is the verdict, §9.1) |
| How to present alternatives and the ranking | §6 |
| How to state a decision and its reason | §7 |
| What each cost metric means; which tool gives it | `knowledge/handbook-economics.md` §0.5, §0.8 |
| How gemini computes a cost or CO2 | `knowledge/handbook-economics.md` §16 |
| How to present uncertainty and sensitivity | §10 here; method in `knowledge/handbook-economics.md` §12, §13 |
| What a scored brief or a page limit asks | §3.2, §16, and the brief's own document in Knowledge |
| The full review checklist | §15 |

## 0.7 What the writer asks, and what it does not

A report asks the user nothing. A value it lacks is named under `Open points` ("not given:
<what>, <why it matters>"); a missing economics key is named with its `economics.<key>` path for
the case lead. A brief's own facts (deliverables, scoring, page limits) come from its document
in Knowledge (search for it), never from memory; how to use them is §3.2 and §16.

---

# 1. What a design report is for

## 1.1 Readers and their questions

A design report has several readers, each with a question (audience analysis, Markel and Selber,
*Technical Communication*, 13th ed., 2021):

| Reader | Question | Reads |
|---|---|---|
| Decision maker (client, jury, investor) | Should we build this, and what does it cost? | executive summary, costs, risks |
| Reviewing engineer | Is it right, and does it meet the rules? | design basis, decisions, compliance, calculations |
| Operator | What runs when, and what are the limits? | plant, capacities, operating strategy |
| Next designer | What was assumed, and what is still open? | assumptions, limitations, open points |

Write so that each finds the answer in its own section, without reading the rest.

## 1.2 The report as evidence

A design report is evidence: every claim must be checkable. In this team that means
(`geomind/geomind/prompts/project/explainer.md`):

- every number comes from the problem state or a tool, digit for digit, with its unit;
- every reference (design, result, study) is one the state or a tool gave;
- every decision names its reason and its source;
- nothing is called compliant that gemini did not judge.

A number that cannot be traced is not evidence, however plausible it looks.

## 1.3 The reference textbooks in brief

- **ANSI/NISO Z39.18-2005 (R2010), *Scientific and Technical Reports: Preparation,
  Presentation, and Preservation*.** The standard for the elements, order and design of a
  technical report: front matter (title, abstract or summary, contents), text (introduction;
  methods, assumptions and procedures; results and discussion; conclusions; recommendations),
  back matter (references, appendices) (§2.1).
- **Markel and Selber, *Technical Communication* (13th ed., 2021).** Write for a named reader
  and a purpose; put the conclusion first; one idea per paragraph; design pages and figures so
  the reader finds what they need.
- **Tufte, *The Visual Display of Quantitative Information* (2nd ed., 2001).** Show the data;
  maximise the share of ink that carries data; avoid decoration and distortion; label directly
  (§12).
- **JCGM 100:2008 (GUM).** A result without its uncertainty is incomplete; state the best
  estimate, the range and how it was obtained (§10).
- **Nygard, "Documenting Architecture Decisions" (2011).** A decision record holds the
  context, the decision and its consequences, kept with the work (§7.1).

---

# 2. Structure

## 2.1 The standard parts of a technical report

After ANSI/NISO Z39.18-2005 (R2010):

| Part | Elements |
|---|---|
| Front matter | title, authors, date; abstract or executive summary; table of contents; lists of figures and tables |
| Text | introduction; methods, assumptions and procedures; results and discussion; conclusions; recommendations |
| Back matter | references; appendices; list of symbols and abbreviations |

## 2.2 A design report outline

For a heating and cooling plant design, the parts map to:

1. **Executive summary** (§4)
2. **Introduction**: the client, the site, the services, the scope of the study
3. **Design basis** (§5): the case, requirements, assumptions, economic basis
4. **Method**: the tools and models (gemini as the physics; the agent team; extra models and
   calculations), the workflow
5. **Alternatives considered** (§6)
6. **The selected design** (§8.1, §8.2): plant, schematic, capacities, operating strategy
7. **Results** (§8.3 to §8.5): energies, costs, emissions
8. **Compliance** (§9)
9. **Uncertainty and sensitivity** (§10)
10. **Decisions** (§7): every major decision with reason and source (may be a table in 5 or 6)
11. **Limitations and open points** (§11)
12. **Conclusions and recommendations**
13. **References and appendices**: sources, the agent log (§13), detailed tables

## 2.3 Short formats: pages and slides

A page limit forces choices, not smaller fonts:

- keep the executive summary, the design, the capacities, the compliance, the costs and the
  decisions; move detail to an appendix or a linked file;
- one table can carry the design basis, one the alternatives, one the compliance;
- one figure carries the plant (schematic), one the year (demand and supply over time);
- in slides, one message per slide, stated in its title (Markel and Selber 2021, on
  presentations).

## 2.4 The explainer's answer

The explainer of the design team finishes with Markdown under the headings `Design`,
`Schematic`, `Capacities`, `Delivered`, `Costs`, `Checks`, `Open points` and `Decisions`
(`geomind/geomind/prompts/project/explainer.md`). It is the core of the report: §8 maps to
`Design` to `Costs`, §9 to `Checks`, §11 to `Open points`, §7 to `Decisions`.

---

# 3. What reviewers look for

## 3.1 General review criteria

Whoever reviews a design report (a client's engineer, a lender's technical adviser, a jury)
asks the same questions:

1. **Is the problem right?** The case matches the brief; requirements say what the brief says;
   assumptions are sourced and confirmed.
2. **Were the alternatives real?** At least two serious options, compared on the same basis.
3. **Is the choice explained?** Each decision has a reason a reader can check.
4. **Does it work?** The whole period simulated; every requirement judged and met; failures
   reported, not hidden.
5. **What does it cost and emit?** On a stated economic basis, with the uncertainty.
6. **What is left?** Limitations and open points, stated plainly.
7. **Can it be reproduced?** Inputs, tools, versions, study keys and the log are given.

## 3.2 Scored briefs: competitions and tenders

Some readers score the report against published criteria: a competition jury, a tender panel, a
funding body. Then the criteria are the reader's questions:

- read the criteria and the weights before writing, and map each to a section of the report
  (a table, as in §16.1);
- answer each criterion where the reader expects it, with its evidence: a criterion on the
  workflow wants the method and the agent log (§13), one on the system wants capacities and
  compliance (§8, §9), one on economics wants the economic basis and the costs (§5.4, §8.4);
- keep to the format limits (pages, slides, video length): they are hard requirements of the
  brief, like any other;
- a brief's criteria, weights and limits are taken from its own document in Knowledge, never
  recalled.

These map onto the general criteria of §3.1: items 2 to 4 for a workflow, items 4 and 5 for a
system, item 7 for the record of how the work was done.

---

# 4. The executive summary

## 4.1 What it holds

On one page or less, in this order:

1. The problem in one sentence: the services, their peaks and annual energies, the site.
2. The recommended design: the plant family, the doublets (number, depth, flow), the main units
   with their capacities, how cooling is made.
3. Whether it meets the requirements (gemini's verdict), in one sentence.
4. The key numbers: capacities, energies delivered against demand, LCOH, LCOC, LCTS, capex, CO2,
   each with its unit and economic basis.
5. The main alternative and why it lost.
6. The largest uncertainty and its effect.
7. What remains open.

## 4.2 How to write it

- Conclusion first, then support (Markel and Selber 2021).
- Every number in it appears in the body with its source; nothing new appears only here.
- No jargon a decision maker cannot read: say "cost of heat" beside `lcoh`.
- Write it last, from the finished body.

---

# 5. The design basis

## 5.1 The case in one table

The design basis states what the plant was designed for, before any result: the period and
step, each service (demand file, peak, annual energy as gemini gave them, supply and return
temperatures), the site (ground, reservoir, brine, gas, air), the utilities (grid CO2
intensity, bought gas). Each row: the value, the unit, the source (file and page, knowledge
document and section, or user answer). How the case was set:
`knowledge/handbook-case.md`.

## 5.2 Requirements

One row per requirement of the case, by its `name`, as a sentence: "each doublet's production
flow between 50 and 300 m3/h in every step it runs". Add the source page and, for a tolerance
the brief did not give, that it is an assumption (`knowledge/handbook-case.md`
§6.8). Rules gemini cannot express are listed here as well, marked "not judged by gemini".

## 5.3 Assumptions and their sources

Every value that did not come from the user's files: the path, the value and unit, the source
or reason, and whether the user confirmed it. Separate the three kinds:

- from a source (a knowledge document, the cost catalogue, a connected server);
- design choices of the team (a return temperature, a search range);
- engineering assumptions without a source, approved by the user.

## 5.4 Economic basis

Currency and price year, discount rate (real or nominal), analysis period, energy and CO2
prices, revenue, cost allocation between heat and cold, the CH4 GWP and its standard; each with
its source. Explained in `knowledge/handbook-economics.md`. A cost without its price year
and currency cannot be compared with any other.

---

# 6. Alternatives considered

## 6.1 Why alternatives are reported

A single design proves only that it works, not that it is a good choice. Reporting the
alternatives shows the search was real and lets the reader see the price of each choice. For a
geothermal heating and cooling plant the usual alternatives differ in:

- how the supply temperature is reached (deeper wells, a heat pump, a boiler);
- how cold is made (absorption or adsorption chiller driven by geothermal heat, compression
  chiller, free cooling);
- how the associated gas is handled (flare, boiler, CHP);
- the number of doublets and the backup.

## 6.2 A fair comparison

Compare only designs that were (`geomind/geomind/prompts/project/explainer.md` and team practice):

- simulated over the whole period of the case and checked by gemini;
- on the same case and the same economics (a study on an older case is named so);
- sized or optimised with the same effort (a sized start against an optimised rival is no fair
  comparison; say what each got).

A family not simulated is not compared; it may be named as screened out, with the reason.

## 6.3 The comparison table

One row per design, as the study gave it (`run_study`, `compare`; skill `comparing-designs`):
design, family, feasible, rank, and the metrics with their units (LCTS, LCOH, LCOC, CO2, capex),
plus the study key `study/<name>` and whether it is `current`. Never re-rank, round or compute
in the table.

## 6.4 Trade-offs and the Pareto front

When two objectives conflict (cost and CO2), a design is on the Pareto front when no other is
better in both. Report the front as gemini gives it (`compare`'s `pareto`), name the trade-off
("design A costs X EUR/MWh less, design B emits Y kt less", each number from the tool), and say
which objective the choice favoured and why.

---

# 7. Decisions and their reasons

## 7.1 The decision record

Each major decision gets a short record (after Nygard 2011, adapted to engineering design):

| Field | Holds |
|---|---|
| Decision | what was chosen, in one sentence |
| Context | the requirement or the problem that forced a choice |
| Options | the alternatives considered |
| Reason | why this one: the numbers that decided, each with its source |
| Source | the file, knowledge document, `study/<name>`, `result/<id>` or calculation id |
| Consequences | what it costs, what it rules out, what stays open |

In a short report the record is one table row or one sentence with its reason and source. A
decision without a reason is an assertion; a reason without a source is an opinion.

## 7.2 The major decisions of a geothermal heating and cooling plant

| Decision | Typical reason and source |
|---|---|
| Plant family | the ranking of the study (`study/<name>`), the trade-off |
| Depth and number of doublets | temperature and flow needed against drilling cost and the flow limits; the study or optimisation |
| How the supply temperature is reached | production temperature at the chosen depth against the supply temperature (heat pump, boiler or depth) |
| How cold is made | the cold demand, the heat available, the COPs; geothermal-driven cooling where it works |
| Return temperatures | design choice within the brine cooling limit and demand met |
| Backup policy | demand met on every day; doublet availability |
| Associated gas handling | methane emissions, energy value, cost |
| What the optimisation changed | the sized start against the optimised design, from the study |

## 7.3 Choices the agents made themselves

List every assumption with `source: agent` (its value and reason) and every case change the
user approved, so the user can overrule them (`geomind/geomind/prompts/project/explainer.md`).
Hidden choices are the first thing a reviewer looks for.

## 7.4 Decisions that rest on a study

Cite the study key that each comparison, ranking, uncertainty range or choice relies on; say
plainly when a study ran on an older case. A structure search (`evolve_structure`) is quoted with
gemini's own explanation and front table (skill `report`).

---

# 8. Results

## 8.1 The plant and its schematic

Name the family, the doublets with their depth and flows, and every unit with its capacity. The
schematic shows the flow of brine, heating water, chilled water, gas and electricity; each unit
labelled with its capacity. A reader must be able to follow the brine from the production well
to the injection well and see where its heat goes.

## 8.2 Capacities

Capacities come from gemini's `capacities` (through `compute_kpis`; `gemini/gemini/evaluate/summary.py`):
for each equipment module its `kind`, design `capacity`, `peak` use in the run and `share`
(peak over capacity). Report them against the peaks of the demand (`peak_heat`, `peak_cold`):

- a share near 1 means the unit sets the plant's limit;
- a share far below 1 means it is oversized, or a backup that rarely runs (say which);
- a unit with no use shown carries the reason gemini gives.

The realised heating and cooling capacities of the plant are the deliverable most readers want
first: give them as gemini gives them.

## 8.3 Energies delivered

Heat and cold delivered over the period (`heat_delivered`, `cold_delivered`) beside the demand
of the case, and where useful the heat from each source (`boiler_heat` and others as gemini
gives them), the electricity and gas bought (`electricity_bought`, `gas_bought`), electricity
sold. Where delivered heat exceeds the demand, say so plainly. Days not covered come from the
coverage gemini reports; never count them by hand.

## 8.4 Costs and key performance indicators

gemini's metrics with their display titles (`gemini/gemini/evaluate/_utils/display.py`):

| Name | Title | Notes |
|---|---|---|
| `capex` | Investment | by module, as `estimate_costs` gives it |
| `opex` | Operating cost | per year |
| `annualised_cost` | Annualised cost | capex annuity plus opex |
| `lcoh` | Cost of heat | with the heat's cost share |
| `lcoc` | Cost of cold | with the cold's share |
| `lcts` | Cost of thermal supply | one cost over heat and cold together |
| `npv` | (no display title) | net present value; needs revenue |
| `payback` | Payback time | needs revenue |
| `co2` | CO2 | CO2-equivalent |
| `methane_emitted` | Methane emitted | vented methane |

Give LCOH, LCOC and LCTS, capex and opex, with the economic basis (§5.4). Say which economic
assumptions are missing or not confirmed. What each metric means and how it is computed:
`knowledge/handbook-economics.md`.

## 8.5 Emissions

CO2-equivalent of the period, with what it contains: CO2 from burnt fuel and released brine
gas, vented methane times its GWP, grid electricity times the grid intensity, and any offset of
on-site power (`knowledge/handbook-economics.md` §9, §16.6). State the GWP standard and the
grid intensity's source. The carbon cost in the opex covers only the plant's own CO2 and methane,
not the grid electricity's CO2 (gemini 0.6.16 and later; `knowledge/handbook-economics.md`
§16.7): say so when both the CO2 and the carbon cost are reported.

## 8.6 Quoting numbers

- Each number with the unit the tool returns, digit for digit: `111667.68 MWh`, not "about 112
  GWh" (`geomind/geomind/prompts/project/explainer.md`).
- No conversion of your own: a UA of `1500000.0 W/K` is written so, not "1.5 MW/K".
- A sum, share or difference is one a tool gave, or a calculation with its id
  (`calculate`, skill `calculator`), or it is left out.
- In a document written by people after the run, rounding for readability is allowed only with
  the exact value in a table or appendix.

---

# 9. Compliance with the requirements

## 9.1 gemini's verdict

A design is final only when gemini's verdict is feasible: `check_results` returns `feasible`
true with no reason (skill `reading-results`; reviewer rule). The report's `passed` is not the
verdict: it tallies only the checks that ran, so a plant that delivers no cold can show `passed`
true while `cold_delivered` makes the verdict infeasible (`knowledge/handbook-economics.md`
§16.7). gemini's verdict has four kinds of reason
(`gemini/gemini/evaluate/verdict.py`): `requirement` (a requirement or a supply temperature
failed, or none could be judged), `failed_step` (rows that failed or were skipped),
`numerical` (a mass or energy residual above tolerance, a loop that did not converge) and
`bound` (an output outside its module's limits or operating limits). A result with a failed step
is not feasible, whatever its totals say.

## 9.2 The compliance table

One row per check gemini made (`gemini/gemini/evaluate/verdict.py`, `requirements`): each check
is `{name, role, unit_path, quantity, passed, value, limit, worst_step}`, one per unit and
requirement, plus the supply temperature of each service, checked in the steps the service
runs.

| Requirement (`name`) | Unit | Rule | Worst value | Limit | Worst step | Passed |
|---|---|---|---|---|---|---|

- `value` is the worst value of the run for `over: each`, otherwise the figure of the run;
- `limit` the bound violated, else the nearest one: it shows the margin;
- `passed` `None` means not judged (a unit that carried no flow, or a field the run does not
  hold): write "not judged" with gemini's reason, never "passed".

## 9.3 What was not judged

Never call the design compliant on a point gemini did not judge. List as open: rules the case
could not express (`knowledge/handbook-case.md` §6.10), checks with `passed` `None`,
and everything outside the model (permits, noise, land, grid connection).

## 9.4 A design that does not pass

When a rule keeps failing after a real change of approach, report the best design with the
passing and failing rules by name, the worst values and their owners, and what was tried (team
rule, QA-090): never an empty result, never a failure dropped. A zero-demand day is no failure
of a supply temperature judged while running (QA-091).

---

# 10. Uncertainty and sensitivity

## 10.1 Stating uncertainty

A result is a best estimate with its uncertainty: the range, how it was obtained (which values
were uncertain, which distributions, how many draws, the seed) and its source
(JCGM 100:2008). Uncertainty and sensitivity runs happen only when the task asks (skill
`economics`); when they did not run, say the result is deterministic and name the largest
uncertain inputs.

## 10.2 Presenting a Monte Carlo result

Give, for each metric, the mean and two percentiles (for example p5 and p95) as the study gives
them, the number of draws, the failed draws, and the study key. A histogram or a cumulative
distribution shows the spread; with few draws, say the percentiles are rough.

## 10.3 Presenting a sensitivity

A one-at-a-time sensitivity moves each uncertain value to its two ends while the others stay at
their base. Present it as a tornado chart or a table, largest effect first: the value, its low
and high end, the metric at each end, the effect. Name the dominant driver in words.

## 10.4 Accuracy of a cost estimate

A concept-stage cost estimate is uncertain by tens of percent. The AACE International
recommended practice 18R-97 classifies estimates by project definition: a Class 5 (concept
screening) estimate is commonly reported with an accuracy of about −20 % to −50 % low and +30 %
to +100 % high, a Class 4 (feasibility) estimate about −15 % to −30 % and +20 % to +50 %
(as reported by secondary summaries of 18R-97; check against the AACE document before quoting).
State the class of the estimate, or at least that capex rests on generic cost data, so a reader
does not take a digit-for-digit figure as precise.

---

# 11. Limitations and open points

State plainly:

- simplifications of the model (daily steps hide hourly peaks; constant air temperature; a
  missing model filled by a simplified calculation, and why it is appropriate);
- assumptions not confirmed by the user;
- requirements not judged (§9.3);
- data of low quality (estimated reservoir values);
- what the case does not constrain;
- what a next study should do.

A limitation stated is a strength of the report; one discovered by the reviewer is a weakness.

---

# 12. Figures and tables

## 12.1 Principles

After Tufte (2001) and Markel and Selber (2021):

- one message per figure, stated in the caption;
- show the data; drop decoration, 3-D effects, heavy grids;
- label axes with quantity and unit; label lines directly rather than through a legend;
- the same quantity in the same unit and colour across figures;
- never distort: bars start at zero; a broken axis is marked.

## 12.2 Figures a heating and cooling report needs

| Figure | Shows |
|---|---|
| Schematic | units, connections, capacities; the brine path |
| Demand and supply over the year | heating and cooling demand and what each source delivers, per step |
| Load duration curve | demand sorted from highest to lowest: base and peak load (Frederiksen and Werner 2013) |
| Days covered | which days the demand was met, per service |
| Capex by kind | where the investment goes |
| Alternatives | cost against CO2, the Pareto front marked |
| Sensitivity (tornado) | which input drives the cost |
| Uncertainty | distribution of LCTS and CO2 |

## 12.3 Tables

Use a table when the reader needs exact values; a figure when the shape matters. Units in the
column header, not in every cell. Align numbers by the decimal point. Keep the order of a table
the same throughout the report (the requirements in the case's order).

## 12.4 Captions and numbering

Number figures and tables in order and refer to each in the text before it appears
(ANSI/NISO Z39.18-2005). A caption says what is shown and its source ("Figure 3. Heat delivered
by source, 2027, daily; result/<id>").

---

# 13. The agent log

## 13.1 Why it is part of the report

When agents did the work, the log is the method: it shows how the problem was analysed, which
models were run, which questions the user answered, which gaps were found and filled. A
reviewer who cannot see the log cannot judge the workflow; a scored brief may score it
(§3.2).

## 13.2 What to record

- the model and provider of each agent role;
- each LLM call: prompt, answer, tool calls with arguments and results, tokens in and out, by
  agent, session and step;
- each question to the user and the answer;
- the studies run and their keys;
- extra calculations and their ids (`calculate`, `run_python`), web searches and their sources;
- totals: tokens and cost per agent and for the run.

## 13.3 How to present it

In the body, a short account: the team (roles), the workflow (in the order it happened), the
number of steps, questions and tokens by agent. In an appendix or a linked file, the full log.
geomind.team's Report page builds a report from a result and includes the agent log of the run
chosen under "Agent log from" (`frontend/src/domains/design/report/report-options.tsx`).

## 13.4 Gaps found and filled

Name every capability the tools lacked and how it was filled: a simplified model, a calculation
with its id, a value found on the web with its source, and why it is appropriate. A brief may
expect gaps and score how they were filled; in any study a gap explained is better than a gap
hidden.

---

# 14. Style

## 14.1 Plain technical English

- Short sentences, active voice, one idea per paragraph (Markel and Selber 2021).
- The same term for the same thing throughout (not "doublet", "well pair" and "geothermal loop"
  in turn).
- No promotional words ("innovative", "robust", "state of the art"): show the number instead.
- Never name an internal version number to the user; say the case or the design was saved.

## 14.2 Numbers and units

- A space between number and unit (`30 MW`), unit symbols upright, no plural (BIPM, *The SI
  Brochure*, 9th ed., 2019, chapter 5).
- Temperature in °C for levels, K for differences.
- Every number with a unit, every cost with currency and price year.

## 14.3 Citations

Every value from a source carries it: file and page, knowledge document and section, catalogue
row id, study key, result reference, calculation id, URL with the date read. A reference list
at the end gives full entries.

---

# 15. Review checklist

For the reviewer and the project lead, before a report goes out:

**Basis**
- [ ] The case is the one the user gave, or every change was approved (`case_changes`).
- [ ] Every requirement of the case appears, by name, in the compliance table.
- [ ] Every assumption has a source or a reason and says whether the user confirmed it.
- [ ] The economic basis states currency, price year, discount rate and period.

**Design and decisions**
- [ ] At least two alternatives, simulated over the whole period and checked, on the same case.
- [ ] Every major decision of §7.2 has a reason and a source.
- [ ] Every agent choice is listed so the user can overrule it.
- [ ] Each study is cited by key; a study on an older case is named so.

**Results**
- [ ] Capacities of every unit and of the plant, against the demand peaks.
- [ ] Heat and cold delivered against demand; surplus named.
- [ ] LCOH, LCOC, LCTS, capex, opex, CO2 with units and basis.
- [ ] Every number traceable to a tool or the state, digit for digit; no number computed by
      the writer.

**Compliance and uncertainty**
- [ ] `passed` only with gemini's feasible verdict and no failure.
- [ ] Every check not judged is named "not judged" with its reason.
- [ ] Uncertainty stated, or the result named deterministic with its main uncertain inputs.
- [ ] Limitations and open points listed.

**Form**
- [ ] Executive summary matches the body.
- [ ] Figures numbered, captioned with source, axes with units.
- [ ] The agent log is included or linked.
- [ ] Within the length limit.

---

# 16. Worked example: a report for a scored design brief

Every number in this chapter is **invented**. The brief, its scores and its limits stand for any
competition, tender or client brief that scores the report; the real criteria of a given brief
are in its own document in Knowledge (search for it), never in this handbook.

## 16.1 Reading the scoring before writing

An invented brief scores half the marks on the **workflow** (how the problem was analysed, which
models ran, which gaps were found and filled, how alternatives were compared, how the final
choice is explained) and half on the **system** (technologies chosen and sized, heating and
cooling capacities, the design), with extra credit for uncertainty analysis, costs and
autonomous verification. Map each criterion to a section before writing:

| Criterion of the brief | Where the report answers it |
|---|---|
| Problem analysed | §5 design basis |
| Models selected and run, gaps filled | §2.2 method, §13.4 |
| Alternatives compared | §6 |
| Final choice explained | §7 |
| Technologies and capacities | §8.1, §8.2 |
| Uncertainty, costs | §8.4, §10 |
| Verification | §9 |
| Agent interaction (prompts, answers, tokens) | §13 |

A criterion with no section is a gap in the report, not in the scoring.

## 16.2 Fitting the page limit

The invented brief allows 5 pages (or 10 slides). One allocation that covers every criterion:

1. Problem and inputs (half a page): the brief's files, the case, one assumptions table with
   sources.
2. Method and agent team (one page): roles, tools, gemini as the physics, the model behind the
   agents, Knowledge, the gaps found and how they were filled.
3. Alternatives and the chosen design (one and a half pages): the comparison table (§6.3), the
   schematic, the capacities.
4. Results (one and a half pages): delivered against demand, the compliance table, costs and
   CO2 with the economic basis, uncertainty and sensitivity.
5. Agent interaction and open points (half a page): questions to the user, tokens per agent, the
   limitations.

Detail goes to an appendix or a linked file (§2.3).

## 16.3 The explainer's answer for an invented case

The case: 100 000 MWh/yr of heat at 90 °C (peak 25 MW) and 20 000 MWh/yr of cold at 12 °C from
a deep doublet reservoir producing 75 °C brine with dissolved gas.

- **Design / Schematic:** two doublets at 3000 m, each at 200 m3/h; a heat pump lifts the
  geothermal heat to 90 °C; an absorption chiller driven by hot water makes the cold; the
  associated gas goes to a boiler (the reason under `Decisions`).
- **Capacities:** each unit as `compute_kpis` gives it, beside the 25 MW peak heat.
- **Delivered:** heat and cold delivered beside the 100 000 and 20 000 MWh/yr of the case; a
  surplus named.
- **Costs:** capex, opex, LCOH, LCOC, LCTS, NPV and CO2 with the economic basis once (currency,
  price year, discount rate, period, `heat_cost_share`); placeholder values named, so NPV reads
  as indicative.
- **Checks:** the verdict first, then each requirement by `name` with its worst value and limit.
- **Open points:** what gemini did not judge; assumptions not confirmed.
- **Decisions:** the family ranking (`study/<name>`), the depth and number of doublets, the
  supply temperature route, the cooling technology, the gas handling (vent, flare, boiler or CHP:
  `knowledge/handbook-economics.md` §17.7), what the optimisation changed.

## 16.4 For the reviewer and the project lead

- A design is final only with gemini's verdict `feasible` true (§9.1; not the report's
  `passed`). A zero-cooling day is no failure of a cooling requirement judged while running.
- When a rule keeps failing after a real change of approach, finish with the best design, the
  passing and failing rules by name and their owners (§9.4).
- Never call the design compliant on a point gemini did not judge.

---

# Appendix A. Templates

## A.1 Report skeleton

```markdown
# <Project>: geothermal heating and cooling plant, <stage> design
<authors>, <date>

## Executive summary
## 1 Introduction
## 2 Design basis
### 2.1 Case  ### 2.2 Requirements  ### 2.3 Assumptions  ### 2.4 Economic basis
## 3 Method: tools, models, agent team
## 4 Alternatives considered
## 5 Selected design: plant, schematic, capacities, operation
## 6 Results: energies, costs, emissions
## 7 Compliance
## 8 Uncertainty and sensitivity
## 9 Decisions
## 10 Limitations and open points
## 11 Conclusions and recommendations
## References
## Appendix: agent log, detailed tables
```

## A.2 Decision record

```markdown
**Decision:** <what was chosen>
**Context:** <requirement or problem>
**Options:** <A, B, C>
**Reason:** <the deciding numbers, each with its source>
**Source:** <file p. / knowledge/<doc> §/ study/<name> / result/<id> / calculation id>
**Consequences:** <cost, what it rules out, what stays open>
```

## A.3 Compliance table

```markdown
| Requirement | Unit | Rule | Worst value | Limit | Worst step | Passed |
|---|---|---|---|---|---|---|
| production_flow_range | <unit_path> | 50 to 300 m3/h, each running step | <value> | <limit> | <time> | yes / no / not judged (<reason>) |
```

## A.4 Assumptions table

```markdown
| Path | Value | Unit | Source or reason | Kind | Confirmed |
|---|---|---|---|---|---|
```

# Appendix B. References

- ANSI/NISO Z39.18-2005 (R2010). *Scientific and Technical Reports: Preparation, Presentation,
  and Preservation*. Baltimore: NISO. ISBN 978-1-880124-66-6.
- Markel, M. and Selber, S. A. (2021). *Technical Communication*, 13th ed. Boston: Bedford/St.
  Martin's.
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information*, 2nd ed. Cheshire, CT:
  Graphics Press.
- JCGM 100:2008. *Evaluation of measurement data — Guide to the expression of uncertainty in
  measurement* (GUM). BIPM.
- Nygard, M. (2011). "Documenting Architecture Decisions". Blog post, Cognitect.
- AACE International Recommended Practice 18R-97. *Cost Estimate Classification System — As
  Applied in Engineering, Procurement, and Construction for the Process Industries*. (Ranges in
  §10.4 from secondary summaries.)
- BIPM (2019). *The International System of Units (SI)*, 9th ed.
- Frederiksen, S. and Werner, S. (2013). *District Heating and Cooling*. Lund:
  Studentlitteratur. ISBN 978-91-44-08530-2.
- gemini source: `gemini/gemini/evaluate/verdict.py`, `summary.py`, `_utils/display.py`.
- geomind: prompts `geomind/geomind/prompts/project/explainer.md`, `reviewer.md`; skills
  `reading-results`, `comparing-designs`, `report`, `economics`, `calculator`, `python`.
- Team: bug files QA-090, QA-091, QA-094 of the team's quality assurance.
