# QA-069: Case lead reports the case complete while site.air.pressure is unset; the design stage then blocks and asks the user again

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | functional-qa-I |
| Found | 2026-11-05 00:25 UTC |
| Versions | frontend <x.y.z>, backend <x.y.z> (geomind <x.y.z>) |
| Where | project 2cc9eadb (QA2 qa-func-3 economics), chat 63c70b89; found by qa-func-3-II, filed from its notes (no evidence file saved) |
| Fixer | hotfix-python |

## Steps

1. New chat with the PDF and both CSVs; let the case lead finish.
2. Continue into the design stage.

## Expected

The case lead's completeness check asks for air pressure (or elevation) before it reports the case done.

## Actual

The case lead reported the case complete; the design stage then blocked on site.air.pressure and asked the user again. Source: .claude/notes/qa-round-2/qa-func-3.md. Not reproduced by functional-qa-I (there the air question came during the case step).
## Evidence

- ![screenshot](../evidence/QA-069/1.png)
- Run JSON: `../evidence/QA-069/run-<id>.json`

## Cause

`gm.case.missing` lists only what the case file needs by itself; a value a plant needs from the case (`site.air.pressure` for every plant of the hackathon example) is named only by `gm.check(plant, case)`, which the case lead never ran, so the case looked complete to it (checked: the hackathon case without pressure gives no missing path, and gm.check of each of its six plants names site.air.pressure).

## Fix

`set_case` now checks the stored case against each of the project's plants (`gm.check`) and returns `plants_need` `[{path, message, plants}]` with a note; the case lead's checklist calls the case complete only when it is empty or each path was asked in the one confirmation question. A project with no plant file gets no such check (the design stage still names the value). geomind 0.4.62 (commit 7a71ecc, tag v0.4.62), backend 1.1.64 (ae8e646), deployed 2026-11-05 01:06 UTC by hotfix-python-II.

## Retest

(Who, when, result.)
