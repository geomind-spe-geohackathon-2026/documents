# QA-106: Results, Constraints: 12 rows for the case's 10 requirements; the supply temperature rules show two or three times with different values

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend,backend |
| Reporter | Fatemeh (screenshots), Claude (DB read and write-up) |
| Found | 2026-11-05 10:41 UTC |
| Versions | backend 1.1.84 |
| Where | https://geomind.team/projects/cf0c3d9c-d925-4ffa-bd29-3ac8205090d3/design/results/c16255f0-a84b-4d1a-91ae-9c6e8af39550 (project geo mind testing, study sized1, chat 27379f2e) |
| Fixer | hotfix-back-II |

## Steps

1. Open the Results of study sized1; scroll to Constraints.

## Expected

One row per requirement of the case (10), each once.

## Actual

"6 of 12 pass": 12 rows for 10 requirements. Heating supply temperature shows three times (93.014 degC each, worst day 19 May 2027); Cooling supply temperature shows twice with different values (10 degC, worst day 31 Oct 2027; 24.121 degC, worst day 21 Oct 2027) and no word on what differs. The case has each rule once.

## Evidence

- ![Results: economics and energy](../evidence/QA-106/1.webp)
- ![Days covered](../evidence/QA-106/2.webp)
- ![Constraints](../evidence/QA-106/3.webp)
- Postgres read-only: case_versions of project cf0c3d9c, number 3 (10 requirements).

## Cause

Guess: the check returns one row per module that serves the role (several pipes or consumers on the heating side?) or per failure group, and the page lists them without the module or the reason that tells them apart (all show "Heating consumer").

## Fix

hotfix-back-II, 2026-11-05 10:47 UTC. Cause (backend, shown by gemini's design): gemini's
`requirements()` adds its own service check per supply, at least `demand.heating.supply_temperature`
on each heating grid and at most `demand.cooling.supply_temperature` on each cooling grid, named
`heating_supply_temperature` / `cooling_supply_temperature`, the same names the case lead gives
its rules. The report had 12 checks (10 case + 2 service). The backend looked up the case limit
by name, so the service checks showed the case's bound, and both rows had the same name, which the
page uses as row key, so a third Heating row was drawn. The two cooling values differ because the
case rule is min = max = 20 °C (10 °C fails as too cold, QA-091) and the service rule is ≤ 20 °C
(24.1 °C fails as too warm).
Fix: backend 1.1.85 (b0b90d1, d2fc41c): the repeat is `<module>.<name>.service`, titled
"... (service supply rule)", with its own bound (≥ 100 degC, ≤ 20 degC); a case rule in °C now
shows its direction (= 100 degC, = 20 degC). Constraints are computed on read, so result c16255f0
shows 12 distinct rows at once. Deploy 11:00 UTC.
- 2026-11-05 11:05 UTC: backend 1.1.85 deployed in 1.1.86 (11:00 UTC)
