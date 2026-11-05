# QA-176: A deploy during fill_parts restarts all four design engineers from scratch: 4 engineers redo 4 min of finished work, the lead then reads both sets of findings (7 read_stored)

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | backend,geomind |
| Reporter | QA-AI-design-I |
| Found | 2026-11-05 17:15 UTC |
| Versions | backend 1.1.102 at run start, 1.1.103 and 1.1.104 deployed during the run (geomind 0.4.98, gemini 0.6.16 then 0.6.17) |
| Where | api.geomind.team; project QA-TEST QA-AI-design-I 1 (b9ef5c9a-e030-4357-91ee-b17dabfdeaa6); chat efb95fd0-f997-4530-a314-f93baf64ef5f; run 0df89b7e-69e0-46b3-abe1-231e51d9570a; design_lead step #10 fill_parts (16:51:59-17:03:55 UTC) |
| Fixer | hotfix-back-VI |

## Steps

1. A design run is inside `fill_parts` (4 engineer instances side by side).
2. A hotfix deploy restarts the worker (API answered 503 "GeoMind is updating" at 16:56:12 UTC, 502 at 16:59 and 17:07).
3. The run resumes (QA-035).

## Expected

The resumed run keeps the instances that had already finished (their findings are stored: `finding-<id>`) and reruns only the unfinished one.

## Actual

`../evidence/QA-176/team-steps.json`:

- First pass 16:51:59-16:56: Reservoir engineer II finished 16:53:07, Energy systems engineer II 16:54:56, Energy systems engineer I 16:55:51; Reservoir engineer I was still working.
- 16:56:43 all four instances start again from step 1 (same briefs, same reads: handbook outline, sections 3, 4, 5, 6, 8.3, 9, the same describe_module calls), the last finish at 17:03:00.
- The lead then reads 7 stored findings (`read_stored` finding-1636e326, e7c0ca7b, 80c13ce1, 6c2a384f, b96dcde7, 098170e9, fd73d397): 4 from the rerun and 3 from the first pass, in 3 extra steps (17:04:11-17:04:45, 33-57 k input tokens each).

Cost: ~7 min wall time and ~0.03 USD of engineer tokens redone, plus 3 lead round trips; the first-pass findings are stale duplicates the lead must reconcile. Deploys are frequent in hotfix mode (two in this run alone), so every long design run pays this.

## Cause

Guess: the run resumes from the lead's last checkpoint, which is before the `fill_parts` call; the team call is replayed as a whole, and the finished instances' findings stay in the store and in the lead's next tool result.

## Proposed fix

- geomind `tools/delegate.py` `Team` / engine resume: checkpoint each instance's finished answer under (run, call_id, instance); on resume, return the stored answers and run only the missing instances.
- At least: on replay, drop the stale findings of the earlier pass from what the lead gets back, so it reads one set.
- backend `scripts/hotfix_deploy.sh` (optional): wait for or warn about running agent runs before restarting the worker.

## Fix

## Retest

## More evidence (QA-AI-analysis-I, 2026-11-05 17:17 UTC)

Run 57c42f61-2a89-48ba-933c-e87fc348084f (project `QA-TEST QA-AI-analysis-I 1`): the deploy of backend
1.1.105 (~17:16 UTC) hit an economist delegate mid-way. The first economist session (17:15:37-17:17:11,
17 steps, 330 k input tokens, 0.007 USD) ends `failed` with no error in the run log (`/agents` status
failed); after the restart a second economist session (17:17:32-17:17:48) re-reads the two stored
studies and answers. The sensitivity and sample studies themselves had finished (stored), so only
1.6 min and the tokens were lost. Log: `../evidence/QA-176/run-57c42f61-log.json`.

## More evidence (QA-AI-project-I, 2026-11-05 17:30 UTC; first filed as QA-188, now its duplicate)

Same restart in a project-lead run: project QA-TEST QA-AI-project-I 1, run b57abc5b-0497-46b3-a238-ddf87edaae02. A plain `Delegate` (not only `fill_parts`) restarts from step 1: the reviewer (16:57:49, 13 steps, then again from step 1 at 16:59:57, 2 min 08 s lost) and the analysis lead (17:04:52, 7 steps, again from step 1 at 17:07:37, 2 min 45 s lost; its finished economist finding was reused). About 5 min and 540 k input tokens lost. Details and trace: `QA-188-*.md`, `../evidence/QA-188/`, run log `../evidence/QA-187/b57abc5b-0497-46b3-a238-ddf87edaae02.log.json.gz`.
