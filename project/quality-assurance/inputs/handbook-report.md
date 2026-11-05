**Writing an Engineering Design Report: A Handbook for Geothermal Heating and Cooling**

How to report a plant design so that a reviewer can follow every decision back to its reason and
its source, and check every number. For the explainer, the reviewer and the project lead, and for
anyone who writes a feasibility study, concept design, competition entry or design memo.

Cite as `knowledge/handbook-report.md`, with the section number (for example
`knowledge/handbook-report.md §7.2`). Every numbered section stands alone. Chapter 0 is the short
version for agents; chapter 15 the review checklist; chapter 16 a worked example for a scored
brief; chapter 17 lessons from reviewed reports; Appendix A templates.

Outline: 0 Quick reference · 1 Purpose · 2 Structure · 3 What reviewers look for · 4 Executive
summary · 5 Design basis · 6 Alternatives · 7 Decisions · 8 Results (8.6 numbers, 8.7 heat by
source, 8.8 COP and SPF, 8.9 energy balance) · 9 Compliance (9.5 scope, 9.6 values) · 10
Uncertainty · 11 Limitations · 12 Figures and tables · 13 Agent log · 14 Style · 15 Checklist ·
16 Worked example · 17 Lessons from reviewed reports · 18 Explaining a result · 19
Recommendations and risks · 20 Indicators beyond cost · 21 gemini's metrics · A Templates · B References.

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

1. **Every number from the state or a tool**, with the unit the tool returns, shown to four
   significant figures (§8.6). Never estimate, compute or convert one; a sum, share or
   difference is a tool's, or it is left out (§8.6).
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
| What a study found, how many runs it took, how to read its history | `knowledge/handbook-studies.md` §0.2, §0.4, §6.1 |
| Heat by source (geothermal, heat pump, boiler) | `knowledge/handbook-economics.md` §1.4 |
| How to round and write numbers | §8.6 |
| What "geothermal share" may claim; heat by source | §8.7 |
| COP, SPF or plant ratio | §8.8 |
| Does the energy balance close; fuel by source | §8.9 |
| What the checks cover; every check with its number | §9.5, §9.6 |
| A short form; which design when several; stale results | §17 |
| Why a cost is what it is; what moved between two results | §18.1, §18.2 |
| Why this design and not another | §18.3 |
| How to write a recommendation, risks, next stage | §19 |
| Full-load hours, capacity factor, specific indicators | §20 |
| What a gemini metric name means (`cop`, `heat_useful`, `capacities` ...) | §21 |
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

- every number comes from the problem state or a tool, with its unit, shown to four significant
  figures (§8.6);
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

The study side of a fair comparison (same case, same effort, compare then optimise):
`knowledge/handbook-studies.md` §5.2.

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

Heat by source (geothermal, heat pump, boiler) comes from gemini's split, never from
subtracting one unit's output from the total: a boiler may also drive a chiller, and a heat pump's
output includes its compressor work (`knowledge/handbook-economics.md` §1.4).

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

- Each number with the unit the tool returns, rounded to **four significant figures**, never
  with more digits than the tool gave: `34.63640461864158 MEUR` is `34.64 MEUR`, `253.8975 MWh`
  is `253.9 MWh`, `111667.68 MWh` is `111700 MWh` (better: `1.117e5 MWh` in a table)
  (`geomind/geomind/prompts/project/explainer.md`; QA-099, QA-234).
- A share from zero to one is a percent: `0.9999925` is `100.0 %`. A value smaller than `1e-9`
  of its limit is `0` (`1.0178e-16` unmet share is `0 %`): it is numerical noise, not a result.
- Rounding is the only change. No conversion of your own: a UA of `1500000.0 W/K` is
  `1.500e6 W/K`, not "1.5 MW/K"; the unit stays the tool's.
- Round once, at the end, from the tool's value; never round a rounded number again, and never
  compute with rounded numbers (ISO 80000-1:2022, Annex B; NIST SP 811, Appendix B.7).
- A sum, share or difference is one a tool gave, or a calculation with its id
  (`calculate`, skill `calculator`), or it is left out.
