# QA-204: Next-step chips: when the project lead passes one suggestion to finish, the user sees only that one chip; the stage's other steps are dropped

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 17:20 UTC |
| Versions | backend 1.1.104 (geomind 0.4.98, gemini 0.6.17) |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 1 (35a70dbe-5e24-4f51-9c6f-50e06d47fe82); chat 134dae07-2e37-4a3a-ae0b-83b5e812017e; run 86524c16-1492-497e-baa1-1e9a8b9b6fc8; project_lead step 2 (finish) |
| Fixer | |

## Steps

1. Project with the reference case and HackathonPlant, already simulated, reviewed and costed in this chat.
2. Message: "Write a short handover summary of this chat for a colleague who takes over tomorrow: what was checked, the key numbers, and what is still open."
3. Read the assistant message's `suggestions` (`GET /assistant/chat/{id}/messages`).

## Expected

Three next steps. `prompts/project/lead.md` says the code chooses up to three from where the work stands and the lead passes `suggestions` "only to fit them to this answer: reword or reorder them, or replace one with another step". So a lead that proposes one step replaces or rewords one chip; the other two stay.

## Actual

One chip only: `[{"label": "Optimise the plant", "message": "Optimise HackathonPlant: reduce bought electricity and the heat pump/boiler split, keeping all requirements met."}]`. The stage's own steps (`Write the report`, `Explain the results`, `Sensitivity analysis`, given after the run before) are gone. The earlier run b57abc5b... passed three and showed three.

## Evidence

- `../evidence/QA-204/86524c16-1492-497e-baa1-1e9a8b9b6fc8.log.json`: project_lead step 2, `finish` input `suggestions` with one item (step `optimise`).
- Messages of chat 134dae07...: last assistant message `suggestions` has one item; the one before (tool loop, run 79d35e37...) has three stage steps.

## Cause

`geomind/geomind/tools/suggestions.py` `next_steps`: `kept = checked(proposed, steps)`; `if kept: return [item for _, item in kept]`. Any non-empty kept list replaces the whole stage list; nothing fills it up to `MAX_SUGGESTIONS`. Also the `finish` docstring says suggestions are "in the user's language", while the module and the lead prompt say English only (Sahand, 2026-11-04).

## Proposed fix

geomind `tools/suggestions.py` `next_steps`: after `checked`, append the stage's own steps whose `step` is not already kept (`shown(step, label)`) until there are `MAX_SUGGESTIONS`. Fix the `finish` docstring to "in English". Unit test: one proposed step gives three chips, the proposed one first.

## Fix

- 2026-11-05 18:58 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest

## More evidence (QA-AI-project-I, 17:57 UTC)

Run 194c3879-076e-4e3a-b6bf-8f54da25a7ae (same chat, case changed by hand): the lead passes two suggestions and the user sees two. One of them has a label that does not match its message: label "Compare 100 vs 400 mD", message "Show the full sensitivity table of the new study on the current case, with each driver's effect on LCOH, LCOC and LCTS." `_fits` checks only length and script, not that the label names the message's action; a fix could keep the code's own label for a known `step` and let the lead change only the message.
