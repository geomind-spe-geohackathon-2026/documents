# QA-122: Agent sees one plant and no studies in QA3 report although the project shows 2 plants and 4 studies, so the explainer can compare no alternatives

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | functional-qa-report-I |
| Found | 2026-11-05 11:17 UTC |
| Versions | backend 1.1.84 (geomind 0.4.80), frontend not read |
| Where | https://geomind.team/projects/91b202b6-6236-45e7-8860-a58437d6eb98/assistant/chat; project QA3 report; run result/11c2e401cd91606b |
| Fixer | hotfix-python |

## Steps

1. In the chat ask: "Why did you choose this configuration, and which alternatives did you compare it with? Give the figures of each alternative from this project and explain how the geothermal heat drives the cooling."
2. Read the answer.

## Expected

The seeded stages are visible to the agents: the project Overview lists Plant version 2, Study "4 done" and the activity log shows studies economics/simulation on HackathonPlant and HeatingAbsorptionCoolingPlant. The explainer compares them with figures.

## Actual

Answer: "list_plants shows exactly one plant ... list_studies returned [] — no study exists ... no alternatives were compared". It took 117 steps (44 retried) and gave no comparison. The seeded plant HackathonPlant and the 4 studies are invisible to the agent (guess: the seed wrote project study rows that list_studies does not read, or the agent lists only plants of the chat). Stage gap, reported as the README asks.

## Evidence

- Chat text: `../evidence/QA-122/chat.txt` (the answer is after the question quoted in Steps)

## Cause

hotfix-back-II, 2026-11-05 11:25 UTC (code read, no prod read). Two separate causes, by design
of the backend-geomind contract, not a seed fault:
1. Plants: the backend's `DatabaseWorkspace.plants` (`backend/src/api/v1/assistant/runs/adapters/workspace.py`,
   `read_plants`) gives geomind only the project's LATEST plant version, under its name. QA3 report
   has v1 HackathonPlant and v2 HeatingAbsorptionCoolingPlant, so the agent sees one plant. Giving
   every version is not a safe backend-only change: geomind's `workspace_plant` refuses a call
   with no name when the project has several plants, and since QA-092 every patched design saves
   a version under its own name, so the default "the project's plant" would break.
2. Studies: geomind's `list_studies` lists the studies stored in THIS CHAT (`study_index`); the
   workspace contract has no method for the project's page studies or results, so studies run on
   the Study page (or by the seed) are invisible to every agent.

## Fix

Proposal (needs a contract change and Sahand's OK, as it changes agent behaviour): an optional
workspace method, e.g. `project_designs(project) -> {plants: [{version, name, note, by}],
studies: [{id, name, kind, status, plant_version, settings, result: {kpis, checks}}]}`, which the
backend serves from its tables, and geomind's `list_plants` / `list_studies` (or a new read tool for
the explainer) show it read-only beside the chat's own designs. The backend side is small once
geomind defines the method; routed to geomind (hotfix-python-III) and Coordinator-III.
- 2026-11-05 14:33 UTC: backend part live in 1.1.90 (hotfix-back-III, commit 37dba02, deployed 14:33 UTC): Workspace.project_designs(project) -> {plants:[{version,name,note,by,created,latest}] oldest first, studies:[{id,name,kind,status,created,plant_version,case_version,settings,result:{id,name,role,plant_version,case_version,kpis,checks}|None}] newest first}; Workspace.plant_version(project, n) -> stored gemini to_dict or None. Warmed before a run. geomind part: hotfix-python-IV.
- 2026-11-05 16:41 UTC: geomind 0.4.97 (0763b4b, tag v0.4.97), backend 1.1.101 (9611e31), deployed 2026-11-05: list_plants project_versions, list_studies lists project studies (project_study with KPIs/checks) first, read_plant(plant_version=N). Not live-retested.
## Retest

(Who, when, result.)
