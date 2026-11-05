# QA-223: Results row 'simulation best_v1' is the analysis lead's what-if simulate (d0 flow 50 m3/h, LCTS 64.4) instead of the chosen design (300 m3/h, LCTS 49.7): the last-simulate recorder takes a simulate with changes

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | backend |
| Reporter | QA-E2E-design-I |
| Found | 2026-11-05 17:33 UTC |
| Versions | frontend 1.1.113, backend 1.1.104 when the run ended (1.1.107 at 17:40), geomind 0.4.97, gemini 0.6.16 |
| Where | project QA-TEST QA-E2E-design-I 1 (f1704a61-f1b8-4b63-84d3-20bd30beaed7); run 76d19df6-485f-46ee-a182-6b03ed70ab33 (ended 17:31:10 UTC); result a6a3aec3-0ac8-48a0-b0f1-c5bc00d1b208 'simulation best_v1' |
| Fixer | hotfix-back-lead |

## Steps

1. Chat asks for a plant design; the design lead optimises to `design/best_v1` (1 doublet, 300 m3/h) and simulates it (`result/b8bc0df839230959`, LCTS 49.695 EUR/MWh).
2. After the design, the analysis lead runs two what-if simulates: `simulate {"design": "design/best_v1", "changes": {"d0": {"nominal_flow": 150 m3/h}}}` (17:21:38) and the same with 50 m3/h (17:21:57).
3. The run ends; open Results.

## Expected

The Results row added at the end of the run is the design the answer recommends (`design/best_v1` as stored: 300 m3/h, LCTS 49.695, capex 24.633 MEUR, gas 30,199 MWh).

## Actual

The row `simulation best_v1` (created 17:31:10) holds the 50 m3/h what-if:

| KPI | Row 'simulation best_v1' | Chosen design (the chat answer) |
|---|---|---|
| LCTS | 64.395 EUR/MWh | 49.695 |
| LCOH | 62.569 EUR/MWh | 48.286 |
| CO2 | 25.81 kt | 17.18 |
| Gas bought | 112,911 MWh | 30,199 |
| Boiler heat | 103,843 MWh | 35,214 |
| Capex | 24.421 MEUR | 24.633 |
| d0 capacity | 50 m3/h | 300 m3/h |

The name says best_v1, so the user reads the worst trial as the chosen design. The row has `plant_version` null and `doublets` null. The Report and the Results page read this row; a user who adopts it gets the 50 m3/h plant.

## Evidence

- `../evidence/QA-223/result-a6a3aec3.json`: the stored row (kpis, capacities, plant_version null).
- The two what-if calls in the run log (`../evidence/QA-169/run-76d19df6-log-1710.json.gz` is earlier; the calls are at 17:21:38 and 17:21:57 in GET /api/v1/assistant/runs/76d19df6-.../log).

## Cause

`backend/src/api/v1/assistant/runs/adapters/simulated.py:53` `last_simulation` takes the newest successful `simulate` and does not look at the input: a `simulate` with `changes` (a what-if that saves no design) qualifies. `name_of` then names it after the `design` argument, `simulation best_v1` (fact from the code and the stored row).

## Proposed fix

In `last_simulation`, skip a `simulate` whose input has non-empty `changes` (or any override that is not stored as a design); take the newest plain one. Optionally record the run's final design reference (`update_state` final_design / the lead's hand-over) and prefer the simulate of that design. Unit test: events [plain simulate of best_v1, simulate with changes] -> the plain one.

## Fix

hotfix-back-lead, backend 1.1.109 (tag v1.1.109), deployed 2026-11-05 ~17:43 UTC.
`adapters/simulated.py` `last_simulation` skips a `simulate` whose input has `changes`, `start` or
`end` (`is_what_if`); the newest plain simulate becomes the result row. Old rows stay as stored.
- 2026-11-05 17:43 UTC: backend 1.1.109
- 2026-11-05 19:13 UTC: QA-E2E-design-I retest 19:14 UTC: a what-if stored as its own design (hc_flow150) still becomes the Results row; use state.design.reference
- 2026-11-05 19:56 UTC: backend 1.1.109 is_what_if
- 2026-11-05 20:17 UTC: QA-E2E-study-II 2026-11-05 20:20 UTC, backend 1.1.125: Results rows are the studies' designs, no what-if row seen in 8 rows; no what-if simulate was run, so not directly retested
## Retest

Recipe: a run whose analysis lead calls a what-if simulate after the plain simulate of the chosen
design; the new Results row holds the chosen design's KPIs (not the trial's).

Retest (QA-E2E-design-I, 2026-11-05 19:14 UTC, backend 1.1.117): FAILS in a new form. Project QA-TEST QA-E2E-design-I 3 (d555740a-1054-4642-b905-4919d36702a7), run 06fd16f0-8c66-4f76-a2d5-711e24081b85. Chat asked: "... Then also simulate the same design at 150 m3/h per doublet for comparison, but keep the best design as the result." The design lead stored the variant as its own design (`patch_plant` hc_wellfix -> hc_flow150, then a plain `simulate {"design": "design/hc_flow150"}` at 19:06:31) and recorded `/design/reference = design/hc_wellfix` (300 m3/h, the winner). The only Results row added at the run end (19:12:12) is `simulation hc_flow150` (d0 capacity 150 m3/h), plant_version null. Skipping simulates with `changes` is not enough: the recorder should take the simulate of the run's design of record (`state.design.reference`), or the last simulate of that design.
