# QA-165: Report from a Study-page result: list_studies shows the result id, but read_result, check_results, compute_kpis and read_stored refuse it (40+ refused calls)

| Field | Value |
|---|---|
| Status | open |
| Severity | blocker |
| Area | geomind |
| Reporter | QA-E2E-report-I |
| Found | 2026-11-05 17:10 UTC |
| Versions | backend 1.1.102-1.1.104 during the run (geomind 0.4.97/0.4.98, gemini 0.6.16/0.6.17), frontend bundle index-TsXgd_n9.js |
| Where | https://geomind.team/projects/0e44cb05-6096-434e-95ee-56b434898015/assistant/chat; project QA-TEST QA-E2E-report-I 1; chat b31664b0-44c2-4d20-9ee7-987f592b5aff; run 3f8270d5-b11e-4c86-b3ca-b0b4d4feb61c; design_lead steps 7-9, reviewer steps 1-23 (16:58-17:03 UTC) |
| Fixer | |

## Steps

1. Project with the reference case (case.json + economics.json), plant v1 HackathonPlant and v2
   HeatingAbsorptionCoolingPlant, and a done whole-year `run` study of v1 on the Study API
   (study a59c86cb-a555-401b-944e-c394b45c560f, result a528d8da-1fad-4175-8aab-3bc3209871f1,
   15/15 checks passed). This is what a user gets from the Study page.
2. Chat: "Write the design report for the simulated HackathonPlant (plant version 1). Put the key
   numbers (heat and cold delivered, LCOH, LCOC, CAPEX, OPEX, CO2) and check them against the
   challenge limits."
3. Deny the Build plant card with "Do not rebuild or re-simulate ... use that result".

## Expected

The agents read the project study's result (KPIs, checks, series) by the id that `list_studies`
gives and write the report from it. No new simulation is needed.

## Actual

`list_studies` returns `project_study` with `result.id = a528d8da-...` and its KPIs (QA-122 fix
works for listing). Every tool that reads a result refuses that id in every form the agents try:
`result/a528d8da-1fad-...`, `result-a528d8da-...`, `result/a528d8da1fad4175...`, the study id,
`study/simulation_HackathonPlant`, `study/simulation HackathonPlant`. 40 of 40 such calls refused
(`unknown_name ... stored result references: none stored`). The reviewer spends 23 steps and
~5 min (16:58:35-17:03:42 UTC) on it, also calls `search_rag` with the uuid, and writes
"gemini's check could not be run" into the verification. The design lead then simulates again
in the chat (and that simulation is of the wrong plant, QA-166).

Speed: ~5 min and ~25 LLM calls lost to the refused reads; the whole report run passed 135 steps
and 17 min before the analysis lead started.

## Evidence

- All 40 refused calls with input and output: `../evidence/QA-165/refused-calls.json`
- Run steps (every tool call, input, output, duration): `../evidence/QA-165/run-3f8270d5-steps.txt`

## Cause

Fact (code read, geomind 0.4.98): `list_studies` (`geomind/tools/gemini/studies.py`) adds the
project's studies from `project_designs(context)["studies"]`, but `read_result`
(`tools/gemini/results.py`), `check_results` / `compute_kpis` (`tools/gemini/assessment.py`),
`read_stored` and `read_study` resolve only references stored in THIS chat (`result/<16 hex>`,
`study/<name>`). Nothing maps a project study or its result id to a readable reference. The
QA-122 fix made the studies visible but not readable.

## Fix

Proposal (geomind, hotfix-python): give a project result a reference the readers accept, e.g.
`list_studies` returns `"reference": "project_result/<uuid>"` per project study, and
`read_result` / `check_results` / `compute_kpis` / `read_study` load it from the backend
(a new workspace read, e.g. `Workspace.project_result(project, id)` returning the stored result
the Results page shows: kpis, checks, capacities, coverage, series). Backend part (hotfix-back):
serve that method from the results table. Also: an `unknown_name` error for a uuid that
`list_studies` listed should say how to read it, not "none stored".

## Retest

(Who, when, result.)
