# QA-188: A deploy (worker restart) restarts the delegated agent that was running from its first step: reviewer and analysis lead redone, about 5 min and 800k tokens lost

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 17:20 UTC |
| Versions | backend 1.1.102 to 1.1.104 during the run (geomind 0.4.96 to 0.4.98 local wheels, gemini 0.6.16/0.6.17); model deepseek/deepseek-v4.1-flash-1017 |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 1 (35a70dbe-5e24-4f51-9c6f-50e06d47fe82); chat 134dae07-2e37-4a3a-ae0b-83b5e812017e; run b57abc5b-0497-46b3-a238-ddf87edaae02 |
| Fixer | hotfix-back-VI |

## Steps

1. API only (no frontend). New project; `POST /design/case` with `gemini/examples/hackathon_2026/case.json`, files `economics.json` and `data/demand.csv`; `POST /plant/flowsheet` with `plants/HackathonPlant.json` (case valid, no missing value).
2. Chat message: "The project already has the case and a plant (HackathonPlant). Check this plant against the challenge requirements, simulate the whole year, have it reviewed, and explain the result: LCOH, the hard limits, and what you would improve."
3. Approve the one `build_plant` card. Run done after 19 min (16:55:10 to 17:14:13 UTC): 84 steps, 82 LLM calls, 213 tool calls, 2.48 M input tokens, 0.0667 USD.
4. While the run works, the backend is deployed twice by hotfix sessions (geomind-celery and geomind-fastapi restarted; backend 1.1.102 to 1.1.103 at about 16:59 UTC, to 1.1.104 at 17:06:56 UTC, container created time).

## Expected

QA-035 made runs resume after a worker restart. A resumed run should go on from the last finished step of the agent that was working, so a deploy costs seconds, not the work done so far.

## Actual

The run resumed and finished (good), but the delegated agent that was running at the restart started again from its step 1, with the same brief, and redid all its work:

| Agent (parent step) | First session | Restart | Work thrown away |
|---|---|---|---|
| reviewer (project_lead step 5) | 16:57:49, steps 1-13 | 16:59:57, step 1 again | 2 min 08 s, 13 LLM calls, ~300 k input tokens |
| analysis_lead (project_lead step 6) | 17:04:52, steps 1-7 (its economist had finished, 60 s) | 17:07:37, step 1 again | 2 min 45 s, 7 LLM calls, ~240 k input tokens |

The second analysis lead read the economist's stored finding `finding-0234f856` instead of costing again, so a finished nested delegate is kept; only the in-flight session is lost. On a hotfix day with deploys every 10 to 20 minutes, every long design or review run loses its current sub-agent at each deploy.

## Evidence

- Run log `../evidence/QA-187/b57abc5b-0497-46b3-a238-ddf87edaae02.log.json.gz`: steps `agent: reviewer` with `index: 1` at 16:57:49 and again at 16:59:57; `agent: analysis_lead` with `index: 1` at 17:04:52 and 17:07:37 (same parent).
- Trace: `../evidence/QA-188/b57abc5b-0497-46b3-a238-ddf87edaae02.trace.txt`.
- `docker ps`: geomind-celery and geomind-fastapi created 2026-11-05 17:06:56 UTC (18:06:56 CET); `/system/health` 1.1.102 at 16:51, 1.1.103 at 17:00, 1.1.104 at 17:14 UTC; `/assistant/runs/{id}` answered 503 "GeoMind is updating" and 502 in between.

## Cause

Guess, from the log: the resume (`engine.resume`, geomind; `adapters.resume`, backend) replays the root run from its stored events, but a `Delegate` tool call with no stored result is run again from scratch as a new nested run; the nested run's own stored steps are not used to resume it.

## Proposed fix

- geomind `engine` resume: when the interrupted tool call is a `Delegate`, resume its nested run (its run id is in the stored events) from its last finished step instead of starting a new nested run. The nested run already stores its events, as the root run does.
- Until then (backend ops): `scripts/hotfix_deploy.sh` could wait for running runs to reach a waiting point or warn the deployer with the number of running runs (the info is in `runs` with status `running`).

## Fix

Same fix as QA-176: geomind 0.4.106 (2aabaa5), backend 1.1.106, ~17:27 UTC. A delegate
interrupted by a restart resumes its nested run from its last finished step instead of a new
run from step 1.
- 2026-11-05 17:29 UTC: geomind 0.4.106 2aabaa5, backend 1.1.106
## Retest

Recipe: Deploy while a delegate (reviewer, analysis lead) works; its steps continue from its last index, not from 1.
