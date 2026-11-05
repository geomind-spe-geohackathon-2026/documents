# QA-212: Design lead patches each plant 6+ times, often one value per call (filled, ready, ok, v1, v2, v3, fix1): 13 patch_plant approval cards in 20 min; QA-145 meant one build and one patch

| Field | Value |
|---|---|
| Status | fixed |
| Severity | blocker |
| Area | geomind |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 17:29 UTC |
| Versions | backend 1.1.104 (geomind 0.4.98, gemini 0.6.17) |
| Where | https://geomind.team/projects/fcc641c0-0119-4182-9a72-adce5a17b3ed; run d4ab496f-4a1f-43fa-b760-0f550fda0714 (hackathon report run), design stage 17:07-17:29 UTC |
| Fixer | hotfix-python-VIII |

## Steps

Design request with two configurations; the design lead asks the engineers (fill_parts), then writes the plants.

## Expected

QA-145 (geomind 0.4.96): engineers propose, the lead builds once and patches once with all the proposals, so one or two approval cards per configuration before the search.

## Actual

Per configuration the lead saved 6+ versions, many with one or two values each:
- hp_2500 -> hp_2500_filled (12 values) -> hp_2500_ready -> hp_2500_ok (1 value: chiller setpoint) -> hp_2500_v1 (1 value: cooler setpoint) -> hp_2500_v2 (1 value: injection pump frequency) -> hp_2500_v3 (2 values: cooler loop) -> hp_fix1 (3 values).
- abs_3500 the same in parallel.
13 patch_plant approval cards between 17:13 and 17:29 UTC, each one more round for the user. The values of the later patches (setpoints from the case, cooler approach, pump frequency) were known from the engineers' findings at the first patch.
The cards are in `../evidence/QA-212/cards.md`.

## Cause

Guess: the lead patches after each refusal of `check`/`simulate` (one missing value at a time) instead of reading every missing value at once (gemini's check lists them all) and patching once; or the engineers' couplings are applied one per call.

## Fix

- 2026-11-05 17:32 UTC: raised to blocker by Sahand 17:32 UTC: report run has 15 plants and no study after 30 min; lead also started a hand-sized build (hp_2500_v4)
- 2026-11-05 17:39 UTC: geomind 0.4.109, commit 03046e7, deployed (backend 1.1.107): design lead prompt goes from first filled build to one set_ranges, size_plant, one optimize per configuration; one patch per round
## Retest
