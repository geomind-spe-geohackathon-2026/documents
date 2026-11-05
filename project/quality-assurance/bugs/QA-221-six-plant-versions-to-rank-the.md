# QA-221: Six plant versions to rank: the design lead re-types every plant with build_plant (one card each, 15-30 s of output each) instead of design/v<N>; it names one 'v1', the reserved alias, and repeats the refused call 3 times

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 17:32 UTC |
| Versions | backend 1.1.105/1.1.106 (geomind 0.4.10x), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 4` (71a75f1c-d83f-41b1-b28e-539cb0340bdf); chat 0893ab3d-3bb9-4fe8-9a8b-0b72378b5623; run f548029f-572c-48cc-8773-de9d1f05bac3 |
| Fixer | hotfix-python-VIII |

## Steps

1. Project with the reference case and economics and six plant versions set through the API:
   v1 HeatingFullCoolingPlant, v2 HeatingHeatPumpCoolingPlant, v3 HackathonPlant, v4 HeatingCoolingPlant,
   v5 HeatingAbsorptionCoolingPlant, v6 HeatingPlant (the plant files of `gemini/examples/hackathon_2026/plants/`).
2. Chat (the no-agent showcase scenario, `reports/no-agent-showcase-gemini-0.6.17.md` section 1-3): "Size
   each one, optimise it on LCTS (20 evaluations per doublet count, seed 0), and rank all six by LCTS and
   CO2 with feasibility. Then, for the best feasible design, run a one-at-a-time sensitivity ... and a Monte
   Carlo of LCTS and CO2 with 5 draws and seed 1."

## Expected

One `run_study(designs=["design/v1", ..., "design/v6"], method="minimize", prepare=["size"], evaluations=20,
seed=0)` (gm.Study does the same in 73 s, 735 simulations), then sensitivity and sampling on the best.

## Actual

The design lead reads the six versions with `read_plant(plant_version=N)` (steps 10-12, fine), then
re-types each plant as a new design through `build_plant`, one approval card each:

| Step | Time (UTC) | Call | Result | LLM time |
|---|---|---|---|---|
| 13 | 17:27:26 | build_plant name `v1` | ok | 14.6 s |
| 14 | 17:27:53 | build_plant name `v1` | refused: "a design with this name is stored with other content; use a new name" | 8.3 s |
| 15 | 17:30:13 | build_plant name `fam1` | ok, but `params.d0.depth` missing (values dropped while re-typing) | 17.3 s |
| 16 | 17:30:43 | build_plant name `v1` | refused, same | 31.1 s |
| 17 | 17:31:29 | build_plant name `v1` | refused, same | 18.8 s |

After 6 minutes not one plant is optimised. `list_plants` gives `project_versions` (version, name, note)
but not the reference `design/v<N>` the study tools accept (QA-152 fix), so the lead does not know it can
pass `design/v1` directly; `v1` as a new design name collides with that alias and the refusal does not
say why. Re-typing a plant through the LLM also drops values (step 15).

## Evidence

- `../evidence/QA-221/run-f548029f-log-partial.json` (log at 17:32 UTC), `approval-cards.log`.

## Cause

- `geomind/geomind/tools/gemini/plants.py` `list_plants`: `project_versions` items carry no `design`
  reference; `read_plant(plant_version=N)` returns the plant without saying "use design/vN".
- `tools/gemini/stored.py:107` reserves `design/v<N>`; `save_design` reports a name clash as "stored with
  other content" instead of "v<N> is the alias of plant version N: use design/vN, or another name".
- Design lead prompt / skill `designing-a-plant`: nothing says that a stored plant version is already a
  design; the lead re-builds.

## Proposed fix

1. `list_plants` and `read_plant(plant_version=N)`: add `"design": "design/vN"` to each version.
2. `save_design`: refuse a name of the form `v<digits>` with a message naming the alias.
3. Skill `designing-a-plant` / `prompts/design/lead.md`: "a plant version is a design: pass
   `design/v<N>` to every study tool; never re-type a stored plant with build_plant".

## Fix

- 2026-11-05 17:40 UTC: geomind 0.4.110, deployed: reuse design/v<N>, never re-type with build_plant
