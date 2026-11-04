# QA-049: The plant asks again for reservoir pressure, permeability and thickness that the case already has

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | backend |
| Reporter | Fatemeh (screenshot), Claude (write-up) |
| Found | 2026-11-04 21:25 UTC |
| Versions | frontend 1.1.33; backend 1.1.40 (API health at write-up) |
| Where | https://geomind.team/projects/55612f74-441f-4a37-9859-a7ea43ab6600/design/study?chat=b34c9901-8c3d-4dad-9694-b33a3dd152a7 (project QA qa-8 manual pipeline) |
| Fixer | hotfix-back |

## Steps

1. The case of project QA qa-8 (case version 10) has site.reservoir.pressure 250 barg, thickness 100 m, permeability 200 mD, reference_depth 2500 m.
2. Open Design > Study: the plant's missing list.

## Expected

Plant parameters that describe the same reservoir come from the case (or the agent is told they are the same values); the plant does not ask for them again.

## Actual

The plant lists as missing: params.d0.reservoir.pressure, d0.reservoir.permeability, d0.reservoir.aquifer_thickness, d0.reservoir.temperature, d0.reservoir.top_depth (plus drainage radius, skin, wellbore radius, roughness). The first ones are in the case already, so the reservoir engineer must copy them, with a chance of a different value or unit.

## Evidence

- ![Study tab with the missing list](../evidence/QA-049/1.webp)
- Postgres read-only: case_versions of project 55612f74, number 10, site.reservoir.

## Cause

Guess: gemini's Doublet takes its reservoir as plant parameters, separate from the case's site. A request to gemini needs Sahand's approval: list it in the gemini requests, do not ask gemini directly.

## Fix

- 2026-11-04 23:25 UTC: hotfix-python: gemini fills a Doublet's reservoir children from the case (engine/apply.py _doublets) once the doublet's design values are set. Checked with gemini 0.6.4: HackathonPlant without d0.reservoir pressure/permeability/thickness/temperature/top_depth and the example case: gm.check lists nothing; without d0.depth it lists only params.d0.depth. So the qa-8 plant (web template, project 55612f74) lists children because its doublet lacks its design values, or it was checked without the case (problems_of(content, None)). Needs that plant JSON (prod DB read was refused for hotfix-python): for hotfix-back to check the template plant and that the Study tab passes the case to gm.check.
- 2026-11-04 23:33 UTC: hotfix-back, backend 1.1.52 (44cde3b), deployed: cause: the web template HeatingCoolingPlant has no plant-level depth and gemini's check does not name it; without it the doublet cannot take its reservoir values from the case (checked locally with gemini 0.6.4 and the hackathon example case: template lists 8 d0.reservoir.* values; with params.depth 2500 m only d0.reservoir.skin is left). Now the plant's problems and the study's missing list name params.depth (and params.backup) first, 'with it each doublet takes its reservoir values from the case'. No prod DB read was needed. gemini part for hotfix-python/Sahand's list: gm.check should name params.depth.
## Retest
