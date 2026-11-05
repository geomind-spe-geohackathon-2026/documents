# QA-237: A comparison request silently switches the project's current plant: the design lead's build_plant of HackathonPlant (only to get a design reference) is saved as Plant version 5, replacing the optimised HeatingAbsorptionCoolingPlant

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind,backend |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 17:45 UTC |
| Versions | backend 1.1.106 (run), 1.1.108 (seen) |
| Where | project `QA-TEST QA-E2E-study-I 1` (8fcbf709-537a-40d9-ac1f-abadd1061775); run 52383511-cdea-47d7-8f61-4a1737248856, design_lead build_plant 17:30:36 UTC |
| Fixer | hotfix-back-lead |

## Steps

1. Project plant versions 1 HackathonPlant, 2 HeatingAbsorptionCoolingPlant; an optimisation run
   wrote 3 (baseline) and 4 (ranged2), both HeatingAbsorptionCoolingPlant: current = v4.
2. Chat: "Compare the two plants of this project ... Which one should we pick?" Approve the card
   "Allow build_plant (write)? Build plant 'hackathon_v1' with 23 modules and 39 connections".

## Expected

A comparison reads both plants and changes nothing; the current plant stays v4 until the user adopts
one ("Use this design as the plant" or a chat request to switch).

## Actual

Plant version 5 "Plant hackathon_v1 built by the assistant" (17:31:10 UTC) is now the project plant;
the Design header shows Plant Version 5 = HackathonPlant. The answer says "Recommendation: pick
HackathonPlant" but never says the plant was already switched. The approval card says "Build plant"
and nothing about replacing the project's current plant. The same happened in the optimisation run
(v3 "baseline", v4 "ranged2": two versions of an unchanged plant).

## Evidence

- Plant versions (API /plant/flowsheet/versions): 5 hackathon_v1 17:31:10, 4 ranged2 17:09:01,
  3 baseline 17:08:09, 2 and 1 seeded.
- Run log: `../evidence/QA-228/run-52383511-log.json` (build_plant at 17:30:36).

## Cause

Fact: every build_plant / set_ranges in a chat is stored as a new project plant version. Guess: the
design lead rebuilds a stored plant only to get a chat `design/<name>` reference (QA-152 / QA-221
workaround), and the backend saves each built design as the project plant.

## Proposed fix

backend/geomind: a design built only to read or compare a stored plant version is not saved as a new
project plant version (or the tools accept `plant_version` directly so no rebuild is needed); a
plant version is written only by an explicit change or adopt; the approval card says "this becomes
the project plant" when it does.

## Fix

hotfix-back-lead, backend 1.1.110 (tag v1.1.110), deployed 2026-11-05 ~17:50 UTC (backend part).
`adapters/versions.py` `VersionRecorder` no longer saves a design an agent builds, changes or
simulates as a plant version; the project plant changes only on an explicit save (Plant page) or
adopt (`POST /design/results/{id}/adopt`). Reverses 1.1.82 (QA-092). Agents still read the saved
versions. geomind part (no rebuild to read a version) with hotfix-python-lead.

## Retest

Recipe: A comparison or design run in chat; afterwards /plant/flowsheet/versions has no new version; adopting the result adds one.

QA-E2E-study-I, 2026-11-05 19:05 UTC: backend part passes. Project QA-TEST QA-E2E-study-I 3: optimisation (run 4885075b), comparison (run b709a671, 67 s, no rebuild) and an adopt-and-simulate request (run 9a45c7ce) wrote no plant version (still 1, 2). Side effect: the chat can no longer adopt at all; filed as a separate bug.
