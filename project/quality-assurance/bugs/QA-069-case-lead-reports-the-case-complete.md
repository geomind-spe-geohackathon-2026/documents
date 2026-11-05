# QA-069: Case lead reports the case complete while site.air.pressure is unset; the design stage then blocks and asks the user again

| Field | Value |
|---|---|
| Status | fixing |
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

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
