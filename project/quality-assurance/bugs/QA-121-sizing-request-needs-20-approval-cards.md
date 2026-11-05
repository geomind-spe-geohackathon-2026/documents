# QA-121: Sizing request needs ~20 approval cards (Build/Patch/Set ranges plant) with raw JSON and a 30+ min run; agent hand-builds plants instead of one size study

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | functional-qa-study-I |
| Found | 2026-11-05 11:16 UTC |
| Versions | backend 1.1.84-1.1.86 (geomind 0.4.80), frontend as live 2026-11-05 |
| Where | https://geomind.team/projects/7a852d89-dfe5-423c-980a-a4ca231353bc/assistant/chat; project QA3 study; first chat of the project (run id in Runs and logs); S2 |
| Fixer | |

## Steps

1. In "QA3 study" (seeded, plant HeatingAbsorptionCoolingPlant with 2 doublets) ask in the chat: "Now run a sizing study: what is the smallest number of doublets and the lowest flow per doublet that still covers the 30 MW heating peak? Keep to the competition limits."
2. Approve every card as it comes (10:33 to 11:16 UTC).
3. After ~14 approvals I denied with "use a single size study ... 1 to 3 doublets, 50 to 300 m3/h".

## Expected

One size study (doublets 1-3, flow 50-300 m3/h) and one short answer; at most one or two approval cards, each readable (what changes, in words).

## Actual

- 14 approval cards (Build plant, Patch plant: plants named three, one, sweep, one_doublet, n1f300 ...) before my correction, then Set ranges and Patch plant cards again; about 20 in 43 minutes.
- Each card shows the whole plant JSON (hundreds of lines, cut with "the whole input is in the run log"), not a sentence on what changes.
- The agent hand-built plants one by one instead of running one size study; only after my instruction did it set ranges and run "study/sized2" (3 doublets x 300 m3/h, feasible), then asked to Set ranges again for a 2-doublet check.
- Set ranges cards show empty ranges for depth and absorption_chiller.capacity ({}).
- No answer on the smallest design after 43 minutes.

## Evidence

- ![screenshot](../evidence/QA-121/1.png)
- Run JSON: `../evidence/QA-121/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
