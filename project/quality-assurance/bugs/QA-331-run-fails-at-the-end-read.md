# QA-331: Run fails at the end: read_case was 'refused for the rest of the run' after 4 no_case errors before the case existed; once the case is stored the project lead calls it again and the whole run ends failed (geomind 0.4.131, QA-269 rule)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | blocker |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 19:41 UTC |
| Versions | backend 1.1.120, geomind 0.4.131 (includes a61840a "QA-269: a tool over its retry limit is refused for the rest of the run, not the run's end") |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 13 (); chat 1b5f7994-12e5-4fd9-8847-53f0de496698; run e4e3e1f7-e5ef-4a0c-8df8-da7d3b8c4419 |
| Fixer | hotfix-python-lead-II |

## Steps

1. New project with the three competition files; chat "Set up the case for our geothermal heating
   and cooling plant from the uploaded challenge brief and the two daily demand files."
2. Approve every card (the run also hits QA-326: the case lead loops on files-only `set_case`).

## Expected

A read tool that failed because the state had nothing yet (`no_case`) works again once the state
has it; a refusal never ends a run whose work is done.

## Actual

- Project lead `read_case()` before any case: 19:28:30 `no_case`, 19:31:41 `no_case`, 19:31:43 and
  19:31:46 `failed_before` ("this exact call already failed at step 6"), 19:31:48 `not_allowed`:
  "read_case: refused for the rest of this run after 2 invalid calls in a row ... one more call of
  read_case ends the run".
- 19:38:39 the project lead stores the case itself (QA-326 workaround), 19:40:32 the case lead sets the
  economics with `ask_economics` (approved) and finishes.
- 19:40:49 the project lead hits its step limit ("continue" answered), calls `read_case` to check the
  stored case, and the run ends **failed**: `{"code": "error", "message": "read_case: called again after it
  was refused for the rest of the run"}` (19:40:58). The case and economics are stored, but the chat
  shows a failed run and no answer.
- Run: 15 min 21 s, 3.06 M input tokens, 0.068 USD.

## Evidence

- `../evidence/QA-331/run-e4e3e1f7.json` (run log), `../evidence/QA-331/run-e4e3e1f7-run.json` (`GET /assistant/runs/{id}` with the error)

## Cause

The QA-269 rule counts `no_case` (a state error: nothing to read YET) as an invalid call and bans the
tool for the run; the ban does not lift when the state changes (a `set_case` stored a case), and the
call after the ban ends the run.

## Proposed fix

geomind (QA-269 code, `engine`/tool guard): (1) do not count state errors (`no_case`,
`not_found` of something that a later write creates) toward the ban; (2) lift a tool's ban when a
write tool of the same object succeeds (`set_case` lifts `read_case`, `build_plant`/`patch_plant`
lift `read_plant`); (3) never end a run for a read tool: refuse the call and go on.

## Speed and accuracy

The run's work (case + economics) is stored but the run is reported failed with no answer.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 19:44 UTC: geomind main after 137797b (0.4.132); pending deploy
## Retest

(Who, when, result.)
