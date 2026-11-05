# QA-154: Economics skill's own sensitivity recipe fails on the reference case: set_case uniform uncertainty on discount_rate is refused because the case's normal 'std' stays (merge patch)

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 16:53 UTC |
| Versions | backend 1.1.102/1.1.103 (geomind 0.4.98), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 1` (4ce816b1-4bd1-48a5-8e77-9414c2b86301); chat fa9cfafb-e39e-4ccd-9dfb-d8427f518c43; run c2b815a8-8c54-4bae-b1c1-769351434fe6 |
| Fixer | |

## Steps

1. Reference case with `economics.json` of `gemini/examples/hackathon_2026`: `discount_rate` has
   `uncertainty {kind: normal, std: 0.01, min: 0.02, max: 0.08}`.
2. Ask for an LCTS sensitivity on the discount rate 2 % to 8 % (with electricity and carbon price).

## Expected

The analysis lead follows skill `economics` ("one-at-a-time sensitivity", step 1, which uses exactly
`set_case(economics={"discount_rate": {"uncertainty": {"kind": "uniform", "min": ..., "max": ...}}})`)
and the case takes the user's range.

## Actual

Analysis lead step 2 (16:53:24): `set_case(economics={"discount_rate": {"uncertainty": {"kind":
"uniform", "min": 0.02, "max": 0.08}}})` -> `unknown_name economics.discount_rate.uncertainty.std:
key 'std'; expected one of about, kind, max, min`. The merge patch keeps the old `std`, a uniform
has no `std`, so the recipe the skill teaches fails whenever the case already declares another kind.
The lead gave up on the user's range and kept the case's normal (here harmless, the bounds were equal;
with other bounds the user's range would silently not be used).

## Evidence

- `../evidence/QA-152/run-c2b815a8-log.json` (same run), analysis lead step 2.

## Cause

`geomind/geomind/tools/gemini/case.py` `merge_patch` (RFC 7386) only drops a key sent as `null`;
`skills/economics/SKILL.md` lines 18-24 do not say so, and the error does not suggest `"std": null`.

## Proposed fix

Either (a) in `set_case`, replace an `uncertainty` object whole when the patch changes its `kind`
(an uncertainty is one value, not a set of fields), or (b) skill `economics` and the error suggestion:
"to change the kind, send the old keys as null, e.g. `{"kind": "uniform", "min": .., "max": .., "std": null}`".
(a) is safer.
