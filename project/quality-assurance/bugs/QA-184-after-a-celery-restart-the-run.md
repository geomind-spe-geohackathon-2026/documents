# QA-184: After a celery restart the run resumes, but the interrupted sessions stay: case_lead 'failed' and its 4 geoscientists 'running' forever in the run's agents

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | backend |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 17:14 UTC |
| Versions | backend 1.1.104 (geomind 0.4.98, gemini 0.6.17) |
| Where | https://geomind.team/projects/fcc641c0-0119-4182-9a72-adce5a17b3ed; run d4ab496f-4a1f-43fa-b760-0f550fda0714 (hackathon report run) |
| Fixer | hotfix-back-VI |

## Steps

1. Start a run; while the case lead and its 4 geoscientists work, deploy the backend (celery restarts; here backend 1.1.104 at about 17:00 UTC).
2. The run resumes (`assistant.runs.resume`) and a new case lead finishes the case.
3. Read `GET /assistant/runs/{id}/agents`.

## Expected

The interrupted sessions are closed (interrupted or cancelled), so no agent of the run stays 'running'.

## Actual

The first case_lead is 'failed' (3 steps) and its Geoscientist I-IV stay 'running' (2-5 steps) for the rest of the run, beside the new
case_lead and Geoscientist I-IV that finished. Any view built from these states shows four geoscientists as still working.
Possibly related to QA-170 (Coordinator shown as still thinking).

## Fix

geomind 0.4.106 (2aabaa5), backend 1.1.106, ~17:27 UTC. Cause: `end_orphans` ended only the
direct children of the resumed run, so the grandchildren (Geoscientist I-IV of the failed
case_lead) never got `run.finished`. Now an ended nested run first ends every open run below it,
and with QA-176 the case lead itself resumes instead of failing. Old runs keep their stale rows.

## Retest

Recipe: Deploy while the case lead and its geoscientists work; afterwards GET /assistant/runs/{id}/agents shows no session `running` once the run ends.
