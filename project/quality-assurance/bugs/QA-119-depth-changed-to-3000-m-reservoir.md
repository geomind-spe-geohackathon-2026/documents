# QA-119: Depth changed to 3000 m: reservoir pressure left at 250 bar(g), not re-derived (PDF: hydrostatic for another depth)

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | functional-qa-case-I |
| Found | 2026-11-05 11:11 UTC |
| Versions | backend 1.1.84 (geomind 0.4.80) |
| Where | https://geomind.team/projects/15b2f15f-46d0-4b09-a44b-0f849127c1f0 (QA3 case); chat 37fb7886-a3b0-46b3-b36f-6afb72971d14; request "reference depth 3000 m, return 55 degC" |
| Fixer | hotfix-python |

## Steps

1. In the case chat ask: "Change the reference depth of the reservoir to 3000 m and the heating return temperature to 55 degC. Nothing else."
2. Approve Set case and Accept case.
3. Read the answer and the case.

## Expected

The PDF (table 3.1 note, as the agent itself quotes) lets the team choose another depth with hydrostatic pressure and the 30 degC/km gradient. A depth change should re-derive or at least flag the reservoir pressure (250 bar(g) was given at 2500 m) and ask the user whether to update it.

## Actual

Only reference_depth and return_temperature changed; "Nothing else moved ... site.reservoir pressure 250 bar(g)" is listed as unchanged and never questioned. At 3000 m the hydrostatic pressure is higher (about 1030 kg/m3 x 9.81 x 3000 m is roughly 300 bar), so the reservoir is modelled with a pressure of the shallower depth. The agent also says "new case version 27 / problem state 30" (app shows about Version 7): same as QA-114.

## Evidence

- Chat text: `../evidence/QA-119/chat-text.txt`

## Cause

Guess: the agent treats reservoir.pressure as an independent input; no rule ties pressure to depth.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
