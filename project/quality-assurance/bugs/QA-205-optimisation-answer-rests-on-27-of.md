# QA-205: Optimisation answer rests on 27 of 240 trials: run_python refuses the study history (list input, data literals), read_stored has no slice, so the analysis lead reads trials one by one (42 read_stored)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 17:24 UTC |
| Versions | backend 1.1.104 (deploy during the run from 1.1.102), frontend bundle index-CEvw1roy.js |
| Where | https://geomind.team; project `QA-TEST QA-E2E-study-I 1` (8fcbf709-537a-40d9-ac1f-abadd1061775); chat c0cae905-a2a8-44cf-8bec-f4899f313e8b; run 4eb8e2f4-e775-4e2a-b257-853eae883724; analysis_lead 17:14:24-17:18:06 UTC |
| Fixer | hotfix-python-lead |

## Steps

1. Project seeded by API: reference `case.json` + `economics.json`, plants HackathonPlant (v1) and
   HeatingAbsorptionCoolingPlant (v2) from `gemini/examples/hackathon_2026/plants/`.
2. Chat: "Optimise this plant for the lowest cost of thermal supply: search the number of doublets
   (1 to 3), the flow per doublet (50 to 300 m3/h) and the absorption chiller capacity, within the
   competition limits." Approve every card.

## Expected

The design lead's `optimize` (study/opt1, 240 trials, 45 s) is summarised from the whole history:
best feasible point, the feasible share, the spread of lcts per variable. One call (a study summary,
or `run_python` over the history table) should do it.

## Actual

- `optimize` itself is fine: 45.3 s, 240 trials, best = 2 doublets, 300 m3/h, 10 MW chiller,
  lcts 49.281 EUR/MWh (the start point).
- The analysis lead then tries to tabulate the history:
  - 17:14:53 `run_python` refused: "the code holds data literals; pass each value as a named input
    instead: line 36: 12; line 14: 0.0; ... line 45: 300" (0.0, 1e-06 and the 300 cap inside a
    loop are refused as data);
  - 17:15:31 `run_python` refused: "inputs.hist: the stored part is list, not one number with its
    unit" (a stored list cannot be an input);
  - 17:15:50 `read_stored` path `result.history.0:20` refused: no slice; "a list of 240".
- So it reads trials one by one: 42 `read_stored` calls by analysis_lead (plus 19 by reviewer,
  14 by economist, 10 by design_lead). The final answer says "the study read 27 of its 240 trials,
  so the flatness is established on those trials" and "Only three of the 27 trials read are
  feasible". The user gets a conclusion drawn on 11 % of the search.
- Each of the two `run_python` calls needed an approval card from the user first, then failed.
- Whole run: 21 min 17 s (about 6 min of it was the build_plant approval waiting for me), 78 steps,
  173 tool calls, 2.41 M input tokens, 0.058 USD.

## Speed and accuracy

| Stage | Wall time | Calls |
|---|---|---|
| design_lead: build_plant, simulate, set_ranges x2, optimize | 17:08:09-17:10:40 (optimize 45 s) | ~25 |
| project_lead -> reviewer | 154 s | 32 (19 read_stored, 2 read_result refused, 1 compute_kpis refused) |
| project_lead -> analysis_lead (+ economist x2: 19 s, 49 s) | 17:14:16-17:21:30 | ~70 (42 read_stored) |
| project_lead -> explainer | 61 s | 12 |

Accuracy vs. the reference: heat 111667.68 / cold 23742.53 MWh from the CSVs match the
simulation; the answer's lcts basis uses 111744.16 / 23758.79 MWh (365.25-day year, see QA-099).
Hard limits in the result hold (300 m3/h, brine cooling 20.7 K <= 40 K, 2 doublets, 100/20 C).

## Evidence

- Run log: `../evidence/QA-205/run-4eb8e2f4-log.json` (steps at 17:14:53, 17:15:31, 17:15:50).

## Cause

Facts: run_python accepts only scalar named inputs with units and refuses numeric literals in code;
read_stored has no list slice; no tool returns a study's history as a table. Guess: the study tools
(`read_study`) give `best` and the raw `history` only.

## Proposed fix

In geomind (agents/tools): (1) `read_study` returns a compact summary of an optimisation history:
n trials, n feasible, best feasible k, min/max of each variable and metric among feasible trials;
(2) `run_python` accepts a stored list/table (a study history) as an input; (3) `read_stored`
accepts a slice `a:b` of a list. The analysis skill should say to use (1) and never to page a
history by hand.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 18:09 UTC: deployed 19:01-19:03 CET: backend 1.1.112, geomind 0.4.118/0.4.119, gemini 0.6.19 (hotfix-python team)
- 2026-11-05 18:28 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
## Retest

(Who, when, result.)
