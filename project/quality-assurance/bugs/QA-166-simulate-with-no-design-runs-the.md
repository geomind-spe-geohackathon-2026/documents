# QA-166: simulate with no design runs the project's latest plant (v2 HeatingAbsorptionCoolingPlant) while the agents report it as plant version 1 HackathonPlant: wrong CAPEX, LCOH, CO2 in the report

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-report-I |
| Found | 2026-11-05 17:12 UTC |
| Versions | backend 1.1.103 at the call (geomind 0.4.98, gemini 0.6.16), frontend bundle index-TsXgd_n9.js |
| Where | https://geomind.team/projects/0e44cb05-6096-434e-95ee-56b434898015/assistant/chat; project QA-TEST QA-E2E-report-I 1; run 3f8270d5-b11e-4c86-b3ca-b0b4d4feb61c; design_lead step 12 (17:05:07 UTC) `simulate {"design": null, "start": "2027-01-01", "end": "2028-01-01"}` -> result/f2d63fe613c99a0f |
| Fixer | |

## Steps

1. Project with plant v1 = HackathonPlant and v2 = HeatingAbsorptionCoolingPlant (the latest).
2. Chat asks for the report of "HackathonPlant (plant version 1)". After QA-165 the design lead
   calls `simulate(design=null)` to "simulate the stored plant HackathonPlant (project plant
   version 1) as it stands".

## Expected

`simulate` runs plant version 1 (the one the agent named), or refuses a call that does not say
which version when the project has several.

## Actual

The chat result is the latest version (v2). Its KPIs equal, to every digit, a Study-page `run`
of plant v2 that I made to check, and differ from the Study-page `run` of v1:

| KPI | Page study v1 (a528d8da) | Chat simulate "v1" (f2d63fe6) | Page study v2 (31f5f0c8) |
|---|---|---|---|
| CAPEX MEUR | 34.64 | 23.96 | 23.96 |
| OPEX MEUR/yr | 3.65 | 4.98 | 4.98 |
| LCOH EUR/MWh | 43.75 | 47.81 | 47.81 |
| LCOC EUR/MWh | 51.45 | 56.21 | 56.21 |
| LCTS EUR/MWh | 45.10 | 49.28 | 49.28 |
| CO2 kt | 13.77 | 20.96 | 20.96 |
| Gas bought MWh | 0 | 65,190 | 65,190 |
| Boiler heat MWh | 254 | 76,830 | 76,830 |

The design lead's hand-back then says "Readable result reference: result/f2d63fe613c99a0f,
produced by simulate ... on the stored plant HackathonPlant (project plant version 1)", and the
analysis lead computes the report KPIs from it. Accuracy: the report numbers are those of the
other plant (CAPEX off by 31 %, CO2 by 52 %).

## Evidence

- KPIs of both page studies: `../evidence/QA-166/page-study-v1-kpis.json`, `page-study-v2-kpis.json`
- Run steps with the simulate call and the chat KPIs (compute_kpis at 17:06:06): `../evidence/QA-166/run1-steps.txt`

## Cause

Fact (code read, geomind 0.4.98): `load_plant(design=None)` -> `workspace_plant`
(`geomind/tools/gemini/plants.py:137`) reads `workspace.plants(project)`, which the backend fills
with the project's LATEST plant version only (QA-122 Cause 1). With one file there, no name is
asked and v2 is simulated. `read_plant(plant_version=1)` (0.4.97) reads v1, so the agent believes
it is simulating v1.

## Fix

Proposal (geomind, hotfix-python): `simulate` (and every tool with `design=None`) takes
`plant_version=N` like `read_plant`, loads that version via `Workspace.plant_version`, and puts
the version it ran into the result (`plant_version` in the summary). With several project
versions and no `plant_version`, refuse with the list of versions. Prompt/skill
`simulating-a-plant`: name the version you simulate.

## Retest

(Who, when, result.)
