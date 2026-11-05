# QA-152: Analysis team cannot run sensitivity, uncertainty or a study on a project plant: every design reference is refused (19 of 56 calls fail, 0 results, 4.8 min)

| Field | Value |
|---|---|
| Status | open |
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
