# QA-090: The design loop does not converge: 2h40, 17.7M input tokens, 900 tool calls, 18 plant variants, no saved simulation result

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | functional-qa-2 |
| Found | 2026-11-05 09:23 UTC |
| Versions | frontend 1.1.7x, backend 1.1.75 at start (06:43 UTC), 1.1.79 at 08:13 UTC |
| Where | https://geomind.team/projects/df514ce2-1d5b-4681-a7e6-5592cc5eac30/assistant/chat/138c18fa-3751-4f74-a76e-b52cbd1105ef; project QA2 functional-qa-2 economics B; run cef908d9-1818-4567-b39d-a8c46fe9fcd2 |
| Fixer | hotfix-python |

## Steps

1. New project (shared memory Off), the three competition files, Auto-approve on.
2. Ask for the full design (case, plant, simulation, economics); answer 9 questions (assumptions, region NL, approve economics rows, chiller per-energy opex 0 as my accounting decision).
3. Watch the design stage from 07:43 UTC to now.

## Expected

The design loop ends with a simulated design and a verdict (pass, or fail with the cap named) in well under an hour, or stops and tells the user what blocks it; every simulated variant is saved as a result.

## Actual

Run cef908d9 at 09:20 UTC (2 h 37 min after start, 1 h 35 min after the last answer): status running, 17.8M input / 1.17M output tokens, 575 steps, 903 tool calls (patch_plant 55, simulate 17, read_stored 163, describe_module 114), 10 design_lead sessions and 17 energy_systems_engineer sessions, about 18 plant variants (design/energy_fix3 ... energy_fix18). The project shows Plant version 2 and Results: No results, although the agents' own notes say that full-year simulations ran (for example energy_fix7: 0 failed steps, 8 of 9 caps pass; two failing temperature caps and 106 failed pipe-pressure steps earlier).

What the agents kept changing: one requirement, R9 (the chilled loop sits at 26 °C on zero-cooling-demand days, and at 10.17 °C over-cooled on 2027-10-31), is chased for ~15 variants: add a bypass (no flow, stagnant), add a circulation pump (forces 1435 t/h, cold_delivered -3.1 million MWh, mass balance breaks), remove the bypass, change the chiller source-temperature floor and part-load floor, move work between integration_engineer, energy_systems_engineer and well_engineer ("the bypass is refused as the integration engineer's path"). Meanwhile the economics cannot be computed (the chiller per-energy opex), which I settled with the user answer 0 EUR/MWh at 08:31 UTC.

The loop has no stop rule that depends on progress: eight of nine caps pass from energy_fix7 on, yet the run goes on and no result is saved for the user.
## Evidence

- Agents of the run (sessions, steps, tool calls): `../evidence/QA-090/agents-cef908d9.json`; agent progress notes about the failures: `../evidence/QA-090/design-loop-agent-notes.txt`

## Cause

Fact: the one remaining failure is the zero-demand behaviour of the cooling loop (a modelling edge, not a design error). Guess: the design lead keeps asking for a perfect pass instead of reporting 8 of 9 caps with the failing one named; and a plant variant that simulates is not stored as a result until the run ends. Related: QA-086 (continue every 30 steps), QA-088 (Results tab).

## Fix

hotfix-python-III, 2026-11-05, geomind 0.4.79 (tag v0.4.79), backend 1.1.84 (deploy 10:30 UTC).
Duplicate in cause of QA-091: the one failing requirement was a supply temperature checked
`always` on zero-demand days; fixed there (set_case converts it to `running`, the case lead writes
`running` and adds heat/cold delivered). The loop's missing stop rule, geomind fc23de0: the design lead chases one failing
requirement for at most three changes, then keeps the design that fails least (simulated for the
whole year and checked), records it as final and names the open requirement (value, limit, steps,
why); the project lead then asks the user once (accept the design with it open, change the
requirement, stop) and never sends the same failure back. Results of agent-simulated designs on
the Results tab: QA-088 / QA-092 (backend 1.1.81-1.1.83).
- 2026-11-05 10:31 UTC: geomind 0.4.79/0.4.80, backend 1.1.84, deployed 10:30 UTC by hotfix-python-III
## Retest

(Who, when, result.)
