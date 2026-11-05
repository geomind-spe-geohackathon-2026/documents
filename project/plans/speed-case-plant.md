# Plan: a fast and correct case and plant

Owner: the coordinator (Coordinator-IV), from the user's request of 2026-11-05 17:35 UTC.
Goal: through parallel agents (IMP-025) and the handbooks, the agents produce a complete, correct
case in under 5 minutes and a plant that passes gemini's checks, from a user's request, much faster
than today. Case and plant come first; the other stages follow the same pattern.

Rules in force: only a team lead reads and writes project files; at most 4 sub-agents per task;
sub-agents may read the global Knowledge only (`.claude/memory/feedback-team-lead-only-writes.md`).
No QA tests (no live checks, no agent/LLM runs) until the user lifts the rule
(`.claude/memory/feedback-no-tests-now.md`); offline unit tests and reading stored run logs are
allowed.

## Baseline (measured before the no-QA-test rule)

- Case: 3 min 45 s to a complete case (QA-140, run 9696f5d4), but no parallel split; 2 approval
  cards and 2 question cards; 6 of 41 tool calls refused first.
- Plant: no run since 2026-11-04 18:00 UTC reached a feasible plant by the agents' own path
  (IMP-023 figures: 529 patch_plant, 0 optimize); QA-143 evaluate_module could not pass with a design.

## Tasks

### A. Measure, offline (analysis session, Sonnet; reads stored run logs through the API, runs nothing)

- A1. For every agent run on production since 2026-11-05 00:00 UTC: time per stage (case, plant,
  sizing, simulate), steps, approval and question cards, first-try refusal rate per tool, the top
  refusal messages, where a run stalls (same call repeated, re-reads, waiting).
- A2. Write the table to this folder (`speed-case-plant-baseline.md`) and the top 10 causes, each
  with the fix it calls for (prompt, skill, tool schema, gemini message). Repeat after every geomind
  release.

### B. Case (hotfix-python)

- B1. QA-140: the case lead always splits into 2-4 geoscientists (geomind 0.4.95, deploying).
- B2. One plan step: the case lead reads the inputs once, maps every case field to a field group
  (site and subsurface, demand series, brine and gas, economics and requirements), and briefs each
  geoscientist with the input passages and the `handbook-case.md` section it needs.
- B3. One write, one approval: the lead merges all answers into a single `set_case` and one
  approval card listing the values with their sources; questions to the user only for values no
  input, Knowledge entry or connector gives, all in one question card.
- B4. The six refusals of the QA-140 run fixed at the tool (no_case, update_state list form,
  set_case files-only, set_case date without time zone): accept the obvious form or say the exact
  form in the error.
- B5. A budget per sub-agent (IMP-027), e.g. 2 minutes and 15 steps for a geoscientist, set by the
  lead; at the limit it returns what it has.

### C. Plant (hotfix-python; gemini where needed)

- C1. IMP-025 plant stage: the design lead picks the plant family and structure from
  `handbook-design.md` (ch 8 configurations, ch 11 designing in gemini), splits the modules into at
  most 4 groups (subsurface and wells, treatment and gas, heating, cooling) for its engineers, who
  return module values with sources; the lead builds the whole plant in one write.
- C2. Then the short path in one go: size (ranged doublets and capacities), simulate, check,
  optimize on the objective; a failed check is re-split to the engineer of that module with gemini's
  message and the handbook's failure-to-fix table (ch 11).
- C3. evaluate_module and patch_plant refusals: from A2's top causes, fix the schemas and skills
  (QA-143 deploying); one example per module call in the skills (IMP-021).
- C4. Budgets as B5 for engineers.

### D. Handbooks (coordinator, documents)

- D1. `handbook-case.md`: a field-by-field checklist (case field, where it comes from, unit, check)
  that the case lead uses as its split plan.
- D2. `handbook-design.md`: a short "design path in gemini" chapter at the top (family choice table,
  module groups, the order build-size-simulate-check-optimize, the failure-to-fix table), so the
  lead reads one section, not the whole book.
- D3. Re-upload both to the global Knowledge after each change.

### E. Display (hotfix-front)

- E1. One line per sub-agent with its step count (live), steps in a window (live).
- E2. A stage timer on the lead's line (elapsed time of the stage), so the speed is visible.

## Order

B1, C3 (QA-143) shipping now; A1-A2 at once (parallel); B2-B5; D1-D2 (parallel with B); C1-C2-C4;
E2. Each item deploys at once. When the user lifts the no-QA-test rule: one timed run for the case,
one for the plant, compared with the baseline.
