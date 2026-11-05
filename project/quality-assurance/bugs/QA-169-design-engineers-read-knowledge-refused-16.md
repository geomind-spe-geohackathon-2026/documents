# QA-169: Design engineers' read_knowledge refused 16 of 50: bare 'handbook-design.md' and titles like '3 Wells' from the lead's brief; the handbook outline doubles numbers ('3 3 The subsurface'); the same refused call is repeated up to 4 times

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-design-I |
| Found | 2026-11-05 17:10 UTC |
| Versions | frontend 1.1.113, backend 1.1.102 at the run start (1.1.104 by 17:10), geomind 0.4.97, gemini 0.6.16 |
| Where | https://geomind.team/projects/f1704a61-f1b8-4b63-84d3-20bd30beaed7/assistant/chat/cd332dde-7afa-4865-8a75-d8f6d4be6354; project QA-TEST QA-E2E-design-I 1; run 76d19df6-485f-46ee-a182-6b03ed70ab33; design_lead fill_parts 16:53-17:05 UTC |
| Fixer | hotfix-python-VIII |

## Steps

1. New project, reference `case.json` + `economics.json` + `data/demand.csv` of `gemini/examples/hackathon_2026/` loaded by the API (case v3, nothing missing).
2. Chat: "Please design a geothermal heating and cooling plant for it: choose the plant layout, size the doublets (1 to 3) ...".
3. Approve build_plant (HeatingHeatPumpCoolingPlant, 2 doublets). The design lead calls `fill_parts` with four briefs (reservoir, energy systems, ...).

## Expected

Each engineer reads the handbook sections it needs once, with a name and a section the tool accepts.

## Actual

`read_knowledge` 50 calls by the engineers, **16 refused** (reservoir_engineer 13 of 28, energy_systems_engineer 3 of 22):

| Refused input | Times | Error |
|---|---|---|
| `{"name": "handbook-design.md", "section": "3 Wells"}` | 3 | name must start with `knowledge/` |
| `{"name": "handbook-design.md", "section": "4 "}` | 3 | same |
| `{"name": "handbook-design.md", "section": "5"}` | 3 | same |
| `{"name": "knowledge/handbook-design.md", "section": "3 Wells"}` | 2 | `unknown_name`: no heading '3 Wells' |
| `{"name": "knowledge/handbook-design.md", "section": "5.5 Gas use and disposal"}` | 2 | same |
| `handbook-design.md` sections `6`, `8.3`; name `finding-53de5f90` | 1 each | name must start with `knowledge/` |

- The lead's brief itself names wrong section titles: "Read handbook chapters 3 and 4 (knowledge/handbook-design.md sections '3 Wells' and '4 ...')". Chapter 3 is "The subsurface", "Wells" is chapter 4.
- The error's outline lists every heading with its number twice, and two headings numbered 1: `1 Designing Geothermal Heating and Cooling Plants, 1.1 Preface, ... 0 0 Design path in gemini, 0.1 0.1 How the lead uses it, ..., 3 3 The subsurface, 4 4 Wells and pumps`. A title copied from it ("3 3 The subsurface") is a third way to get it wrong.
- Every new engineer instance repeats the same three refused calls (16:55:03, then again in later rounds): the refusal teaches nothing across instances.
- The handbook read during the run was the old upload (outline 0.1 "How the lead uses it", 0.1-0.5 only); handbook-design v2 (f1a84a92) was uploaded at 17:01:45 UTC, mid-run.

Speed: reservoir_engineer spent 698 s of LLM time, energy_systems_engineer 390 s in this fill (log `llm_calls[].duration`); about 13 of those rounds were spent on refused reads.

## Evidence

- `../evidence/QA-169/refused-read-knowledge.json`: every refused call (agent, ts, call id, input, error) and the lead's brief to the reservoir engineer.
- Run log at 17:10 UTC: `../evidence/QA-169/run-76d19df6-log-1710.json.gz`.

## Second run (QA-AI-design-I, 2026-11-05 16:50-17:04 UTC)

Run 0df89b7e-69e0-46b3-abe1-231e51d9570a, project QA-TEST QA-AI-design-I 1 (API only, backend 1.1.102-1.1.104, geomind 0.4.98): same pattern, 13 of 50 `read_knowledge` refused, all from the design engineers:

- 10x bare `handbook-design.md` (sections "5", "4", "3 Wells", outline): "expected a Knowledge document 'knowledge/<name>'; a project file is the lead's to read" (the second half is wrong: it is a Knowledge file, not a project file).
- 1x section "3 Wells" with the right name: no such heading (the lead's brief named it).
- 3x a skill or a finding through read_knowledge: `evaluating-a-module`, `knowledge/evaluating-a-module`, `finding-54590b50`. The lead's briefs say "Read ... skill evaluating-a-module", but `proposer_tools` (`geomind/agents/design/proposal.py:56`) gives the engineers no `read_skill` and no `read_stored`; each instance also spent a `search_knowledge("evaluating a module skill")` on it (6 calls over two passes).

Extra proposed fix: give the engineers `read_skill` (or have the brief say "no skills: your prompt holds the rules"), and make the lead prompt (`prompts/design/lead.md` step 3) say section numbers only ("section 4"), never invented titles.

## Cause

- `geomind/geomind/tools/knowledge_only.py:30` `read_knowledge` refuses a name without the `knowledge/` prefix although only Knowledge documents are possible for that tool (fact).
- `geomind/geomind/tools/files.py:350` `section_text` lists `f"{item['number']} {item['title']}"` while `sections.headings` keeps the number inside the title, so each number is printed twice (fact from the message; the cause in `sections.headings` is a guess). The Preface heading "1 Designing ..." also collides with chapter 1.
- The design lead's brief writes section titles from memory instead of the outline (prompt `geomind/geomind/agents/design/lead`; handbook chapter 0.3 module groups).

## Proposed fix

1. `read_knowledge` (knowledge_only.py): accept `handbook-design.md` and add the `knowledge/` prefix itself; accept `section` as a number prefix ("3 Wells" -> "3", "4 " -> "4") or match a title without its number.
2. `sections.headings`: strip the leading number from the title so the outline reads `3 The subsurface`; give the Preface heading no number.
3. Design lead prompt / handbook ch 0.3: in each brief name sections by number only ("sections 3 and 4"), taken from the outline, never by a typed title.
4. Engineers: a refused identical call must not be repeated (the repeat guard of read_case, QA-157, also for read_knowledge).

## Fix

- 2026-11-05 17:27 UTC: geomind 0.4.104, commit 356e1dc, deployed: bare Knowledge name, '3 Wells'-style section keys, outline numbers once; lead prompt part (sections by number) still open with QA-178
## Retest

Retest (QA-E2E-design-I, 2026-11-05 19:14 UTC, backend 1.1.117): run 06fd16f0 (project QA-TEST QA-E2E-design-I 3): 48 read_knowledge calls by 7 agents, 1 refused (`{"name": "finding-9878dd62"}` by the energy systems engineer: a finding id sent to read_knowledge, not a Knowledge document). No bare 'handbook-design.md', no '3 Wells' titles, no repeats. Works.
- 2026-11-05 19:13 UTC: QA-E2E-design-I: 1 of 48 refused (a finding id), run 06fd16f0
