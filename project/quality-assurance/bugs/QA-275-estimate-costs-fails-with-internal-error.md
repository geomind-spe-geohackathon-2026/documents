# QA-275: estimate_costs fails with internal error AttributeError 'str' object has no attribute 'get' (tools/gemini/assessment.py:227) on a ranked design's result; the answer has no NPV and no payback

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 18:27 UTC |
| Versions | backend 1.1.108-1.1.11x during the run (geomind main 6724bdf at report time) |
| Where | project `QA-TEST QA-E2E-study-I 2` (8eabf827-1f43-4cf8-86a4-39147bea32a0); chat ae934804-eca5-4b3c-99a7-dd60665b5ee9; run 83182f0e-8ee2-4230-a98f-8f0bc905caf3 |
| Fixer | |

## Steps

Seeded project (reference case.json + economics.json, which the case names as a file; plants v1, v2).
Chat chip "Optimise the design" ("Optimise the design and simulate the best one."); deny the first
build_plant with a reason; approve the rest. The design lead ranks design/best and
design/familyB_v2 with run_study (18:16:41); the explainer costs the winner.

## Expected

estimate_costs returns capex, opex, lcoh/lcoc/lcts, NPV and payback for result/e1a512f49e3d5e00.

## Actual

18:19:02 explainer estimate_costs {"reference": "result/e1a512f49e3d5e00"} -> internal error:
"estimate_costs: internal error AttributeError: 'str' object has no attribute 'get' at
gemini/assessment.py:227; a bug of the tool or gemini". The final answer: "NPV and payback are not
available: the cost tool returned an internal error on this result".

## Evidence

Run log: `../evidence/QA-276/run-83182f0e-log.json` (shared with QA-276), step at 18:19:02.

## Cause

Guess: `changed_keys` (geomind/tools/gemini/assessment.py, near line 227 of the deployed version)
compares the economics the run ran on with the current case's; the case names its economics as a
file ("economics.json", a str) on one side and a dict on the other, and a nested `.get` is called
on a str. The result comes from run_study (a ranked study), whose economics may be stored as the
file name.

## Proposed fix

geomind assessment.py: resolve an economics file name to its dict before comparing (or treat a str
vs dict as "the same file" when the file's content equals the dict); add a unit test with a case whose
economics is a file name and a result from run_study.

## Fix

- 2026-11-05 19:00 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest
