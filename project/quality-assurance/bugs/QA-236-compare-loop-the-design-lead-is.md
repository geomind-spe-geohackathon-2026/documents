# QA-236: Compare loop: the design lead is called twice (plan, then build) and the build call re-reads everything the plan call read: read_case 6x, handbook 0 and list_plants again; the brief also says 'read the files and set the case' on a complete case

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-design-I |
| Found | 2026-11-05 17:45 UTC |
| Versions | backend 1.1.102-1.1.106 (geomind 0.4.98, gemini 0.6.16/0.6.17) |
| Where | api.geomind.team; project QA-TEST QA-AI-design-I 2 (3b95e854-f402-4f9b-9179-a6a820e7aac7); chat 85dbe5e6-dfea-4ffb-a7e3-b07487b3898d; run 5d0216a6-4acb-487b-a885-396a5e99366d; design_lead 17:30:05-17:31:35 UTC |
| Fixer | |

## Steps

1. Reference case and economics loaded; chat auto-approve on.
2. "Compare a direct-use plant with absorption cooling against a heat pump plant with a compression chiller for this case. Use 1 to 3 doublets, keep every hard limit of the challenge, and tell me which one has the lower LCTS." The coordinator routes `loop: compare`.

## Expected

One read of the case and the handbook's chapter 0 for the whole comparison.

## Actual

- Plan call (17:30:05-17:31:08, 11 steps, 63 s LLM): `read_case {}`, then `read_case` requirements, site, demand, economics, utilities (the full read already holds them); handbook 0, 10.7, 0.8; `list_plants`; 4 `calculate` (2 refused, QA-235); `update_state`; finish "Plan only, nothing built yet".
- Build call (17:31:19-): `read_case {}`, `list_plants`, handbook 0 again, `list_profiles`, `read_plant` again, `read_case` site, requirements, utilities, economics again, handbook 0.8 again, `read_stored` the plan's finding. Five steps (16 s) re-reading what the plan call just read.
- The design lead's brief from `agents/project/drivers.py:294` adds "The project's files: ... Read them with read_rag and set the case from them with set_case (files), before you ask the user for anything." although the case is complete (v3, missing 0).
Same pattern in run 1 (one design call): `read_case {}` then 5 section reads in steps #1-#4.

## Cause

Facts: `agents/project/comparison.py:64` makes the plan a separate design_lead call ("Plan a comparison and build nothing yet"); the build call starts with a fresh context. `drivers.py:294` appends the file sentence whenever the project has files, without checking the case.

## Proposed fix

- geomind `agents/project/comparison.py`: one design_lead call that plans and builds, or pass the plan's case summary in the build brief and tell the lead not to re-read it.
- geomind `agents/project/drivers.py:294`: add the files sentence only when the case is missing values.
- geomind `prompts/design/lead.md`: "read_case once with no section: it returns every section" (also QA-157 for the case lead).

## Fix

## Retest
