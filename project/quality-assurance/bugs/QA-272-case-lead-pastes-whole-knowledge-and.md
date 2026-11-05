# QA-272: Case lead pastes whole Knowledge and files into its context: search_rag gives 8 matches of up to 1.5k chars (the brief PDF it already read in every answer), read_rag reads both 365-row demand CSVs and the 20k assumptions document whole, twice: 26% of its input; speed, see QA-150

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

search_rag returns short snippets (a few hundred characters) and leaves out a project file the agent has already read in full; the lead reads the demand CSVs only as far as their header (set_case loads the series itself); a long Knowledge document is read by section.

## Actual

In 679f3555 the case lead: `read_rag` of GEMINI_Heating_Demand_Daily_2027.csv (8.0 k chars) and Cooling (7.8 k), later again with length 1200; the brief PDF (4.0 k) twice; knowledge/hackathon-2026-assumptions.md whole (20.5 k) twice; four `search_rag` calls of 8 matches each, ~1.1-1.5 k chars per match, ~12-13 k per call, every answer starting with the brief PDF's page 1 that is already in the context. Over group B: search_rag 24 calls (median 12.9 k chars, max 17.9 k), read_rag 39 calls (median 7.8 k, max 24.7 k). Knowledge and file text are 2.35 M of 9.23 M case_lead input tokens (25.5%), geoscientist 26.5%; each read stays in the context for the rest of the run.

## Evidence

- Analysis: `documents/project/plans/speed-case-plant-baseline-0.4.10x.md`, section 'Case stage: prompt size'; script `documents/project/plans/speed-baseline-scripts/prompt.py` (`python3 prompt.py <data dir> case_lead`).
- Measured over 215 case_lead calls (9.23 M input tokens, mean 42.9 k per call; 75% served from the prompt cache) and 62 geoscientist calls in 11 case runs, group B.

## Cause

Fix in geomind: search_rag snippet length and count (e.g. 4 x 400 chars) and skip files already read in this run; read_rag of a CSV returns head + shape unless asked for rows; the case prompt points to the assumptions document's sections (outline) instead of a full read.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
