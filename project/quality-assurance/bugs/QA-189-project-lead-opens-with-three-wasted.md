# QA-189: Project lead opens with three wasted calls: read_stored('design') refused, read_case of the whole case, then read_stored of its own read_case result

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 17:20 UTC |
| Versions | backend 1.1.102 to 1.1.104 during the run (geomind 0.4.96 to 0.4.98 local wheels, gemini 0.6.16/0.6.17); model deepseek/deepseek-v4.1-flash-1017 |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 1 (35a70dbe-5e24-4f51-9c6f-50e06d47fe82); chat 134dae07-2e37-4a3a-ae0b-83b5e812017e; run b57abc5b-0497-46b3-a238-ddf87edaae02 |
| Fixer | |

## Steps

1. API only (no frontend). New project; `POST /design/case` with `gemini/examples/hackathon_2026/case.json`, files `economics.json` and `data/demand.csv`; `POST /plant/flowsheet` with `plants/HackathonPlant.json` (case valid, no missing value).
2. Chat message: "The project already has the case and a plant (HackathonPlant). Check this plant against the challenge requirements, simulate the whole year, have it reviewed, and explain the result: LCOH, the hard limits, and what you would improve."
3. Approve the one `build_plant` card. Run done after 19 min (16:55:10 to 17:14:13 UTC): 84 steps, 82 LLM calls, 213 tool calls, 2.48 M input tokens, 0.0667 USD.

## Expected

The project lead plans and writes briefs with references, never copies (`prompts/project/lead.md`). With the case and plant in the problem state it needs at most `case_changes` (case unchanged?) and then the `design_lead` brief.

## Actual

Project lead steps 1 to 4 (16:55:12 to 16:55:32 UTC, 20 s, 31 320 input tokens) before the first brief:

1. `read_stored({"reference": "design"})`: refused, `unknown_name`, "expected a result-... key that a result gave" (it also brings the 5 357-char `reading-results` skill into the context). In the same step `read_case({})`: the whole case, 10 442 chars.
2. `case_changes({})`: `[]` (useful).
3. `read_stored({"reference": "result-602708b77b9556b6"})`: the stored copy of its own `read_case` output of step 1 (same content, again).
4. The `design_lead` brief (good: goal, references, hand-back, do-not-change).

Three of five calls are wasted. Small per run, but it is every project run, and the 10 k-char case then rides in every later project-lead call (steps 5 to 8, 10-12 k input tokens each).

## Evidence

- Run log `../evidence/QA-187/b57abc5b-0497-46b3-a238-ddf87edaae02.log.json.gz`, steps `agent: project_lead`, index 1 to 4.
- Trace: `../evidence/QA-189/b57abc5b-0497-46b3-a238-ddf87edaae02.trace.txt`, the first lines.

## Cause

- The lead's tool list has `read_stored` with no word on what it reads; the model tries it as a reader of the state's `design`. The prompt says the problem state is a message, but unlike reviewer.md and explainer.md it does not say "No tool reads it".
- `read_case` is offered to the lead without a rule on when; it reads the whole case to plan, then re-reads the stored copy.

## Proposed fix

- `geomind/prompts/project/lead.md`, Inputs or Rules: "The problem state is the `Problem state` message at the end of the conversation; no tool reads it. `read_stored` reads only a `result-...` or `finding-...` reference a tool gave you. Plan from the state and `case_changes`; read the case only when a brief needs a value the state does not show, and one section at a time."
- Or drop `read_case` and `read_stored` from the project lead's tools (`agents/project/lead.py`): it writes references, and its teams read.
