# QA-322: Report and results: 'Cop' 18.86 is heat delivered / electricity bought (geothermal and boiler heat included), not a COP; and the cooling Days covered calls the only (electric) chiller 'backup' on 219 days while the text says 'gemini has no cooling backup'

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | backend,gemini,frontend |
| Reporter | Sahand (reviewer notes), Manual QA-IV |
| Found | 2026-11-05 19:21 UTC |
| Versions | backend 1.1.118 (geomind 0.4.130, gemini 0.6.26) |
| Where | project 0b986dd6-8f95-4383-9d15-5e589ff122c9, result 54b2e4f4-a6a5-4475-9fad-57d93112d504 (B_r1_best); report export of that result |
| Fixer | hotfix-python-lead-II |

## Steps

Open the report (or Results) of B_r1_best: one compression chiller (electric) is the only cooling unit; heat from doublet + exchanger + 2 MW heat pump + gas boiler.

## Expected

- A COP figure that is a COP: per machine (heat pump: heat out / its electricity; chiller: cold / its electricity), or named 'heat delivered per MWh of electricity bought' if it is a plant ratio.
- Days covered, cooling: one consistent rule. Either the electric chiller is the plant (then 219 cooling days are 'plant', and the 146 days without cooling demand are not counted as 'plant'), or it is backup (then the note 'gemini has no cooling backup' is wrong).

## Actual

- 'Cop 18.86' = 111.7 GWh heat / 5.921 GWh electricity: the ratio of all heat (63 % geothermal, 36 % boiler) to the electricity bought. It reads as an impossible heat pump COP (a reviewer flagged it at once).
- Cooling: 'Geothermal or plant 146, Backup 219, Short 0' and the chart all orange, with the text 'On cooling days the whole supply is the plant: gemini has no cooling backup'. The 146 'plant' days are the days with no cooling demand; all 219 days with demand are 'backup' (since the QA-238 fix the electric chiller's cold counts as backup).

## Evidence

- `../evidence/QA-322/report-b-r1-best.pdf` pages 2-3 (Sahand's reviewer).

## Fix

## Retest
