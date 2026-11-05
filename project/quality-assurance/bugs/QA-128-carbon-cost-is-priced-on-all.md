# QA-128: Carbon cost is priced on all CO2e including grid electricity, possibly double counting the ETS cost inside the electricity price

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | gemini |
| Reporter | handbook-economics |
| Found | 2026-11-05 14:13 UTC |
| Versions | frontend <x.y.z>, backend <x.y.z> (geomind <x.y.z>) |
| Where | <URL>; project <name/id>; chat <id>; run <id>; step <n> |
| Fixer | |

## Steps

1. Simulate and cost gemini's hackathon example (`gemini/examples/hackathon_2026`).
2. Read the carbon cost line of the economics.

## Expected

Carbon is priced on the emissions the plant pays a carbon price for (its own fuel combustion and flared gas). Grid electricity carries its carbon cost inside the electricity price (EU ETS covers power generation), so it is either not priced again or priced only when the case says so.

## Actual

gemini prices carbon on ALL CO2e, grid electricity included (`gemini/evaluate/_utils/cost.py` `_bills` -> `emitted_steps`). In the hackathon example 0.45 of 0.71 MEUR/yr of carbon cost comes from grid electricity, which may double count the ETS cost already in the electricity price.

## Evidence

- ![screenshot](../evidence/QA-128/1.png)
- Run JSON: `../evidence/QA-128/run-<id>.json`

## Cause

Found by handbook-economics (via Coordinator-IV, 2026-11-05 ~14:20 UTC) while writing handbook-economics.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 15:14 UTC: gemini 0.6.16 (carbon price only on the plant's own CO2e; grid electricity's CO2 counted in co2, not priced again), backend 1.1.97, deployed ~15:20 UTC
## Retest

(Who, when, result.)
