# QA-263: Vague 'is this a good investment?': the economist runs the sensitivity on 2 of the case's 6 uncertain values (no electricity, gradient, permeability, gas) and the answer says 'the discount rate dominates', while gradient (13.6) and electricity (11.8 EUR/MWh) move LCTS more

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 18:11 UTC |
| Versions | backend 1.1.112 (geomind 0.4.118/0.4.119, gemini 0.6.19), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 6` (d168c5d1-acd4-4795-9442-f2dbe56d0b2d); chat 2fd795ec-8012-40cc-8666-6eca57ecd2a3; run bf7b2f00-d408-4afa-8ad1-c34eb8f2a25b |
| Fixer | hotfix-python-lead |

## Steps

1. Project with the reference case + economics (6 declared uncertainties: site.ground.gradient,
   site.reservoir.permeability, economics.energy.electricity, economics.energy.gas, economics.discount_rate,
   economics.carbon.price) and plant version 1 = HackathonPlant.
2. Chat, vague on purpose: "Is this plant a good investment?"

## Expected

If the answer includes a sensitivity, it ranks all the case's uncertain values (or says which it left out and
why), so "what dominates" is true. gemini's sensitivity of all six on this plant (page study 957c9714, project 1):
gradient 13.59, electricity 11.84, discount rate 10.85, permeability 4.12, carbon 3.40, gas 0.00 EUR/MWh.

## Actual

Good overall (4 min 1 s, 874 k input tokens, 0.0124 USD; costs, NPV 28.453 MEUR, payback 7.74 yr, p5/p50/p95 LCTS
37.97/46.10/54.31 EUR/MWh all right). But the economist (step 8) called
`sensitivity(values=["economics.discount_rate", "economics.carbon.price"], ...)`, no reason given, and the final
answer says: "Sensitivity ...: **the discount rate dominates** - lcts 40.058 at 0.02 to 50.911 at 0.08 (effect 10.853
EUR/MWh); the carbon price moves lcts ... (effect 3.4004)" and the improvement line "firm up the discount rate with
the client: it is the dominant driver ... the investment case rests more on the financing assumption than on any
physical parameter". Wrong: the geothermal gradient (13.59) and the electricity price (11.84) both move LCTS more,
and the gradient is a physical parameter. The Monte Carlo in the same answer did use all six.

## Evidence

- `../evidence/QA-263/run-bf7b2f00-log.json`: economist step 8 (sensitivity input), analysis lead finish.
- Reference rows: page study 957c9714 in project `QA-TEST QA-AI-analysis-I 1` (result e566ac5b).

## Cause

- Skill `economics` and `sensitivity`'s doc: `values` is for "drivers the user names"; with no names the economist
  should leave it out (all declared values move), but it picked the two economics keys it thought relevant.
- The lead reported "dominates" over a subset without saying it was a subset.

## Proposed fix

1. `prompts/analysis/economist.md` / skill `economics`: "without drivers named by the user, call `sensitivity`
   without `values` (every declared uncertainty); with `values`, say in the answer which declared values were left out".
2. `sensitivity` answer: list the declared uncertain values that were not moved (`not_moved`), so the lead can
   see it ranked a subset.

## Fix

- 2026-11-05 18:34 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)

- 2026-11-05 18:48 UTC, QA-AI-analysis-I, backend 1.1.117: fresh project `QA-TEST QA-AI-analysis-I 9`
  (6e8d019d-6524-4464-a8bb-cb0a022afa69). "Is this plant a good investment?" (run 0e4bfd2f, 59 s, 0.0070 USD): costs and
  NPV right, no sensitivity run this time ("you did not ask for one"). Follow-up "Yes, run the sensitivity: what drives
  the LCTS most?" (run 486f038f, 48 s, 0.0049 USD): `sensitivity` without `values` (all six declared uncertainties);
  ranking gradient 13.594, electricity 11.843, discount rate 10.853, permeability 4.118, carbon 3.400, gas 0.000
  EUR/MWh: equal to the page study 957c9714 row for row; the answer says "the ground temperature gradient drives the
  LCTS most" and that six values were moved. Verified.
  Logs: `../evidence/QA-263/run-0e4bfd2f-retest-log.json`, `run-486f038f-retest-log.json`.
