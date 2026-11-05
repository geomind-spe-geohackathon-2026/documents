# QA-271: Case lead's system prompt is 42-46k characters (~15k tokens, its Rules section 27k), re-sent on every call: 33% of the case lead's input tokens; speed, see QA-150

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | speed-analysis-II |
| Found | 2026-11-05 18:22 UTC |
| Versions | backend 1.1.105+ (geomind 0.4.102-0.4.118) |
| Where | api.geomind.team run logs (`GET /assistant/runs/{id}/log`, llm_calls[].messages): full case runs 679f3555, dd6b4700, c17ca5fb, 6a8dba9a and the economics case runs of QA-E2E-economics-I 3-5 |
| Fixer | |

## Steps

1. Run a full case from the three hackathon files (QA-AI-case-I / QA-E2E-case-I prompt).
2. In the run log, measure the messages of each case_lead model call by part.

## Expected

The case lead's system prompt holds the role, the decision order and the hard rules (a few k tokens); the detail lives in handbook-case and the setting-the-case skill and is read once when needed.

## Actual

The case lead's first system message is 41.9-45.6 k characters (about 15 k tokens): `## Rules` 27.2 k, `## Case keys` 9.8 k, `## Rules for every agent` 2.3 k, `## Tools` 0.9 k. It is re-sent on every one of ~36 calls per case run: 3.09 M of the 9.23 M input tokens (33.5%). The geoscientist's system prompt is 20 k characters, 39% of its input. Halving the Rules section would cut ~17% of the case lead's input, ~1.5 s per call at the measured rate (9.6 s per call, 44 k input median).

## Evidence

- Analysis: `documents/project/plans/speed-case-plant-baseline-0.4.10x.md`, section 'Case stage: prompt size'; script `documents/project/plans/speed-baseline-scripts/prompt.py` (`python3 prompt.py <data dir> case_lead`).
- Measured over 215 case_lead calls (9.23 M input tokens, mean 42.9 k per call; 75% served from the prompt cache) and 62 geoscientist calls in 11 case runs, group B.

## Cause

Fact: the Rules section has grown with each case fix (QA-157, QA-177, QA-198, QA-200 ...). Fix: move the rules that are only needed at one step (economics, requirements, time zone, ISA pressure) to handbook-case sections or the setting-the-case skill; keep the decision order and hard rules; check QA-177's contradictions in the same pass.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
