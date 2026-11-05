# QA-160: Flow limit 50-300 m3/h becomes two requirements (max_production_flow, min_stable_flow): the geoscientist proposes two, the case lead keeps them, the prompt says ONE with min and max

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 16:54 UTC |
| Versions | backend 1.1.102 (geomind 0.4.98) |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 1 (23e6faf0-7fa0-450b-860e-16cfe5fdd91b); run f5f86362-4596-4264-b00a-8c26e5adc5f3; geoscientist (Geoscientist IV) step 3, case_lead step 12 |
| Fixer | |

## Steps

1. Run 1 of QA-AI-case-I: competition files, one chat request to set the case.
2. Read the requirements of the stored case (`GET /design/case?project=...`).

## Expected

`prompts/case/lead.md`: "A range the brief gives with both ends (a flow of 50 to 300 m3/h) is ONE
requirement with `min` and `max`, never two." Reference `gemini/examples/hackathon_2026/case.json`:
one `production_flow_range` {on doublet, quantity production_flow, over each, when running, min 50,
max 300, unit m3/h}.

## Actual

- Geoscientist IV (requirements brief) proposes two values, `requirements.max_production_flow`
  (max 300) and `requirements.min_stable_flow` (min 50), each with its own requirement object
  (evidence file).
- The case lead's `set_case(requirements=...)` (step 12, 16:54:19) keeps both; the case holds 9
  requirements instead of 8.
- The check is the same in gemini, so results do not change, but the verdict and the report show two
  rows for one hard rule of the brief, and the rule of the prompt is broken.
- Also seen in the same findings: Geoscientist IV proposes `annual_operation` as min = max = 330 d
  ("exact"), the lead sets max 330 only (right); the geoscientist prompt has no requirement rules.

## Evidence

- `../evidence/QA-160/geoscientist-IV-flow.json` (the two proposals)
- Full run log: `../evidence/QA-153/run-f5f86362.json`

## Cause

The requirement rules (one range = one requirement; durations; counts) are only in
`prompts/case/lead.md`. `prompts/case/geoscientist.md` has none, and the lead's brief to
Geoscientist IV did not copy them; the lead then merges the findings without applying its own rule.

## Proposed fix

- geomind `prompts/case/geoscientist.md`: add the requirement rules (a range with both ends is ONE
  requirement with `min` and `max`; days are a duration, `when: running`; a count has no
  `over`/`when`/`unit`), or have the lead's brief for the requirements group always carry them.
- geomind `prompts/case/lead.md`, merge step: "merge requirement proposals on the same `on` and
  `quantity` into one with `min` and `max`".

## Speed and accuracy

Accuracy: 9 requirements vs 8 in the reference (the extra two supply-temperature requirements are
by the prompt's rule; the flow split is not). No speed effect.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
