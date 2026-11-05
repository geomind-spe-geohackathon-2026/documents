# QA-157: Case lead's final checklist reads the case 6 times in 5 steps (one refused as a repeat): 33 s and 270 k input tokens; the prompt asks for one read_case

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 16:57 UTC |
| Versions | backend 1.1.102 (geomind 0.4.98) |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 1 (23e6faf0-7fa0-450b-860e-16cfe5fdd91b); run f5f86362-4596-4264-b00a-8c26e5adc5f3; case_lead steps 21-26 |
| Fixer | |

## Steps

1. Run 1 of QA-AI-case-I (competition files, one chat request to set the case, approve all).
2. After `ask_economics` is approved, read the case lead's last steps in the run log.

## Expected

`prompts/case/lead.md` step 6: "`read_case` once more, the checklist, then `finish`" and "Checklist
before you hand over (`read_case` once more)". One step, then `finish`.

## Actual

| Step | Time | LLM s | Input tokens | Call |
|---|---|---|---|---|
| 21 | 16:56:45 | 5.0 | 53.9 k | `read_case()` whole case (economics included) |
| 22 | 16:56:50 | 2.5 | 53.3 k | `read_case(section="economics")` |
| 23 | 16:56:53 | 6.6 | 55.5 k | `read_case(section="site")`, `read_case(section="demand")` |
| 24 | 16:56:59 | 5.1 | 53.4 k | `read_case(section="utilities")`, `read_case(section="time")` |
| 25 | 16:57:05 | 6.7 | 53.6 k | `read_case()` again: refused by the repeat guard ("the same call as step 21") |
| 26 | 16:57:11 | 12.4 | 53.8 k | `finish` |

Every answer text says the same thing ("The case and economics are set. Let me do the final
checklist read."). Steps 22-25 add nothing: 26 s and about 216 k input tokens for nothing. Then the
project lead reads the case again (`read_case(section="site")`, `case_changes`) before `accept_case`.

## Evidence

- `../evidence/QA-157/steps-21-26.txt`
- Full run log: `../evidence/QA-153/run-f5f86362.json`

## Cause

The model does not trust a whole `read_case` (its output may be stored and outlined when long, so
it re-reads by section), and the prompt names the checklist as a separate read. Guess: the whole
case output is long (economics inline) and comes back partly outlined.

## Proposed fix

- geomind `prompts/case/lead.md`: "Step 6 is ONE `read_case()` call in the same step as nothing
  else; check the list against that output and call `finish` in the next step. Never read a section
  you just read whole."
- geomind `agents/case/lead.py`: after a whole `read_case` that follows `ask_economics`, refuse a
  further `read_case` once (like the repeat guard, but for section reads of a case not changed
  since).
- Optional: `read_case` returns the case without the economics block unless asked (smaller
  output, fewer re-reads).

## Speed and accuracy

Speed: 26 s and ~216 k input tokens per case run (of 6 min 18 s and 1.61 M in total). No accuracy
effect.

## Reproduced

Run 2 (17:00-17:04 UTC, project QA-TEST QA-AI-case-I 2 cf19d767-b62b-4caa-a90e-4386e6e3c744, run 519ccc65-564e-4d1e-9139-a23777cd1107, backend 1.1.104, log `../evidence/QA-153/run-519ccc65.json`): case_lead steps 20-25 (17:03:36-17:03:54) are again checklist reads (`read_case` 9 times in the run), 18 s and ~315 k input tokens before `finish`.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
- 2026-11-05 17:35 UTC, QA-AI-case-I, run 3 (geomind 0.4.100, backend 1.1.104; project QA-TEST QA-AI-case-I 3 f400fa2d-292d-4358-b3c1-9f4a51f51f7f; run 84526204-bfb7-4611-a476-abde6317c58e; log `../evidence/QA-153/run-84526204.json`): still present (open): after `ask_economics`, steps 16-18 read the case 6 times (`read_case()` whole, then economics, site, demand, requirements, utilities) and one refused `read_stored(path='plants_need')`; 7 s here (fast LLM calls), 170 k input tokens.
