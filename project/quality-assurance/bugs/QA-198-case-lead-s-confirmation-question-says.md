# QA-198: Case lead's confirmation question says 'The case is set from the three project files' when no case exists (both set_case calls were refused)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-case-I |
| Found | 2026-11-05 17:21 UTC |
| Versions | frontend 1.1.113, backend 1.1.103 (geomind 0.4.98) |
| Where | https://geomind.team/projects/92b44928-ff0d-4954-a554-f166477af892/assistant/chat; project QA-TEST QA-E2E-case-I 3; run 6a2d6017; case_lead (1st instance) step 8, ask_user |
| Fixer | |

## Steps

1. New project, upload PDF + 2 CSVs, ask for the complete case.
2. Wait for the confirmation question (17:09:49 UTC).

## Expected

The question says what is really stored. If no `set_case` succeeded, it says the case is not stored yet
(and why), or the lead stores the file values first.

## Actual

The question begins: "The case is set from the three project files (time 2027-01-01 to 2028-01-01 daily;
heating and cooling demand from the two CSVs; ground, reservoir, brine and gas from the requirements PDF
page 2; the PDF's constraints as requirements). These values are NOT in the files and need your approval
before they enter the case."
At that moment the project has **no case** (`GET /design/case?project=92b44928...` 404). The lead's only
two `set_case` calls (steps 8, 9) were refused: `unknown_name` (source=project, no case) and
`case_incomplete` (files alone). No set_case approval card was ever shown in this run before the question.
A user who answers "approve all" believes the file values are already in the case.

## Evidence

- Run log: `../evidence/QA-197/run-6a2d6017-log.json.gz`, case_lead 8-9 (refused set_case), case_lead 8 (2nd block) ask_user.
- Case API 404 at 17:10 UTC; screenshot of the question text in the chat of project 3.
- Projects 1 and 2 (same input) stored the file values first (2 approved set_case), so the wording fits there.

## Cause

Guess: the prompt's template for the question ("The case is set from the files; these values are not")
is used whether or not a set_case succeeded; the model does not check its last set_case result.

## Proposed fix

geomind `agents/case/lead.py`: before `ask_user`, the lead states only what `case_changes`/`read_case`
shows as stored; or a guard in the question tool: if the project has no case, refuse a question text that
says "case is set". Better: fix QA-200 so the first set_case does not fail.

## Fix

- 2026-11-05 17:53 UTC: geomind 0.4.111-0.4.114 (HEAD 778970d), deployed in backend 1.1.110 at 18:51 CET
## Retest
