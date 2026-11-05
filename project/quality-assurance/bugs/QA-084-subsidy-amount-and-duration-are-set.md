# QA-084: Subsidy amount and duration are set in the case economics although the user said no subsidy

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | functional-qa-2 |
| Found | 2026-11-05 06:41 UTC |
| Versions | frontend 1.1.71, backend 1.1.71 (values set), read on backend 1.1.75; geomind 0.4.65 |
| Where | https://geomind.team/projects/aa8023ca-33b3-4e5a-a7ea-5afad6ed4c1e/design/case (Economics tab); project QA2 functional-qa-2 economics; chat f349646d-953b-41c5-a349-09903a5e29c5; runs 6921d00e (set at 04:3x UTC) and f59e5d2c |
| Fixer | |

## Steps

1. New project, three competition files, Auto-approve on; ask for case, design, simulation and full economics.
2. Answer the economics question: "Approve all the sourced catalogue rows as recommended ... I assume no subsidy, so leave revenue.subsidy.cap and revenue.subsidy.capacity unused." (the question had listed the rows, the NL rows included).
3. Open Design > Case > Economics and read economics.json.

## Expected

With the user saying 'I assume no subsidy' the case economics has no subsidy revenue, or the agent asks whether the amount and duration rows should stay.

## Actual

economics.json holds revenue.subsidy.amount 48.699 EUR/MWh (row sde-basisbedrag-geothermal-pbl-2026-over-20mw, a Dutch SDE++ amount) and duration 15 yr. The agent kept both (and set only cap and capacity aside, the two keys I named). Note on my own wording: I named only cap and capacity; a user saying 'no subsidy' means all subsidy keys. If the NPV later counts this subsidy, it overstates revenue.

## Evidence

- Case economics read from the page: `../evidence/QA-084/case-economics.json` (about.sources lists the row ids). Still to check: whether the NPV of a finished simulation includes the subsidy.

## Cause

Guess: the agent reads 'no subsidy' as unusable cap/capacity keys only and keeps the other subsidy rows because 'approve all' covered them; it does not ask.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
