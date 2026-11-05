# QA-153: Case lead saves Knowledge values (assumptions document) into a case version before the user confirms them

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 16:55 UTC |
| Versions | backend 1.1.102 (geomind 0.4.98, gemini 0.6.16) |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 1 (23e6faf0-7fa0-450b-860e-16cfe5fdd91b); chat a606d755-166c-4fb8-a91b-e6319dbe7273; run f5f86362-4596-4264-b00a-8c26e5adc5f3; case_lead steps 9-17 |
| Fixer | hotfix-python |

## Steps

1. New project, upload the three competition files (PDF, heating CSV, cooling CSV).
2. Chat: "Set up the case for our geothermal heating and cooling plant from the uploaded challenge
   brief and the two daily demand files." Approve every card (script, backend API only).

## Expected

The prompt `geomind/prompts/case/lead.md` (steps 3-4, "Values from 3 and 4 go into the ONE
confirmation question", "The user confirms every value from 3 and 4 before the case is final",
"Set the case ... once with everything the files and the user state, once more with the values the
user confirmed"): the first `set_case` holds only file values; values from the Knowledge base
(`knowledge/hackathon-2026-assumptions.md`) are set only after the user approves them.

## Actual

Timeline of the case lead (run log steps, UTC):

| Step | Time | Call | Result |
|---|---|---|---|
| 9 | 16:53:30 | `set_case(source="project", files=...)` | refused: project has no case (wasted step, 12.3 s LLM) |
| 10 | 16:53:43 | `set_case(changes=...)` full | refused: CSV dates without offset, need `time_zone` (14.0 s) |
| 11 | 16:53:57 | `set_case` with `time_zone: UTC` | stored, case version 1 |
| 12 | 16:54:19 | `set_case(requirements=...)` | stored, case version 2 |
| 15 | 16:54:54 | `set_case` with site.air 10 degC / 101325 Pa, sand 20 mg/l, return temperatures 60/25 degC, return pressures 6/4 bar, dew point margin, indoor 26 degC / 50 %, grid CO2 300 g/kWh, gas composition: all from `knowledge/hackathon-2026-assumptions.md` | stored, **case version 3 at 16:55:05** |
| 17 | 16:55:13 | `ask_user` "please confirm them" (16 values) | user answered approve all at 16:55:30 |

So version 3 holds 16 unconfirmed Knowledge values 25 s before the question asks about them. On
`stop` or `change some` the saved case already carries them (and the design team could read them).
Also: `time_zone: UTC` is set in version 1 as an "assumption" that the same question asks to
confirm. Five `set_case` calls (2 refused) where the prompt asks for two.

Case versions of the project (`GET /design/case/versions`): 1 16:54:19, 2 16:54:29, 3 16:55:05
(the Knowledge values), 4 16:56:45 (economics).

## Evidence

- Run log: `../evidence/QA-153/run-f5f86362.json` (steps 9-17 of `case_lead`)
- Step list: `../evidence/QA-153/steps.txt`; answers given: `../evidence/QA-153/answers.json`

## Cause

Prompt: `geomind/prompts/case/lead.md` step 3 says "`set_case` with everything the files and the user
state" but the model reads the assumptions document as a file-like source ("An assumptions document
in the knowledge base ... comes before the cost catalogue") and sets it at once. Nothing in code
stops a `set_case` of Knowledge-sourced values before the confirmation `ask_user` (guess).

## Proposed fix

- geomind, `prompts/case/lead.md`: state plainly "values from the knowledge base (the assumptions
  document included) are NEVER in a `set_case` before the user approves them in the ONE confirmation
  question; set them in the `set_case` after approve all". Put the step order as: set file values
  (one call, with `time_zone` named as an assumption) -> ONE question -> ONE `set_case` with the
  approved values.
- Optional guard in `geomind/agents/case/lead.py` (like `economics_missing`): refuse once a
  `set_case` whose changes cite `knowledge/` before an `ask_user` of this run.
- Say in the prompt that CSV dates without an offset need `time_zone` in the first call (saves the
  refused step 10, 14 s), and that `source="project"` is only for a project case.json (step 9, 12 s).

## Speed and accuracy

- Run total 6 min 18 s, 1.61 M input tokens, 0.036 USD. The two refused `set_case` cost 26 s.
- Accuracy of the final case vs. `gemini/examples/hackathon_2026/case.json`: all values equal
  (units written as the PDF writes them: degC as °C, 80 mol% for 0.8, 50 % for 0.5).

## Reproduced

Run 2 (17:00-17:04 UTC, project QA-TEST QA-AI-case-I 2 cf19d767-b62b-4caa-a90e-4386e6e3c744, run 519ccc65-564e-4d1e-9139-a23777cd1107, backend 1.1.104, log `../evidence/QA-153/run-519ccc65.json`): same pattern. The first stored `set_case` (approval request-315, 17:02:09) already holds the Knowledge values (return temperatures, return pressures, dew point margin, indoor 26 degC / 50 %, air, gas composition, CO2 intensity); the confirmation question comes at 17:02:24. Again 5 `set_case`, 2 refused (`source="project"`, then the missing `time_zone`).

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 17:07 UTC: geomind 0.4.100 (592d31a, tag v0.4.100), deployed in backend 1.1.104 hotfix image 2026-11-05: case lead asks the ONE confirmation question (Knowledge values, time_zone) before the first set_case and saves after approve all in one set_case. Not live-retested.
## Retest

(Who, when, result.)
- 2026-11-05 17:35 UTC, QA-AI-case-I, run 3 (geomind 0.4.100, backend 1.1.104; project QA-TEST QA-AI-case-I 3 f400fa2d-292d-4358-b3c1-9f4a51f51f7f; run 84526204-bfb7-4611-a476-abde6317c58e; log `../evidence/QA-153/run-84526204.json`): the ONE confirmation question (`ask_user`, 17:14:57) comes before any `set_case`; the first `set_case` after approve all (17:15:13). No case version holds unconfirmed values. Verified. Left over (filed as QA-218): 4 `set_case` calls, 2 refused (a files-only call, then the full call without `columns`), requirements in a separate call; and the prompt now contradicts the handbook and itself (QA-177).
- 2026-11-05 17:32 UTC: QA-AI-case-I run 84526204 on geomind 0.4.100
## More evidence (QA-E2E-case-I, 2026-11-05 16:50-17:20 UTC)

- Project QA-TEST QA-E2E-case-I 1, run cf319cd4 (backend 1.1.102, geomind 0.4.97): the first good
  set_case (approved 16:54:30) wrote 46 leaves incl. return temperatures/pressures, indoor values,
  air, sand, gas composition and CO2 intensity (case v2: `demand.heating.return_temperature` 60 degC
  already set); the confirmation question with the same 17 values came only at 16:55:55, after a
  2nd set_case for requirements. The curator then wrote this order as lesson
  `case-lead-one-confirmation-question` ("Set the case from the project files and the knowledge base's
  assumptions document first, then gather ...", run a5118d9e; see QA-199).
- Both runs started before backend 1.1.104 (geomind 0.4.100). Project 2, run a5118d9e (17:07, geomind 0.4.98/0.4.99): better order (file values first, question,
  then the confirmed values in one set_case). Not seen again after that.
