# QA-207: Catalogue: Eurostat band labels wrong in the NL electricity and gas rows (band ID labelled 20,000-69,999 MWh, IE 70,000-149,999 MWh, gas I4 1,000,000-3,999,999 GJ, I3 100,000-999,999 GJ)

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | data |
| Reporter | handbook-econ-report-I |
| Found | 2026-11-05 17:24 UTC |
| Versions | Knowledge data-economics.csv 74a0d44b; geomind data/knowledge/data-economics.csv (main) |
| Where | data-economics.csv lines 64-67 (ids, `item`) |
| Fixer | |

## Steps

1. Compare each row's band code with its consumption range and its source series (CEIC republishing Eurostat `nrg_pc_205` / `nrg_pc_203`).

## Expected

Eurostat non-household bands: electricity ID 2 000-19 999 MWh, IE 20 000-69 999 MWh, IF 70 000-149 999 MWh; gas I3 10 000-99 999 GJ, I4 100 000-999 999 GJ, I5 1 000 000-3 999 999 GJ.

## Actual

The ranges (and values) follow the source series, but the band codes in id and item are one band too low:

| Row now | Range in item and source | Correct band | New id |
|---|---|---|---|
| `electricity-nl-eurostat-2024-band-id` | 20 000-69 999 MWh | IE | `electricity-nl-eurostat-price-2024-band-ie` |
| `electricity-nl-eurostat-2024-band-ie` | 70 000-149 999 MWh | IF | `electricity-nl-eurostat-price-2024-band-if` |
| `gas-nl-eurostat-2024-band-i3` | 100 000-999 999 GJ | I4 | `gas-nl-eurostat-price-2024-band-i4` |
| `gas-nl-eurostat-2024-band-i4` | 1 000 000-3 999 999 GJ | I5 | `gas-nl-eurostat-price-2024-band-i5` |

An agent choosing "band IE" for a plant buying 20-70 GWh/yr (the usual rule, handbook-economics §10.2) gets the 70-150 GWh price (138.02 instead of 115.02 EUR2015/MWh, +20 %).

## Evidence

- The rows quoted above (`geomind/data/knowledge/data-economics.csv`).

## Cause

Fact: band letters mislabelled when the rows were added; ranges and values are right.

Fix (data): rename ids (the `price-` form of QA-202) and the band letter in `item`; values unchanged; note old -> new ids in data-economics.md; re-upload. Then handbook-econ-report-I updates handbook-economics §0.4 and §10.1.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
