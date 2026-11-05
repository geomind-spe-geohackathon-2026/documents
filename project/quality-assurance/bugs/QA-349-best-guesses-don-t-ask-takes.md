# QA-349: 'Best guesses, don't ask' takes 17.5 min and 0.048 USD: the case lead sends ask_economics 6 times against the new refusals (agent values, Dutch subsidy), then the project lead re-delegates the open subsidy and per-energy keys for 2 more refusals

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 20:18 UTC |
| Versions | backend 1.1.126 (geomind with 35c2cb0, QA-320 fix) |
| Where | project "QA-TEST QA-E2E-economics-I 16"; run 45becf5b-36c2-496f-a8e0-68e46e7ffa76 |
| Fixer | m8 |

## Steps

1. Reference case, no economics. Chat (20:00:21 UTC): "Fill in the economics yourself with your
   own best guesses, including the per-MWh operating costs and a subsidy; I don't want to be
   asked."
2. Approve all on the one card (20:05:40).

## Expected

The QA-320 result (assumptions file for 42 keys, the rest open) in 2-3 minutes, as for "Set up
the economics" (project 15: 2 min 37 s, 0.008 USD).

## Actual

Accuracy is right (QA-320 verified). Speed is not: 17 min 36 s, 1.46 M input tokens, 88.7k output
tokens, 0.048 USD (6x the normal economics run).

- Case lead, first nested run: `ask_economics` refused 5 times in a row (steps 5, 7, 8 "probe",
  9, 10: keys without a source, the Dutch SDE++ subsidy for a case with no country, subsidy with
  source "agent"), accepted at step 11 (card at 20:05:31, 5 min). After approve all, 7 more steps
  and `finish` at 20:07:43.
- Project lead (step 4, 20:08:03) delegates AGAIN: "Follow-up ... fill the per-MWh operating
  costs and a subsidy". Second case-lead run: 15 steps, 2 more refused `ask_economics` (chiller
  per-energy with source "agent"; the Dutch subsidy rows), several 30-67 s LLM calls, `finish`
  at 20:17:09: "Both delegated items could NOT be set".
- Final answer at 20:17:30 is correct and honest ("Two items could not be filled in").

## Evidence

- Run JSON: `../evidence/QA-349/run-45becf5b.json.gz` (ask_economics calls: case_lead steps 5,
  7-11 and 8, 10 of the second run; project lead step 4)

## Cause

Fact: the new `ask_economics` refusals (QA-320) work, but the case lead learns them one at a time
by trial (each refusal names one class of problem); the project lead treats the open keys the
user asked for as unfinished work and re-delegates them although the case lead's finish already
said no source gives them.

## Proposed fix

geomind:
1. `ask_economics` refusal lists ALL problems at once (agent sources, foreign national rows,
   missing values) with the keys to move to `open`, so one retry suffices; or move them to Open
   itself and say so in the card.
2. Case lead skill: "a key no source gives goes to Open; never retry it with another value".
3. Project lead: do not re-delegate keys a lead reported as "no source" in its finish; tell the
   user instead.

## Fix

- 2026-11-05 20:26 UTC: geomind b68b884 + 7057fe2 + 42a884c; pending deploy
## Retest
