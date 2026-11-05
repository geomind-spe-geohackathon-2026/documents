# QA-AI-case-I: the case stage through the API (2026-11-05)

Thread QA-AI-case-I of `documents/project/plans/qa-round-e2e-ai.md`. Backend layer only: the
driver script creates a project, uploads the three competition files
(`gemini/examples/hackathon_2026/`), sends one chat message, answers every card through
`POST /assistant/runs/{id}/answer`, then reads `/runs/{id}/log` and `/agents`. Every tool call and
LLM round trip of both runs was read. Model: `deepseek/deepseek-v4.1-flash-1017` for every agent.

| Run | Project | Request | Answers | Backend |
|---|---|---|---|---|
| 1 `f5f86362-4596-4264-b00a-8c26e5adc5f3` | QA-TEST QA-AI-case-I 1 (23e6faf0) | "Set up the case for our geothermal heating and cooling plant from the uploaded challenge brief and the two daily demand files." | approve every card | 1.1.102 |
| 2 `519ccc65-564e-4d1e-9139-a23777cd1107` | QA-TEST QA-AI-case-I 2 (cf19d767) | "... Where the files say nothing, use your own reasonable assumptions." | change some; typed "demand.heating.return_temperature = 55 degC; site.air.relative_humidity = 0.8"; approve all | 1.1.104 |

Both runs ended `done` with a case gemini accepts and its economics set. The backend restarted
(deploy) at 16:56:35 UTC during run 1: one `GET /runs/{id}` answered 504 after 30 s; the run went
on (Celery) and nothing was lost.

## Result

The case stage works and is fast: a complete case with economics in 4.5-6.3 min and 0.03 USD,
the IMP-025 split ran (4 geoscientists in parallel, 58 s / 60 s), and every value matches the
competition data. What remains is waste (re-reads, refused calls) and one rule break: Knowledge
values are stored before the user confirms them (QA-153).

## Timing (run 1 / run 2)

| Stage | Run 1 | Run 2 | Notes |
|---|---|---|---|
| Coordinator route | 2.7 s | 3.3 s | |
| Project lead to the case lead | 9 s | 7 s | `read_case` refused (no case), harmless |
| Case lead: `list_files`, `read_case`, 3x `read_rag` | 3 s | 3 s | each file read once |
| Case lead writes 4 briefs | 21.4 s (3.3 k out tokens) | ~20 s | briefs 2-3.6 k chars with the PDF text |
| `geoscientists` (4 in parallel) | 57.7 s | ~60 s | longest instance: requirements (Geoscientist IV) 37.8 s in one LLM call |
| Re-reading the outlined team result | 3 steps, 5.3 s, 116 k in | same | QA-156 |
| `set_case` until stored (2 refused of 3) | 49 s | ~45 s | QA-153 (source="project", time_zone) |
| Confirmation question to answer | 17 s | 25 s (incl. change some) | |
| Economics (`ask_economics`) | 25 s | 22 s | one question, approve all |
| Final checklist reads | 33 s (6 `read_case`) | 18 s | QA-157 |
| Project lead: check and `accept_case` | 36 s | 33 s | IMP-029 |
| **Whole run** | **6 min 12 s, 1.61 M in / 56 k out, 0.036 USD** | **4 min 31 s, 1.44 M in / 41 k out, 0.027 USD** | |

Per agent (run 1): case lead 26 steps, 237 s LLM, 1.29 M input; geoscientists 16 steps, 167 s
(parallel), 256 k; project lead 5 steps, 42 s; coordinator 1 step. Tool calls: case lead
`read_case` 9, `set_case` 5 (2 refused), `read_stored` 5, `search_rag` 6; geoscientists
`search_knowledge` 8, `read_knowledge` 3 (the same document), `describe_case` 8. Run 2 the same
within one or two calls.

Cards per run: 3-4 `set_case` approvals, 2-3 questions, 1 `accept_case` approval (IMP-029).

## Accuracy (stored case vs. `gemini/examples/hackathon_2026/case.json` and `economics.json`)

| Part | Result |
|---|---|
| time | 2027-01-01 to 2028-01-01, 1 d: equal |
| demand | both CSVs, right columns, MW, `time_zone` UTC (confirmed); supply 100 / 20 degC; returns 60 / 25 degC (run 2: 55 degC as the user typed); return pressures, dew point margin, indoor 26 degC / 50 %: equal |
| site | surface 12 degC, gradient 30 °C/km, depth 2500 m, thickness 100 m, pressure 250 barg, permeability 200 mD, density 1030, viscosity 0.4 mPa.s, GLR 0.8, CH4 80 mol% / CO2 20 mol%, sand 20 mg/l, air 10 degC / 101325 Pa: equal (units as the PDF writes them). No uncertainty ranges: the PDF gives none (studies set them) |
| utilities | CO2 300 g/kWh; gas composition digit for digit: equal. Question text in run 2 showed N2 with a wrong digit (QA-163) |
| requirements | run 1: 9 (flow range split in two, QA-160) plus heating/cooling supply temperature requirements (by the prompt's rule, not in the reference); run 2: 9 with one flow range |
| economics | every value of the assumptions document as written there (the document rounds the reference: 0.0607 vs 0.06073 EUR/W boiler, 1239.13 vs 1239.1304 EUR/m drilling); the catalogue adds circulation pump, electric boiler, ice and thermal storage keys the reference lacks; no per-energy map, no subsidy: as the document says |
| extra questions | run 1 asks the user for outside relative humidity and grid gas heating value, neither needed (QA-161) |

## Bugs and ideas

| Id | Severity | Area | Title |
|---|---|---|---|
| QA-153 | major | geomind | Knowledge values saved into a case version before the user confirms them (both runs) |
| QA-156 | minor | geomind | Team result outlined to 684 characters; 5 `read_stored` calls (both runs) |
| QA-157 | minor | geomind | Final checklist reads the case 6 times (both runs) |
| QA-160 | minor | geomind | Flow range 50-300 m3/h split into two requirements (run 1 of 2) |
| QA-161 | minor | data | User asked for outside humidity and gas heating value, which nothing needs |
| QA-163 | minor | geomind | Confirmation question retypes a number with a wrong digit |
| IMP-029 | idea | geomind, backend | Fewer approval cards in a case run |
| IMP-030 | idea | geomind | The lead hands the assumptions document to the geoscientists |

Not found: no wrong value in the stored case, no question repeated, no lost user answer, the
"change some" follow-up asked with `ask_user` (no options) and recorded the typed values as
`source: user` assumptions; economics asked once; the IMP-025 split always 4 groups, one call.

Evidence: `evidence/QA-153/run-f5f86362.json`, `evidence/QA-153/run-519ccc65.json` (full run logs)
and each bug's folder. Driver script: `~/qa-ai-case/drive.py` on the Dell (not in a repo).
