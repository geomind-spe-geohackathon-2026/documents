# QA-243: Economics written without the one economics question: ask_economics refused twice (unit EUR/W/K, invented row id), the lead then puts the whole economics into a set_case card (cut JSON)

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-case-I |
| Found | 2026-11-05 17:44 UTC |
| Versions | frontend 1.1.113, backend 1.1.105-1.1.107 (geomind 0.4.100+) |
| Where | project QA-TEST QA-E2E-case-I 4 (290484c7); runs 679f3555 (case_lead 18-19) and ff712a26 (case_lead 6-8) |
| Fixer | |

## Steps

1. Project 4: PDF + 2 CSVs, case request; approve all on the case question (17:31 UTC).
2. (QA-230 blocks set_case; a new request "Write the case now" from the chip, 17:40.)

## Expected

The case lead asks the ONE economics question (ask_economics, handbook-case 8.5 and 12; the
assumptions document's Economics table) and the user approves it before any economics enter the case.

## Actual

- Run 679f3555 case_lead 18: `ask_economics` refused: `invalid_unit` "capex.heat_exchanger: unit 'EUR/W/K';
  expected EUR/(W/K), EUR/W, ...". Step 19: refused again: `unknown_name` "row = 'analysis-period-dea-25yr' is
  not in knowledge/data-economics.csv" (an invented row id; the assumptions doc value 25 yr needs no row).
  The lead then gives up asking: no economics question is ever shown in this project.
- Run ff712a26 case_lead 6 and 8: `set_case` with `economics: {kind: economics, ... opex, capex, energy ...}`
  beside the case; the approval card summary names only case keys and the JSON is cut at 1500 chars
  (QA-196), so the economics are not visible on the card. Approve -> `economics.json` stored (case v2).
- Final answer: "Economics — the full cost catalogue from the assumptions document ..." as if confirmed.
- Speed: 2 refused ask_economics round trips (~25 s, ~150 k input tokens).

## Evidence

- `../evidence/QA-243/run4-679f3555.json.gz`, `run4-ff712a26.json.gz`, `case-project4-v2.json`.
- Projects 1 and 2 (same input, geomind 0.4.97-0.4.99) did show the economics question (approve all).

## Cause

Facts: ask_economics refuses 'EUR/W/K' though it is the same unit as EUR/(W/K); a value from the
assumptions document is sent with a `row` id that does not exist. Guess: after two refusals the lead
treats the case question's "approve all" as approval of the economics too.

## Proposed fix

geomind ask_economics: accept `EUR/W/K` (and other slash forms gemini's units accept) and ignore/omit
`row` for a value whose source is a Knowledge document, not a catalogue row. Case lead prompt: never write
economics with set_case unless the user answered the economics question; if ask_economics fails, fix and
ask again. set_case call summary (engine/session.py call_summary) already lists economics.* leaves only
when they are under `economics` as a dict of leaves: check it names them on the card.

## Fix

## Retest
