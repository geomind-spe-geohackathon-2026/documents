# QA-112: Knowledge assumptions: bought gas composition sums to 1.001, case cannot be set

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | data |
| Reporter | functional-qa-case-I |
| Found | 2026-11-05 10:49 UTC |
| Versions | backend 1.1.84 (geomind 0.4.80) |
| Where | https://geomind.team/projects/15b2f15f-46d0-4b09-a44b-0f849127c1f0 (QA3 case); chat 37fb7886-a3b0-46b3-b36f-6afb72971d14; the case-setup question, step ~30 |
| Fixer | |

## Steps

1. In the QA3 case project chat ask the agent to set up the case from the three competition files.
2. Approve the confirmation question for values the files do not give ("approve all").
3. The agent stops: the bought-gas composition does not sum to 1.0 and it asks the user for a split.

## Expected

The sourced default set in Knowledge (`hackathon-2026-assumptions.md`, row "Bought natural gas composition") is
usable as written: mole fractions sum to 1.0, the case is complete, the user is not asked for
gas data nobody on the team has.

## Actual

Knowledge row (line 46 of `inputs/hackathon-2026-assumptions.md`): CH4 0.825 + C2H6 0.040 + C3H8 0.013 +
CO2 0.012 + N2 0.111 = 1.001. gemini requires exactly 1.0, so the agent (correctly) did not alter the
sourced value and left utilities.gas.composition open; the case lists it as missing for every later
stage. The agent behaved right; the data is wrong.

## Evidence

- Chat text of the question: `../evidence/QA-112/chat-text-gas-question.txt`

## Cause

Fact: the sum of the five fractions in the Knowledge file is 1.001. Guess: a rounding slip; N2 0.110 or CH4 0.824 would fix it, but the choice is the team's (Sahand), not ours.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

functional-qa-case-I, 2026-11-05 ~11:00 UTC: retested in the same chat (a fresh chat was not needed): asked the agent to read the corrected Knowledge row; it read all five full-precision fractions, called the sum 1.0 and set utilities.gas.composition; no question to the user. Passes. The stored digits are a separate minor issue: QA-118.
- 2026-11-05 11:06 UTC: retest passed on the live site, functional-qa-case-I
