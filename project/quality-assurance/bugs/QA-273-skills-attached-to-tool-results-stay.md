# QA-273: Skills attached to tool results stay in the case lead's context for the rest of the run: reading-results 38k chars on its first read_stored, finding-sources 18k, setting-the-case 10k: 15% of its input (geoscientist 25%); speed, see QA-150

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
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

A skill sent with a tool's first call is short and fits the agent (the case lead does not need the full reading-results skill for plant results), or it is dropped from the context after the step that used it.

## Actual

Skill text attached to tool results in the case lead's context: reading-results 37.9 k chars (sent with the first read_stored, which the case lead uses to read the geoscientists' findings), finding-sources 17.8 k (first list_files / read_rag / search_rag), setting-the-case 9.8 k (first read_case), web-search 5.3 k, calculator 4.1 k, working-in-a-team 3.5 k. Together 1.39 M of 9.23 M input tokens (15%); for the geoscientist 0.23 of 0.92 M (25%, setting-the-case and finding-sources).

## Evidence

- Analysis: `documents/project/plans/speed-case-plant-baseline-0.4.10x.md`, section 'Case stage: prompt size'; script `documents/project/plans/speed-baseline-scripts/prompt.py` (`python3 prompt.py <data dir> case_lead`).
- Measured over 215 case_lead calls (9.23 M input tokens, mean 42.9 k per call; 75% served from the prompt cache) and 62 geoscientist calls in 11 case runs, group B.

## Cause

Fact: skills are attached once per agent and tool and then stay in the message history. Fix: a case-lead form of reading-results (findings only) or a size cap per skill; drop a skill's text from later calls once the agent has acted on it.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
