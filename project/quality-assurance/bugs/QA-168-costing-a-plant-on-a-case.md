# QA-168: Costing a plant on a case without economics: the analysis lead fills the economics by hand from the catalogue, asks approval for one set of prices and writes another (9 values changed, HX capex unit EUR/W), then the plant cannot be simulated

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 17:08 UTC |
| Versions | backend 1.1.103/1.1.104 (geomind 0.4.98), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 2` (3901ff00-1047-4f82-8329-2ee02e450025); chat 7b90c59c-d002-47ec-b437-40b4bc66e18b; run a5ea3998-2945-403f-ab17-aa6991157aab |
| Fixer | |

## Steps

1. Project with the competition files, the reference `case.json` WITHOUT its `economics` key, and plant
   version 1 = `plants/HackathonPlant.json` (all through the API).
2. Chat: "What does the stored plant cost on this case? Give capex, LCOH, LCOC, LCTS and NPV, and tell me
   where each price comes from."
3. Answer the question card with "approve all"; approve the `set_case` card.

## Expected

The economics are proposed once from the catalogue the way the case lead does it (`ask_economics`:
recommended rows, `value_2015`, citations), the user approves exactly those values, the case gets
exactly those values, the plant is simulated and costed. With the catalogue's rows the result should
be near the reference (`economics.json`: LCTS 45.10 EUR/MWh for this plant, page study 817f5a54 in
project 1).

## Actual

The coordinator routes to `analysis_lead` (tool loop). It has no `ask_economics`, so it reads
`knowledge/data-economics.csv` by hand with `read_rag` (8 reads, 3 cut to an outline because the
table is >20 000 chars, 1 refused for a wrong row filter; steps 7-20, 1 min 50 s), choosing columns
without `value_2015`. It asks with `ask_user` (step 21) and says "all in 2015 EUR, real", but lists raw
values of other years and currencies. After "approve all" it writes, after 2 refused `set_case`
calls, values it never showed:

| Key | Asked and approved | Written into the case (step 26) | Reference economics.json |
|---|---|---|---|
| energy.electricity | 0.145 EUR/kWh (Eurostat 2024) | 115 EUR/MWh | 105.75 EUR/MWh |
| revenue.heat | 98 EUR/MWh (2019) | 114.6 EUR/MWh | 60 |
| carbon.price | 74 EUR/t (2025) | 57.48 EUR/t | 57.03 |
| analysis_period | 15 yr | 25 yr | 25 |
| capex.heat_exchanger | 0.5 EUR/(W/K) | 0.1089 EUR/W (another quantity) | 0.5 EUR/(W/K) |
| capex.injection_pump | 0.5 EUR/W | 0.09903 EUR/W | 0.5 |
| capex.cooler | 0.1 EUR/W | 0.04909 EUR/W | 0.1 |
| capex.absorption_chiller | 0.3 EUR/W | 0.2339 EUR/W | 0.3 |
| capex.gas_makeup | 820 EUR/kWe | 636 893 EUR | 50 000 EUR |
| capex.flare | 66 344 USD | 57 700 EUR | 100 000 EUR |
| opex.fixed.production_pump | 20 %/yr | 20 %/yr | 2 %/yr |
| accounting.gwp.CH4 | (not asked) | 27.9 | 29.8 (fossil methane, AR6) |

The `set_case` approval card shows only "Change the case: economics.accounting..., and 33 more"
(`approval-cards.log`), so a user cannot see that the values differ from the ones just approved.

Then `simulate` fails: `params.hx.nominal_duty is missing; expected the design value the cost is given
per` (the HX capex now per W, the plant has no nominal duty), and the run ends with no cost at all
(30 lead steps, 6 min, 1.19 M input tokens, 0.0182 USD). The project's case now holds these
economics. Also: `simulate(changes={"plant": {"project_plant": ...}})` was tried (refused).

## Evidence

- `../evidence/QA-168/run-a5ea3998-log.json`, `run-a5ea3998-trace.txt` (steps 7-30), `approval-cards.log`.
- Question text: run request-227 (step 21); written values: step 26 `set_case` input.

## Cause

- `geomind/geomind/agents/analysis/lead.py` has `set_case` but not `ask_economics`
  (`tools/gemini/economics.py`, only the case lead has it: `agents/case/lead.py:146`). The analysis
  lead prompt says "If a value you need is missing ... ask the user with ask_user", so it builds the
  economics itself.
- Nothing ties the values written by `set_case` to the values the user approved in `ask_user`; the
  lead recomputed them between the question and the write (converting units and years itself, which
  its own prompt forbids: "never compute one yourself").
- The `set_case` approval card (QA-121, one sentence) lists only paths, not values.

## Proposed fix

1. Route "the case has no economics" to the case lead (`ask_economics`), or give the analysis lead
   `ask_economics` and a rule: "economics missing -> `ask_economics`, never `ask_user` + `read_rag` of
   the catalogue". `ask_economics` already reads `value_2015` and the citations.
2. `set_case` of economics after a question: write the values `ask_economics` returned (by row id),
   not values typed by the agent; refuse a value that is not a catalogue row's `value_2015` or the
   user's typed answer.
3. The `set_case` approval card for economics: show each changed value with its unit.
4. Data: the catalogue's recommended row for `capex.heat_exchanger` should keep the gemini unit
   EUR/(W/K) (the lead picked `heat-exchanger-dea-2025-station`, EUR/W); check `in_case` rows of
   `knowledge/data-economics.csv` against gemini's units.
