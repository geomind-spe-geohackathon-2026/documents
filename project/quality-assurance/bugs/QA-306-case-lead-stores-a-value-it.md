# QA-306: Case lead stores a value it computed itself: site.air.pressure 101204.92615896827 Pa from an ISA formula, although the approved question said 'elevation 10 m, gemini derives the ISA pressure' (handbook-case 8.6: no computed values)

| Field | Value |
|---|---|
| Status | wont-fix |
| Severity | minor |
| Area | geomind |
| Reporter | QA-E2E-case-I |
| Found | 2026-11-05 18:57 UTC |
| Versions | backend 1.1.116-1.1.118 |
| Where | project QA-TEST QA-E2E-case-I 6 (80139e85), run 3bb1de01, case v2 |
| Fixer | |

## Steps

1. New project, no files: "I want a geothermal plant that heats and cools a new district. What do you need?"
   then "Trondheim ... For everything else, use your own reasonable assumptions."
2. Question 2 of 3 lists "site.air.pressure = elevation 10 m | gemini derives the ISA pressure from it". Approve all.

## Expected

The case holds what was approved (the elevation, for gemini to derive the pressure), or the value as a
source states it; never a number the agent computed (handbook-case 8.6 "No computed values").

## Actual

`site.air.pressure = {"unit": "Pa", "value": 101204.92615896827}` with
`site.air.about.pressure: "ISA (ISO 2533:1975) at the site's elevation 10 m: p = 101325*(1-2.25577e-5*h)^5.25588 Pa"`
(`../evidence/QA-306/case-project6-v2.json`). The approval card (18:39 UTC) showed
"changes.site.air.pressure.elevation: 10 m", so the stored value differs from the approved card.

## Evidence

- Case v2 JSON; run log of 3bb1de01 (set_case after the approval).

## Cause

Guess: set_case or the lead turns {elevation} into a pressure; if gemini does it in set_case, the case
should keep the elevation form; if the lead does it, it breaks 8.6.

## Proposed fix

geomind/gemini: store `site.air.pressure` as `{elevation: 10, unit: m}` (if gemini's schema takes that form, as the card
implies) and let gemini derive at run time; prompt: never write a formula result.

## Fix

- 2026-11-05 20:08 CET, hotfix-python member-5: by design, no code change. The value is no number
  the agent computed: geomind's `set_case` (`geomind/tools/gemini/air.py`, `pressure_from_elevation`)
  takes `site.air.pressure` as `{"elevation": {value, unit}}` and sets the ISA pressure in Pa at
  that elevation (ISO 2533:1975), with its source in `site.air.about.pressure` and an entry in
  `converted`. gemini's case schema has no elevation form, and a case without `site.air.pressure`
  is `missing_value`, so the case keeps the pressure, not the elevation. The approved input (the
  elevation 10 m) is what the card showed; the stored Pa value is its documented conversion.
- What was wrong is the question's wording, "gemini derives the ISA pressure": it is `set_case`.
  The case lead's prompt now says "set_case sets the ISA pressure from it (ISO 2533); the user
  confirms the elevation, never the ISA pressure" (geomind commit 76a46bd).
- Status: wont-fix (by design); the wording fix is in 76a46bd. Keeping the elevation in the case
  would need gemini to take an elevation form: a gemini request, only with Sahand's permission.
- 2026-11-05 19:09 UTC: by design: set_case converts the approved elevation to ISA pressure (ISO 2533); wording fixed in geomind 76a46bd
## Retest
