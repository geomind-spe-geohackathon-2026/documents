# QA-151: Task: improve handbook-design.md for design accuracy and fewer re-reads

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | Coordinator-V |
| Found | 2026-11-05 16:51 UTC |
| Versions | frontend 1.1.113, backend 1.1.101 (geomind 0.4.97, gemini 0.6.16) |
| Where | Task (Sahand 2026-11-05 16:51 UTC); Knowledge file handbook-design (id 6d617b90), source `documents/project/quality-assurance/inputs/handbook-design.md` and geomind `handbook-design.md` |
| Fixer | |

## Steps

1. Read the design runs and the findings of QA-AI-design-I and QA-E2E-design-I.
2. Improve handbook-design.md: clear design path, competition hard limits (1-3 doublets, 50-300 m3/h, <=40 K, 100 C / 20 C supply), sizing rules, when to simulate, what not to re-read.
3. Re-upload it to Knowledge and note the new id in STATUS.md.

## Expected

The design team reaches a valid plant that meets the hard limits in fewer steps and with accurate sizing.

## Actual

Design runs are slow and patch by hand (QA-145); handbook last updated 18:10 UTC 2026-11-04 (ch 0 design path).

## Evidence

See Where.

## Cause

Guess: the handbook lacks concrete sizing rules and a fixed order of steps.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
