# QA-079: The same case and cost questions are asked three times in one run although the user answered each time

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | frontend |
| Reporter | functional-qa-2 |
| Found | 2026-11-05 04:49 UTC |
| Versions | frontend 1.1.71, backend 1.1.69-1.1.71 (geomind 0.4.65) |
| Where | https://geomind.team/projects/aa8023ca-33b3-4e5a-a7ea-5afad6ed4c1e/assistant/chat/f349646d-953b-41c5-a349-09903a5e29c5; project QA2 functional-qa-2 economics; run 6921d00e-f1ba-49e0-9be6-92c85ad4a2c6 |
| Fixer | hotfix-front |

## Steps

1. New project, three competition files attached, Auto-approve on; ask for the case, design, simulation and full economics.
2. Answer the case-lead question (air, return temperatures, gas, grid limits) with assumptions and "unknown", then "approve all" for the two derived values, then answer the economics question (approve rows, chiller price unknown, no subsidy).
3. Look at the chat after the run.

## Expected

A question the user answered is not asked again in the same run (QA-009, QA-061).

## Actual

The chat lists "You answered" three times each for the same three questions in the same order: (a) the case values, (b) "approve all", (c) the economics rows. I had to answer all three questions three times (9 answers) in one run before the design stage ran. The same run later failed (QA-078). Related: QA-009 (fixed), QA-061.
## Evidence

- ![screenshot](../evidence/QA-079/1.png)
- Run JSON: `../evidence/QA-079/run-6921d00e.json`

## Cause

Guess: the nested leads (case_lead, design_lead) restart and re-ask because the answer is not carried into their own context, or the restart after the 30-step continue replays the questions.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 04:51 UTC: hotfix-python-II: not geomind. run_events of 6921d00e: case_lead made exactly 3 requests (seq 239, 281, 316, 04:20-04:22), each once; the only later request is the design lead's (seq 2074). The chat shows each answered question three times: a display of the answers/requests, for hotfix-front. The run's failure is QA-078 (fixed in geomind 0.4.68).
- 2026-11-05 05:05 UTC: not re-asked: events of 6921d00e have each request once (239, 281, 316) and one answer each. The chat showed each answer twice (steps log + decision list) and a third time in the tester's live view. frontend 1.1.76 (bbe626c) shows each once; pushed, build checked, deploy at 05:30 UTC
## Retest

(Who, when, result.)
