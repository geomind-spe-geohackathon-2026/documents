# QA-191: Economics accuracy vs reference economics.json: rounded capex/opex (heat pump 0.738 vs 0.73786 ...), no uncertainty ranges, gwp.standard differs or open; the 'Cited' prices have no catalogue row

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | data |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 17:13 UTC |
| Versions | backend 1.1.102/1.1.104 (geomind 0.4.10x); Knowledge 8bd08430 (hackathon-2026-assumptions.md), 74a0d44b (data-economics.csv) |
| Where | projects "QA-TEST QA-E2E-economics-I 1" (run bf3990c4) and "... 2" (run 2d5ced06) |
| Fixer | |

## Steps

1. Reference case without economics; chat "Set up the economics of this case." (twice, two
   projects).
2. Compare the question card and the stored `economics.json` with
   `gemini/examples/hackathon_2026/economics.json`.

## Expected

Approve all gives the reference economics exactly (the assumptions file says it is "taken from
gemini's sample"): same numbers, the uncertainty ranges the studies need, the same GWP standard
name, every time.

## Actual

Accuracy table (stored values, project 1, before the user's changes; project 2 same numbers):

| Key | App | Reference | Diff |
|---|---|---|---|
| capex.heat_pump | 0.738 EUR/W | 0.73786 | +0.02 % |
| capex.boiler | 0.0607 EUR/W | 0.06073 | -0.05 % |
| capex.chp | 0.962 EUR/W | 0.96155 | +0.05 % |
| capex.drilling | 1239.13 EUR/m | 1239.1304347826087 | ~0 |
| opex.fixed.heat_pump | 0.224 %/yr | 0.2239 | +0.04 % |
| opex.fixed.chp | 1.026 %/yr | 1.0263 | -0.03 % |
| discount_rate, energy.electricity, energy.gas, carbon.price | value right | have `uncertainty` | uncertainty missing |
| accounting.gwp.standard | run 1: "IPCC AR6 GWP100" (catalogue row); run 2: left OPEN | "IPCC AR6 WG1 table 7.15, GWP100 of fossil methane" | differs / missing |
| every other key | equal | | |

- The rounding comes from the Knowledge file: `hackathon-2026-assumptions.md` lists "0.738",
  "0.0607", "0.962", "0.224", "1.026", "1239.13" (rounded) while the sample has full digits. The
  agents copy the file faithfully. Effect on LCOH is ~0.05 % at most, but the team's rule for gas
  composition (QA-112) is exact sample values, "do not round".
- The file's "Uncertainty ranges (studies only)" section is never set: a sensitivity or
  uncertainty study later has no ranges for discount rate, electricity, gas and CO2 price and must
  ask again (the reference has them in `economics.json`).
- The card cites the electricity, gas and CO2 prices as "Cited: Eurostat nrg_pc_205 ... 2025" /
  "Instrat" but `data-economics.csv` has no row for them (only NL 2024 Eurostat rows and ESMA
  57.48 EUR/t), so the card shows "no row" for the three main prices; the handbook-economics.md
  §8.1 holds the Instrat derivation. Run 2's card dropped the citation and wrote only
  "knowledge/hackathon-2026-assumptions.md".
- Run 1 and run 2 differ on the same input (gwp.standard set vs open; citation text).

## Evidence

- Stored economics, project 1: `../evidence/QA-191/economics-project1.json`
- Question cards: `../evidence/QA-191/card-run1.txt`, `../evidence/QA-191/card-run2.txt`

## Cause

Fact: rounded numbers and no uncertainty in the economics table of
`documents/project/quality-assurance/inputs/hackathon-2026-assumptions.md` (Knowledge 8bd08430);
`ask_economics` has no place for `uncertainty`; no catalogue rows for the three cited prices.

## Proposed fix

1. Knowledge (data): write the exact sample values in `hackathon-2026-assumptions.md` (0.73786,
   0.06073, 0.96155, 0.2239, 1.0263, 1239.1304347826087) and the GWP standard text
   "IPCC AR6 WG1 table 7.15, GWP100 of fossil methane"; re-upload.
2. Knowledge (data): add catalogue rows `electricity-eu-eurostat-2025-band-ie` (105.75 EUR/MWh
   2015), `gas-eu-eurostat-2025-band-i4` (39.92), `carbon-price-eu-ets-instrat-2025` (73.43 ->
   57.03) to `data-economics.csv`, so the card can name a row and its URL.
3. geomind: let `ask_economics` carry an optional `uncertainty` per value (from the assumptions
   file's ranges), or have the case lead set them in the same approve all.

## Fix

## Retest
