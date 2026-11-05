# QA-206: Catalogue: duplicate row id opex-absorption-chiller-hre4-2017-500kw (two rows, %/yr and EUR/MW/yr), a row cited by id is ambiguous

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | data |
| Reporter | handbook-econ-report-I |
| Found | 2026-11-05 17:24 UTC |
| Versions | Knowledge data-economics.csv 74a0d44b; geomind data/knowledge/data-economics.csv (main) |
| Where | data-economics.csv lines 107 and 154 |
| Fixer | handbook-econ-report-I |

## Steps

1. `grep -n opex-absorption-chiller-hre4-2017-500kw geomind/data/knowledge/data-economics.csv`

## Expected

One row per `id`; an id cited in a case (`about.sources`, `ask_economics` rows) names exactly one value.

## Actual

Two rows share the id:
- line 107: item "Absorption chiller, water-LiBr, 500 kW: fixed O&M over investment", 3400 EUR/unit/yr, `price_year` EMPTY, `value_2015` 4.0 %/yr, HRE4 D3.2 pp. 43-44, sect. 5.6.6;
- line 154: item "Water-LiBr absorption chiller, steam heated, 500 kW, fixed O&M", 3400 EUR/unit/yr, `price_year` 2015, `value_2015` 6800 EUR/MW/yr, same report p. 49.
Same source figure (3400 EUR/yr on 85 000 EUR for 500 kW), two bases.

## Evidence

- The rows quoted above (`geomind/data/knowledge/data-economics.csv`).

## Cause

Fact: the 2026-11-05 addition (QA-006) added the EUR/MW/yr row under the id of the older %/yr row.

Fix (data): keep both bases under two ids: line 107 -> `opex-absorption-chiller-hre4-2017-500kw-share` (4.0 %/yr = 3400 / 85 000; set `price_year` 2015 as line 154 says), line 154 -> `opex-absorption-chiller-hre4-2017-500kw-per-mw` (6800 EUR/MW/yr = 3400 / 0.5 MW). Note both in data-economics.md; re-upload csv and md.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
