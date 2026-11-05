# QA-161: Every case run asks the user for site.air.relative_humidity and utilities.gas.heating_value: no Knowledge document gives them or says they are not needed

| Field | Value |
|---|---|
| Status | verified |
| Severity | minor |
| Area | data |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 16:55 UTC |
| Versions | backend 1.1.102 (geomind 0.4.98) |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 1 (23e6faf0-7fa0-450b-860e-16cfe5fdd91b); run f5f86362-4596-4264-b00a-8c26e5adc5f3; case_lead steps 13 and 17 |
| Fixer | hotfix-back-VI |

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

hotfix-back-VI, 2026-11-05 ~17:20 UTC, data only (no code, no deploy). Checked in gemini 0.6.17:
no module reads `site.air.relative_humidity` (a wet cooler uses the atmosphere's wet-bulb
temperature), and no module reads `utilities.gas.heating_value` (burners and the flare call
`fluid.heating_value()`, computed from the composition). Both stay open.

- `inputs/hackathon-2026-assumptions.md`: two "Case values" rows, "Not set, not needed ... Do not
  ask for it", and the rule that such a key is never searched or asked.
- `inputs/handbook-case.md`: §2.4 and §2.5 mark both optional (never ask); §12.4 row "not set, not
  needed: leave open, never search or ask (QA-161)".
- documents 432089b. Global Knowledge: hackathon-2026-assumptions.md efc6f7e1, handbook-case.md
  5f31745a (replaces 7897ad80), both searchable.
- Not done here (geomind, hotfix-python): `prompts/case/lead.md` "ask only for what set_case
  reports missing or plants_need"; the geoscientists' noise (O2, H2S, import/export limits).

## Retest

Recipe: a new QA-TEST project with the three competition files, one chat request to set the case;
the case lead's one confirmation question must not ask for `site.air.relative_humidity` or
`utilities.gas.heating_value`, and no `search_rag` step looks for them.
- 2026-11-05 19:25 UTC: QA-AI-case-I run 9c02d335, geomind 0.4.131
## More evidence (QA-E2E-case-I, 2026-11-05)

- Before the 17:20 UTC Knowledge fix: run a5118d9e (project QA-TEST QA-E2E-case-I 2, 17:09 UTC): the question still asks for both, with
  a false reason: "site.air.relative_humidity ... needed for the outside-air dew point and the cooler
  duty"; "utilities.gas.heating_value ... needed for the fuel input of any boiler or CHP". In gemini
  `site.air.relative_humidity` is read by no module (only `demand.cooling.indoor_relative_humidity` is,
  `gemini/modules/grids/coolinggrid.py:155`). After my answer the same lead says "The knowledge base is
  explicit that site.air.relative_humidity and utilities.gas.heating_value are read by no module",
  so it read the Knowledge only after asking. Run cf319cd4 (project 1) asked for the humidity too.
- 2026-11-05 19:30 UTC, QA-AI-case-I, run 9c02d335-d9e5-48a8-a687-1c244aeeaee4 (project QA-TEST QA-AI-case-I 12, geomind 0.4.131, backend 1.1.120; log `../evidence/QA-326/run-9c02d335.json`): the confirmation question asks for neither the outside relative humidity nor the grid gas heating value (only the indoor relative humidity 0.5 from the assumptions document); same in run f4018b98, which says 'Not set, deliberately: ... utilities.gas.heating_value (gemini computes it from the composition)'. Verified.