- Write the number and the unit with a space (`45.1 EUR/MWh`, `12 %`), the unit symbol upright
  and never pluralised (BIPM SI Brochure, 9th ed., §5.4.3).
- Four significant figures are presentation, not accuracy: a concept capex is uncertain by tens
  of percent (§10.4). Say so once instead of trimming digits further.

Invented example: a tool gives LCOH `48.927109216402506 EUR/MWh` and an unmet share
`2.3e-17`. The report writes "LCOH 48.93 EUR/MWh; unmet heat 0 %", and in `Costs` one line: "A
concept-stage estimate; capex accuracy about −30 % to +50 % (§10.4)".

## 8.7 Heat by source: what "geothermal" may claim

A share of heat is named by where the energy came from, never by the plant's name. gemini's
daily coverage splits each service into `geothermal` (heat taken from the brine), `electricity`
(the work a heat pump or a compression chiller adds), `backup` (boilers, CHP, electric boilers,
compression chillers used as cooling backup) and `short` (unmet) (`gemini/gemini/evaluate/
coverage.py`, `KEYS`, `BACKUP_ROLES`). Heat by source for the year is in
`knowledge/handbook-economics.md` §1.4.

- A heat pump's output is not all geothermal: its electricity is a separate source. "Geothermal
  covers 100 %" for a plant with a heat pump on grid power is wrong (QA-270); write "brine heat
  x %, heat-pump electricity y %, boilers z %" with the tool's figures.
- Renewable claims follow a stated rule. The EU Renewable Energy Directive counts as renewable
  only `E_RES = Q_usable × (1 − 1/SPF)` of a heat pump's output, and only when its seasonal
  performance factor is high enough (Directive (EU) 2018/2001, Annex VII). Name the rule if the
  report claims a renewable share, or make no such claim.
- Produced gas burned on site is a fuel of the plant: name it beside gas bought (§8.9).

Invented example: a year delivers 100 GWh of heat: brine 70 GWh, heat-pump electricity 18 GWh,
boilers 12 GWh. The report says "brine heat 70 %, heat-pump electricity 18 %, boilers 12 %",
never "geothermal 88 %".

## 8.8 Performance ratios: say what is divided by what

A coefficient of performance (COP) is one machine's useful heat (or cold) divided by that
machine's electricity, at stated conditions (EN 14511 for rated values). A seasonal performance
factor (SPF) is the same over a season, inside a stated boundary: the SEPEMO-Build boundaries H1
to H4 add, step by step, the source pumps, the backup heater and the distribution pumps (SEPEMO-Build;
Zottl et al., 2012). A plant ratio such as "heat delivered per MWh of electricity bought" includes
geothermal and boiler heat and is not a COP: name it in words (QA-322).

- Quote a COP only from the tool for that unit (per-unit results, `compute_kpis`), with the
  boundary; never divide two plant totals and call it a COP.
- A heat-pump COP far above the Carnot limit `T_hot / (T_hot − T_cold)` (kelvin) is an error of
  definition, not a good machine (Çengel and Boles, 2019, ch. 6).

Invented example: a plant delivers 120 GWh of heat and buys 6 GWh of electricity; its heat pump
alone makes 30 GWh from 7.5 GWh of its own electricity, partly self-generated. The heat pump's
SPF (H1) is 4.0; "20 MWh of heat per MWh bought" is a plant ratio, and calling it COP 20 is
wrong.

## 8.9 The energy balance closes

The first law holds for the plant and for each unit: energy in (brine heat, electricity, fuel by
source, absorbed heat) equals energy out (heat and cold delivered, rejected heat, losses), within
the tolerance gemini reports (`gemini/gemini/evaluate/balances.py`, `ENERGY_INPUTS`). Show every
input, so a reader can check a unit's efficiency.

- List fuel by source: gas bought, produced gas burned, gas flared. Showing only gas bought next
  to boiler heat makes a reader compute an efficiency above 100 % (QA-323).
- A boiler efficiency above about 1.0 on the lower heating value, or a balance residual above
  gemini's tolerance, is a finding for the reviewer, not a number to explain away.
