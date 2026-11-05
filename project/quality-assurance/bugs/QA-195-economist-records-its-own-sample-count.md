# QA-195: Economist records its own sample count and seed as a user-confirmed assumption ('source: user, confirmed: true, the user gave the sample count and seed') although the user gave none

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 17:16 UTC |
| Versions | backend 1.1.104/1.1.105 (geomind 0.4.100/0.4.102), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 1`; chat fa9cfafb-e39e-4ccd-9dfb-d8427f518c43; run 57c42f61-2a89-48ba-933c-e87fc348084f |
| Fixer | |

## Steps

1. Chat: "Now run the sensitivity again on the stored baseline design design/HackathonPlant_v1: rank the
   electricity price, the discount rate and the carbon price by their effect on LCTS, and give the LCTS
   p5, p50 and p95 over the case's uncertainty." (no sample count, no seed)

## Expected

The economist picks samples and seed, records them as its own assumption (`source: agent`,
`confirmed: false`) and says so.

## Actual

Economist `update_state` (steps 11, 15, accepted at 16): assumption `A-unc-seed` "200 samples, seed 0
(the user's choice)", `source: user`, `confirmed: true`, reason "The user gave the sample count and seed
in the task". Its answer to the lead says "200 samples, seed 0 - the user's choice, assumption
A-unc-seed confirmed". The analysis lead noticed and replaced it (step 5: "The task gave no sample count
or seed", unconfirmed), so the user's final answer is right; a lead that copies the economist would
report a user confirmation that never happened.

Accuracy of the numbers is right: sensitivity rows equal the page study `sensitivity` on plant
version 1 (electricity 40.019 -> 51.862, discount rate 40.058 -> 50.911, carbon 43.953 -> 47.353 EUR/MWh;
study 957c9714); LCTS p5/p50/p95 38.10/46.45/54.13 EUR/MWh (seed 0) against 37.97/46.10/54.31 for the page
study `sample` with seed 42 (5d7bbf26).

## Evidence

- `../evidence/QA-176/run-57c42f61-log.json` (economist steps 11, 15, 16; analysis lead step 5).

## Cause

Guess: the lead's brief to the economist said "200 samples, seed 0" (the lead's own choice, written as an
instruction), and the economist reads every value in its task as the user's. Prompt
`prompts/analysis/economist.md` has no rule on the source of a value that comes from the brief.

## Proposed fix

`prompts/analysis/economist.md` (and the lead's brief rule): "A value in your task is the lead's unless
the task quotes the user; record it as `source: agent`, `confirmed: false` unless the problem state
already holds it confirmed." Optionally `update_state` refuses `source: user, confirmed: true` from a
sub-agent that has no `ask_user`.
