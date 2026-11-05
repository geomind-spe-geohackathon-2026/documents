# QA-325: Report does not say what the checks cover: 12/12 pass reads as full validation, but there is no reservoir pressure, injectivity or long-term thermal breakthrough check (one-year run)

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | backend |
| Reporter | Sahand (reviewer notes), Manual QA-IV |
| Found | 2026-11-05 19:23 UTC |
| Versions | backend 1.1.118 (geomind 0.4.130, gemini 0.6.26) |
| Where | report of result 54b2e4f4 (B_r1_best, project 0b986dd6) and result 8878eafd (no-agent, project 8d5d21e0); reviewer notes from Sahand 20:20 CET |
| Fixer | |

## Expected

Next to 'All N checks pass' the report says what was checked and what the model does not check (one simulated year: no reservoir pressure decline over the lifetime, no thermal breakthrough, injectivity only as modelled), so a judge does not read it as full subsurface validation.

## Actual

'12 passed, 0 failed, 0 not assessed' with no scope; the reviewer read it as complete validation.

## Fix

## Retest