- A plausibility check of a large figure is allowed with `calculate` and its id: brine heat is
  `ρ · c_p · V̇ · ΔT`.

Invented example: 200 m3/h of brine cooled by 30 K with ρ c_p = 4.0 MJ/(m3 K) gives
`calculate`: 200/3600 × 4.0e6 × 30 = 6.67 MW. A result that claims 20 MW of brine heat from the
same flow and cooling is wrong somewhere; the reviewer names it.

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

## 9.5 Say what the checks cover

"All 12 checks pass" reads as full validation unless the report says what was checked (QA-325).
Next to the verdict, state in one or two lines:

- the period simulated and its time step (for example one year of daily steps), and that the
  plant's lifetime behaviour was not simulated unless a study did so;
- the case's rules that were checked, and the quantities gemini can bound but this case did not
  (`knowledge/handbook-case.md` §6.10);
- what lies outside the model: reservoir pressure decline over the years, thermal breakthrough
  between wells, injectivity beyond the modelled value, scaling and corrosion, permits.

Thermal breakthrough and pressure decline are lifetime questions of the doublet: their time
scale depends on well spacing, flow and reservoir thickness, and they are judged with a
reservoir model over decades (Grant and Bixley, 2011; Willems et al., 2017). A
one-year plant simulation does not answer them; the report names them as open (§11).

Invented example: "gemini's verdict is feasible: 9 of 9 checks pass over one simulated year
(daily steps). Not checked: pressure decline and thermal breakthrough over the 30-year life
(no reservoir model run), CO2 limit (the case sets none)."

## 9.6 Every check with its number

A requirement's value, limit and worst step are in `check_results` `requirements`, not only in
`read_result`. Never write that a requirement "rests on gemini's verdict" when its entry has a
value: quote the value and the limit (QA-124; skill `reading-results`). Only a check with
`passed` `None` has no value, and it is "not judged" with its reason (§9.2).

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
- [ ] Every number traceable to a tool or the state, to four significant figures; no number computed by
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

# 17. Lessons from reviewed reports

Each lesson is general; the bug file named in brackets is where the team learnt it.

## 17.1 Answer the question that was asked

A follow-up question gets its own answer, not the earlier report again. A format the user names
("short form", "for my manager", "one slide") sets the length: one table and three to five lines
of recommendation, not the full eight headings (QA-289, QA-333). The rule is the old one of
technical writing: the reader's question decides the content and the length (Markel and Selber,
2021). Run the explainer once per question; re-running it with the same brief adds
nothing.

Invented example: "Short form for my manager: v1 or v2?" The answer is a two-column table
(LCTS, capex, CO2, verdict) and "Recommend v1: 8 % lower LCTS, both feasible; open: no
lifetime reservoir study."

## 17.2 Report what was asked; offer the rest

A report of an existing design reports that design and its existing studies. A sensitivity or
an uncertainty study the user did not ask for is offered as a next step (the finish
suggestions), never run inside the report (QA-257). A study run without being asked costs time
and tokens and changes what the user has to read.

## 17.3 Which design: when the project holds several

When the project holds more than one plant version and the request names none, the report
either compares the current versions on the same case (a plain simulate each is cheap) and
recommends one with its reason, or asks the project lead which to report. Never call the latest
version "the recommended design" without that comparison (QA-337). A fair comparison is §6.2.

## 17.4 Never claim a model is missing without looking

Before writing "gemini cannot model X", look it up: `list_plants`, `list_modules`,
`describe_module`. A module can serve several roles: a `HeatPump` in the role `chiller` is an
electric compression chiller (`gemini/gemini/evaluate/coverage.py`, `BACKUP_ROLES`; QA-334).
Compare a choice with the reference plant families `list_plants` gives, and give the reason from
the design and its numbers.

## 17.5 A result belongs to one case and one design

