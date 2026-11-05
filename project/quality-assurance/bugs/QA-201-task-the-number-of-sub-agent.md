# QA-201: Task: the number of sub-agent instances per team lead (now MAX_INSTANCES = 4 in geomind tools/delegate.py) set by a backend env variable, value 8

| Field | Value |
|---|---|
| Status | fixing |
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

## Retest
