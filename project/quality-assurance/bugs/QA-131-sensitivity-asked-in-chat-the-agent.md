# QA-131: Sensitivity asked in chat: the agent tries run_python by hand (26 of 41 calls refused) instead of gemini's sensitivity study, and computes nothing

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | Fatemeh (asked for the run review), Claude (DB read and write-up) |
| Found | 2026-11-05 14:14 UTC |
| Versions | backend 1.1.86 and later during the runs (2026-11-05 10:10 to 14:07 UTC) |
| Where | https://geomind.team/projects/cf0c3d9c-d925-4ffa-bd29-3ac8205090d3 (project geo mind testing), chat 27379f2e-0103-4ddf-a020-f0cd4deb20a6; run 5cd1f2b8-feb5-4343-ab5c-b25bb8ec3adc |
| Fixer | hotfix-python |

## Steps

1. After the design, the user asks: "Run the one-at-a-time lcts sensitivity on the electricity price, discount rate, heat price and drilling cost, outside gemini's case if the schema still has no uncertainty block."

## Expected

The agent runs gemini's sensitivity study on the design (study kind `sensitivity`, as the user-run Sensitivity study in project SPE GeoHackathon 2026 did) with the four ranges, and reports the swing of lcts per driver.

## Actual

12 minutes, 2.36M input tokens: the economist cannot vary a driver (`estimate_costs` reads only the case's economics); the analysis lead then tries `run_python` by hand: 41 calls, 26 refused ("the case field is str, not one number", "economics.discount_rate does not exist", "no input has a source", the stored design, case and result cannot be loaded). Final answer: "The one-at-a-time lcts sensitivity was not computed — no lcts at any range end, no swing". Before that, the main run waited 76 minutes (11:44 to 13:00 UTC) on the ranges question for this sensitivity.

## Evidence

- Postgres read-only: run_events of run 5cd1f2b8 (tool counts, refusals); the chat's last assistant message, 14:07 UTC.

## Cause

Guess: the analysis lead does not use (or does not have) the sensitivity study, and run_python's input rules cannot take a stored design, case or result. Fix: the analysis lead runs `run_study` with kind sensitivity or sample on a stored design, the ranges as study settings; run_python only as a last resort.

## Fix

- 2026-11-05 14:38 UTC: geomind 0.4.88 (sensitivity values=; ranges into the case with set_case then sensitivity, never run_python), backend 1.1.92, deployed

Cause: gemini's sensitivity moves the values the case declares an `uncertainty` for; the case declared none for the four drivers, the economist has no `set_case`, and nothing told the lead to write the user's ranges into the case, so it hand-coded run_python, which cannot load a stored design, case or result. Fix: `sensitivity` takes `values` (only the named case paths move; an undeclared one is an error listing the declared ones and the set_case form); the economics skill and the analysis lead's rules give the path: `set_case(economics={key: {uncertainty: {kind: uniform, min, max}}})` with the user's ranges (merge patch, values and sources stay), then the economist's `sensitivity(values=[...])`; never run_python.

## Retest
