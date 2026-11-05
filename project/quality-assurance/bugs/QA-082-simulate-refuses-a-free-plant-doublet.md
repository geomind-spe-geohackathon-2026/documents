# QA-082: simulate refuses a free-plant doublet with 'd0.gradient: no value ... empty takes it from the case' (30 errors): case values are not taken over, patch_plant refuses them as case values

| Field | Value |
|---|---|
| Status | open |
| Severity | blocker |
| Area | gemini |
| Reporter | functional-qa-I |
| Found | 2026-11-05 06:05 UTC |
| Versions | backend 1.1.73, gemini 0.6.8, geomind 0.4.67+ (health 2026-11-05 06:05 UTC) |
| Where | project 61134432, chat cb8b9b2d-edce-4f69-9dfb-6b015a821601, run c4f00b5c-167e-4458-a8ab-bfe8aaed13fe, run JSON steps 11, 20, 34, 45, 49, 54, 64, 76, 81, 95 |
| Fixer | |

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

## Cause

Guess: the case fallback ('empty takes it from the case') works only when the doublet sub-objects are absent, not for a doublet with explicit sub-blocks; the agent builds the doublet with sub-blocks and then cannot clear them.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
