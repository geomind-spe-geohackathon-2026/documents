# QA-161: Every case run asks the user for site.air.relative_humidity and utilities.gas.heating_value: no Knowledge document gives them or says they are not needed

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | data |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 16:55 UTC |
| Versions | backend 1.1.102 (geomind 0.4.98) |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 1 (23e6faf0-7fa0-450b-860e-16cfe5fdd91b); run f5f86362-4596-4264-b00a-8c26e5adc5f3; case_lead steps 13 and 17 |
| Fixer | |

## Steps

1. Run 1 of QA-AI-case-I: competition files, one chat request to set the case.
2. Read the case lead's confirmation question (`ask_user`, request-444).

## Expected

For the competition case every value the case needs is in the files or in
`knowledge/hackathon-2026-assumptions.md` ("It holds every value the case and the economics need that
the three competition files ... do not give"). The confirmation question asks only to confirm.
The reference `gemini/examples/hackathon_2026/case.json` sets neither `site.air.relative_humidity`
nor `utilities.gas.heating_value`, and runs.

## Actual

- Geoscientist II and III report both as missing; the case lead searches the Knowledge base for both
  (step 13, `search_rag` x2, 9.8 s LLM, nothing found) and then asks the user, in the ONE question:
  "STILL MISSING - please give me these two, with their units: A. site.air.relative_humidity ...
  B. utilities.gas.heating_value (J/kg or kJ/kg) ... it is needed to price and burn the gas."
- Both are optional in gemini: `gemini/case/utilities.py` `Gas.heating_value` is an optional field,
  and the grid gas composition is set (gemini computes a lower heating value from a composition,
  `gemini/streams/fluid.py` `heating_value()`). The reason given to the user ("needed to price and
  burn the gas") is not true for this case.
- Geoscientist III also lists `utilities.gas.composition.O2`, `.H2S`, `utilities.electricity.import_limit`
  and `export_limit` as missing (not asked, but noise in the findings).
- Every real user of the competition case gets this extra question; a user who types values
  changes the case away from the reference.

## Evidence

- `../evidence/QA-161/question-and-findings.json` (the question and the geoscientists' missing items)
- Full run log: `../evidence/QA-153/run-f5f86362.json`

## Cause

`knowledge/hackathon-2026-assumptions.md` gives the indoor humidity but not the outside one, and
says nothing about the grid gas heating value; `describe_case` does not say that
`utilities.gas.heating_value` is optional or follows from the composition, so the lead treats it as
needed.

## Proposed fix

- data (Knowledge), `knowledge/hackathon-2026-assumptions.md` (source in
  `documents/project/quality-assurance/inputs/`): add to "Case values" a line "Outside air relative
  humidity: not set (the reference case leaves it open; only an air cooler or cooling tower needs it)"
  or a Team value with its reason; and "Grid gas heating value: not set; gemini computes it from the
  composition". Re-upload to global Knowledge.
- geomind `prompts/case/lead.md`: ask the user only for a value `set_case` reports as missing or in
  `plants_need`, never for an optional key nobody gives; list optional open keys in `about.open`.
- gemini (ask Sahand first): `describe_case("utilities.gas")` could say "optional; from the
  composition when not given".

## Speed and accuracy

Speed: one extra search step (about 10 s) and a longer question. Accuracy: with approve all the case
matches the reference; with typed values it does not.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
