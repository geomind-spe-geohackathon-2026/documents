# QA-183: Approval card of patch_plant with the change list says 'Change 0 value(s) of design/... : .' although the call changes 10+ values

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | geomind,backend |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 17:14 UTC |
| Versions | backend 1.1.104 (geomind 0.4.98, gemini 0.6.17) |
| Where | https://geomind.team/projects/fcc641c0-0119-4182-9a72-adce5a17b3ed; run d4ab496f-4a1f-43fa-b760-0f550fda0714 (hackathon report run) |
| Fixer | hotfix-python-VIII |

## Steps

1. Design stage: the design lead calls `patch_plant` with the change list form (`changes: [{path, value, source, reason}, ...]`, new in 0.4.96 QA-145).
2. The approval card opens.

## Expected

A first sentence like "Change 12 values of design/hp_2500 and save it as 'hp_2500_filled': d0.depth, d0.drainage_radius, ...".

## Actual

"Change 0 value(s) of design/hp_2500 and save it as 'hp_2500_filled': ." (requests request-1088 and request-1095). The JSON below shows 10+ changes.

## Cause

Guess: the one-sentence summary of QA-121 counts the changes of the old mapping form only; the list form of QA-145 gives 0 and no paths.

## Fix

## Retest
