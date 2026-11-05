# QA-282: Study form/API accepts evolve settings that cannot run (polish > 0 with population 16: 'polish searches with minimize, which needs at least 5 per variable'); the study is created and fails at once instead of being refused at creation

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | backend |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 18:28 UTC |
| Versions | backend 1.1.115, frontend 1.1.126 |
| Where | https://geomind.team/projects/4678c5c6-66fc-46dd-9d1e-358c3c5c1d24/design (No-agent showcase) |
| Fixer | |

## Steps

POST /design/study with kind evolve, settings {objectives: [lcts, co2], evaluations: 160, population: 16, seed: 0, polish: 2, prepare: [size]}.

## Expected

Refused at creation (422 with the rule), or the form limits polish by population.

## Actual

The study is created, queued and fails at once: `study_failed: study.evolve: population = 16; polish searches with minimize, which needs at least 5 per variable`. Two such failed studies now stand at the top of the Study list of the showcase project (they were mine, sent by API).

## Evidence

- ![screenshot](../evidence/QA-282/1.png)

## Fix

- 2026-11-05 18:56 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest
