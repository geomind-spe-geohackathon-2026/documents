# QA-312: Chat cannot make a result the project plant: 'Use the best design as the project plant' ends after 9 min (96 calls, 45 search_rag/read_knowledge) with 'no tool registers a stored design as a plant version; use the Plant page'

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | geomind,backend |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 19:05 UTC |
| Versions | backend 1.1.115+ (after QA-237's backend part, 1.1.110) |
| Where | project `QA-TEST QA-E2E-study-I 3` (ac687987-8bfe-452f-8013-7a4b577a3655); chat 00be49e5-9d56-4c05-8dc3-40f2a0a1d919; run 9a45c7ce-e328-403e-839e-e89d20fb4e95 |
| Fixer | hotfix-python-lead-II |

## Steps

After an optimisation in the same chat (study/lcts_best), ask: "Use the best design from the
optimisation as the project plant, then simulate January 2027 only and tell me the peak boiler load
that month." Approve the card.

## Expected

The chat does what the Results page button "Use this design as the plant" does
(`POST /design/results/{id}/adopt`): a new plant version, said in the answer (with one approval
card "this becomes the project plant").

## Actual

- The design lead searches how for most of the run: 24 search_rag, 21 read_knowledge, 7 read_skill,
  16 read_stored; patch_plant refused once for a reserved name "v<N>", then patch_plant
  'LctsBestPlant' (approval card "Change 1 value(s) ... name") stores a chat design only.
- Answer: "The project plant was not changed — this is open ... No tool in the design team's set
  registers a stored design as a project plant version ... Registering it needs the project/plant
  page". Plant versions stay 1, 2.
- 9 min 05 s, 63 steps, 96 calls, 2.41 M input tokens, 0.047 USD.
- The January part is fine: peak boiler 17.64 MW (equal to the whole-year peak 17.636 MW of the same
  design, which falls on a January day). The window "2027-01-01 to 2027-02-01, 32 steps" counts one
  day of February.

## Evidence

Run log: `../evidence/QA-312/run-9a45c7ce-log.json`.

## Cause

Fact: since backend 1.1.110 (QA-237) an agent's build/patch is no longer saved as a plant version and
only the page's adopt or save changes the project plant; no agent tool calls adopt.

## Proposed fix

geomind + backend: an `adopt_result` (or `save_plant_version`) tool for the design lead, effect
write, approval card "Make <design> the project plant (new version N)"; the project lead routes
"use / adopt / make this the plant" to it directly. Simulate windows: end date exclusive or say
"31 days".

## Fix

Backend backend part 1.1.122 (Workspace.save_plant_version), hotfix-back-lead-II.

- 2026-11-05 19:12 UTC: geomind main 71d80ab (0.4.131+), gemini dev 5782a138 (0.6.27); QA-312 also needs back-lead's DatabaseWorkspace.save_plant_version
## Retest

Chat: 'make this result the project plant', approve: a new plant version appears.

- 2026-11-05 19:52 UTC: QA-E2E-study-II 2026-11-05 retest in QA-TEST QA-E2E-study-II 1 (geomind 0.4.130 era, deploy 36): 'Use the optimised design as the project plant' = 1 approval card, 3 steps, 0.003 USD, new plant version v3 on the Plant page. See QA-330 for adopting a comparison design
