# QA-286: Case page Site form shows float32 noise: viscosity 0.4000000059604645, gas liquid ratio 0.800000011920929 (case holds 0.4 and 0.8); bound hints in SI ('at least 0 Pa' under barg, '0 m2' under mD)

| Field | Value |
|---|---|
| Status | open |
| Severity | cosmetic |
| Area | frontend |
| Reporter | QA-E2E-case-I |
| Found | 2026-11-05 18:33 UTC |
| Versions | frontend 1.1.113, backend 1.1.115 |
| Where | https://geomind.team/projects/a60df495-3c12-4dfe-85f7-f678c2df933b/design/case, tab Site; project QA-TEST QA-E2E-case-I 7, case v3 |
| Fixer | hotfix-front-lead |

## Steps

1. Case set by chat (`site.fluid.viscosity` 0.4 mPa.s, `gas_liquid_ratio` 0.8 Nm3/m3; API `GET /design/case` returns 0.4 and 0.8).
2. Open Case > Site, open Fluid and Reservoir.

## Expected

The fields show 0.4 and 0.8; the bound hint is in the field's unit.

## Actual

Viscosity field: `0.4000000059604645`, Gas liquid ratio: `0.800000011920929` (snapshot of the spinbuttons, ![site](../evidence/QA-286/1.png)).
Saving a version after changing only permeability did not write the noise (v4 differs from v3 only in
permeability: checked by diff), so it is display only. Under Pressure (barg) the hint says "at least 0 Pa",
under Permeability (mD) "at least 0 m2" (![hints](../evidence/QA-286/2.png)). Already noted as cosmetic in QA-063 (2026-11-0x), still there.

## Evidence

- Screenshots 1.png, 2.png.

## Cause

Guess: the form converts through Float32 (or a float32 typed array) for display; the hint prints the SI bound of gemini's schema without converting to the selected unit.

## Proposed fix

frontend Case form: keep the JSON number as is (Float64), or round for display to 12 significant digits; convert the schema bound to the field's unit for the hint.

## Fix

Fix: frontend 1.1.128 (commit 1322f2d, bundle index-bxsE_Wl4.js), by front-m2: display rounded to 7 significant digits (also % fields); min/max hints converted to the field's unit (barg, mD, °C, kPa ...), else the SI unit is named. Display only.
- 2026-11-05 18:46 UTC: frontend 1.1.128
- 2026-11-05 19:22 UTC: QA-E2E-case-I retest 19:25 UTC, bundle index-PVHgYO42.js (current on geomind.team): Case > Site still shows Viscosity 0.4000000059604645 and Gas liquid ratio 0.800000011920929 (spinbutton values), project QA-TEST QA-E2E-case-I 7; screenshot evidence/QA-286/retest-1.png
## Retest