Every number quoted must come from a result that ran the current design on the current case. A
result that ran an older case version or another plant is stale: say so at the top ("this
result ran on an earlier case; run it again before sending") or run it again (QA-290, QA-233).
A study made on an older case is named as such (§0.4). The reviewer's check of a stale result is
§0.5.

## 17.6 One read, then write

Every read is quoted, or it is not made. A reviewer with a feasible verdict at step 2 is done
after recording it; an explainer reads the five tools of §0.3 once and writes (QA-187, QA-218).
A section of a handbook is opened by its number with `read_knowledge`, after the outline;
`search_rag` only finds which document holds a topic (QA-351).

## 17.7 Name the design and the case that ran

Say which design a result ran, by the reference the state gives (`design.reference`,
`design.result`), and on which case. A simulate without a named design may run another plant
than the one the answer describes (QA-166). Internal version numbers differ from what the app
shows: say "the saved case" or "the plant saved as the project's design", not "case version 16"
(QA-114). "The plant simulates the full year" is true only of a result that did; a plant page
that still lists missing values contradicts it (QA-092).

## 17.8 A claim about a unit rests on its series

"Not used", "runs at full load" or "oversized" is read from the unit's results, not guessed.

- Used or not: a unit that carries flow on any step is used; give its peak and its mean (or its
  energy of the period). Two answers about the same result must agree (QA-123).
- Capacity against peak use: when a unit's rated capacity is far above its peak use, say so
  with both numbers; a capacity left at the top of its search range is a sign the sizing did not
  bound it (QA-324).
- Rated against operating point: a pump or a machine running above its rating is a finding,
  even when every check of the case passes, because the case may not bound it (QA-130). Name it
  under `Open points` and for the design lead.

Invented example: an exchanger rated 12 MW peaks at 7.9 MW and averages 4.1 MW: "used all
year; peak 66 % of rating". A dry cooler rated 20 MW peaks at 6 MW: "oversized: peak 30 % of
rating; its size was not optimised".

## 17.9 When two outputs disagree, say so

Two outputs of one result that contradict each other (a coverage that says the source was off
while the running-time check says it ran; a delivered energy above the demand while coverage
says met exactly; a feasible verdict beside a value over a hard limit) are a finding, not a
choice (QA-214, QA-226, QA-132). The reviewer names both numbers, their tools and the gap; the
report quotes neither as settled until it is explained. A verdict is only as good as the checks
the case holds (§9.5).

## 17.10 No number by subtraction or by hand

A quantity the tools do not give is not built from two that they do: "geothermal heat =
heat delivered − boiler heat" is wrong when other sources (heat-pump electricity, produced gas)
also feed the heat (QA-228). Use the tool's split (§8.7) or leave it out.

## 17.11 Say how much evidence an answer rests on

An optimisation or study answer says how many trials it ran and how many it read: "best of
240 trials, all read" (QA-205; `knowledge/handbook-studies.md` §6.1). A ranking of families
rests on a like-for-like comparison (§6.2); a winner chosen between a sized design and a
re-typed or unsized rival is no result (QA-278). A broad question ("is it a good investment?")
covers every declared uncertainty (`knowledge/handbook-studies.md` §3.1; QA-263).

## 17.12 An approved change is not a deviation

Every case change the user approved (`case_changes`) is part of the case. A reviewer that
rejects a design because the case "differs from what the user gave" after the user approved the
difference is wrong (QA-317). Report approved changes under `Decisions` (§7.3); reject only a
change nobody approved.

## 17.13 What moved between two results

Before saying "nothing changed", compare the versions: the case, the plant and the economics of
each result (QA-266, QA-294). The answer names what differs between them and the effect on each
headline metric (§18.2). A user who says "do not change the case, just tell me X" gets X from a
what-if that is not saved, or the reason it cannot be given (QA-268).

---

# 18. Explaining a result: why, and what moved

## 18.1 Why a cost is what it is

A levelised cost is the discounted cost of the period divided by the discounted energy
delivered (Short, Packey and Holt, 1995, ch. 4; IEA/NEA, 2020, ch. 2). Its definitions in gemini
are `knowledge/handbook-economics.md` §6 and §16.4. To explain a levelised cost, split its
numerator into its parts, as the tools give them:

| Part | From | Typical driver |
|---|---|---|
| Annualised capex | `estimate_costs` (capex by kind, annuity) | wells (drilling depth, count), heat pumps |
| Fixed opex | `estimate_costs` | share of capex per year |
| Electricity | `estimate_costs`, `compute_kpis` | pumps, heat pumps, chillers |
| Fuel | `estimate_costs`, `compute_kpis` | backup boilers, gas bought |
| Carbon | `estimate_costs` | the plant's own CO2 and methane |

The explanation names the largest two parts with their share, then what drives each.
Shares are the tool's or come from `calculate` with its id (§8.6). For geothermal heat the
wells usually dominate capex, so the cost falls with flow per doublet and full-load hours
(Frederiksen and Werner, 2013, ch. 8; Grant and Bixley, 2011).

Invented example: LCTS 52.0 EUR/MWh = annualised capex 31.0, electricity 12.5, fixed opex
6.0, fuel 2.0, carbon 0.5 (EUR/MWh, all from the tool). "Capex is 60 % of the cost, mostly the
two doublets; electricity 24 %, mostly the heat pump. More full-load hours on the wells lower
the cost most."

## 18.2 What moved between two results

Explain a change between two results by its causes, one at a time:

1. List what differs: case, plant, economics, period (§17.13). Name each difference with both
   values.
2. Give each headline metric for both results and the change, as the tools give them.
3. Attribute the change: when only one input differs, the whole change is its effect. When
   several differ, the effect of each is known only from runs that change one at a time (a
   one-at-a-time sensitivity, `knowledge/handbook-studies.md` §3.2); without them, say the
   effects are not separated.

| Metric | Result A | Result B | Change |
|---|---|---|---|
| LCTS (EUR/MWh) | 48.20 | 51.60 | +3.40 |
| Capex (MEUR) | 41.00 | 41.00 | 0 |
| Electricity bought (GWh) | 18.30 | 18.30 | 0 |

Invented example: only the electricity price differs (60 to 75 EUR/MWh). LCTS rises 3.40
EUR/MWh; capex and energies are unchanged, so the whole rise is the electricity cost.

## 18.3 Why this design and not another

A recommendation says why the chosen design beats each rival on the criterion the case ranks by
(usually LCTS among feasible designs), and what it gives up: "v1 costs 4.1 EUR/MWh less than v2
because it needs no heat pump; it emits 2.0 kt more CO2 a year from backup gas". Every rival
named was simulated and checked on the same case (§6.2); a rival not simulated is named as
screened out with its reason. When two designs are within the cost estimate's accuracy (§10.4),
say the ranking is not decided by cost alone and name the other criteria (CO2, risk,
robustness under the uncertainty study).

---

# 19. Recommendations, risks and next steps

## 19.1 Project stages

A geothermal heating project moves from screening through feasibility, exploration drilling,
field development and construction to operation; the cost and the risk of each stage differ,
and the largest risk (the resource) is resolved only by the first well (ESMAP, 2012, ch. 2).
Cost estimates follow the same stages (AACE 18R-97; §10.4). A concept-stage report recommends
what the next stage must establish, not only the design: the resource (flow, temperature,
injectivity, gas), the demand (measured profiles), the prices, the permits.

## 19.2 Writing a recommendation

Each recommendation has an action, its reason, the evidence and the condition under which it
holds (Markel and Selber, 2021). Write it as one sentence plus the evidence:

"Build two doublets with a heat pump (action), because it is the only feasible design below 50
EUR/MWh (reason; `study/<name>`, ranked table), provided the production flow of 200 m3/h per
doublet is confirmed by the first well test (condition)."

Recommendations the user did not ask for go into the finish suggestions as next steps (§17.2).

## 19.3 Risks

A risk register lists each risk with its cause, consequence, likelihood, effect on the headline
metric and the response (ISO 31000:2018). For geothermal heat the usual ones are: resource
below expectation (flow or temperature), reinjection problems (injectivity, scaling,
corrosion), induced seismicity, price risk (electricity, gas, carbon), demand below forecast,
and cost overrun (ESMAP, 2012; Grant and Bixley, 2011). Quantify a risk only from a study
(sensitivity or uncertainty); otherwise name it as open with the study that would size it.

| Risk | Cause | Effect on | Evidence | Response |
|---|---|---|---|---|
| Flow below plan | lower permeability | LCTS, heat coverage | `study/<name>` tornado | well test; heat pump margin |

---

# 20. Indicators beyond cost

## 20.1 Full-load hours and capacity factor

Full-load hours are the energy a unit delivers in a year divided by its capacity; the capacity
factor is that over the hours of the year (8760 h) (Frederiksen and Werner, 2013). A base-load
geothermal unit has many full-load hours, a peak boiler few; both say whether a unit is sized
to its role. Quote them from a tool or compute with `calculate` and its id.

Invented example: a 10 MW geothermal exchanger delivers 60 GWh in a year: `calculate`
60000 / 10 = 6000 full-load hours, capacity factor 6000 / 8760 = 0.68 (68 %).

## 20.2 Specific indicators

Indicators per unit of service let a reader compare plants of different size: capex per MW of
peak heat (MEUR/MW), CO2 per MWh delivered (kg/MWh), electricity per MWh delivered. Primary
energy and its factors follow EN ISO 52000-1:2017; state the factors and their source when a
primary-energy figure is given. Each indicator says its numerator, denominator and boundary,
as a COP does (§8.8).

---

# 21. gemini's metrics: what each one is

Names, titles and display units are gemini's (`gemini/gemini/evaluate/_utils/display.py`,
`summary.py`; `gm.evaluate.metrics()`). Write the title in prose and the unit as given. The
search objectives are `annualised_cost`, `lcts`, `lcoh`, `lcoc` and `co2` (`OBJECTIVES`); the
others are results, not targets.

