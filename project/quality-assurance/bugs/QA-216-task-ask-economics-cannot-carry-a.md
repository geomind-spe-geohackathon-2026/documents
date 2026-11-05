# QA-216: Task: ask_economics cannot carry a value's uncertainty, so the assumptions file's economics ranges (discount rate, electricity, gas, carbon) never reach the case and later studies must ask again (QA-191 part 3)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | handbook-econ-report-I |
| Found | 2026-11-05 17:30 UTC |
| Versions | geomind main 802aa38 |
| Where | geomind/geomind/tools/gemini/economics.py (`ask_economics` values) |
| Fixer | hotfix-python-lead |

## Steps

1. A case whose economics come from `knowledge/hackathon-2026-assumptions.md` ("Uncertainty ranges": four economics keys with an `uncertainty` in JSON).
2. Approve all in the one `ask_economics` question; then ask for an uncertainty study.

## Expected

The stored economics carry each value's `uncertainty` as gemini's sample `economics.json` has it
(discount_rate normal std 0.01, 0.02-0.08; electricity uniform 80-140; gas triangular 25-70;
carbon triangular 30-110), so `sample_uncertainty` and `sensitivity` run without a new question.

## Actual

`ask_economics` values are `{key, value, unit, source}`: there is no place for `uncertainty`, so
the ranges are dropped (QA-191 Actual, run bf3990c4 and 2d5ced06).

## Evidence

- `../evidence/QA-191/economics-project1.json` (no `uncertainty` on the four keys).

## Cause

Fact: the value schema of `ask_economics` (tools/gemini/economics.py) has no `uncertainty` field.

Proposal: accept an optional `uncertainty` object per value (gemini's form: `{kind: uniform|triangular|normal, min, max, std?}`), show it on the card as one line ("range: triangular 25-70 EUR/MWh"), and set it with the value on approve all. The case lead passes the assumptions file's JSON unchanged.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 18:09 UTC: deployed 19:01-19:03 CET: backend 1.1.112, geomind 0.4.118/0.4.119, gemini 0.6.19 (hotfix-python team)
- 2026-11-05 18:28 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
## Retest

(Who, when, result.)

- 2026-11-05 18:08 UTC, QA-E2E-economics-I (observation, status left to the fixer): in project
  "QA-TEST QA-E2E-economics-I 6" (run 74ef2d84) the stored economics carry the reference
  uncertainty on discount_rate, energy.electricity, energy.gas and carbon.price
  (`../evidence/QA-186/economics-retest-project6.json`).
