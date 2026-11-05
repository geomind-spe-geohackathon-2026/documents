# QA-140: Case stage runs no parallel instances: the case lead calls geoscientist once (instance null), no field-group split (IMP-025)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | Manual QA-II (timed run approved by the user), Claude (write-up) |
| Found | 2026-11-05 14:57 UTC |
| Versions | frontend 1.1.107, backend 1.1.95 (geomind 0.4.91) |
| Where | https://geomind.team/projects/c0f655e9-2a4b-4f5a-bde7-574d4627ab1d/assistant/chat/832d3e5d-0e36-46ab-9044-7459a1bb3e40; project "QA-TEST manual-qa IMP-025 parallel case timing"; run 9696f5d4-4f99-4c2c-9db9-173d94e11eab |
| Fixer | |

## Steps

1. New project; upload the three competition files (GEMINI_Hackathon_Challenge_Requirements.pdf, the daily heating and cooling demand CSVs) to the project documents.
2. In a new chat send "Build the case for the attached challenge files." (files named in the message).
3. Approve every card; answer the two question cards "approve all". One run only, approved by the user to time IMP-025.

## Expected

IMP-025 case stage (geomind 0.4.91): the case lead splits the case by field groups and runs up to 4 geoscientist instances at once (Geoscientist I, II, ...), each named in the agents list (`instance` set) and shown as its own line in the chat (frontend 1.1.107).

## Actual

The case lead called `geoscientist` once: one session, `instance: null`, 2 LLM calls, 18.8 s, three `describe_case` calls, then `finish`. No second instance, no split by field groups; the case lead then wrote the case itself (5 `set_case` calls). The chat shows "Case lead · Thinking" and no Geoscientist I/II lines, so the 1.1.107 display could not be checked.

The run itself was fast and complete:
- request 14:52:55 UTC to end 14:56:39 UTC: 3 min 45 s; case version 3, `missing: []`, `problems: []`;
- 2 approval cards (set_case) + 2 question cards (case values, economics);
- 28 LLM calls, 955,129 input tokens (752,128 cached), 27,085 output, 0.018 USD; 41 tool calls.

6 of 41 tool calls were refused first and then recovered:
1. project_lead `read_case`: no_case (no case yet);
2. project_lead `update_state`: invalid_input, `/questions` given an object instead of a list (or `/questions/-`);
3. case_lead `read_case`: no_case;
4. case_lead `set_case(source='project')`: unknown_name, the project has no case.json;
5. case_lead `set_case` with `files` only: case_incomplete;
6. case_lead `set_case`: invalid_value, demand CSV `time` '2027-01-01' has no offset and no `time_zone` for the file (both series).

## Evidence

- ![screenshot](../evidence/QA-140/1.png) (chat during the run: "Case lead · Thinking", no instance lines)
- Run log JSON (API /assistant/runs/{id}/log): `../evidence/QA-140/run-9696f5d4.json.gz`
- GET /assistant/runs/9696f5d4.../agents: coordinator, project_lead, case_lead, one geoscientist (instance null).

## Cause

(Guess, marked as one.) The case lead's prompt/skill still allows a single geoscientist brief for the report text; the parallel Team call with a list of {role, task} briefs is not chosen when the source is one short PDF. Refusals 1 and 3 are the expected first read on an empty project but cost two calls; 2, 5 and 6 are format slips that IMP-012-style fixes in code could absorb.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 15:14 UTC: geomind 0.4.92 (case lead always splits into 2-4 geoscientists, single tool removed), backend 1.1.97, deployed ~15:20 UTC
## Retest

(Who, when, result.)