## 21.1 Energies and peaks

| Name | Title | Means | Mistake to avoid |
|---|---|---|---|
| `heat_delivered` | Heat delivered | heat into the heating grid over the period | not the demand; may exceed it |
| `heat_useful` | | the part of it that met demand | |
| `heat_surplus` | | heat above demand | report it plainly (§8.3) |
| `cold_delivered`, `cold_useful`, `cold_surplus` | | the same for cold | |
| `boiler_heat` | Heat from the boilers | heat of the backup boilers | not "non-geothermal heat" (§17.10) |
| `electricity_bought`, `electricity_sold` | Electricity bought / sold | energy over the grid edge | net export is sold, not negative bought |
| `gas_bought` | Gas bought | gas from the grid | not all fuel: produced gas is separate (§8.9) |
| `peak_heat`, `peak_cold` | Peak heat / cold demand | the highest delivered power of a step | per step: a daily step hides the hourly peak (§11) |
| `annual_energy` | Energy per year | a period energy scaled to a year | state the basis once (QA-099) |

A `None` value comes with its reason (for example "the plant has no CoolingGrid"): quote the
reason, never a zero.

## 21.2 Costs and emissions

| Name | Title | Means |
|---|---|---|
| `capex` | Investment | overnight investment, MEUR |
| `opex` | Operating cost | cost per year: fixed O&M, electricity, fuel, carbon |
| `annualised_cost` | Annualised cost | capex as an annuity plus opex, per year |
| `lcoh`, `lcoc` | Cost of heat / cold | levelised, with the `heat_cost_share` that splits shared costs |
| `lcts` | Cost of thermal supply | levelised over heat and cold together; the ranking metric |
| `payback` | Payback time | simple payback, `capex / (revenue − opex)`, not discounted; needs sale prices in the case (`gemini/gemini/evaluate/costs.py`) |
| `co2` | CO2 emissions | CO2-equivalent of the period: fuel, released gas, vented methane by GWP, grid electricity (§8.5) |
| `co2_emitted` | CO2 emitted | CO2 mass the plant itself releases to the atmosphere (kg), no grid share |
| `methane_emitted` | Methane emitted | vented methane mass |

