# QA-202: Catalogue carbon-price row ids name the report year, not the price year: 'ESMA EU ETS 2025' gives the 2024 price (51.56 vs 57.48 EUR/t), shown with 16 digits

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | data |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 17:20 UTC |
| Versions | frontend 1.1.114, backend 1.1.104 (geomind 0.4.102); Knowledge data-economics.csv 74a0d44b |
| Where | project "QA-TEST QA-E2E-economics-I 2" (8ac1457c-8962-4425-b04a-8324af087473); run 2d460136-b1eb-4a21-b5e6-e04dff1266a2 |
| Fixer | |

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

## Fix

## Retest
