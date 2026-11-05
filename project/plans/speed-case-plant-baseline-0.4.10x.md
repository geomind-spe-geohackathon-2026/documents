# Speed baseline, second run: geomind 0.4.96 to 0.4.118

Written by speed-analysis-II, 2026-11-05 (UTC times), for Coordinator-V and QA-150. Same method as
[speed-case-plant-baseline.md](speed-case-plant-baseline.md) (the first baseline: 41 runs, geomind
up to 0.4.95), which stays as the reference; see its "How to read the numbers". Read-only: only
GET calls; nothing was started, answered, cancelled or changed.

## Scope

- Every run that started on production after 16:36 UTC (geomind 0.4.96 live) and had ended by
  18:10 UTC: **50 runs** (49 QA-TEST runs of the QA threads, 1 other), in two groups:
  - **A**: started 16:36-17:21 UTC, **26 runs**, geomind 0.4.96 to 0.4.100 (backend 1.1.100-1.1.104).
  - **B**: started after 17:21 UTC, **24 runs**, geomind 0.4.102 to 0.4.118 (backend 1.1.105+).
- Correction: the first and second passes of this file (documents 0b6a45a, 4b07d27) saw only 9
  and 3 runs: `/workspace/projects` now pages by cursor (`next`, at most 50), and `fetch.py` read
  only the first 50 projects. `fetch.py` now follows the cursor (85 projects, 164 runs).
- The QA threads run single stages (a case, a design, a study, an economics question, a report),
  while the first baseline was dominated by long full design runs. Compare shares and per-run
  numbers, not totals.
- New since backend 1.1.99: every step has `ts`; gaps between steps are measured below.

## Totals per stage

Group A (0.4.96-0.4.100, 26 runs):

| Stage | Runs with it | Steps | Tool calls | Refused | Refused % | Active min total | Active min per run | Q cards | A cards |
|---|---|---|---|---|---|---|---|---|---|
| case | 10 | 327 | 523 | 37 | 7% | 52 | 5.2 | 3 | 16 |
| plant | 7 | 431 | 697 | 110 | 16% | 130 | 18.6 | 0 | 0 |
| sizing | 4 | 13 | 21 | 5 | 24% | 3 | 0.7 | 0 | 0 |
| simulate | 13 | 46 | 66 | 12 | 18% | 8 | 0.6 | 0 | 0 |
| other | 26 | 749 | 1343 | 166 | 12% | 114 | 4.4 | 1 | 1 |

Group B (0.4.102-0.4.118, 24 runs):

| Stage | Runs with it | Steps | Tool calls | Refused | Refused % | Active min total | Active min per run | Q cards | A cards |
|---|---|---|---|---|---|---|---|---|---|
| case | 11 | 277 | 417 | 44 | 11% | 47 | 4.3 | 5 | 12 |
| plant | 7 | 279 | 476 | 42 | 9% | 59 | 8.4 | 1 | 0 |
| sizing | 3 | 12 | 12 | 3 | 25% | 1 | 0.5 | 0 | 0 |
| simulate | 10 | 28 | 39 | 3 | 8% | 3 | 0.3 | 0 | 0 |
| other | 24 | 568 | 1010 | 68 | 7% | 84 | 3.5 | 2 | 1 |

All calls: A 2650 calls, 330 refused (12%); B 1954 calls, 160 refused (8%). First baseline: 8914, 1525 (17%).

## Compared with the first baseline

| Measure | First baseline (<= 0.4.95) | A (0.4.96-0.4.100) | B (0.4.102-0.4.118) |
|---|---|---|---|
| All calls refused | 17% | 12% | 8% |
| Case: refused | 11% | 7% | 11% |
| Case: active min per run | 4.7 | 5.2 | 4.3 |
| Case: wall min (target < 5) | - | - | 6.1-14.6 for a full case (679f3555 13.2, dd6b4700 6.1, c17ca5fb 14.6, 6a8dba9a 7.2) |
| Case: instances (parallel geoscientists) | 0 | 4 | 4 |
| Plant: refused | 16% | 16% | 9% |
| Plant: active min per run | 77.9 | 18.6 | 8.4 |
| Fresh design run, wall | 70 min (QA-145) | - | 19.5 (5d0216a6), 23.6 (56c8a22e), 4 engineers in parallel |
| Simulate: refused | 35% | 18% | 8% |
| First-try refusal evaluate_module | 52% | 60% (5 tries) | 100% (1 try; 2 calls in all) |
| First-try refusal patch_plant | 40% | 14% | 29% |
| First-try refusal build_plant | 43% | 25% | 14% |
| First-try refusal calculate | 52% | 75% | 29% |
| First-try refusal run_python | 81% | 100% (1) | not called |
| First-try refusal read_stored | 9.7% | 7% | 6% |
| First-try refusal set_case | - | 52% | 21% |

