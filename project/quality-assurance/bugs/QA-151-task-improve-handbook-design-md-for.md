# QA-151: Task: improve handbook-design.md for design accuracy and fewer re-reads

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | Coordinator-V |
| Found | 2026-11-05 16:51 UTC |
| Versions | frontend 1.1.113, backend 1.1.101 (geomind 0.4.97, gemini 0.6.16) |
| Where | Task (Sahand 2026-11-05 16:51 UTC); Knowledge file handbook-design (id 6d617b90), source `documents/project/quality-assurance/inputs/handbook-design.md` and geomind `handbook-design.md` |
| Fixer | handbook-design-I |

## Steps

1. Read the design runs and the findings of QA-AI-design-I and QA-E2E-design-I.
2. Improve handbook-design.md: clear design path, competition hard limits (1-3 doublets, 50-300 m3/h, <=40 K, 100 C / 20 C supply), sizing rules, when to simulate, what not to re-read.
3. Re-upload it to Knowledge and note the new id in STATUS.md.

## Expected

The design team reaches a valid plant that meets the hard limits in fewer steps and with accurate sizing.

## Actual

Design runs are slow and patch by hand (QA-145); handbook last updated 18:10 UTC 2026-11-04 (ch 0 design path).

## Evidence

See Where.

## Cause

Guess: the handbook lacks concrete sizing rules and a fixed order of steps.

## Fix

- 2026-11-05 ~17:40 UTC, handbook-design-I: documents 401c58f, handbook-design v2. Cause (facts from
  the QA-145 run log): 139 `search_rag` calls, most for the same equipment values (well roughness,
  drainage radius, heat transfer coefficient, Carnot fraction, exchanger approach, boiler
  efficiency, pipe size, cooler fan power) that no Knowledge file gave in one place; the handbook
  still said to start from gemini's sample plants (rejected, IMP-023) and quoted prices that
  disagree with hackathon-2026-assumptions (compression chiller 0.16 vs 0.3 EUR/W).
  Change: chapter 0 now holds the gated checklist (0.1), the family decision order (0.2), the
  module groups with the well engineer (0.3), what `size_plant` sets and leaves (0.4), the failure
  table with the gemini 0.6.15-0.6.17 messages (0.5), where each value comes from (0.6: case,
  Knowledge, own choice, ask the user), a design-values table with paths, units, values and
  source/assumption status from gemini's sample README (0.7), the hackathon hard limits (0.8) and
  read-once/search-once rules (0.9). Prices removed (economics are the case's); 11.5, 11.6, 11.8
  and 12.6 no longer use sample plants as templates; carbon price per gemini 0.6.16. Section numbers
  kept (prompts and skills cite 0, 10.x, 11.x); checked with geomind `tools/sections.py`.
- Knowledge: handbook-design.md re-uploaded as f1a84a92 (replaces 6d617b90), searchable ready.
  No code change, no LLM run.
- 2026-11-05 ~17:35 UTC, handbook-design-I (Sahand: handbooks general, no competition data): documents
  bdbe89e, handbook-design v3. 0.7 says how to choose each value (published values only), 0.8 says
  how each kind of case limit binds the design, chapter 12 is worked lessons on an invented case
  (base/peak, doublet count, supply above reservoir temperature, flow range, gas use, QA lessons);
  every hackathon number removed. The sample plant values and the limits' consequences moved to
  hackathon-2026-assumptions.md ("Plant design values", "What the limits mean"). Section keys by
  number, stated in the front matter and 0.3 (QA-169). Knowledge: handbook-design 17f26c53 (was
  f1a84a92), hackathon-2026-assumptions ee185062 (was 9f98c448).
- 2026-11-05 17:01 UTC: handbook-design v2, documents 401c58f; Knowledge f1a84a92 (was 6d617b90)
## Retest

(Who, when, result.)
