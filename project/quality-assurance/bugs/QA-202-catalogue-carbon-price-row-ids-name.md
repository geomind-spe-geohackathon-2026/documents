# QA-202: Catalogue carbon-price row ids name the report year, not the price year: 'ESMA EU ETS 2025' gives the 2024 price (51.56 vs 57.48 EUR/t), shown with 16 digits

| Field | Value |
|---|---|
| Status | verified |
| Severity | minor |
| Area | data |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 17:20 UTC |
| Versions | frontend 1.1.114, backend 1.1.104 (geomind 0.4.102); Knowledge data-economics.csv 74a0d44b |
| Where | project "QA-TEST QA-E2E-economics-I 2" (8ac1457c-8962-4425-b04a-8324af087473); run 2d460136-b1eb-4a21-b5e6-e04dff1266a2 |
| Fixer | handbook-econ-report-I |

## Steps

1. Project with economics set from the assumptions file (carbon 57.03 EUR/t).
2. Chat: "Two changes to the economics: use a discount rate of 7 %, and take the carbon price from
   the ESMA EU ETS 2025 row of the cost catalogue instead. Also tell me: is the CO2 of the grid
   electricity priced too?"

## Expected

The 2025 EU ETS price from ESMA (row `carbon-price-eu-ets-esma-2026`, item "EU ETS EUA average
spot price, 2025", 74 EUR/t -> 57.48 EUR/t 2015), or a question back because two ESMA rows fit
"2025". The value shown rounded (57.48 EUR/t).

## Actual

- The agent took row `carbon-price-eu-ets-esma-2025`, whose item is the **2024** price (65 EUR/t
  -> 51.55865788847466 EUR/t 2015), because the row id carries the report's year (ESMA's "EU
  Carbon Markets 2025" report covers 2024). It says "status verified, year 2025" and only further
  on "average spot price 2024". The value is 10 % below the 2025 price the user meant.
- The approval card, the stored value and the answer show 51.55865788847466 (16 digits).
- Good: discount 0.07 (no QA-120 regression); `about.sources` updated for both keys this time
  (unlike QA-186); the grid-CO2 answer is right and cites handbook-economics.md 3.6/16.7 (QA-128
  convention). Speed: 2 min 49 s, 0.0125 USD, 694k input tokens; two approval cards.

## Evidence

- Set case card: `../evidence/QA-202/set-case-card.txt`
- Chat answer: `../evidence/QA-202/chat-answer.txt`
- Rows: `geomind/data/knowledge/data-economics.csv` lines 61-62

## Cause

Fact: catalogue ids `carbon-price-eu-ets-esma-2025` (price 2024) and
`carbon-price-eu-ets-esma-2026` (price 2025) are named after the publication year.

## Proposed fix

1. Knowledge (data): rename the ids by price year (`carbon-price-eu-ets-esma-price-2024`,
   `...-price-2025`) or put the price year first in the item; re-upload data-economics.csv.
2. geomind (economics skill / `set_case` note): when a user names a year, match the row's price
   year, and ask back if two rows fit; round values shown to the user to 4 significant digits
   (cf. QA-099).

## Corrected rows (handbook-econ-report-I, 2026-11-05)

### Rule for every row id

- A **price row** (energy, carbon, revenue, subsidy: a value that is the price of one year)
  names its **price year** in the id, after `price-`: `carbon-price-eu-ets-esma-price-2025`.
  The publication year stays in the `year` column and in `source`.
- A **technology row** (capex, opex, a factor from a catalogue) may keep the publication year in
  its id (`boiler-gas-dea-2018-2-3mw`): `price_year` is the authoritative column. 28 rows are of
  this kind (DEA 2017/2018/2025, HRE4 2017, IRENA 2013, EPA 2019); they need no rename, but the
  `item` should end with "(prices of <price_year>)" so a reader never takes the id's year for it.
- `item` starts with what the value is **for**, with its year: "EU ETS EUA average spot price
  2025 (ESMA, EU Carbon Markets 2026 report)".

### The three carbon-price rows

| Old `id` | New `id` | `item` | `year` (publication) | `price_year` | `value` `unit` | `value_2015` `unit_2015` | Source |
|---|---|---|---|---|---|---|---|
| `carbon-price-eu-ets-esma-2026` | `carbon-price-eu-ets-esma-price-2025` | EU ETS EUA average spot price 2025 (ESMA, report of 2026) | 2026 | 2025 | 74 EUR/t CO2e | 57.4757 EUR/t CO2e | ESMA, EU Carbon Markets report 2026 (as in the row now); 74 × 100/128.75 |
| `carbon-price-eu-ets-esma-2025` | `carbon-price-eu-ets-esma-price-2024` | EU ETS EUA average spot price 2024 (ESMA, report of 2025) | 2025 | 2024 | 65 EUR/t CO2e | 51.5587 EUR/t CO2e | ESMA, EU Carbon Markets report 2025; 65 × 0.7932 (HICP 2024→2015, as the row's conversion) |
| `carbon-price-nl-co2-levy-rijksoverheid-2026` | `carbon-price-nl-co2-levy-price-2026` | NL CO2-heffing industrie, tariff 2026 | 2026 | 2026 | 78.67 EUR/t CO2 | 61.1029 EUR/t CO2 | Rijksoverheid (as in the row now); × 0.7767 (HICP 2025→2015, no 2026 index: say so in `note`) |

Every other column stays. The new row of QA-191 C becomes `carbon-price-eu-ets-instrat-price-2025`
(price 2025, published 2026).

Other price rows already name the price year (`electricity-nl-eurostat-2024-*`,
`gas-nl-eurostat-2024-*`: price 2024 S2, published 2025): keep them, rename only to the `price-`
form for one pattern (`electricity-nl-eurostat-price-2024-band-id`, ...). The SDE++ rows name the
round (2026), which is the price year too: keep.

References to update after the rename: `knowledge/handbook-economics.md` (§0.4 table and §8.1;
handbook-econ-report-I will do it when the new CSV is in Knowledge), `data-economics.md` (add a
"2026-11-05, QA-202" note listing old → new ids).

### Precision: `value_2015` to 6 significant digits

The conversions are exact products; 16 digits claim a precision no source has. Store
`value_2015` with at most 6 significant digits (enough for every sample value: 0.73786,
1239.13); round only for display to the user (4 significant digits, QA-099). 38 rows:

| Row `id` | `value_2015` now | write (6 significant digits) |
|---|---|---|
| `carbon-price-eu-ets-esma-2026` | 57.4757281553398 | 57.4757 |
| `carbon-price-eu-ets-esma-2025` | 51.55865788847466 | 51.5587 |
| `carbon-price-nl-co2-levy-rijksoverheid-2026` | 61.10291262135922 | 61.1029 |
| `electricity-nl-eurostat-2024-band-id` | 115.01546759736655 | 115.015 |
| `electricity-nl-eurostat-2024-band-ie` | 138.01856111683986 | 138.019 |
| `gas-nl-eurostat-2024-band-i4` | 37.507733798683276 | 37.5077 |
| `gas-nl-eurostat-2024-band-i3` | 44.41976679622432 | 44.4198 |
| `sde-basisbedrag-geothermal-pbl-2026-over-20mw` | 48.699029126213595 | 48.699 |
| `sde-basisbedrag-geothermal-pbl-2026-under-12mw` | 62.05825242718447 | 62.0583 |
| `sde-net-subsidy-geothermal-pbl-2026-over-20mw` | 27.49514563106796 | 27.4951 |
| `thermal-storage-tank-dea-2025-3000m3` | 168.55429713524322 | 168.554 |
| `thermal-storage-pit-dea-2025-70000m3` | 64.85472270187223 | 64.8547 |
| `ice-storage-mlakar-2022-low` | 23249.8663132687 | 23249.9 |
| `ice-storage-mlakar-2022-high` | 31704.363154457318 | 31704.4 |
| `opex-thermal-storage-tank-dea-2025` | 0.282326369282891 | 0.282326 |
| `flare-capex-proxy-epa-2019` | 57700.03506496464 | 57700 |
| `gas-makeup-capex-proxy-npro-chp-1mwe` | 636893.2038834952 | 636893 |
| `scale-inhibitor-proxy-watertap-2020` | 2.908067875204125 | 2.90807 |
| `waste-disposal-norm-proxy-covra-2026` | 45.93115622241835 | 45.9312 |
| `pipe-om-dea-2025-transmission-share` | 0.15824036711765171 | 0.15824 |
| `ice-storage-om-proxy-irena-2013-pcm-low` | 1.6666666666666667 | 1.66667 |
| `ice-storage-om-proxy-irena-2013-pcm-high` | 4.166666666666666 | 4.16667 |
| `scale-inhibitor-chemanalyst-2024-atmp-hamburg` | 0.7694665811430211 | 0.769467 |
| `scale-inhibitor-spitsov-2023-ro-jurbysoft` | 2.1455054458252554 | 2.14551 |
| `scale-inhibitor-spitsov-2023-ro-aminat-k` | 2.6816940661680038 | 2.68169 |
| `waste-disposal-tfa-france-2022` | 1027.221366204417 | 1027.22 |
| `production-pump-esp-kennisagenda-2016-250kwel` | 0.7183478000598623 | 0.718348 |
| `production-pump-esp-kennisagenda-2016-500kwel` | 0.5986231667165519 | 0.598623 |
| `production-pump-schlagermann-2023-332kwel` | 1.5457689466758628 | 1.54577 |
| `waste-disposal-tfa-france-per-kg-filter-density` | 3.8671863198283942 | 3.86719 |
| `corrosion-inhibitor-indexbox-2026-eu-amine-low` | 1.941747572815534 | 1.94175 |
| `corrosion-inhibitor-indexbox-2026-eu-amine-high` | 3.1067961165048543 | 3.1068 |
| `ice-storage-om-spice-2024-single-building-2000kwh` | 0.8769237514798088 | 0.876924 |
| `ice-storage-om-spice-2024-mid-size-10000kwh` | 0.7427277453722017 | 0.742728 |
| `ice-storage-om-spice-2024-district-cooling-50000kwh` | 0.5129999897400002 | 0.513 |

`in_case` values with 17 digits (1239.1304347826087) belong to QA-208 (the `in_case` column).

## Fix

- 2026-11-05 17:30 UTC: geomind 802aa38 (data/knowledge) + documents a67e69e; Knowledge data-economics.csv d131d47f, .md fc16fbd5, handbook-economics 8a18dc2d, hackathon-2026-assumptions ad05815c (2026-11-05 ~17:45 UTC, handbook-econ-report-I). Catalogue read from Knowledge at run time: no deploy needed.
## Retest

- 2026-11-05 18:02 UTC, QA-E2E-economics-I: PASSES. Project "QA-TEST QA-E2E-economics-I 5", run
  f7097fbc: "Use the EU ETS average spot price of 2025 from ESMA in the cost catalogue as the carbon
  price" -> row `carbon-price-eu-ets-esma-price-2025`, 57.4757 EUR/t (6 digits), summary names the
  2024 row as the other one. (The run's many set_case calls are QA-256.)
- 2026-11-05 18:03 UTC: QA-E2E-economics-I 18:02 UTC, run f7097fbc: right row and 57.4757 EUR/t; see Retest
