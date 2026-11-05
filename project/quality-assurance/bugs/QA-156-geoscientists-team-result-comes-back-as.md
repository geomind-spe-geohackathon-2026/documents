# QA-156: Geoscientists team result comes back as a 684-character outline; the case lead needs 5 read_stored calls in 3 extra steps to read the findings

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 16:53 UTC |
| Versions | backend 1.1.102 (geomind 0.4.98) |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 1 (23e6faf0-7fa0-450b-860e-16cfe5fdd91b); run f5f86362-4596-4264-b00a-8c26e5adc5f3; case_lead steps 3-6 |
| Fixer | |

## Steps

1. Run 1 of QA-AI-case-I (competition files, one chat request to set the case).
2. Read the run log: the case lead's `geoscientists` call (step 3) and the next steps.

## Expected

`CaseLead` builds the member as `Delegate(Geoscientist(), max_summary_tokens=FINDINGS_TOKENS)` with
`FINDINGS_TOKENS = 8000` ("The most tokens of the geoscientist's findings the case lead reads
back"). The lead should get the four findings (each about 2-4 k tokens) in the `geoscientists`
result and merge them in the next step.

## Actual

- Step 3 (16:52:00): `geoscientists` with 4 briefs, 57.7 s. Its output is
  `{"note": "read_stored(reference)", "summary": "{\"Geoscientist I\": \"{\\\"values\\\": [... …",
  "reference": "result-634981c8fa3ab7b2"}`: the summary is 684 characters, about 150 per instance,
  cut in the middle of the first value.
- Step 4 (16:53:19): `read_stored(result-634981c8fa3ab7b2)` -> only the 4 keys and "too long to show whole".
- Step 5 (16:53:21): `read_stored(finding-aebabf16)`, `read_stored(finding-46ce72d9)`.
- Step 6 (16:53:22): `read_stored(finding-3da2fbe9)`, `read_stored(finding-ceab470c)`.
- Cost: 3 extra LLM round trips (5.3 s LLM, 116 k input tokens), on every case run.

## Evidence

- `../evidence/QA-156/team-call.json` (steps 3-6 with timing, tokens and outputs)
- Full run log: `../evidence/QA-153/run-f5f86362.json`

## Cause

The `Team` tool (`geomind/tools/delegate.py`) returns `{instance: answer}` for all briefs. That dict
goes through the generic large-result store (`geomind/tools/stored.py`, `stored_form` /
`outline`, `SUMMARY_CHARACTERS = 600`, `SMALL_CHARACTERS = 150`), so each member's
`max_summary_tokens=8000` is never applied to the team result. (Read from the code and the log.)

## Proposed fix

geomind, `tools/delegate.py` `Team`: return each instance's answer within the member's
`max_summary_tokens` (sum of the members' budgets for the whole result) and mark the team result as
not to be outlined by `stored_form` when it fits that budget; or give `Team` a `max_summary_tokens`
(8000 per instance for the geoscientists). Keep the reference for the full findings.

## Speed and accuracy

Speed only: about 5-6 s and 116 k input tokens per case run. No accuracy effect: the lead read all
four findings by hand.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
