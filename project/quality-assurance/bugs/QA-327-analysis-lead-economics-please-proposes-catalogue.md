# QA-327: Analysis lead ('economics please') proposes catalogue rows (EU discount 4 %, NL electricity 115 EUR/MWh, heat cost share 0.87) and never reads the case's own assumptions file

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 19:27 UTC |
| Versions | backend 1.1.122 |
| Where | project "QA-TEST QA-E2E-economics-I 12"; run 72d93b9f-b095-47e4-966f-2b81fb739b2e; analysis_lead steps 3-7 |
| Fixer | hotfix-python-lead-II |

## Steps

1. Reference (competition) case, no economics, no site country.
2. Chat: "economics please". The coordinator routes it to the ANALYSIS lead (a "Set up the
   economics" request goes to the case lead).
3. Read the economics question.

## Expected

The same economics as the case lead gives for this case: the values of
`knowledge/hackathon-2026-assumptions.md` (written for this case; equal to the reference
`economics.json`), catalogue rows only for keys it lacks.

## Actual

The analysis lead reads only `handbook-economics.md` sections 0, 5, 6.4, 2.2 (steps 3-6) and asks
with catalogue rows: discount_rate 0.04 (`discount-rate-financial-eu`), energy.electricity
115.015 EUR/MWh (`electricity-nl-eurostat-price-2024-band-ie`, prices of the Netherlands),
heat_cost_share 0.87 (Fiaschi), and so on; the card's own summary: "45 from catalogue rows,
general; 4 from catalogue rows of the Netherlands; ... 1 from catalogue rows of Denmark". Approve
all stored them (discount 0.04, electricity 115.015). The same request in project 8 an hour earlier
(run 658ca8f2) did use the assumptions file, so the behaviour depends on the run.

The change-some path itself now works (QA-298 verified on this run).

## Evidence

- Card: `../evidence/QA-327/card.txt`
- Run JSON: `../evidence/QA-327/run-72d93b9f.json.gz`

## Cause

Guess: the analysis lead's economics skill has no "the case's own assumptions document comes
first" rule (the case lead's has it); `ask_economics` gets only catalogue rows from it. Related to
QA-320 (case lead with "don't ask me").

## Proposed fix

geomind: one shared economics recipe for every agent that calls `ask_economics` (case lead,
analysis lead): first search the knowledge base for a document written for this case
(`hackathon-2026-assumptions.md` here) and take its values; catalogue rows only for missing keys,
of the site's region. Or route "economics please" to the case lead like "set up the economics".

## Fix

- 2026-11-05 19:34 UTC: geomind main 0df5771, gemini dev e6284347 (0.6.31); pending deploy
## Retest
