# QA-130: Production pump runs at 300 m3/h against a rated 162.6 m3/h (185 % of its rating) in a design that passes every check

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | gemini,geomind,frontend |
| Reporter | Fatemeh (asked for the run review), Claude (DB read and write-up) |
| Found | 2026-11-05 14:14 UTC |
| Versions | backend 1.1.86 and later during the runs (2026-11-05 10:10 to 14:07 UTC) |
| Where | https://geomind.team/projects/cf0c3d9c-d925-4ffa-bd29-3ac8205090d3 (project geo mind testing), chat 27379f2e-0103-4ddf-a020-f0cd4deb20a6; result lcts_best c5db89bc-2edc-44ae-85d9-df03168913bf |
| Fixer | hotfix-python |

## Steps

1. Open the Results of lcts_best (12 of 12 pass); Capacities.

## Expected

A unit's peak stays within its rating, or the check names the overload.

## Actual

Production pump d0: rating 162.6 m3/h, peak 300 m3/h, share 1.85 (185 % of the rating), in a design that passes every check (Max production flow 300 m3/h passes its limit).

## Evidence

- Postgres read-only: results.content.capacities of c5db89bc: `{'kind': 'Production pump', 'name': 'd0', 'value': 162.586, 'peak': 300.0, 'unit': 'm3/h', 'share': 1.845}`.

## Cause

Guess: the rating shown is the pump's nominal flow (d0.nominal_flow, optimised), not its maximum; or sizing does not size the pump to the flow the schedule asks. Either the label is wrong (then say "nominal", no share above 100 %) or the plant runs a pump past its rating unchecked (then a requirement or a sizing rule is missing).

## Fix

- 2026-11-05 14:28 UTC: gemini 0.6.15 (doublet flow capped at its pump's nominal_flow), backend 1.1.89, deployed 14:27 UTC

Cause: the schedule ran every doublet up to the case's flow maximum (300 m3/h) whatever its `nominal_flow`, the flow its pump is designed and priced for (162.6 m3/h after the optimiser); no check compared the two. Fix: the gemini 0.6.15 schedule runs a doublet at most at its nominal_flow (never below the case minimum), so a smaller pump costs the heat it cannot give. No frontend part.

## Retest

- 2026-11-05 14:44 UTC: Manual QA-II 15:10 UTC: same study, both production pumps 300 m3/h, peak 300 m3/h, 100 % of the rating (was 185 %)
