# QA-174: patch_plant approval card says 'Change 0 value(s)' and lists no path while the call sends 113 changes

| Field | Value |
|---|---|
| Status | duplicate |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-design-I |
| Found | 2026-11-05 17:15 UTC |
| Versions | backend 1.1.102 at run start, 1.1.103 and 1.1.104 deployed during the run (geomind 0.4.98, gemini 0.6.16 then 0.6.17) |
| Where | api.geomind.team; project QA-TEST QA-AI-design-I 1 (b9ef5c9a-e030-4357-91ee-b17dabfdeaa6); chat efb95fd0-f997-4530-a314-f93baf64ef5f; run 0df89b7e-69e0-46b3-abe1-231e51d9570a; every patch_plant approval of the run (requests 1020, 1039, 1058, ...) |
| Fixer | |

## Steps

1. Project with the reference case and economics; chat: "Design a geothermal heating and cooling plant for this case ... simulate it for the full year".
2. The design lead calls `patch_plant` with the list form `changes: [{path, value, source, reason}, ...]` (the form its prompt asks for, step 4 of `prompts/design/lead.md`).
3. Read the run's `request.message` (GET /assistant/runs/{id}).

## Expected

"Change 113 value(s) of design/start and save it as 'assembled': params.d0.depth, params.d0.drainage_radius, ..."

## Actual

Every patch_plant card of the run: `Change 0 value(s) of design/start and save it as 'assembled': .` (113 changes sent), `Change 0 value(s) of design/complete and save it as 'ready': .` (1 change sent). The user approves values the sentence says do not exist; only the raw JSON below shows them.

## Evidence

- `../evidence/QA-174/patch-calls.json`: the two calls (113 changes each) whose cards said 0.
- Run log steps design_lead #21-#27 (16:06-17:10 UTC).

## Cause

Fact: `geomind/engine/session.py` `call_summary` (line ~741) counts `_leaves(item.get("changes") or {})`. `_leaves` (line 701) walks only dicts; the list form of `changes` is not a dict, so it returns `[]`: count 0, no paths. The dict form (QA-026 era) still works.

## Proposed fix

geomind `engine/session.py` `call_summary`, patch_plant branch: when `changes` is a list, take `[c["path"] for c in changes if isinstance(c, dict) and "path" in c]`; keep `_leaves` for the dict form. Unit test with both forms. List at most ~8 paths then "and N more" (113 paths would flood the card).

## Fix

- 2026-11-05 17:23 UTC: duplicate of QA-172; fixed with it in geomind 0.4.105
## Retest