Formulas: `knowledge/handbook-economics.md` §6, §16.4, §16.5. LCOH and LCOC depend on the split
of shared costs: quote them with the split; compare plants by LCTS (§0.4).

## 21.3 Ratios and capacities

| Name | Means | Note |
|---|---|---|
| `heating_coverage`, `cooling_coverage` | share of the demand met over the period | a share 0..1: write it as a percent (§8.6) |
| `heat_pump_cop` | heat of the heating heat pumps over their own electricity | the machines' seasonal ratio (§8.8) |
| `cop` | heat delivered over all electricity bought | a plant ratio, not a machine's COP (QA-322) |

`capacities` (from `compute_kpis`) gives, per unit, `{kind, capacity, peak, share}`: the rated
capacity, the peak use over the period and `share` = peak / capacity. A `share` near 1 is a unit
at its limit; one far below 1 an oversized unit (§17.8). `peak` `None` comes with the reason the
unit carried nothing.

Invented example: `heating_coverage` 0.99962 is "99.96 % of the heat demand met"; `cop` 15.2
with `heat_pump_cop` 3.9 is "the heat pumps run at a seasonal ratio of 3.9; the plant delivers
15.2 MWh of heat per MWh of electricity bought".

---

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
- ISO 80000-1:2022. *Quantities and units — Part 1: General*, Annex B (rounding of numbers).
- NIST SP 811 (2008). Thompson, A. and Taylor, B. N. *Guide for the Use of the International
  System of Units (SI)*, Appendix B.7 (rounding).
