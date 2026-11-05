# QA-192: Economics approve all sets catalogue proxy rows with a known unit mismatch (circulation pump EUR/W heat as EUR/W shaft, ice storage EUR/MWh cold) for kinds the plant may never have

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 16:52 UTC |
| Versions | backend 1.1.102 (geomind 0.4.10x) |
| Where | project "QA-TEST QA-E2E-economics-I 1", run bf3990c4, case lead step 7 (`ask_economics`); same in project 2, run 2d5ced06, step 5 |
| Fixer | hotfix-python-lead |

## Steps

1. Reference case, no economics, no plant. Chat: set up the economics.
2. Read the economics question card.

## Expected

Keys the case's source (the assumptions file) does not give, for equipment that no plant has yet,
stay open, or are offered only when their unit fits the key. A value whose unit does not fit is
not put under "approve all".

## Actual

The card puts these under "approve all", with the tool's own warning:

- `economics.capex.circulation_pump = 0.09 EUR/W` (row circulation-pump-proxy-dea-2017-over-1mw):
  "the row's unit is EUR/W heat; set as EUR/W, which the key reads per W of shaft power ... the
  row is heat, not shaft power: not converted, the user decides". A pump's shaft power is about
  1-2 % of the heat it moves, so this cost is wrong by a factor of 50-100 if a design uses a
  circulation pump.
- `economics.capex.ice_storage = 23249.8663132687 EUR/MWh` "the row's unit is EUR/MWh cold; set
  as EUR/MWh, which the key reads per J of energy capacity" (and 15 significant digits, cf.
  QA-099).
- `economics.opex.fixed.electric_boiler = 1070 EUR/MW/yr`, thermal_storage, ice_storage opex.
- The intro also says opex.per_energy is "open because the case has cooling", a reason a user
  cannot follow.

A user who presses approve all (the default) stores these. The reference `economics.json` has
none of these keys. In project 1 I removed them by hand ("our plant has none of them").

## Evidence

- Question card text: `../evidence/QA-192/card-run1.txt` (lines with circulation_pump,
  ice_storage, electric_boiler, thermal_storage)

## Cause

`ask_economics` (`geomind/tools/gemini/economics.py`, `recommended` / `catalogue_basis`) fills
every key the case lead leaves out with the catalogue's recommended row, even when
`fitted_units` finds a basis mismatch it only notes.

## Proposed fix

geomind `economics.py`: a row whose unit basis does not match the key (heat vs shaft, cold energy
vs J capacity) goes to "Open" with the note, never into approve all; and when there is no plant
yet, ask only the keys the source gives plus those of the kinds the case needs, leaving equipment
kinds no source names open until a plant uses them (the plant stage already asks for missing
economics, QA-105). Round shown values to 4 significant digits.

## Fix

- 2026-11-05 18:09 UTC: deployed 19:01-19:03 CET: backend 1.1.112, geomind 0.4.118/0.4.119, gemini 0.6.19 (hotfix-python team)
- 2026-11-05 18:27 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
## Retest
