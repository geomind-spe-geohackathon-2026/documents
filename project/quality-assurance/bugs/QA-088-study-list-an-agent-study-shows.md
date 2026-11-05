# QA-088: Study list: an agent study shows done but has no result (Progress '-', Results tab empty)

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | backend |
| Reporter | Sahand |
| Found | 2026-11-05 09:07 UTC |
| Versions | frontend 1.1.77, backend 1.1.79 (geomind 0.4.73) |
| Where | geomind.team/projects/df514ce2-1d5b-4681-a7e6-5592cc5eac30/design/study?chat=138c18fa-3751-4f74-a76e-b52cbd1105ef; project QA2 functional-qa-2 economics B; study filters_sized |
| Fixer | hotfix-back |

## Steps

1. Let the agents run a study in a chat (here the design team ran `filters_sized`).
2. Open Design > Study, then Results.

## Expected

A done study shows its result in the list (a short summary: feasible or not, the main metrics) and
the Results tab shows its results.

## Actual

The study list shows `filters_sized` with Progress '-', Status done, Result only an 'Open run' link;
the Results tab is grey (no results). Sahand: "why do the studies seem to have no results".

## Evidence

- ![screenshot](../evidence/QA-088/1.webp) (Sahand)

## Cause

Guess: agent studies keep their result in the chat artifact `study/<name>.result` (hotfix-back,
QA structures view), while the study list and the Results tab read only page studies'
`result.content`; or the study was a sizing step with no run.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
