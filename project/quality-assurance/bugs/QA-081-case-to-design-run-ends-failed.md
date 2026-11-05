# QA-081: Case-to-design run ends 'failed' (internal error in geomind) after 68 min and 10.6M tokens at 05:25:47 UTC, minutes before the 1.1.73 deploy; no resume, no design; live step counter inflated (3757 steps, 7 study links vs 261 in JSON)

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | backend |
| Reporter | functional-qa-3 |
| Found | 2026-11-05 05:27 UTC |
| Versions | backend 1.1.72 (geomind 0.4.68, gemini 0.6.7) at the end; started under 1.1.69 (04:17 UTC); frontend 1.1.71 |
| Where | https://geomind.team/projects/932b318c-f285-4827-aefe-c8fa3327735b/assistant/chat/510ab94f-c4f7-4019-9f75-cb40229b374e; project QA2 functional-qa-3 studies; run bd7aa40e (started 04:17:25, ended 05:25:47 UTC) |
| Fixer | |

## Steps

1. New project (shared memory off), PDF + both CSVs attached, auto-approve on; send: build the case from the files and design the plant, run the GEMINI checks, explain each decision.
2. Answer the grouped case question (values unknown or assumptions), approve all on the two economics and requirement-change cards, answer the dew-point question ('unknown, leave open'), approve CO2 intensity 209.21 g/kWh (Ember row), then answer 'indoor 24 degC, 50 %, labelled assumptions'.
3. The run goes on for about 68 min and then stops.

## Expected

A stored plant and results, or a plain statement of what blocked it; a run cut by a restart resumes (QA-035) or says 'send your message again' (QA-025).

## Actual

- Chat ends with 'The assistant stopped with an internal error in geomind' (no detail). Run status failed, 261 steps in the JSON, 10,592,775 tokens in, 397,267 out, 0.29 USD, 4,103 s; no plant stored. Last step: design_lead step 17 (a patch_plant of `params.cooling_consumer.dew_point_margin` was refused with invalid_value, 'give it in the case'), the last LLM answer is cut mid-thought ('let me check whether gemini has a cooling consumer that runs without a latent-load check').
- The run ended at 05:25:47 UTC; backend commit for 1.1.73 is at 05:26 UTC and the API still reported 1.1.72 at 05:27:35 UTC. So a deploy restart may have killed it, but the run was not resumed and the text is not the QA-025 'send your message again'.
- The live chat at the moment of failure showed 'Worked through 3757 steps, 745 needed another try' and seven 'sized_v1' study links; after a reload it shows 440 steps / 83 retries and one 'sized_v1' (JSON: 261 steps). The live counter and study list are inflated by duplicates.
- Before that, with auto-approve ON, the chat still asked three times for the same case values and approvals (see QA-079); the repeated 'You answered: ...' line is shown three times in 'Steps so far'.
- Separate: demand.cooling.indoor_temperature and indoor_relative_humidity were asked for in the first question, then the agent said they were not needed, and asked again 40 min later as blockers.

## Evidence

- ![screenshot](../evidence/QA-081/1.png)
- Run JSON (gzip, 36 MB unpacked): `../evidence/QA-081/run-bd7aa40e.json.gz`; live view at failure: `../evidence/QA-081/live-3757-steps.png`

## Cause

Guess: the worker restart of the 1.1.73 deploy (05:26 UTC) ended the run as failed instead of resuming it (QA-035 regression), or the run hit an uncaught error after the refused dew_point_margin patch. The log of the worker at 05:25:47 UTC decides.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
