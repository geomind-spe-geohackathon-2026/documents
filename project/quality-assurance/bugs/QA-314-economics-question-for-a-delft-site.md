# QA-314: Economics question for a Delft site says 'Every value is the GEMINI hackathon assumptions document' while 8 keys come from Dutch catalogue rows; analysis_period 15 yr is taken from the SDE++ subsidy period

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 19:05 UTC |
| Versions | geomind 0.4.131 (backend live at 19:00 UTC) |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 11 (ed373904-e143-412b-b1b5-f4a21fe6f48b); run f4018b98-e445-4c8f-a3f5-4c6eea269d10; case_lead `ask_economics` request-464 |
| Fixer | |

## Steps

1. New project with the three competition files. Chat: "Set up the case from the uploaded brief and
   the two demand CSVs. The site is in Delft, Netherlands: take the outside air temperature and
   humidity for 2027 from a weather service, not a constant."
2. Approve all; read the economics question.

## Expected

The question's note says where the values come from, true for every line. `analysis_period` is the
plant's economic life (the assumptions document gives 25 yr; the reference `economics.json` 25 yr).

## Actual

- Note: "Every value is the GEMINI hackathon assumptions document (knowledge/hackathon-2026-assumptions.md),
  so results compare with gemini's sample case".
- But 8 keys come from Dutch catalogue rows (the tool's country rule for a Delft site): discount_rate
  0.051 (PBL SDE++ 2025), **analysis_period 15 yr (row `analysis-period-sde-2025-subsidy-period`, the
  SDE++ subsidy duration)**, electricity 115.015 EUR/MWh (NL 2024), gas 37.5077 EUR/MWh (NL band I5),
  carbon 61.1029 EUR/t (NL CO2 levy for industry), heat revenue 114.555 EUR/MWh (ACM cap 2026),
  drilling 1246.83 EUR/m, degasser 1006240 EUR. The rest are the document's values. Each line shows
  its row, so the user can see it, but the note says the opposite and "results compare with gemini's
  sample case" is false (LCOH changes with every one of them).
- `analysis_period` 15 yr from a subsidy period: the economic life of a geothermal plant is 25-30 yr;
  a 15-year analysis drops 10 years of revenue and raises LCOH. The subsidy duration belongs in
  `revenue.subsidy.duration`.

## Evidence

- `../evidence/QA-314/answers.json` (entry with request-464: the whole question)
- `../evidence/QA-314/run-f4018b98.json` (run log)

## Cause

1. The model writes the note before or apart from the tool's rows (the tool fills keys it did not
   name with the country rule); the note is free text.
2. Knowledge `data-economics.csv`: the row `analysis-period-sde-2025-subsidy-period` is filed under
   `economics.analysis_period`, so the country rule recommends it for any Dutch site.

## Proposed fix

- geomind (`ask_economics`): write the source summary of the question from the rows it shows
  ("N keys from the assumptions document, M from catalogue rows of NL ..."), not from the model's note;
  or refuse a note that says "every value" when rows of another source are in the list.
- data: move the SDE++ period row to `economics.revenue.subsidy.duration` (or mark it "not an
  analysis period" so the rule never recommends it for `analysis_period`); re-upload.
- geomind `prompts/case/lead.md`: when an assumptions document covers the case, name every key it
  gives in `values` so the tool's country rule does not replace them silently; when the user moves
  the site, say in the question which keys follow the new country.

## Speed and accuracy

Accuracy: 8 of ~50 economics values differ from the reference economics, 1 of them (analysis period)
on a wrong basis. Run 7 min 20 s, 0.036 USD.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
