# QA round: 5 E2E threads + 4 AI threads (Sahand, 2026-11-05 16:47 UTC)

Sahand lifted the "no QA tests" rule for these nine threads only (live runs on geomind.team, LLM
use, browser). All run on the NTNU Dell, in hotfix mode, and change NO code: they only test and
report. Input is always the competition data: `gemini/examples/hackathon_2026/`
(challenge PDF, `GEMINI_Heating_Demand_Daily_2027.csv`, `GEMINI_Cooling_Demand_Daily_2027.csv`,
reference `case.json`, `economics.json`, `study*.json`, `plants/`) and
`documents/project/quality-assurance/inputs/hackathon-2026-assumptions.md`.

## How every thread reports

- Bugs go through `documents/project/quality-assurance/qa.py` (README there), the files the hotfix
  sessions already read: `python3 $QA new ... --reporter <thread name> --area <geomind|backend|frontend|knowledge>`,
  fill `bugs/QA-<nnn>-*.md`, evidence in `evidence/QA-<nnn>/`, then `qa.py save`.
- A bug is not only code: wrong or missing Knowledge data (RAG files, `data-economics.*`,
  handbooks), a prompt or skill that misleads, an agent that splits tasks badly, a wrong tool
  choice, a slow step, a wrong number. Each bug file states: problem, evidence (run id, step, tool
  call, input and output), where it comes from (repo, file, agent, prompt, Knowledge file),
  proposed fix and where to make it.
- Every bug records speed (wall time per stage and per tool call, tokens, cost) and accuracy (the
  value the agents produced vs. the competition data, the challenge hard limits and the reference
  JSON in `gemini/examples/hackathon_2026/`).
- Ideas that are not defects: `IMPROVEMENTS.md` (IMP-<nnn>).
- At the end of a round: one report `quality-assurance/reports/<thread name>-<date>.md` with a
  timing table and an accuracy table, and update the thread's row in `SCENARIOS.md`.
- Every project a thread creates on geomind.team is named `QA-TEST <thread name> <n>` and is kept
  (no delete). A thread never touches another thread's project.
- Stage files by path, commit and push `documents` after each bug (qa.py does it).

## E2E threads (agent-browser by Vercel, against https://geomind.team, chat-first)

Each starts its OWN project. A thread whose section needs earlier stages sets them up FAST and
outside its scope (load the reference `case.json` / `economics.json` / a plant from `plants/` by
hand on the Case, Plant pages or the API), so it never waits for another thread and never tests
another thread's section. It reports bugs only in its own section.

| Thread | Section (its scope only) | Scenarios |
|---|---|---|
| QA-E2E-case-I | Chat to a complete case: upload the challenge PDF and the two CSVs, one request; the case lead and geoscientists; every question card (approve all, change some, typed answer, own assumptions, refuse); values from files vs. Knowledge vs. connectors (weather, site); the Case page shows what the agents set. | S1 (case part), S3, S6 (case values) |
| QA-E2E-economics-I | From a loaded reference case: chat to economics: the economics question, prices and sources from Knowledge (`data-economics`), carbon price, discount rate, the Economics shown in the app. | S3 (economics part), S6 (prices) |
| QA-E2E-design-I | From a loaded reference case and economics: chat to a plant design: design team, sizing, the Plant page canvas, plant versions, hard limits (1-3 doublets, 50-300 m3/h, <=40 K, 100 C / 20 C supply). | S4 (design part) |
| QA-E2E-study-I | From a loaded reference plant: chat to studies: simulate, sensitivity, optimisation, comparison; the Results page, charts, adopting a result, Runs and logs (steps, cancel, resume, JSON). | S4 (study and results), S7 |
| QA-E2E-report-I | From a loaded reference plant and a finished simulation: chat to the report: Report page, numbers vs. results, export PDF, next-step chips, explainer answers to questions about the design. | S5 |

## AI threads (backend layer only, no frontend: api.geomind.team REST + stream, run logs)

They drive the agents through the backend API (create project, upload files, chat, answer
approvals, read `/events` and the run JSON) with scripts, or the geomind evals harness
(`geomind/evals/`) when it is cheaper. They read EVERY tool call and EVERY agent round trip
(prompt, arguments, result, the next decision, delegation briefs and returns) and judge it: was the
right agent asked, was the split right, was the tool right, were arguments right, was a result
re-read for nothing, was Knowledge enough, how long did each take.

| Thread | Agents in scope (geomind/geomind/agents) | Focus |
|---|---|---|
| QA-AI-case-I | `case/` lead and geoscientists; Knowledge used by the case | Task split (2-4 geoscientists, IMP-025), briefs, file reading of the PDF and CSVs, values vs. competition data, missing Knowledge, questions asked to the user, time per round trip. |
| QA-AI-design-I | `design/` lead, energy, integration, process, proposal, reference, reservoir, well | Proposals, one patch_plant by the lead (QA-145), simulate calls, re-reads, hard limits, sizing accuracy vs. reference plants, time per sub-agent. |
| QA-AI-analysis-I | `analysis/` lead, economist, reference; study tools | Economics values and sources, LCOH/NPV accuracy vs. `economics.json`, study set-up (sensitivity, optimisation), number of simulations, time per study. |
| QA-AI-project-I | `project/` coordinator, lead, drivers, review, reviewer, comparison, explainer; `support/` curator, summarizer | Routing to the right team, delegation and hand-back, review quality, report/summary content vs. results, next-step suggestions, overhead time between stages. |

Each AI thread runs its own projects (`QA-TEST <thread> <n>`); the stage before its scope is
loaded from the reference JSON, never produced by another thread.

## Never stop (Sahand, 2026-11-05 18:28 Trondheim)

QA threads (QA-E2E-*, QA-AI-*) never stop or wait after finding a bug: file it with qa.py and go
on at once. When a stage is blocked by a bug, load that stage from the reference JSON (or work
around it) and keep testing what comes after. When a round is done, start the next one: another
scenario of your section, other inputs (vague request, no files, change some, deny), retests of
fixed bugs as they deploy, accuracy and speed comparisons. Never end with "done, waiting".