The design stage changed most: engineers now propose from the brief and the lead builds once
(QA-145), so `evaluate_module` almost disappeared (2 calls in group B against thousands before)
and the plant stage fell from 78 to 8 active min per run.

Top-10 causes of the first baseline, per run:

| Cause | First baseline | A | B |
|---|---|---|---|
| T1 missing value | 6.1 | 0.5 | 0.25 |
| T2 evaluate_module inlets | 4.2 | 0.15 | 0.08 |
| T3 read_stored / read_result reference | 6.9 | 3.7 | 2.0 |
| T4 calculate / run_python | 4.7 | 1.2 | 1.1 |
| T5 patch_plant not_allowed / invalid_value | 3.4 | 0.04 | 0 |
| T6 unknown name evaluate_module / patch_plant | 2.1 | 0.23 | 0.04 |
| T7 no case / unknown plant reference | 2.2 | 1.1 | 0.75 |
| T8 patch/build/simulate invalid input | 2.0 | 0.08 | 0 |
| T9 set_case / update_state | 1.7 | 1.3 | 0.9 |
| T10 nested stopped | 0.7 | 0.12 | 0.12 |

T1, T2, T5, T6, T8 are near 0. T3, T4, T7, T9 remain; their main forms in group B:

- T3: `read_result` with a group path `d0` / `d1` (13 calls in 5 runs: analysis_lead, economist,
  design_lead, reviewer; QA-262); the paths are `d0.reservoir`, `d0.well`, ... ;
  `read_stored` with a key the result does not have (5).
- T4: `calculate` with bare numbers (7; QA-235), a case path that does not exist (4), a wrong unit (2).
- T7: `read_case` before any case exists (17 calls, every full case run: case_lead 1-4, project
  lead 1; QA-261).
- T9: `set_case` with files only (5; QA-200), a demand file whose first column is `date` (2).

## Where the time goes now (step timestamps, group B)

- **The model is the time.** Model calls: case_lead 34 min, design_lead 32, economist 19,
  explainer 19, analysis_lead 17, project_lead 16. Tool time outside the model is small; the
  long tools are team calls (geoscientists ~1 min, fill_parts) and studies (optimize 45 s,
  sample_uncertainty 26 s).
- **Input size** (median / max input tokens per call): explainer 51 k / 92 k, case_lead 44 k / 77 k,
  design_lead 39 k / 72 k, analysis_lead 32 k / 77 k, economist 30 k / 48 k.
- **Long outputs**: design engineers take 16-20 s per call (energy_systems_engineer 106 s with
  11.3 k output tokens, 88 s with 10.7 k); a geoscientist call hit the 16,000-token output limit
  (93 s); explainer 86 s with 9.5 k. Final write-ups by three agents in a row (analysis_lead,
  reviewer, explainer) stay (QA-179, QA-187).
- **User waits** show as gaps between steps after a card: 236f17d4 9.7 min after `ask_user`,
  194c3879 2.6 min after `set_case`. The log gives these calls duration 0 (QA-220).
- **Repeats**: read_knowledge repeated 34 times (A: 96), read_case re-read 66 (A: 84),
  list_studies 7 (A: 23; QA-219).

## Slow spots filed (linked to QA-150)

- QA-219: economist calls `list_studies` with no arguments 4-6 times in one run (A; down in B).
- QA-220: approval-gated calls and `ask_user` are logged with duration 0, so user waits are invisible.
- QA-261: every full case run calls `read_case` before a case exists (17 refused calls in 6 runs).
- QA-262: `read_result` with a group path `d0` / `d1` is refused (13 calls in 5 runs).
- Already filed by the QA threads: QA-152, 157, 159, 179, 187, 199, 200, 209, 235.

## Next pass

On ended runs after the next geomind release: copy the scripts to a fresh work dir (the scripts
use one dir; `analyse.py` reads every run in its `data/`), set the start filter in `fetch2.py`,
keep only ended runs. Group the runs by deploy time from `.claude/STATUS.md`.