- Directive (EU) 2018/2001 (Renewable Energy Directive), Annex VII: energy from heat pumps.
- EN 14511 (all parts). *Air conditioners, liquid chilling packages and heat pumps … — rating
  conditions and test methods*. CEN.
- Zottl, A., Nordman, R. et al. (2012). *Concept for evaluation of the SPF*. SEPEMO-Build
  project (EU Intelligent Energy Europe), system boundaries H1–H4.
- Çengel, Y. A. and Boles, M. A. (2019). *Thermodynamics: An Engineering Approach*, 9th ed.
  New York: McGraw-Hill. Ch. 6 (second law, Carnot COP).
- Grant, M. A. and Bixley, P. F. (2011). *Geothermal Reservoir Engineering*, 2nd ed.
  Burlington, MA: Academic Press.
- Willems, C. J. L., Nick, H. M., Weltje, G. J. and Bruhn, D. F. (2017). "An evaluation of
  interferences in heat production from low enthalpy geothermal doublets systems". *Energy* 135,
  500–512.
- Short, W., Packey, D. J. and Holt, T. (1995). *A Manual for the Economic Evaluation of Energy
  Efficiency and Renewable Energy Technologies*. NREL/TP-462-5173. Golden, CO: NREL.
- IEA and NEA (2020). *Projected Costs of Generating Electricity, 2020 Edition*. Paris: OECD.
- ESMAP (2012). *Geothermal Handbook: Planning and Financing Power Generation*. Technical Report
  002/12. Washington, DC: World Bank.
- ISO 31000:2018. *Risk management — Guidelines*.
- EN ISO 52000-1:2017. *Energy performance of buildings — Overarching EPB assessment — Part 1*.
- Frederiksen, S. and Werner, S. (2013). *District Heating and Cooling*. Lund:
  Studentlitteratur. ISBN 978-91-44-08530-2.
- gemini source: `gemini/gemini/evaluate/verdict.py`, `summary.py`, `coverage.py`,
  `balances.py`, `_utils/display.py`.
- geomind: prompts `geomind/geomind/prompts/project/explainer.md`, `reviewer.md`; skills
  `reading-results`, `comparing-designs`, `report`, `economics`, `calculator`, `python`.
- Team: bug files QA-090, QA-091, QA-094, QA-099, QA-124, QA-187, QA-218, QA-233, QA-234,
  QA-257, QA-270, QA-289, QA-290, QA-322, QA-323, QA-325, QA-333, QA-334, QA-337, QA-351,
  QA-092, QA-114, QA-123, QA-130, QA-132, QA-166, QA-205, QA-214, QA-226, QA-228, QA-263,
  QA-266, QA-268, QA-278, QA-294, QA-317, QA-324 of the
  team's quality assurance.
