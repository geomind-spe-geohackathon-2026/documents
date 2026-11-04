# QA-007: ask_economics fails again and again on a different check each time

| Field | Value |
|---|---|
| Status | open |
| Severity | blocker |
| Area | geomind |
| Reporter | Fatemeh (screenshots), Claude (write-up) |
| Found | 2026-11-04 ~19:00 UTC |
| Versions | frontend 1.1.33, backend 1.1.14 (geomind 0.4.25) |
| Where | https://geomind.team/projects/886404e4-3b22-41bd-8986-1a8bc869e25e/assistant/chat/33c76f29-064f-4047-9926-ff8937beddf7; economics question, retries after QA-004 |
| Fixer | |

## Steps

1. Same run, after QA-004.
2. The case lead sends the question again.

## Expected

One retry that fixes what was refused, then the question.

## Actual

The retry puts `accounting.gwp.CH4` and `utilities.electricity.co2_intensity` in `open`; refused `unknown_name` (utilities.electricity.co2_intensity is a case value, not an economics key). The same refusal came at least twice in a row; the run may stop on "the same call failed N times".

## Evidence

- No screenshot yet; the run JSON goes in `../evidence/QA-007/` once the run ends.

## Cause

Guess: (a) the tool cannot drop the GWP row's unit (QA-004); (b) the check before asking misses gemini's refusals; (c) the case lead puts a non-economics key in `open`; the tool could drop such a key with a note instead of refusing the whole question.

## Fix

## Retest
