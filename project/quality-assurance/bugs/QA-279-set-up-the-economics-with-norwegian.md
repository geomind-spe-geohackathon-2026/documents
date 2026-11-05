# QA-279: 'Set up the economics with Norwegian prices where they differ' drops the case's assumptions file for every key: Dutch discount rate, French radioactive-waste tariff (3.87 EUR/kg), 20 %/yr pump opex, 636893 EUR gas make-up

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 18:27 UTC |
| Versions | backend 1.1.110+ (geomind 0.4.110+), Knowledge data-economics.csv d131d47f, hackathon-2026-assumptions ad05815c |
| Where | https://geomind.team/projects/fa001b0b-183c-4f2e-94b4-1655d0ea56f9/assistant/chat; project "QA-TEST QA-E2E-economics-I 7"; run 5c1cd7b2-5d55-41ab-b8a2-9989c61d292c; case lead, ask_economics after step ~118 |
| Fixer | |

## Steps

1. Reference case (competition), no economics.
2. Chat: "Our plant will be built in Trondheim, Norway, and will be financed by the municipality.
   Set up the economics with Norwegian prices where they differ."
3. (Deny the weather-file card, QA-280.) Read the economics question card.

## Expected

The case's own assumptions document (`knowledge/hackathon-2026-assumptions.md`) stays the base
for every key; only where a NORWEGIAN source differs (there is one row: district cooling price,
SSB 2017) is the value replaced, and the card says which keys it changed and that no Norwegian
electricity/gas/heat price exists in the Knowledge.

## Actual

The card drops the assumptions file for EVERY key and takes the catalogue's "recommended" rows,
most of them neither Norwegian nor the team's values:

| Key | Card | Assumptions file | Row taken |
|---|---|---|---|
| discount_rate | 0.051 | 0.05 | PBL SDE++ 2025 geothermal (Netherlands) |
| energy.electricity, energy.gas, revenue.heat | OPEN | 105.75, 39.92, 60 | none |
| revenue.cold | 103.547 EUR/MWh | 60 | SSB 2017 (Norway, the only NO row) |
| opex.variable.waste_disposal | 3.86719 EUR/kg | 0.2 | French TFA radioactive waste (cf. QA-041) |
| opex.variable.chemical | 1.94175 EUR/kg | 3 | amine corrosion inhibitor market page |
| opex.fixed.production_pump | 20 %/yr | 2 | ECN 2012 ESP replacement |
| capex.gas_makeup | 636893 EUR | 50000 | nPro CHP proxy |
| capex.flare | 57700 EUR | 100000 | EPA proxy |
| capex.pipe | 1148.56 EUR/m | 500 | DEA distribution 5-25 MW |
| capex.heat_exchanger | 0.108893 EUR/W | 0.5 EUR/(W/K) | DEA station, unit basis differs |
| accounting.gwp.CH4 | 27.9 | 29.8 | IPCC SM (no carbon credit) |
| accounting.allocation.heat_cost_share | 0.76 | 0.8 | Fiaschi 2021 |
| capex.drilling | 1246.83 | 1239.13 | NL 2013 2300 m |

The card's own footer says the rows are "prices of Denmark, Norway, the Netherlands: they fit only
a site there". So "Norwegian prices where they differ" produced mostly Dutch, Danish and French
values. After my typed answer "Take every value from the assumptions file ... keep its EU prices"
the lead re-asked correctly in 45 s.

## Evidence

- The question card: `../evidence/QA-279/economics-question-card.txt`
- Run JSON: `../evidence/QA-279/run-5c1cd7b2.json.gz`

## Cause

Guess (from the card note): once the user names a country, the case lead treats the competition
assumptions file as not applicable (it is "for the GEMINI hackathon case") and lets
`ask_economics` fill every key from the catalogue's recommended rows; the region filter only
labels rows ("prices of ...") and does not prefer the case's base values.

## Proposed fix

geomind case lead skill (economics recipe) and `ask_economics`:
1. "Where they differ" = keep the existing base (assumptions file or current economics) and
   replace only keys for which a row of the named country exists; list the replaced keys.
2. Never recommend a row whose region differs from the named site over the base value (Dutch
   discount rate, French TFA tariff); put such keys in "Open" with the base value as the default.
3. Prefer the catalogue's general rows over proxies with a different unit basis (heat exchanger
   EUR/W vs EUR/(W/K)), cf. QA-192.

## Fix

- 2026-11-05 18:55 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest
