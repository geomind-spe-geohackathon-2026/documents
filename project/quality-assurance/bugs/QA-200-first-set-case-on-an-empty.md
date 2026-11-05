# QA-200: First set_case on an empty project: 2-8 refused calls (source without a case, files alone, no time_zone, partial patch called 'older shape') before one succeeds

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | QA-E2E-case-I |
| Found | 2026-11-05 17:21 UTC |
| Versions | frontend 1.1.113, backend 1.1.102-1.1.104 (geomind 0.4.97-0.4.99) |
| Where | geomind.team; projects QA-TEST QA-E2E-case-I 1/2/3; runs cf319cd4 (case_lead 7-9), a5118d9e, 6a2d6017 (case_lead 8-9 and 2nd instance 4-11) |
| Fixer | |

## Steps

1. New empty project, upload PDF + the two CSVs (dates `2027-01-01`, no offset), ask for the case.
2. Read the case lead's set_case calls in the run log.

## Expected

The first set_case on an empty project carries the header, the time, both series with `time_zone`
(the zone the lead puts in its question, handbook-case) and succeeds at once.

## Actual

| Run | set_case calls | refused | refusals |
|---|---|---|---|
| cf319cd4 (project 1) | 5 | 3 | `unknown_name` source=project (no case); `invalid_value` no time_zone (2 paths); `case_incomplete` "this file has an **older shape**; expected a header" for a partial patch sent after the refused full call |
| a5118d9e (project 2) | 6 | 1+ | as above |
| 6a2d6017 (project 3) | 9 | 8 | source=project; files alone x2; no time_zone x2; power missing x2; `requirements[0].case_requirement`, `over` missing |

Each refused call is one LLM round trip of the case lead with 50-70 k input tokens (10-25 s). In run 3
the case was never stored (QA-198, QA-197). The "older shape" message is misleading: nothing was stored,
the case is not old, the call simply lacks the header because the lead thought the 1st call had worked.

## Evidence

- Run 1 log (`../evidence/QA-199/run-cf319cd4-log.json.gz`) case_lead 7, 8, 9 (inputs and errors quoted in
  QA-E2E-case-I report); run 3 log `../evidence/QA-197/run-6a2d6017-log.json.gz`.

## Cause

Facts: the lead tries `source: "project"` and `files` alone first (the tool's error says neither can
set a new case); the time zone is known (the lead says it will "set UTC") but is not in the call until
gemini refuses it (QA-158 changed the prompt in 0.4.99; run 3 still failed twice on it).

## Proposed fix

geomind `agents/case/lead.py` prompt / skill `setting-the-case`: one worked first call for an empty project
(header + time + demand power with `file`, `column`, `unit`, `time_zone` + site + requirements in the
gemini sample shape). geomind set_case tool: when the project has no case and the call has no header,
say "no case is stored yet; the first call needs format, kind, name and time" instead of "older shape".

## Fix

- 2026-11-05 18:59 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest
