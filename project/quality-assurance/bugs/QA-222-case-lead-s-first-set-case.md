# QA-222: Case lead's first set_case is refused in every run (2 refusals in each of 3 runs): files-only call, source=project, missing time_zone, dropped columns; the 'date' column error does not name the columns argument

| Field | Value |
|---|---|
| Status | duplicate |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 17:35 UTC |
| Versions | geomind 0.4.98 (runs 1, 2), 0.4.100 (run 3); backend 1.1.102-1.1.104 |
| Where | api.geomind.team; runs f5f86362 (project QA-TEST QA-AI-case-I 1), 519ccc65 (... 2), 84526204 (... 3) |
| Fixer | |

## Steps

1. New project with the three competition files; chat "Set up the case ... from the uploaded
   challenge brief and the two daily demand files."
2. Read the case lead's `set_case` calls in the run log.

## Expected

One full `set_case` (prompt `case/lead.md`: "ONE `set_case` with everything ..."; "never a
files-only call: `files` alone sets no case").

## Actual

| Run | Refused call 1 | Refused call 2 | Then |
|---|---|---|---|
| 1 (0.4.98) | `set_case(source="project", files=[...], columns=...)`: "project has no case" (12 s) | full call without `time_zone`: "has no offset" (14 s) | stored, then requirements in another call |
| 2 (0.4.98) | same `source="project"` | same `time_zone` | same |
| 3 (0.4.100) | `set_case(files=[...], columns=...)` only: "files alone set no case" (11 s) | full call, `columns` dropped: "first column = 'date'; expected 'time'" (12 s) | stored with `columns`, then requirements in another call |

Each run loses about 23-26 s and two LLM round trips (~140 k input tokens), and writes the
requirements in a separate `set_case` (another approval card).

## Evidence

- Run logs: `../evidence/QA-153/run-f5f86362.json`, `run-519ccc65.json`, `run-84526204.json`
  (case_lead steps 9-12 / 10-13)

## Cause

1. The model starts with a files-first call although the prompt forbids it; `set_case`'s skill
   or argument description probably still invites it (guess).
2. The error for a time column of another name says "expected 'time'" and gives no fix; it does
   not say "pass `columns={file: {date: time}}`", so the model drops or forgets `columns` (run 3).

## Proposed fix

- geomind `tools/gemini/case.py` (`set_case`): on the 'first column = date; expected time' error,
  add a suggestion with the exact `columns` argument; when a call has `files` and `columns` but no
  `changes`, keep them and say "send changes now with these files and columns" instead of failing.
- geomind `prompts/case/lead.md` step 4: give one full example call with `changes` (each series
  with `file`, `column`, `unit`, `time_zone`), `columns` and `requirements` together, so the
  first call is right.

## Speed and accuracy

23-26 s and ~140 k input tokens per run; one extra approval card for the requirements call.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 18:35 UTC: duplicate of QA-200
## Retest

(Who, when, result.)
- 2026-11-05 18:05 UTC, QA-AI-case-I, run 6a8dba9a-c35a-4474-8f66-d749a3a95964 (project QA-TEST QA-AI-case-I 6, ed01f425-6c69-4ec4-af65-fcc7902ac04e; geomind 0.4.114, backend 1.1.110; 17:56:00-18:03:13 UTC; log `../evidence/QA-230/run-6a8dba9a.json`) (geomind 0.4.114): still 2 refusals before the first stored `set_case`: (1) files-only call, (2) full call with `"unit": ""` on every fraction (dissolved gas CH4/CO2, gas composition, indoor relative humidity) and `columns` dropped: "problems at 10 paths". The suggestions now name the `columns` argument. New variant: an empty unit string is refused although the key takes "no unit" (`describe_case`: "no unit, or a unit of a fraction"); proposal: treat `"unit": ""` as no unit in `set_case` (geomind) or gemini's reader, or say "leave out unit" in the error.
- 2026-11-05 19:05 UTC, QA-AI-case-I: run 7825eeac (project QA-TEST QA-AI-case-I 9, 0.4.114+): again files-only call (18:50:03) then the full call without `columns` (18:50:13), stored at 18:50:25. Run 55a9cd7b (project 10, no files): first `set_case` refused for `"unit": "mol/mol"` on the dissolved gas. So 6 of 6 case runs lose the first one or two `set_case` calls.
- 2026-11-05 19:10 UTC, QA-AI-case-I run f4018b98 (project 11, Delft with a weather connector): 3 refused `set_case` (files-only with 3 files; files-only again; `columns` only) before the full call at 19:04:32. 7 of 7 case runs.
