# QA-187: Reviewer runs 13-15 steps and 39 read_result after check_results gave its verdict at step 2 (6.5 min, 750k tokens for one check)

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
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

The reviewer prompt (`geomind/prompts/project/reviewer.md`) says: `check_results` once, `case_changes`, `compute_kpis`, `update_state` with the verification, `finish`. With the design lead's result already checked, that is 2 to 4 LLM calls, well under a minute.

## Actual

| Reviewer session | Start (UTC) | LLM calls | Input tokens | Wall time | `check_results` at |
|---|---|---|---|---|---|
| 1 (cut by a deploy, QA-188) | 16:57:49 | 13 | ~300 k | 2 min 08 s | step 2 |
| 2 | 16:59:57 | 15 | ~450 k | 4 min 49 s | step 2 |

Together 28 LLM calls, 753 662 input tokens, 393 s of LLM time, 0.0244 USD (37 % of the run's cost, the largest agent). After the verdict at step 2 (`feasible: true`, 15 of 15 requirements pass) each session goes on for 11 to 13 steps:

- 39 `read_result` over the two sessions: every module (`flare`, `boiler`, `heat_pump`, `d0.esp`, `loads`, `chiller`, `d0.reservoir`, `d1.reservoir`, `production`, `injection`, `grid`, `chiller_cooler`, `cool_users`, `heat_users`) and day ranges of `d0.reservoir.liquid_flow`, `chiller.generator_in.mass_flow`.
- 16 `read_case`: the whole case (10 442 chars) at step 1, then the sections `demand`, `economics`, `requirements`, `site`, `utilities` one by one, and in session 2 the whole case again at step 14 (all already in the conversation).
- 9 `read_stored`: the design lead's finding `finding-1623a86d` three times per session (whole, then `path: answer`), and `read_stored` of its own `check_results` output.
- Single LLM calls of 25 to 54 s with 2 000 to 5 400 output tokens (session 2 steps 11, 13, 15): the reviewer writes its own engineering review.

The verdict did not change: the final report is `passed: result/305d0f094cf4abfb`, which `check_results` gave at step 2.

## Evidence

- Run log: `../evidence/QA-187/b57abc5b-0497-46b3-a238-ddf87edaae02.log.json.gz` (`/assistant/runs/{id}/log`), steps with `agent: reviewer`.
- Compact trace (every LLM call and tool call, time, tokens): `../evidence/QA-187/b57abc5b-0497-46b3-a238-ddf87edaae02.trace.txt`.
- Per agent figures: `../evidence/QA-187/b57abc5b-0497-46b3-a238-ddf87edaae02.agents.json`.
- The project lead's brief to the reviewer (step 5, tool `reviewer`): "What to hand back: gemini's verdict ..., the requirement-by-requirement check with value vs limit, and **your own review of what gemini cannot see (structure, dispatch, backup policy, whether the plant as loaded is a sound answer to the challenge, any case value that looks wrong or missing)**."

## Cause

1. The project lead widens the reviewer's job (fact, brief above): "structure, dispatch, backup policy, sound answer to the challenge" is an engineering review, which the reviewer prompt does not ask for and which needs every module's result. `geomind/prompts/project/lead.md` gives the reviewer brief only as an example ("brief: verify `design.reference` on `design.result`") and no rule against adding scope.
2. The reviewer prompt has no stop after the verdict: nothing says "after `check_results`, `case_changes` and `compute_kpis`, record and finish; never read module results unless a failure needs its days". `read_result` is "when a failure needs its days", but here there was no failure (guess: the model reads it as allowed anyway).
3. `read_case.kept()` lets the reviewer read a section it already holds in the whole case; the tool does not answer "already in the conversation".

## Proposed fix

- `geomind/prompts/project/lead.md`, Rules: "The reviewer's brief names `design.reference` and `design.result` and asks for gemini's verdict, the case changes, a stale result and the unconfirmed assumptions; never ask it for an engineering review, an improvement or a judgement of the structure: those are the `analysis_lead`'s."
- `geomind/prompts/project/reviewer.md`, Rules: "Your calls are `check_results`, `case_changes`, `compute_kpis` (in one step), then `update_state` and `finish`. Call `read_result` only for a failure of kind `requirement` or `failed_step`, on its module and days. A passed verdict needs no `read_result`." Add the counter-example of this run.
- Code guard (geomind, `agents/project/reviewer.py` or the tool layer): a step budget for the reviewer (e.g. 6 steps), and `read_case` with `section` after a whole `read_case` in the same session returns a short note pointing at the earlier result instead of the data.
- Expected gain on this run: about 6 min and 700 k tokens of 19 min and 2.48 M.
