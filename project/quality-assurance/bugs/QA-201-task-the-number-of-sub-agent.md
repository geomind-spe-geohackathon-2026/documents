# QA-201: Task: the number of sub-agent instances per team lead (now MAX_INSTANCES = 4 in geomind tools/delegate.py) set by a backend env variable, value 8

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | backend,geomind |
| Reporter | Sahand (task) |
| Found | 2026-11-05 17:21 UTC |
| Versions | backend 1.1.104 (geomind 0.4.98) |
| Where | geomind tools/delegate.py:233 (MAX_INSTANCES = 4), prompts/case/lead.md:41 ('2 to 4 field groups'); backend settings/.env |
| Fixer | hotfix-back-VI |

## Steps

Task from Sahand (2026-11-05 17:21 UTC), not a failure: a team lead (case lead's geoscientists, design lead's fill_parts team, ...) may start at most 4 sub-agent instances in one call.

## Expected

One backend env variable (for example `GEOMIND_MAX_TEAM_INSTANCES`) sets the most instances a team lead may start in one call; production sets it to **8**.
geomind reads it at run time (no default: a missing value is an error, per the project rule), and the prompts that say "2 to 4" take the number from it.

## Actual

`MAX_INSTANCES = 4` is a constant in `geomind/geomind/tools/delegate.py:233`; `prompts/case/lead.md:41` says "2 to 4 field groups".

## Cause

Constant in code.

## Fix

geomind 0.4.106 (2aabaa5), backend 1.1.106, ~17:27 UTC. `GEOMIND_TEAM_SIZE` (runtime
`team_size`) replaces `MAX_INSTANCES = 4`: a team call refuses more briefs, an unset value is an
error naming the variable (no default), 1 to 10 allowed; a run without it refuses to start. The
prompts (case lead, geoscientist, design lead, engineers) take the number through `{team_size}`.
Set to 8 in backend `.env`, `.env.dev`, `.env.dev.example`, `.env.example` (all four now hold the
same 89+1 variables; `.env.dev` got the 8 it lacked); geomind `.env.example`; prod worker
`GEOMIND_TEAM_SIZE=8` checked. Infrastructure `.env` / `.env.example` pairs: names match.
- 2026-11-05 17:29 UTC: geomind 0.4.106 2aabaa5, backend 1.1.106
## Retest

Recipe: Ask a lead for a split into more than 4 groups; up to 8 instances run (Roman I-VIII); 9 briefs are refused naming 8.
