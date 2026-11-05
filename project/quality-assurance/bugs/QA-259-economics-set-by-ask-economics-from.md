# QA-259: Economics set by ask_economics from the assumptions document carry no uncertainty, although the document gives the ranges; a later sensitivity or Monte Carlo on that case has nothing to move

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 18:05 UTC |
| Versions | backend 1.1.108 (geomind 0.4.107+), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 5` (ed21ea3b-4489-498e-9f76-8f56eb15a39c); run da297015-fa41-4885-9cca-a178f7548bc1 (economics set), run ce5d9ffc (change) |
| Fixer | |

## Steps

1. Case without economics; chat "What does the stored plant cost on this case? ..." (QA-168 retest). The analysis lead
   asks one `ask_economics` from `knowledge/hackathon-2026-assumptions.md` section 1.4; answer "approve all".
2. Read the stored `economics.json` (`GET /design/case/files/economics.json?project=...`).

## Expected

The values AND the uncertainty the document gives ("Uncertainty ranges (studies only)": electricity uniform 80-140
EUR/MWh, gas triangular 25-70, CO2 triangular 30-110, discount rate normal std 1 % 2-8 %), as in the reference
`economics.json`, offered in the same question, so the case supports `sensitivity` and `sample_uncertainty`.

## Actual

Neither the `ask_economics` input nor the stored economics hold any `uncertainty` (discount_rate `{value: 0.06}` after
the change, carbon.price `{value: 80, unit: EUR/t}`). The values equal the reference, but the reference case has
uncertainty on 4 economics keys and this one on none, so "how sensitive is LCTS to ..." on this project must first ask
again for every range (or fails "a case without declared uncertainty is an error").

## Evidence

- `../evidence/QA-168/run-da297015-retest-log.json` (ask_economics input: no `uncertainty`).
- `../evidence/QA-186/run-ce5d9ffc-retest-log.json`.

## Cause

Guess: `tools/gemini/economics.py` `ask_economics` builds values from catalogue rows / document rows and has no field
for a distribution; the assumptions document puts the ranges in a separate table ("studies only").

## Proposed fix

`ask_economics`: when the source document or the catalogue gives a range for a key, propose it as the key's
`uncertainty` in the same question (one line per key: value, unit, source, range), and write it with the value.
