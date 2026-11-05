# QA-283: Empty project, 'design me a geothermal plant': the project lead briefs from a case.json that does not exist, and the case team takes the hackathon-2026 assumptions document as this project's brief without asking where the site is

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 18:30 UTC |
| Versions | backend 1.1.114 (geomind 0.4.114+) |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 4 (588c282d-fd39-4ea1-b495-d167817739c3, empty: no files, no case, no plant); chat 2083a333-28d2-4b82-9922-3d3073087b0d; run b0388d26-c47c-4ff6-89d9-b5e7180f9822; request-351 |
| Fixer | |

## Steps

1. New empty project (no files, no case). New chat.
2. Message: "design me a geothermal plant".

## Expected

GeoMind is general, the competition is one example. With nothing in the project, the team asks the user first, in one question, for what only the user has: the site (or its location), the demand (files or values), the services. It does not decide that this is the hackathon case.

## Actual

- Coordinator -> project (right). Project lead: `list_studies` `[]`, `list_plants`, `read_case` -> `no_case`; it never calls `list_files`, then briefs the case lead (quoted): "set the case first, from the project's files (the project's case.json and the data files it names, via set_case(source="project"))". There is no case.json and no file.
- Case lead (10 calls): `list_files` `[]`, then "The knowledge base holds a hackathon-2026 assumptions document that reads as this case's brief", reads it whole, splits into four geoscientists (16 Knowledge reads, 4 instances), who fill the hackathon site, brine, utilities and requirements (12 degC, 30 K/km, 2500 m, 250 barg, 1030 kg/m3, flow 50-300 m3/h ...).
- Only after 5 min 33 s (18:23:56 to 18:29:29 UTC; 0.017 USD; 517 k input tokens) the user gets a question, and only for the demand files the brief names: "the two demand CSVs the brief names (GEMINI_Heating_Demand_Daily_2027.csv ...) are not in the project".
- The `hackathon-2026-assumptions.md` header says "Guidance for the GEMINI hackathon 2026 case only".

## Evidence

- `../evidence/QA-283/b0388d26-c47c-4ff6-89d9-b5e7180f9822.log.json`, `../evidence/QA-283/b0388d26-c47c-4ff6-89d9-b5e7180f9822.trace.txt`: project_lead steps 1-3 and its brief (case_lead user message), case_lead steps 1-10, geoscientist briefs, request-351.

## Cause

- `prompts/project/lead.md` has a template brief "the case from the project's files" and no rule to look first (`list_files`) and to say "the project has no files" in the brief.
- The case lead / handbook-case let a Knowledge document "that reads as this case's brief" become the case; nothing asks whether the user's project is that case. (Case-team behaviour, in QA-AI-case-I's area; reported here because the project lead's brief starts it.)

## Proposed fix

- `prompts/project/lead.md`: "Before a case brief, call `list_files`; in an empty project (no files, no case) ask the user once, with `ask_user`, for the site and the demand (upload files, or describe them), with the option 'use the GEMINI hackathon 2026 example'; never brief from a file that is not there."
- `prompts/case/lead.md` (or handbook-case): "A Knowledge document written for one named case (`hackathon-2026-*`) is that case's brief only when the user or the project's files name that case."

## Fix

- 2026-11-05 18:58 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest
- 2026-11-05 19:00 UTC (20:00 CET), QA-AI-case-I, project QA-TEST QA-AI-case-I 10 (40d0f25a-2b9e-4785-b41a-5f3ca414adf4), run 55a9cd7b-18ce-43a9-b260-a4982eb07a1c (geomind 0.4.114+): "design me a geothermal plant" on an empty project. The project lead calls `list_files`, `list_studies`, `list_plants` and asks the user in 10 s for the site, the demand and the services, offering the hackathon example case as an option; no brief from a non-existent case.json. The reported flow is fixed. Choosing the example case leads to a new problem, filed as QA-309 (demand files not available, peaks as constant demand). Verified for this bug.
- 2026-11-05 18:58 UTC: QA-AI-case-I run 55a9cd7b: asks in 10 s; follow-up QA-309
