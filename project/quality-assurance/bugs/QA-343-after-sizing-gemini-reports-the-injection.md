# QA-343: After sizing, gemini reports the injection pump's values one at a time (frequency, then the cooler loop first guess, then efficiency): 3 patch cards in 2 min for family B in run 86867082, although all three are known up front

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | gemini,geomind |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 20:07 UTC |
| Versions | backend 1.1.125+ (geomind 0.4.132, gemini 0.6.33) |
| Where | run 86867082-66b2-4cb1-9c34-bdfc479f278c, project e7dd5fb1-4fb5-477e-969a-9378a3ba803f, design_lead family B, 21:05-21:07 CET |
| Fixer | |

## Steps

Family B (heat pump + boiler + compression chiller) is sized; the design lead runs it and patches what gemini reports.

## Expected

One message from gemini naming every value the sized plant still needs (QA-175 does this for build/patch), so the lead patches once.

## Actual

Three patch cards in a row, each for what the previous answer named:
1. request-1965: `injection_pump.frequency` 50 Hz ("gemini's invalid_binding asks for a value or default of injection_pump.frequency").
2. request-2070: `compression_cooler.loop_pressure` 3 bar and `flow` 400 kg/s ("gemini's invalid_design asks for the closed condenser loop's first guess").
3. request-2107: `injection_pump.efficiency` 0.7 ("gemini reports injection_pump.efficiency missing after sizing").
The values are in the assumptions document and the case, known before sizing.

## Cause

Guess: the run/simulate path after sizing raises the first binding or design error only (invalid_binding, invalid_design, missing_value come from different stages); QA-175 collected missing values for build/patch but not for these run-time checks. Also the injection pump's frequency and efficiency could be filled by size (fixed-speed pump, case pump efficiency).

## Fix

## Retest
