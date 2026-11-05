# QA-159: Economist costs one result in 7 round trips instead of 2-3: re-reads the case and its own estimate_costs output 5 times, and gets 4 unrelated skills (20 k chars) attached to its tool results

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 16:52 UTC |
| Versions | backend 1.1.102 (geomind 0.4.98), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 1` (4ce816b1-4bd1-48a5-8e77-9414c2b86301); chat fa9cfafb-e39e-4ccd-9dfb-d8427f518c43; run 389be3c3-2005-4360-b4dc-7a02ee18da0d |
| Fixer | |

## Steps

1. Project with the reference case and economics and plant version 1 = `plants/HackathonPlant.json`.
2. Chat: "Cost the stored plant (HackathonPlant, plant version 1) on the project's case: run the year,
   then give capex, opex, LCOH, LCOC, LCTS, NPV and CO2, each with its unit and the source of the prices used."

## Expected

Lead: simulate, brief the economist. Economist: `estimate_costs`, `update_state`, `finish` (the brief
already says the result and that the economics are the case's).

## Actual

The answer is right (capex 34.636 MEUR, opex 3.6539 MEUR/yr, LCOH 43.753, LCOC 51.445, LCTS 45.102
EUR/MWh, CO2 13.774 kt, equal to the page study `run` on the same plant: 34.636 / 3.654 / 43.753 /
51.445 / 45.102 / 13.774; NPV 28.453 MEUR checks with capex 34.636 MEUR, 4.4763 MEUR/yr, 5 %, 25 yr).
Whole run 75 s, 26 calls, 367 k input tokens, 0.0055 USD. But the economist took 7 LLM calls
(106 k input tokens, 35 s):

| Step | Call | Needed? |
|---|---|---|
| 1 | read_case(economics), estimate_costs | estimate_costs yes; the lead had read the economics already |
| 2 | update_state | yes |
| 3 | read_stored(result-875d..., the estimate_costs output it already had), read_case() whole case | no |
| 4 | read_stored(result-b5ca..., the economics of step 1 again) | no |
| 5 | read_case(about) | looking for price sources; the case has none |
| 6 | read_case(design) -> error, no such section | no (prompt speaks of `design.reference` in the state) |
| 7 | finish | yes |

Skills sent automatically with the first call of a tool, whatever the agent: `setting-the-case`
(7.3 k chars, with `accept_case`/`set_case`, tools the economist does not have), `working-in-a-team`
(3.4 k, about geoscientists and fill_parts), `reading-results` (5.1 k), `economics` (4.5 k). The
analysis lead gets `designing-a-plant` (13.8 k chars) for one `read_plant`. These stay in the
context of every later call of the session. The lead also read its own brief back (`read_stored
finding-58ceef99`, step 10).

The same pattern in the next run (c2b815a8): the economist read the case or the economics 7 times in
29 steps.

## Evidence

- `../evidence/QA-159/run-389be3c3-log.json`, `../evidence/QA-159/run-389be3c3-trace.txt` (economist
  steps 1-7, 16:51:43-16:52:18).

## Cause

- Guess: the skill attachment is keyed by tool (the first call of a tool in a session), not by the
  agent's role (`geomind/geomind/tools/skills.py`, and the `Skill ...` lines in tool docstrings, e.g.
  `tools/state.py:254` update_state -> `working-in-a-team`).
- Economist prompt (`prompts/analysis/economist.md`): "each price's source is its catalogue row or
  document as the case's `about.sources` names it" sends it looking for `about`; `design.reference`
  / `verification.result` are named as if always set.

## Proposed fix

1. `geomind/tools/skills.py`: attach a skill with a tool only when the skill is in the agent's own
   list (or give `update_state` and `read_case` no skill for sub-agents); never `setting-the-case` to
   an agent without `set_case`.
2. `prompts/analysis/economist.md`: "The brief and `estimate_costs` give everything for costs: do not
   read the case again or `read_stored` a result you already got. If the case has no `about.sources`,
   say the prices' source is the case's economics file and stop."
3. Lead prompt: do not `read_stored` your own brief.
