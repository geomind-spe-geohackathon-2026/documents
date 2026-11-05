# QA-353: comparison_driver asks for family_design_lead again and again after the user denies it (request-2858, 2865, 2996, same task, reasons ignored); the run never reaches a comparison

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 20:44 UTC |
| Versions | backend 1.1.130 (geomind 0.4.135, gemini 0.6.34) |
| Where | run 86867082-66b2-4cb1-9c34-bdfc479f278c, project e7dd5fb1-4fb5-477e-969a-9378a3ba803f, 21:40-21:44 CET |
| Fixer | m3 |

## Steps

1. Design stage: the comparison driver ran family_design_lead three times (approved, 20:55 CET); family A finished (minimize, LCTS 29.03, 10/10 checks), B and C partly.
2. The comparison driver asks again: "Allow family_design_lead (write)?" with the same task text.
3. Deny with a reason: "No new family run ... Compare the families you have now ... and answer."

## Expected

The driver takes the denial and its reason, compares the stored results and finishes.

## Actual

It asks again with the same call: request-2858 (denied 21:40), request-2865 (denied 21:42 with "do not call family_design_lead any more"), request-2996 (21:44). The reasons are ignored; the run made no comparison after 70 min and 0.34 USD and was cancelled by QA.

## Cause

Guess: the comparison driver is a deterministic driver (0 tokens in the agents list) that re-issues family_design_lead while some family has no verified result, and it does not read the denial reason; QA-143's failed_before does not cover denied calls.

## Fix

- 2026-11-05 20:47 UTC: geomind 8361717: a denied family run is never asked again; the driver compares what has results with the user's words; pending deploy
## Retest
