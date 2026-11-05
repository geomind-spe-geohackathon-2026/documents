# QA-317: Reviewer rejects a feasible design because the case 'differs from the one the user gave' although the user approved every case change (economics, requirements) by card; the run ends recommending none and fails on update_state '/design/reference'

| Field | Value |
|---|---|
| Status | fixing |
| Severity | blocker |
| Area | geomind |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 19:14 UTC |
| Versions | backend 1.1.118 (geomind 0.4.130, gemini 0.6.26) |
| Where | run bfcec811-c5ad-496e-a829-6ec44de3251c (hackathon report run II), project 0b986dd6-8f95-4383-9d15-5e589ff122c9; ended failed 20:13 CET |
| Fixer | hotfix-python-lead-II (m5) |

## Steps

1. Case stage: the case lead asks the user to approve the Knowledge values, the requirement tolerances and the economics; the user answers "approve all" each time and approves every set_case card (requests 302, 350, 367, 406).
2. Design: family B is optimised; gemini's verdict on result/fdade671505ff209 is feasible, 12/12 checks, LCTS 29.55 EUR/MWh.
3. The reviewer verifies it.

## Expected

Verified; the comparison recommends B; the run ends done with the answer.

## Actual

The reviewer rejects B: "the case differs from the one the user gave (the economics file, and the requirements brine_cooling_limit, cold_delivered, ... were all added); the user must approve that change, or the case goes back with set_case(source='origin')". The comparison driver then answers "No family produced a verified design ... I recommend none." The project lead then fails on `update_state: path = '/design/reference'; 'reference' does not exist there` (run status failed, error geomind_refused). 96 min, 0.36 USD, no answer for the user.

## Cause

Guess: the reviewer compares the case with the 'given' origin (the files) through case_changes, and does not know that these changes were approved by the user in the case stage (the approvals are on the set_case cards and the ask_user answers). The approval of case changes must be recorded (for example in the problem state or on the case version) and the reviewer must accept approved changes. Second bug: the project lead's update_state on /design/reference after a "recommend none" (speed baseline cause 9) ends the run as failed instead of answering.

## Evidence

- Run log export: scratchpad copy; the comparison driver's final answer quotes the rejection.

## Fix

## Retest
