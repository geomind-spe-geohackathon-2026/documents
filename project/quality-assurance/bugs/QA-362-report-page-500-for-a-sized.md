# QA-362: Report page 500 for a sized/study result: document.study_origin calls title_of(objective) with objective None (backend core/gemini/evaluate.py:42 name.replace)

| Field | Value |
|---|---|
| Status | open |
| Severity | blocker |
| Area | backend |
| Reporter | Sahand (screenshot), Coordinator-V (log) |
| Found | 2026-11-05 21:49 UTC |
| Versions | live 2026-11-05 22:49 Trondheim |
| Where | Design > Report, 'Draft from b_sized'; POST /api/v1/reporting/design/preview 500 (21:48:57 and 21:49:00 UTC) |
| Fixer | |

## Steps

1. Open Report for a project whose result is a sized/study result (b_sized).

## Expected

The report renders; a study with no objective (a sizing or plain study) says so instead of naming an objective.

## Actual

'internal - Internal server error' (screenshot). Traceback: services.py:191 findings -> document.studies (document.py:984) -> study_origin (document.py:1178) -> gemini_evaluate.title_of(objective) -> evaluate.py:42 `name.replace` with name None.

## Evidence

- ![screenshot](../evidence/QA-362/1.png)
- geomind-fastapi log, AttributeError: 'NoneType' object has no attribute 'replace'

## Cause

study_origin builds 'with the objective ...' even when the study has no objective (sizing). Fix: skip the objective clause when objective is None (and make title_of tolerate None). Likely from the QA-313 report rework. Sahand's bug: top.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
