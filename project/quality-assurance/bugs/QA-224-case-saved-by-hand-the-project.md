# QA-224: Case saved by hand: the project lead asks approval 'Allow set_case (write)? Set the case.' with only {source: project}; the card names no version and no change (permeability 200 -> 150 mD)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 17:36 UTC |
| Versions | backend 1.1.106/1.1.107 (geomind 0.4.98+, gemini 0.6.17) |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 1 (35a70dbe-5e24-4f51-9c6f-50e06d47fe82); chat 134dae07-2e37-4a3a-ae0b-83b5e812017e; run 194c3879-076e-4e3a-b6bf-8f54da25a7ae; request-57 |
| Fixer | hotfix-python-lead |

## Steps

1. Project with the reference case (version 3) and HackathonPlant, simulated, reviewed and costed in this chat.
2. Save the case by hand (`POST /design/case`, base 3, the Case form's call): `site.reservoir.permeability` 200 -> 150 mD. Case version 4.
3. Message: "I saved the case form with a new reservoir permeability (site.reservoir.permeability). Does the plant still meet the requirements, and what does it do to LCOH?"

## Expected

The user's own saved case is the case: load it by rule (as `ProjectLead.forward` does for a chat with no case) or, if an approval is kept, a card that says what it loads: "Load the project's case, version 4: site.reservoir.permeability 200 -> 150 mD", in one sentence (QA-121, QA-026).

## Actual

Routing is right (coordinator -> project, with a task naming the path, no value). The project lead runs `case_changes` (`[]`: the chat's state is still the old case), `list_studies`, `list_plants`, `read_case` site and requirements (still 200 mD), then `set_case({"source": "project"})`, which stops the run for approval at 17:34:08 UTC:

`Allow set_case (write)?\n\nSet the case.\n\nWhat the call sends:\n{\n  "source": "project"\n}`

The user cannot see which case or which change is approved. Approving their own saved form is also one card more.

## Evidence

- `../evidence/QA-224/194c3879-076e-4e3a-b6bf-8f54da25a7ae.log.json`: project_lead steps 1-3; the run's `request` (request-57).

## Cause

- `set_case` is effect `write`, so every call asks, also `source: "project"`, which only loads what the user saved. The call summary for this form has no text (QA-026 fixed the summary for values, not for `source`).
- `ProjectLead.forward` loads the project case by rule only when the state has no case (`has_project_case`); a newer project case version than the state's is not loaded by rule.

## Proposed fix

geomind:
- `agents/project/lead.py` `has_project_case`: also true when the project's case version is newer than the state's; then load it by rule (the `LOAD_CASE` call) before the first model call, with no approval: the user saved it.
- Or, in the `set_case` tool's call summary: for `source: "project"` say "Load the project's case, version <n>" and list the paths that differ from the state's case (`case_changes` against the project case).
- Also: `case_changes` gave `[]` here although the project case differs from the chat's; the lead had to read the case to find out. A `case_changes` that compares with the project's newest version would let the lead skip the reads.

## Fix

- 2026-11-05 17:53 UTC: geomind 0.4.111-0.4.114 (HEAD 778970d), deployed in backend 1.1.110 at 18:51 CET
## Retest
