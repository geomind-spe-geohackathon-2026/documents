# QA-191: Economics accuracy vs reference economics.json: rounded capex/opex (heat pump 0.738 vs 0.73786 ...), no uncertainty ranges, gwp.standard differs or open; the 'Cited' prices have no catalogue row

| Field | Value |
|---|---|
| Status | verified |
| Severity | minor |
| Area | data |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 17:13 UTC |
| Versions | backend 1.1.102/1.1.104 (geomind 0.4.10x); Knowledge 8bd08430 (hackathon-2026-assumptions.md), 74a0d44b (data-economics.csv) |
| Where | projects "QA-TEST QA-E2E-economics-I 1" (run bf3990c4) and "... 2" (run 2d5ced06) |
| Fixer | handbook-econ-report-I |

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
2. Knowledge (data): add catalogue rows `electricity-eu-eurostat-price-2025-band-ie` (105.75 EUR/MWh
   2015), `gas-eu-eurostat-price-2025-band-i4` (39.92), `carbon-price-eu-ets-instrat-price-2025` (73.43 ->
   57.03) to `data-economics.csv`, so the card can name a row and its URL.
3. geomind: let `ask_economics` carry an optional `uncertainty` per value (from the assumptions
   file's ranges), or have the case lead set them in the same approve all.

## Correct values and sources (handbook-econ-report-I, 2026-11-05)

Read from gemini 0.6.17 `examples/hackathon_2026/economics.json` (the reference) and its README
"Cited" table (lines 161-180). Exact digits; do not round.

### A. `hackathon-2026-assumptions.md`, economics table: replace the rounded values

| Key | Write exactly | Unit | Source as the reference README states it |
|---|---|---|---|
| `capex.drilling` | 1239.1304347826087 | EUR/m | Team: Mijnlieff et al. 2013, 5.7 MEUR / (2 × 2300 m), one price for every depth |
| `capex.heat_pump` | 0.73786 | EUR/W | DEA 0019 sheet "40 Comp. hp, waste heat 10 MW", 0.95 MEUR/MW_h (EUR 2025) / 1.2875 |
| `opex.fixed.heat_pump` | 0.2239 | %/yr | same sheet, fixed O&M 2126.745 EUR/MW_h/y over 0.95 MEUR/MW_h |
| `capex.boiler` | 0.06073 | EUR/W | DEA 0019 sheet "44 Natural Gas DH Only", 0.0638024 MEUR/MW_h (EUR 2020) / 1.0506 |
| `opex.fixed.boiler` | 3.25 | %/yr | same sheet, 2073.58 EUR/MW_h/y over 0.0638024 MEUR/MW_h |
| `capex.chp` | 0.96155 | EUR/W (electric) | DEA 0019 sheet "06 Gas engines, natural gas", 1.01020 MEUR/MW_e (EUR 2020) / 1.0506 |
| `opex.fixed.chp` | 1.0263 | %/yr | same sheet, 10367.88 EUR/MW_e/y over 1.01020 MEUR/MW_e |
| `accounting.gwp.standard` | IPCC AR6 WG1 table 7.15, GWP100 of fossil methane | text | IPCC AR6 WG1 ch. 7 table 7.15 (Forster et al. 2021), as quoted by Muñoz, Schmidt and Weidema (2024), ERL 19(12) 121002, https://doi.org/10.1088/1748-9326/ad8edd |
| `accounting.gwp.CH4` | 29.8 | - | same |

Every other economics value of the file already equals the reference (checked): discount_rate
0.05, analysis_period 25 yr, electricity 105.75, gas 39.92 EUR/MWh, carbon 57.03 EUR/t, revenue
heat and cold 60 EUR/MWh, heat_cost_share 0.8, chemical 3 and waste 0.2 EUR/kg, the Team capex
and fixed opex of the other kinds. Add one line under the table: "`accounting.gwp.standard` is
never open: write it as above." (run 2 left it open).

### B. Uncertainty: the four values that carry one in the reference

| Key | `uncertainty` exactly |
|---|---|
| `discount_rate` | `{"kind": "normal", "std": 0.01, "min": 0.02, "max": 0.08}` |
| `energy.electricity` | `{"kind": "uniform", "min": 80, "max": 140}` (EUR/MWh) |
| `energy.gas` | `{"kind": "triangular", "min": 25, "max": 70}` (EUR/MWh; mode = the value 39.92) |
| `carbon.price` | `{"kind": "triangular", "min": 30, "max": 110}` (EUR/t; mode = the value 57.03) |

Source: Team (assumptions of gemini's sample, no external source). The file's "Uncertainty
ranges" section also lists geothermal gradient (normal, std 2 K/km, 25-35) and permeability
(triangular 100-400 mD, mode 200): those are case values (`site.*`), not economics. The
reference `economics.json` has nothing else with an uncertainty. Write the four rows above in
JSON form in the file so the case lead can pass them through unchanged.

### C. Three catalogue rows for `data-economics.csv` (the "Cited" prices have no row)

Columns as the CSV header (`id,group,item,value,unit,price_year,value_2015,unit_2015,status,source,publisher,year,page,url,quote,conversion,path,in_case,note`):

```
electricity-eu-eurostat-price-2025-band-ie,energy prices,"Electricity, non-household, EU27_2020, band IE, excl. VAT, 2025 mean",136.15,EUR/MWh,2025,105.75,EUR/MWh,secondary,"Eurostat nrg_pc_205, electricity prices for non-household consumers",Eurostat,2025,"2025-S1 and 2025-S2, API data of 2026-10-19",https://ec.europa.eu/eurostat/databrowser/view/nrg_pc_205/default/table,"2025-S1 0.1381 EUR/kWh, 2025-S2 0.1342 EUR/kWh (EU27_2020, band IE 20 000-69 999 MWh, X_VAT)","mean 0.13615 EUR/kWh = 136.15 EUR/MWh (EUR 2025); / HICP 128.75/100 = 105.75 EUR2015/MWh",economics.energy.electricity,105.75,"EU average where the case names no country; values as quoted in gemini examples/hackathon_2026/README.md"
gas-eu-eurostat-price-2025-band-i4,energy prices,"Natural gas, non-household, EU27_2020, band I4, excl. VAT, 2025 mean (GCV)",51.4,EUR/MWh (GCV),2025,39.92,EUR/MWh (GCV),secondary,"Eurostat nrg_pc_203, gas prices for non-household consumers",Eurostat,2025,"2025-S1 and 2025-S2",https://ec.europa.eu/eurostat/databrowser/view/nrg_pc_203/default/table,"2025-S1 0.0545 EUR/kWh, 2025-S2 0.0483 EUR/kWh (EU27_2020, band I4 100 000-999 999 GJ, X_VAT)","mean 0.0514 EUR/kWh = 51.4 EUR/MWh (EUR 2025); / 1.2875 = 39.92 EUR2015/MWh",economics.energy.gas,39.92,"Per kWh of gross calorific value; gemini prices gas on the lower heating value (handbook-economics §3.3)"
carbon-price-eu-ets-instrat-price-2025,carbon,"EU ETS allowance, 2025 volume-weighted auction average",73.43,EUR/t CO2e,2025,57.03,EUR/t CO2e,secondary,"EU ETS 2025 summary and the beginning of 2026 auctions (W. Przedlacki)",Instrat Foundation,2026,8 January 2026,https://energy.instrat.pl/en/eu-ets-2025-summary/,"The average CO2 allowance price in 2025 amounted to EUR 73.43 per tCO2 (volume-weighted average)","73.43 / 1.2875 = 57.03 EUR2015/t",economics.carbon.price,57.03,"213 primary-market auctions of 2025; a secondary source (Commission/EEA pages not opened)"
```

Status `secondary` for all three: the values were read through gemini's sample README, not
re-opened in the Eurostat API or the Instrat page for this fix. The Eurostat databrowser URLs
are the dataset pages; the reference README cites the dataset codes and the API date, not a URL.
After adding them: re-upload `data-economics.csv` and `.md` (with a "2026-11-05" note: rows 155
to 157), and let the assumptions file cite these row ids for the three prices.

## Fix

- 2026-11-05 17:30 UTC: Data part: exact sample values, gwp.standard text, the four economics uncertainties as JSON in the assumptions file, three cited catalogue rows. geomind 802aa38 (data/knowledge) + documents a67e69e; Knowledge data-economics.csv d131d47f, .md fc16fbd5, handbook-economics 8a18dc2d, hackathon-2026-assumptions ad05815c (2026-11-05 ~17:45 UTC, handbook-econ-report-I). Catalogue read from Knowledge at run time: no deploy needed. Code part (ask_economics carrying uncertainty) filed as QA task below.
## Retest

- 2026-11-05 17:53 UTC: QA-E2E-economics-I 17:51 UTC, run 4aa5be35 (project QA-TEST QA-E2E-economics-I 5): approve all gives every reference value exactly (0.73786, 0.06073, 0.96155, 0.2239, 1.0263, 1239.1304347826087, gwp.standard text) and names the new catalogue rows; uncertainty still not set: tracked in QA-216
