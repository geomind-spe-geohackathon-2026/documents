# QA-278: Showcase scenario through the agents picks the wrong winner: HeatingFullCoolingPlant re-typed by hand is optimised to 52.5 EUR/MWh (rank 6) while gemini optimises the stored version to 32.4 (rank 1); 57 min and 0.17 USD against 46 s for the same three page studies

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 18:25 UTC |
| Versions | backend 1.1.105 -> 1.1.112 during the run (geomind 0.4.10x -> 0.4.119, gemini 0.6.17 -> 0.6.19), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 4` (71a75f1c-d83f-41b1-b28e-539cb0340bdf); chat 0893ab3d-3bb9-4fe8-9a8b-0b72378b5623; run f548029f-572c-48cc-8773-de9d1f05bac3 (17:25:32-18:22:21 UTC) |
| Fixer | |

## Steps

The no-agent showcase (`reports/no-agent-showcase-gemini-0.6.17.md`, sections 1-3) through the agents:

1. Project with the reference case + economics and six plant versions (API): v1 HeatingFullCoolingPlant, v2
   HeatingHeatPumpCoolingPlant, v3 HackathonPlant, v4 HeatingCoolingPlant, v5 HeatingAbsorptionCoolingPlant, v6
   HeatingPlant (`gemini/examples/hackathon_2026/plants/*.json`).
2. Chat: "Size each one, optimise it on LCTS (20 evaluations per doublet count, seed 0), and rank all six by LCTS and
   CO2 with feasibility. Then, for the best feasible design, run a one-at-a-time sensitivity of LCTS to every
   uncertain value the case declares, and a Monte Carlo of LCTS and CO2 with 5 draws and seed 1 (mean, p5, p95)."
3. Approve every card.

## Expected

The agents' ranking equals gemini's on the same plant files: page studies `minimize` (lcts, 20, seed 0, size first)
on the stored versions, run right after the agents (gemini 0.6.19, 21-35 s each, all three in 46 s): v1 32.38 EUR/MWh
(feasible, 2 doublets 3232 m, 276 m3/h), v2 38.03, v4 38.16. The showcase (gemini 0.6.17, gm.Study, 735 simulations in
73 s) also ranks HeatingFullCoolingPlant first (36.0). The stress test then runs on that winner.

## Actual

| Family | Agents LCTS / CO2 | gemini page study | Match |
|---|---|---|---|
| v1 HeatingFullCoolingPlant | 52.46 / 21.35 kt, rank 6 | 32.38 / 9.13 kt (showcase 36.0 / 7.74), rank 1 | no |
| v2 HeatingHeatPumpCoolingPlant | 38.03 / 12.90, rank 1 | 38.03 / 12.90 (showcase 38.0) | yes |
| v3 HackathonPlant | 41.30 / 13.05 | 41.30 (project 1, be37a85f; showcase 41.3) | yes |
| v4 HeatingCoolingPlant | 44.30 / 15.34 | 38.16 / 11.69 (showcase 41.9) | no |
| v5 HeatingAbsorptionCoolingPlant | 49.34 / 20.96 | showcase 49.3 | yes |
| v6 HeatingPlant | 44.62, infeasible (no cold) | showcase 27.9, infeasible | value differs, verdict same |

So the agents recommend v2 (38.03) and stress-test it, while v1 is 6 EUR/MWh cheaper and has 30 % less CO2. The answer
even says "the cheapest thermal supply is also the lowest-carbon one" about v2.

Why: the design lead never optimises the stored versions. It re-types every plant with `build_plant` (QA-221): v1
was rebuilt by hand 7 times (names v1, fam1, f1, v1_start ...; 4 refused) and the plant finally optimised,
`design/v1_start`, differs from the stored v1 in 579 lines of its JSON (free-module connections written by the LLM
instead of the class). Its optimum: 2 doublets, 2605 m, 266 m3/h, chiller 3.9 MW, 52.46 EUR/MWh. v4 went the same way
(`v4_start` refused, `v4_one` patch refused, `v4_plant` built). The families that came out right (v2, v3, v5) are those
it re-typed closely.

Time and cost: 56 min 49 s, 362 tool calls (54 refused), 7.0 M input tokens, 0.168 USD; 136 design-lead steps, 38
reviewer steps; LLM time 2 074 s. gemini's own work in it: 6 `optimize` calls 158 s, sizing ~12 s, sensitivity 2.1 s,
5-draw sample 1.1 s, about 3 min. The stress test of the (wrong) winner itself was fine and fast: sensitivity of all six
declared values (gradient 13.48, electricity 8.10, gas 7.47, discount 7.15, carbon 4.38, permeability 2.03 EUR/MWh) and
5 draws seed 1 (LCTS mean 41.81, p5 38.45, p95 46.74 EUR/MWh; CO2 mean 13.83, p5 12.54, p95 15.22 kt).

Two deploys (1.1.106 ~17:45, 1.1.112 ~18:05) restarted the run; the design lead then rebuilt v3 and v4 again (17:57-18:12).

## Evidence

- `../evidence/QA-278/run-f548029f-log.json` (all steps), `approval-cards.log`.
- Page studies (no LLM) in the same project: minimize v1 bad20375 (result bad20375-c27b-4e2c-99e3-7eb63aa28e14), v2
  f5ae9d08-975f-4fc0-aedc-c0b7f68cbf31, v4 d9a4723e-5180-4db3-892b-4f8f1016819d (results).

## Cause

- QA-221: plant versions are not offered as `design/v<N>` and the lead re-types them; re-typing through the LLM changes
  the plant (structure and values) without anyone checking it against the stored version.
- No check that a re-built design equals its source; the reviewer checks feasibility, not identity.
- The comparison driver runs one family per design-lead session, in series (23 driver steps).

## Proposed fix

1. QA-221 fix: `run_study(designs=["design/v1", ..., "design/v6"], method="minimize", prepare=["size"])` in one call
   (gemini runs the families in parallel; 46 s here).
2. `build_plant` from a stored version (or `from_class` of a stored class plant) must not be the path; if the lead
   re-builds, `build_plant` warns when the result differs from a project plant version of the same name/type.
3. Comparison of N stored families: one study, not N design rounds; the reviewer checks the winner only.

## Fix

- 2026-11-05 18:57 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
