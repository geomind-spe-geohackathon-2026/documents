# QA-361: Case lead's second economics card drops the 42 approved values from the assumptions document ('a source with no value') after the %/yr unit fix; approve all would leave every capex, price and discount rate open (run 807ac8c3)

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 21:46 UTC |
| Versions | backend 1.1.134 (geomind 0.4.138), gemini 0.6.35 |
| Where | https://geomind.team/projects/6314fe82-909f-4f26-b952-fcac92baf50b; chat 6880e841-6d8d-4acd-9f65-ce00d1ae4bf6; run 807ac8c3-15ad-4d6a-9534-cd90fc8e6dd6; case_lead, requests 367 and 390 |
| Fixer | m4 |

## Steps

1. Report run on the three competition files, manual cards (no auto-approve).
2. case_lead economics card request-367: 42 values from knowledge/hackathon-2026-assumptions.md sec. 5.1-5.3 plus 7 catalogue rows. Answered "approve all".
3. The lead asks again (request-390): "Same values as approved, with the annual-rate unit the case requires on the fixed operating costs (the document prints them as %/yr)".

## Expected

The second card carries the same 42 values, with only the fixed opex unit changed (0.01 -> 1 %/yr ...).

## Actual

The second card lists only the 7 catalogue rows under "Values". All 42 document values (discount rate, period, prices, carbon, revenue, every capex and fixed opex) are listed under "Left open, no source the rules accept gives them: a source with no value". "approve all" would save a case with no costs, so no plant can be costed. I answered "change some" with the values written out.

## Evidence

- Card JSON: `../evidence/QA-361/request-390.json`
- Third card after my 'change some' with the values: `../evidence/QA-361/request-415.json`. It keeps only the 15 fixed-opex lines (with %/yr); the other 27 are again 'a source with no value'. The case still has no economics (case version 1, economics null).

## Cause

Guess: the lead re-submits the values with a source but without the value field (or the value-source pairing is lost when the unit is rewritten), so the tool's source rules treat each as 'a source with no value'.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
