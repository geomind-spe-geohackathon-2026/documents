# QA-085: NL-specific cost rows (electricity, gas, heat price, SDE subsidy) are set for a case with no site country; the region is neither asked nor labelled

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | functional-qa-2 |
| Found | 2026-11-05 06:41 UTC |
| Versions | frontend 1.1.71, backend 1.1.71 (values set), read on backend 1.1.75; geomind 0.4.65 |
| Where | https://geomind.team/projects/aa8023ca-33b3-4e5a-a7ea-5afad6ed4c1e/design/case (Economics tab); project QA2 functional-qa-2 economics; chat f349646d-953b-41c5-a349-09903a5e29c5; runs 6921d00e (set at 04:3x UTC) and f59e5d2c |
| Fixer | hotfix-python |

## Steps

1. New project, three competition files, Auto-approve on; ask for case, design, simulation and full economics.
2. Answer the economics question: "Approve all the sourced catalogue rows as recommended ... I assume no subsidy, so leave revenue.subsidy.cap and revenue.subsidy.capacity unused." (the question had listed the rows, the NL rows included).
3. Open Design > Case > Economics and read economics.json.

## Expected

The brief gives no country. A region assumption is asked or clearly labelled (user assumption, to be confirmed), or country-neutral rows are used.

## Actual

economics.json uses Dutch/NL-specific rows without a label: energy.electricity 115.02 EUR/MWh (electricity-nl-eurostat-2024-band-id), energy.gas (gas-nl-eurostat-2024-band-i4), revenue.heat 114.555 EUR/MWh (heat-price-nl-cap-2026, a Dutch heat price cap), subsidy (SDE++), capex.drilling and degasser (nl-2013). The agent's own question text said 'The brief gives no site country, so no row of the site's country could be preferred', yet it recommended NL rows and the user is not told that NL is assumed. These prices drive OPEX, revenue, LCOH and NPV.

## Evidence

- Case economics: `../evidence/QA-085/case-economics.json`.

## Cause

Fact: source ids in about.sources. Guess: the catalogue's 'recommended' row per key happens to be the NL one; the agent did not state the implied region.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 10:01 UTC: geomind 0.4.78 + gemini 0.6.12 in backend 1.1.83 (5b2691e), deployed 2026-11-05 10:00 UTC by hotfix-python-II
- 2026-11-05 18:41 UTC: reopened by QA-E2E-case-I: site Trondheim, Norway in the case, economics question still recommends 9 NL rows (see file)
## Retest

(Who, when, result.)

## Seen again (QA-E2E-case-I, 2026-11-05 18:40 UTC, backend 1.1.116)

Project QA-TEST QA-E2E-case-I 6 (80139e85), no files, site given by the user: "Trondheim, Norway"
(the case holds `about.site: "Trondheim, Norway"`). The economics question (run 3bb1de01) recommends
rows "prices of the Netherlands" for electricity (115.015 EUR/MWh, electricity-nl-eurostat-price-2024-band-ie),
gas (37.5077, gas-nl-...), drilling (drilling-nl-2013-2300m), degasser (degasser-nl-2013) and the
discount rate (0.051, pbl SDE++ NL), while it takes a Norway row for the cold revenue. The note under
the list says "name the site's country to take its rows" although the country is already in the case.
Evidence: `../evidence/QA-085/QA-E2E-case-I-project6-economics-question.txt` (9 NL rows, 1 NO row).
Proposed fix: ask_economics / the economist pick rows by `about.site` country first; when none exists for
that country, the EU row (not another country's), and say so in the question.
