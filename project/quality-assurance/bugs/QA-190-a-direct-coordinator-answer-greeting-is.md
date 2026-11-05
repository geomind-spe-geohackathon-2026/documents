# QA-190: A direct coordinator answer (greeting) is stored as loop 'tool' on the run

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 17:20 UTC |
| Versions | backend 1.1.102 to 1.1.104 during the run (geomind 0.4.96 to 0.4.98 local wheels, gemini 0.6.16/0.6.17); model deepseek/deepseek-v4.1-flash-1017 |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 1 (35a70dbe-5e24-4f51-9c6f-50e06d47fe82); chat 134dae07-2e37-4a3a-ae0b-83b5e812017e; run de19a6c9-44ba-4fa7-bf71-3945951fd44f |
| Fixer | |

## Steps

1. Project QA-TEST QA-AI-project-I 1 with the reference case and plant; new chat.
2. Message "Hello. What can your team do for this project?".

## Expected

The coordinator routes it `kind: "answer"` (it did, 3.7 s, 2 250 tokens, a good answer, good next-step chips). The run row and the run log say the run was a direct answer, not a tool loop.

## Actual

`GET /assistant/runs/de19a6c9-...` and the run log both have `"loop": "tool"`. The Runs and logs page and any count of runs by loop show a greeting as a tool run with the analysis lead.

## Evidence

- `../evidence/QA-190/run-de19a6c9.json` (`"loop": "tool"`, status done, 2 250 / 111 tokens).
- `../evidence/QA-190/de19a6c9-44ba-4fa7-bf71-3945951fd44f.log.json`: step 1 coordinator answer `{"kind": "answer", ...}`, step 2 agent `answer`, model `rule`.

## Cause

`geomind/geomind/run.py` `loop_of`: an `answer` route is run as `LOOPS["tool"](Answer(...))`, and `Route.loop` defaults to `"tool"` (`agents/project/coordinator.py`), so the loop name recorded is `tool`.

## Proposed fix

geomind: record the loop as `answer` for a `kind: "answer"` route (a named `answer` entry in `LOOPS`, or the loop name taken from `route.kind` when it is `answer`). Backend needs no change if it stores geomind's loop name; check the Runs page filter accepts `answer`.
