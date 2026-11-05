# QA-152: Analysis team cannot run sensitivity, uncertainty or a study on a project plant: every design reference is refused (19 of 56 calls fail, 0 results, 4.8 min)

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 16:58 UTC |
| Versions | backend 1.1.102/1.1.103 (geomind 0.4.98, gemini 0.6.16/0.6.17), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 1` (4ce816b1-4bd1-48a5-8e77-9414c2b86301); chat fa9cfafb-e39e-4ccd-9dfb-d8427f518c43; run c2b815a8-8c54-4bae-b1c1-769351434fe6 |
| Fixer | |

## Steps

1. Project with the reference case (`gemini/examples/hackathon_2026/case.json` + `economics.json`) and
   one plant version (`plants/HackathonPlant.json`), set through the API (no agent built it).
2. Chat message 1: cost the stored plant (worked: run 389be3c3, 75 s, numbers equal to the page study).
3. Chat message 2: "how sensitive is LCTS of this design to the electricity price (80 to 140 EUR/MWh),
   the discount rate (2 % to 8 %) and the carbon price (30 to 110 EUR/t)? Rank them, and give the LCTS
   spread over the case's uncertainty (p5, p50, p95)."

## Expected

The economist runs `sensitivity(values=[economics.energy.electricity, economics.discount_rate,
economics.carbon.price], metrics=[lcts])` and `sample_uncertainty(metrics=[lcts])` on the project
plant and returns a ranking and p5/p50/p95. The same studies started from the page API (kind
`sensitivity` and `sample` on plant_version 1, no LLM) run fine: studies 957c9714, 5d7bbf26.

## Actual

No number. Run done after 4 min 48 s, 56 tool calls, 19 errors, 828 k input tokens, 0.0153 USD; two
economist sessions (29 steps together) send the same refused calls:

| Tool | Refused | Inputs tried |
|---|---|---|
| `sensitivity` | 5 | design/HackathonPlant (2x), design/project, design/hackathon_plant, design/reference-economics-HackathonPlant |
| `sample_uncertainty` | 3 | design/HackathonPlant (2x), design/HackathonPlant_v1 |
| `run_study` | 1 | designs [design/HackathonPlant] |
| `read_study` | 4 | study/817f5a54-... (2x), study/reference-economics-HackathonPlant, study/reference_economics_HackathonPlant |
| `read_plant`, `read_stored` | 4 | design/HackathonPlant, result/<project result id> |

Every refusal is `unknown_name ... stored design references: none stored yet in this chat for
design`. The analysis lead then asks `support_lead` to "store the project plant as a design
reference"; support answers "Not routed: no member can do this request". Final answer: "I cannot give
the sensitivity ranking or the p5/p50/p95 LCTS spread".

The same happens to any project whose plant came from the Plant page or from an earlier chat: the
analysis team can simulate it (`simulate` with no design runs the project plant) but cannot run any
study on it. `list_studies` lists the project's own studies (`project_study` with id), but
`read_study` takes only `study/<name>` of the chat, so a page study cannot be read either.

## Evidence

- Run log: `../evidence/QA-152/run-c2b815a8-log.json`; one line per call: `../evidence/QA-152/run-c2b815a8-trace.txt`
- Economist step 2 (16:53:50) first refusal; steps 6-18 and the second economist session 3-8 repeat it.
- Analysis lead step 11 (16:57:38): `support_lead` "Not routed".

## Cause

- `geomind/geomind/tools/gemini/study.py` `prepared()` loads every design with
  `stored.load_design(context, design, ...)` (`tools/gemini/stored.py:90`), which reads only a chat
  artifact `design/<name>`. A project plant / plant version is never a chat artifact; only
  `build_plant`, `patch_plant`, `merge_designs`, `union_designs`, `set_ranges`, `size_plant`,
  `optimize` save one, and none of them is a tool of the analysis lead or the economist
  (`agents/analysis/lead.py`, `economist.py`).
- `simulate` and `read_plant` already accept the project plant (`plants.load_plant(...,
  project_plant)`, `version_plant(...)`), so only the study tools lack it.
- `read_study` does not accept a `project_study` id that `list_studies` returns.
- Prompts: the economist's prompt names `design.reference` in the problem state; nothing tells it
  what to do when the state has none (the plant came from the page), so it guesses names.

## Proposed fix

1. geomind `tools/gemini/study.py` (`sensitivity`, `sample_uncertainty`, `run_study`, `compare` where
   designs are read, `optimize`) and `stored.load_design`: accept the same plant sources as
   `simulate`/`read_plant` (`project_plant` or `plant_version`, or a `design` value of the form
   `plant_version/<n>`), building the plant with `plants.version_plant`/`workspace_plant`.
   Alternative: one tool `adopt_plant(plant_version, name)` for the analysis lead and the economist
   that stores the plant version as `design/<name>`, and the `simulate` answer giving that
   reference.
2. `read_study`: accept the `project_study` id `list_studies` returns (or `list_studies` returns a
   `study/<key>` the tool takes).
3. The refusal message of a study tool on a chat with no stored design should name the way out
   (`plant_version=` or the adopt tool), so the agent does not guess 10 names.
4. Analysis lead prompt: when the economist answers "no design reference", do not re-delegate the
   same task (the second economist session repeated all refused calls).

## Second report (QA-E2E-study-I, chat in the browser, 2026-11-05 16:52-16:59 UTC)

Same bug, reached from the web chat. Backend 1.1.102 -> 1.1.104 (a deploy happened during the run;
the run survived). Project `QA-TEST QA-E2E-study-I 1` (8fcbf709-537a-40d9-ac1f-abadd1061775), chat
c0cae905-a2a8-44cf-8bec-f4899f313e8b, run d6f8e79a-0056-4099-9398-81104925a418. Seeded by API with
the reference case and the plants HackathonPlant (v1) and HeatingAbsorptionCoolingPlant (v2).

- Message 1 "simulate the current plant for 2027" worked (run 61721f4c, 40 s, 15 steps).
- Message 2: "How sensitive is the cost of thermal supply of this plant to the gas price, the
  electricity price and the carbon price? Use the uncertainty ranges in the economics file and show
  me which one matters most."
- Result: no number, 7 min 29 s, 50 steps, 83 tool calls, 978 k input tokens, 0.024 USD.
  `sensitivity` refused 6 times with `unknown_name` for design/HeatingAbsorptionCoolingPlant (3x),
  design/11c2e401cd91606b (the simulate result hash), design/current, design/project_plant.
  `read_stored` 23 calls, `read_skill` 11 calls (the `economics` skill re-read 6 times by the
  economist), `read_case` 10 calls. `support_lead` again "cannot route".
- The final answer correctly refuses to rank, and tells the user the design lead must `build_plant`
  the same plant first: the user cannot act on that from the chat.
- Also seen in the same answer: the energy basis is heat 111744.16 MWh/yr, cold 23758.79 MWh/yr
  (a 365.25-day year) while the simulation delivered 111667.68 / 23742.53 MWh (QA-099 still shows).

Evidence: `../evidence/QA-152/run-d6f8e79a-log-e2e.json`.

Extra proposed fix from the E2E side: the `economics` skill (geomind/agents/analysis/... skills)
tells the economist to call `sensitivity(design, ...)` "on the verified design"; until the tools
take the project plant (no design = the project plant, as `simulate` does), the skill should say
so, and the lead should not re-delegate the same refused call.

## Fix

- 2026-11-05 17:02 UTC: geomind 0.4.99 (163c82b, tag v0.4.99), pushed 2026-11-05; NOT deployed yet (deploy freeze during the live run): the backend hotfix-mode deploy picks it up. QA-152: design/<project plant name> or design/v<N> in every design tool; QA-158: case lead prompt asks time_zone as an assumption.
- 2026-11-05 17:07 UTC: Deployed: geomind 0.4.100 in backend 1.1.104 hotfix image, 2026-11-05.

- 2026-11-05 17:22 UTC, QA-AI-analysis-I, backend 1.1.105: fresh project `QA-TEST QA-AI-analysis-I 3`
  (cdb636b7-f6ae-4395-b8c0-ad19bc5cacd4), plant version 1 from the API, run 7a70bf41-cdbf-4448-a405-46869b534cd0.
  The lead used `design/HackathonPlant`; the economist ran `sensitivity` (0.9 s) and `sample_uncertainty`
  (24.8 s) at the first try. Rows equal the page study (electricity 11.84, discount rate 10.85, carbon
  3.40 EUR/MWh) and p5/p50/p95 37.97/46.10/54.31 EUR/MWh equal the page `sample` study with seed 42.
  Whole run 1 min 56 s, 0.0066 USD, 0 refused study calls. Verified. Log:
  `../evidence/QA-152/run-7a70bf41-retest-log.json`.

## Retest

- 2026-11-05 17:22 UTC: retest QA-AI-analysis-I 17:22 UTC backend 1.1.105: sensitivity and sample on project plant at first try, numbers equal page studies
