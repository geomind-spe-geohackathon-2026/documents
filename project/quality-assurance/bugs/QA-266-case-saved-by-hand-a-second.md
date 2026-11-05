# QA-266: Case saved by hand a second time (150 -> 175 mD), same message: coordinator says 'nothing has changed since the re-simulation', routes to the analysis lead, which answers from the 150 mD results as the case as it stands

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 18:16 UTC |
| Versions | backend 1.1.114 (geomind 0.4.114+, with the QA-224/QA-227 fixes) |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 1 (35a70dbe-5e24-4f51-9c6f-50e06d47fe82); chat 134dae07-2e37-4a3a-ae0b-83b5e812017e; run 266b7476-1fed-469c-a14e-746d753cbb19 |
| Fixer | |

## Steps

1. The chat of QA-227: the case was saved by hand at 150 mD (version 4), the run then re-simulated and costed the plant on it.
2. Save the case by hand again (`POST /design/case`, base 4): `site.reservoir.permeability` 150 -> 175 mD, case version 5.
3. Send the same message as before: "I saved the case form with a new reservoir permeability (site.reservoir.permeability). Does the plant still meet the requirements, and what does it do to LCOH?"

## Expected

The project's case is newer than the chat's (version 5 vs 4): the run loads it (the QA-224 fix) and the design team re-simulates on 175 mD, or at least the answer says the case changed and the stored results are for 150 mD.

## Actual

- Coordinator (6.4 s): `{"kind": "loop", "loop": "tool", "agent": "analysis_lead", "task": "The user repeats the question on the saved permeability (site.reservoir.permeability, case version 4, 150 mD, triangular 100/400). Nothing has changed since the re-simulation: the unchanged design/hackathon was already run on this case ..."}`.
- Analysis lead: one LLM call, no tool call, answer from the conversation: "Yes - the unchanged design/hackathon still meets every requirement on the case as it stands (permeability 150 mD ...), and the new permeability raises LCOH by 0.888 EUR/MWh ... No simulation, costing or study was re-run for this answer".
- The case as it stands is 175 mD. The user gets a confident, wrong statement of the current case and stale numbers; nothing says the case changed. Run 30 s, so the speed looks good while the answer is wrong.
- The chips do say "Run the study again: The case changed after the study" (the project state knows), so code knows what the agents do not.

## Evidence

- `../evidence/QA-266/266b7476-1fed-469c-a14e-746d753cbb19.log.json`: coordinator step 1 (its route and task), analysis_lead step 1 (no tool call, its finish).
- `GET /design/case?project=35a70dbe...`: version 5, permeability 175 mD; the run's problem state still version 4 values.

## Cause

- The coordinator reads only the conversation and the chat's problem state; it is told nothing about a newer project case, so a repeated message reads as a repeated question. Its prompt even says to answer "what the conversation already says".
- The QA-224 fix loads a newer project case in `ProjectLead.forward`; the tool loop (analysis lead) has no such guard, and the analysis lead answered without `read_case`.

## Proposed fix

geomind:
- Load a newer project case into the chat's state by rule at the start of every run, before the coordinator (in `Run` / the loop set-up, not only in `ProjectLead.forward`), and put "Case changed since the last run: <paths>" into the problem state message the coordinator reads.
- `prompts/project/coordinator.md`: "A message that says the user saved or changed the case is an app event: `loop: project` with a task, never a repeat, whatever the conversation says."
- `prompts/analysis/lead.md`: a question about the case "as it stands" reads `read_case` (cheap) before it answers from earlier results.

## Fix

- 2026-11-05 18:56 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest
- 2026-11-05 18:58 UTC (19:58 CET), QA-AI-case-I, project QA-TEST QA-AI-case-I 8 (8b943903-52a4-4f0d-836f-e4150a8320ff), chat 485a131e-a87d-4339-bc82-cd120c8e5005: after the 150 mD flow (QA-227 retest, run 8b7f20e7) the case was saved by hand a second time, 150 -> 175 mD (case version 5), and the same message sent; run 64913dcb-62c3-4fb6-a244-57ca88654ab2 (geomind 0.4.114, 18:47:47-18:53:38 UTC). The coordinator routed it with "The project's saved case differs from the chat's case ...: 150 mD -> 175 mD. Load it ... earlier results are of the old case"; the project lead loaded it (card "Load the project's saved case, version 5: 150 mD -> 175 mD"), the design lead re-simulated design/HackathonPlant (result/06d7a6ba5b4bdd0a), the reviewer checked it, the economist compared 175 vs 150 mD, and the answer says "LCOH ... from 44.6406444200559 to 44.13359336933912 EUR/MWh", feasible. Not reproduced: the answer is on the 175 mD case. 5 min 51 s, 0.030 USD. Evidence: `../evidence/QA-266/run-64913dcb.json`. (Deployed now: Version: 0.4.130.)
