# QA-304: Approved site.air.pressure (101325 Pa) left out of the stored case; the summary says 'no module needs it' but gemini's Atmosphere module raises missing_value without it

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-case-I |
| Found | 2026-11-05 18:55 UTC |
| Versions | backend 1.1.116+ (geomind 0.4.12x, gemini 0.6.2x) |
| Where | project QA-TEST QA-E2E-case-I 9 (dbe6165f), run 08d3739c, case v2 |
| Fixer | hotfix-python-lead-II |

## Steps

1. PDF + 2 CSVs, site Delft, real outside air (connector). The confirmation question (18:44:35 UTC) item 12:
   "site.air.pressure = 101325 Pa | knowledge/hackathon-2026-assumptions.md, 'Case values' | constant; the projection gives no pressure". Approve all.
2. Read the stored case.

## Expected

`site.air.pressure` 101325 Pa in the case, as approved (the reference case.json has it too).

## Actual

`site.air` = {temperature: file, relative_humidity: file}; **no pressure** (`../evidence/QA-304/case-project9-v2.json`).
The final answer: "Deliberately left open — ... site.air.pressure (no module needs it)". gemini
`gemini/modules/environment/atmosphere.py:25,113`: the Atmosphere module takes `site.air.pressure` from the
case; "a run without it raises missing_value". A design with a cooler / air-side module will fail later on the
design stage, and the user's approved value is silently gone.

## Evidence

- Case v2 JSON; run log in `../evidence/QA-301/run-08d3739c-log.json.gz` (the set_case calls after the 20 refusals
  drop the pressure leaf).

## Cause

Guess: during the QA-301 retry loop the lead rebuilt the changes and dropped the leaf; then it justified the
gap with the QA-161 rule ("not needed: leave open") applied to the wrong key (QA-161 is about
`site.air.relative_humidity` and `utilities.gas.heating_value` only).

## Proposed fix

geomind case lead final checklist (handbook-case 11.2): every approved value is in the stored case (diff the
question's lines against read_case); the "not needed" list is exactly the keys the Knowledge names. Knowledge:
handbook-case 12.4 marks site.air.pressure as needed (Atmosphere).

## Fix

- 2026-11-05 19:12 UTC: geomind main 71d80ab (0.4.131+), gemini dev 5782a138 (0.6.27); QA-312 also needs back-lead's DatabaseWorkspace.save_plant_version
## Retest
