# QA-082: simulate refuses a free-plant doublet with 'd0.gradient: no value ... empty takes it from the case' (30 errors): case values are not taken over, patch_plant refuses them as case values

| Field | Value |
|---|---|
| Status | fixed |
| Severity | blocker |
| Area | gemini |
| Reporter | functional-qa-I |
| Found | 2026-11-05 06:05 UTC |
| Versions | backend 1.1.73, gemini 0.6.8, geomind 0.4.67+ (health 2026-11-05 06:05 UTC) |
| Where | project 61134432, chat cb8b9b2d-edce-4f69-9dfb-6b015a821601, run c4f00b5c-167e-4458-a8ab-bfe8aaed13fe, run JSON steps 11, 20, 34, 45, 49, 54, 64, 76, 81, 95 |
| Fixer | hotfix-python |

## Steps

1. Case from the PDF (QA-080 fix live, flow range now accepted).
2. Build a free plant with doublet d0 and size it, then call simulate on it.

## Expected

simulate fills d0.gradient, surface_temperature, permeability, thickness, reservoir.* from the case (the message itself says 'empty takes it from the case') and runs the year.

## Actual

36 simulate calls, 30 missing_value: 'd0.gradient: no value [K/m]: Increase of undisturbed rock temperature with depth; empty takes it from the case; d0.surface_temperature: no value [K] ...; d0.permeability ...; d0.thickness ...'. patch_plant refuses the same paths ('gradient is not a design value of the plant; give it in the case, at site.ground.gradient'). simulate(changes={'d0': {...}}) accepts the leaves (design lead's workaround), then asks for d0.reservoir.pressure/temperature, d0.esp.head_coefficients/stage_count/motor_efficiency/..., params.control.dispatch ('least_cost' only), and unknown_name for d0.gradient in some forms. So the design lead spent about 60+ steps and one 30-step extension to simulate once; judging points 2, 4 and 6 (simulate, compare, capacities) still not reached after ~35 min on 1.1.73. Case values (site.ground.gradient 30, surface temp 12, permeability 200 mD, thickness 100 m, reservoir pressure 250 bar(g)) exist in the case.
## Evidence

- ![screenshot](../evidence/QA-082/1.png)
- Run JSON: `../evidence/QA-082/run-<id>.json`

## Update 2026-11-05 ~06:40 UTC, backend 1.1.75 / gemini 0.6.10 (functional-qa-I)

Retried in chat cb8b9b2d (new message, same project; run 004bb7f9, 114 s, done). The design lead again ends without a simulation. In its own words (full text: evidence/QA-082/final-chat-0640.txt, screenshot final-chat-0640.png): 'the simulator reports [gradient 30 C/km, surface temperature 12 C, permeability 200 mD, thickness 100 m] as missing. The only route that accepts them is passing them in the simulation call - and the moment the pump's six operating values are supplied alongside, GEMINI demands a pump stage count and head/power curve coefficients that no project file ... provides ... If instead the plant is left for the case to fill, the reservoir and sink sub-values are not filled from the case, and GEMINI's own two checks contradict each other: the plant reader reports zero issues while the simulator demands values.' So the plain d0.gradient error still reproduced for the agent in the prod worker at about 06:35 UTC (design names: design/A_sized, a_start_2, b_nogas; I could not export the run JSON, the download did not land). Full text per call is in the earlier run JSON c4f00b5c. Good: the final answer is plain and honest (what, why, what the user can decide).

## Cause

Guess: the case fallback ('empty takes it from the case') works only when the doublet sub-objects are absent, not for a doublet with explicit sub-blocks; the agent builds the doublet with sub-blocks and then cannot clear them.

## Fix

Findings (hotfix-python-II): the 30 failing simulate calls were all after 05:30 (gemini 0.6.8). In a fresh process, inside the prod worker, `gm.simulate` of the run's `design/A_sized` on the chat's own case and files now succeeds; `d0` is a `Doublet`, `apply_case` sets its ground and reservoir values, and its `depth` (2500 m) is given. So the plain `d0.gradient: no value` failure did not reproduce, and its cause is not found; copying the chat's files out of prod for a local run was refused by the permission check. Fixed what the run showed: (1) gemini 0.6.9 (2b771f5f): `gm.check` names a doublet without a depth first, saying the case's reservoir temperature and pressure reach it only with it (the plain issue of the same path is not repeated); (2) geomind 0.4.70: `simulate`'s `changes` set the plant's own options (`{"control": {"dispatch": ...}}`, `{"backup": {"value": ...}}`), which the agent tried 8 times and got `unknown module path 'control'`, so runs stopped on `dispatch is missing`. The ESP curves (stage_count, head/power coefficients) are design inputs of the well engineer with no default; with QA-076's ownership fix the well engineer can write them. backend 1.1.75 (6dfb1c7), deployed 2026-11-05 06:30 UTC. Retest: simulate a design in a new chat; if `d0.gradient: no value` comes back, note the design and time.
- 2026-11-05 07:02 UTC: root cause: geomind run_summary read ESP curves on the unapplied plant; fixed in geomind 0.4.72 (8abe06d), backend 1.1.76 (4822fb4), deployed 07:00 UTC
Root cause (2026-11-05 ~06:40 UTC, hotfix-python-II), reproduced in the prod worker through geomind's own `run_plant` with chat cb8b9b2d's stored designs, case files and state: `gm.simulate` of design/A_sized RUNS (365 steps); then `run_summary` -> `with_curve` -> `curve_ranges` read the ESP's curves on the plant WITHOUT the case applied, and reading an unset parameter raises gemini's whole-plant `uninitialized parameters` error, which lists d0.gradient, surface_temperature, permeability and thickness (the values the case fills). So every simulate with an ESP failure group was reported as those values missing although it had run. Fix: geomind 0.4.72 (commit 8abe06d, tag v0.4.72): the summary gives that failure group without the curve. Checked with the fix patched in the prod worker: the run's real failures come back (d0.esp out_of_range, the derived one-stage ESP at about 301 m3/h against the hand-written maximum_flow 300 m3/h; negative outlet pressure of cooling_return_pipe and cooling_supply_pipe; heating supply 358.6 K under 373.15 K). backend 1.1.76 (4822fb4), deployed 2026-11-05 07:00 UTC.

## Retest

(Who, when, result.)
