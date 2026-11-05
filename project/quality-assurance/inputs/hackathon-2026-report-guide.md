# Report guide: GEMINI hackathon 2026

Guidance for the GEMINI hackathon 2026 case only; a starting point, the agents may depart from it
with a recorded reason.

For the project lead, the explainer and the reviewer, and for whoever writes the report. Cite as
`knowledge/hackathon-2026-report-guide.md`. Your prompts still hold: every number comes from the
problem state or a gemini tool, digit for digit, with its unit and reference.

## What the jury scores (organisers' kick-off slides)

- **Challenge 1, 50 %: the agentic workflow.** It analyses the problem, works with the GEMINI
  digital twin, selects and runs the right models, finds missing modelling capabilities and fills
  them with extra calculations or tools, compares alternatives, and explains the reasoning behind
  the final configuration.
- **Challenge 2, 50 %: the heating and cooling system.** Deep geothermal heat for direct heating
  and, where possible, for cooling. Selected and sized technologies (heat exchangers, heat pumps,
  absorption/adsorption cooling, chillers, storage, auxiliaries); the realised heating and cooling
  capacities; the designed system; and the interaction with the agent (prompts, answers, tokens).
- **Bonus:** multi-agent collaboration, automated optimisation, uncertainty analysis,
  techno-economic assessment, automatic model generation, autonomous verification.
- "Missing models are part of the challenge": a simplified model or an external tool is welcome
  when its use is explained (`calculate`, `run_python`, `web_search` with their sources).

Deliverables: a technical report of at most 5 pages or at most 10 slides, a video of at most
5 minutes, and the agent's interactions recorded (prompts, answers, token use).

## The answer the explainer writes

The explainer's headings: `Design`, `Schematic`, `Capacities`, `Delivered`, `Costs`, `Checks`,
`Open points`, `Decisions`. For this case each must hold:

- **Design / Schematic:** the family, the doublets (number, depth, flow), each unit with its
  capacity, how the 100 °C supply is reached (from 87 °C at 2500 m: heat pump, boiler or depth),
  how the 20 °C cold is made, and where the associated gas goes (flare, boiler, CHP).
- **Capacities:** from `compute_kpis`'s `capacities`: heating and cooling capacity of each unit
  and of the plant, against the peaks of the case (30.0 MW heat, 10.0 MW cold; heating CSV,
  cooling CSV).
- **Delivered:** heat and cold delivered over 2027 beside the demand (111.67 GWh heat, 23.74 GWh
  cold, PDF p. 1), the share of heat from geothermal, heat pump and boiler as gemini gives each,
  and the days not covered.
- **Costs:** LCOH, LCOC, LCTS, capex, opex, NPV and CO2, with the economics source
  (`knowledge/hackathon-2026-assumptions.md`) and the CH4 GWP 29.8.
- **Checks:** gemini's verdict (`check_results`, the reviewer's `gemini verdict`) for each of the
  8 requirements by `name`; the doublets' flow 50 to 300 m3/h, brine cooling at most 40 K and at
  most 330 days running, heat and cold delivered over 365 days.
- **Open points:** what gemini cannot judge or the case does not constrain, and every assumption
  not confirmed by the user.
- **Decisions:** every major engineering decision with its reason and its source (a file, the
  Knowledge, a `study/<name>`, a `result/<id>`): the family over the others (the `run_study`
  ranking table), the depth and number of doublets, the return temperatures (team design choice,
  QA-094), the backup policy, the cooling technology, the gas handling, what the optimisation
  changed from the sized start, and the uncertainty and sensitivity when they ran.

## The report (5 pages)

1. Problem and inputs: the three competition files, the case, the assumptions (one table, with
   sources).
2. Agent architecture: the teams (project lead; case lead and geoscientist; design lead with the
   process, integration, reservoir, well and energy systems engineers; reviewer; analysis lead and
   economist; explainer), the tools, gemini as the physics, the model (DeepSeek on OpenRouter),
   the Knowledge base.
3. Geothermal assessment and design: the alternatives compared (at least two, from
   `design.alternatives` and `design.study`), the final plant and its schematic.
4. Results: capacities, energies delivered, checks, costs, CO2, uncertainty and sensitivity.
5. Agent interaction: prompts, answers, questions to the user, tokens and cost per agent; what the
   agents found missing in gemini and how they filled it.

geomind.team's Report page builds most of this from a result: sections Summary, Plant,
Capacities, Days covered, Constraint checks, Costs, Capital cost by kind, Uncertainty and
sensitivity, Agent log and tokens, Appendix. Choose the run under "Agent log from" so the export
holds every LLM call, the prompts and the tokens by agent, session and step.

## For the reviewer and the project lead

- A design is final only with `"passed": true` in gemini's verdict. A zero-cooling day is no
  failure under `cold_delivered` (QA-091).
- When a rule keeps failing after a real change of approach, finish with the best design, the
  passing and failing rules by name and their owners (QA-090), never with nothing stored.
- Never call the design compliant on a point gemini did not judge.
