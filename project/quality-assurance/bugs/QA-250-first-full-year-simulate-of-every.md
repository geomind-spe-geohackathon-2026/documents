# QA-250: First full-year simulate of every agent-built plant fails 365 of 365 steps: d0.esp flow 301.4 m3/h above its 300 m3/h maximum_flow (157-207 steps) and injection_pump 'discharge pressure below suction' (208-365 steps); 3 plants in 2 runs

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | gemini,geomind |
| Reporter | QA-AI-design-I |
| Found | 2026-11-05 17:55 UTC |
| Versions | backend 1.1.102-1.1.109 (geomind 0.4.98-0.4.110, gemini 0.6.16/0.6.17) |
| Where | api.geomind.team; run 0df89b7e-69e0-46b3-abe1-231e51d9570a (project QA-TEST QA-AI-design-I 1) simulate 17:11:53 UTC; run 5d0216a6-4acb-487b-a885-396a5e99366d (project QA-TEST QA-AI-design-I 2) simulate 17:41:05 and 17:47:36 UTC |
| Fixer | hotfix-python-lead |

## Steps

1. Reference case and economics; the design team builds HeatingHeatPumpCoolingPlant (run 1), HeatingAbsorptionCoolingPlant and HeatingHeatPumpCoolingPlant (run 2) from gemini's classes, fills them with `fill_parts`, `size_plant`, then `simulate` the year.

## Expected

The first simulate of a complete, sized plant runs; at most a few steps fail and name a design fix.

## Actual

| Run / plant | failed steps | failures |
|---|---|---|
| 0df89b7e `design/sized` (B) | 365 / 365 | `d0.esp` out_of_range 157x: "flow = 0.08374 m3/s ... expected flow at most 0.08333 m3/s (maximum_flow at this speed)"; `injection_pump` 208x: "head = nan Pa; discharge pressure is below suction pressure" |
| 5d0216a6 `design/C_direct_absorption_sized` (C) | 365 / 365 | `d0.esp` 207x (same 0.08373 > 0.08333); loop at `drive_mixer.fluid_out` no convergence 83x; a stream p = -8.09e18 Pa 75x |
| 5d0216a6 `design/B_heatpump_compression_sized` (B) | 365 / 365 | `injection_pump` 365x: head nan, discharge below suction |

The verdict then says only "no_value: the run gives no value of this field" for every requirement, and check_results gives co2 0, no coverage. In run 1 this cost a repair team round (`fill_parts` 126 s) and two more simulations.

Where the values come from (`../evidence/QA-250/simulate-failures.json`):
- Engineers set `params.d0.esp.maximum_flow` = 300 m3/h and `minimum_flow` = 50 m3/h with source "case:requirements.production_flow_range", `best_efficiency_flow` 200-300 m3/h (assumption), and the lead sets `d0.nominal_flow` = 300 m3/h (the top of the band). The doublet then delivers 301.4 m3/h, 0.5 % above the pump's maximum, on every day it runs at nominal flow. gemini's reference plant uses an open pump window (`maximum_flow` 1 m3/s, `minimum_flow` 0, best 0.04 m3/s) and lets the requirement judge the band.
- Injection pump: engineers give `pump_type unspecified`, `efficiency` 0.7 or 0.75 and `frequency` 50 Hz (assumption), no `pressure_setpoint` and no `nominal_head`; gemini's reference has `pressure_setpoint` 60 bar, `nominal_flow` 600 m3/h, `nominal_head` 15.74 bar, `frequency` 60 Hz.

## Cause

Facts above. Guesses: (1) the case's flow band (a requirement on the doublet) is copied into the ESP's operating window, so a tiny solver overshoot fails the step; (2) gemini's doublet solver does not cap the flow at the pump's `maximum_flow` (QA-130 capped at the pump's nominal flow); (3) without `pressure_setpoint` the injection pump has no discharge target.

## Proposed fix

- geomind `prompts/design/well.md` / `reservoir.md` and handbook-design 4.x (data): never copy a requirement band into the pump window; the ESP window is the pump's (open, as gemini's sample) and the band is judged by the requirement. Injection pump: give `pressure_setpoint` (from the reservoir pressure plus the injectivity drawdown, a gemini evaluation) and `nominal_head`, as the sample.
- geomind `prompts/design/lead.md`: `nominal_flow` strictly inside the band (not the edge), or let `size_plant` choose it.
- gemini (via Sahand): clip the operating flow to `maximum_flow` within a tolerance, or report "nominal_flow equals maximum_flow" at `patch_plant` time; `injection_pump` without a setpoint should be a `missing_value` at build time, not 365 nan steps.

## Fix

- 2026-11-05 18:29 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
- 2026-11-05 19:16 UTC: QA-E2E-design-I retest: first full-year simulate 365/365 failed (m_dot nan), then 330/365 (ESP flow 8.8e6 m3/s) until d0.well/riser segment set; run 06fd16f0
## Retest

Retest (QA-E2E-design-I, 2026-11-05 19:20 UTC, backend 1.1.117): still fails, other messages. Run 06fd16f0 (project QA-TEST QA-E2E-design-I 3, HeatingHeatPumpCoolingPlant, 1 doublet x 300 m3/h): first whole-year `simulate design/hc_ready` (18:57:50) **365 of 365 steps failed**: "Stream: m_dot = nan kg/s; expected a finite mass flow" (path ""); after one more patch `simulate design/hc_fixed` (18:58:24) **330 of 365 failed**: "d0.esp: flow = 8808335.2 m3/s gives head = 3824522 Pa and power = 4.8e13 W; expected flow at most 0.1133 m3/s". The design lead then needed a well engineer round (6 min) to set `d0.well.segment` below_esp / `d0.riser.segment` above_esp and 6 more values; `simulate design/hc_wellfix` (19:06:01) passed with 0 failed steps. So an agent-built plant still does not run on its first full-year simulate; the missing segment values were not reported as missing by patch_plant's check.
