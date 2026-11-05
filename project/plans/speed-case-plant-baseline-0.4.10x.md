# Speed baseline, second run: geomind 0.4.96 to 0.4.10x (first pass)

Written by speed-analysis-II, 2026-11-05, for Coordinator-V and QA-150. Same method and scripts as
[speed-case-plant-baseline.md](speed-case-plant-baseline.md) (the first baseline, 41 runs, geomind
up to 0.4.95), which stays as the reference. Read-only: only GET calls; nothing was started,
answered, cancelled or changed.

## Scope of this pass

- Runs: the **9 runs that started on production after 16:36 UTC** (geomind 0.4.96 live, backend
  1.1.100) and had ended by 17:27 UTC. All are QA-TEST runs of the QA threads (QA-E2E-*, QA-AI-*).
- Versions: these 9 ran on geomind **0.4.96 to 0.4.98** (backend 1.1.100 to 1.1.103). geomind
  0.4.100 went live with backend 1.1.104 at ~17:20 UTC; 0.4.102 with 1.1.105 later. Runs on
  0.4.100+ are for the second pass.
- Caveat: 9 runs is a small set and the QA threads test single stages (a case, a study, an
  economics question), while the first baseline was dominated by full design runs. Compare shares
  and per-run numbers, not totals. Only 2 runs have a plant stage, 1 has sizing.
- New: every step now has `ts` (backend 1.1.99). Gaps between steps are measured below.

## Totals per stage (9 runs)

| Stage | Runs with it | Steps | Tool calls | Refused | Refused % | Active min total | Active min per run | Q cards | A cards |
|---|---|---|---|---|---|---|---|---|---|
| case | 2 | 55 | 86 | 7 | 8% | 9 | 4.3 | 0 | 3 |
| plant | 2 | 33 | 52 | 6 | 12% | 7 | 3.3 | 0 | 0 |
| sizing | 1 | 3 | 3 | 0 | 0% | 1 | 1.0 | 0 | 0 |
| simulate | 6 | 11 | 16 | 2 | 12% | 1 | 0.2 | 0 | 0 |
| other | 9 | 271 | 465 | 53 | 11% | 34 | 3.8 | 0 | 0 |

Whole set: 622 tool calls, 68 refused (11%). First baseline: 8914 calls, 1525 refused (17%).

## Per run

| Started (UTC) | Run | Project | Status | Wall min | Case steps / min | Plant | Sizing | Simulate | Other | Calls (refused) | Q / A cards | Instances |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 11-05 16:50 | cf319cd4 | QA-TEST QA-E2E-case-I 1 | done | 12.3 | 40 / 6.0 | - | - | - | 17 / 2.1 | 98 (6) | 0 / 2 | 4 |
| 11-05 16:50 | 61721f4c | QA-TEST QA-E2E-study-I 1 | done | 0.6 | - | - | - | 1 / 0.0 | 10 / 0.5 | 16 (1) | 0 / 0 | 0 |
| 11-05 16:51 | bf3990c4 | QA-TEST QA-E2E-economics-I 1 | done | 18.8 | 15 / 2.6 | - | - | - | 9 / 0.5 | 29 (2) | 0 / 1 | 0 |
| 11-05 16:51 | 389be3c3 | QA-TEST QA-AI-analysis-I 1 | done | 1.2 | - | - | - | 1 / 0.0 | 18 / 1.2 | 26 (2) | 0 / 0 | 0 |
| 11-05 16:52 | d6f8e79a | QA-TEST QA-E2E-study-I 1 | done | 7.5 | - | - | - | 1 / 0.1 | 48 / 7.1 | 83 (13) | 0 / 0 | 0 |
| 11-05 16:53 | c2b815a8 | QA-TEST QA-AI-analysis-I 1 | done | 4.8 | - | - | - | 1 / 0.1 | 44 / 4.4 | 56 (19) | 0 / 0 | 0 |
| 11-05 17:01 | 7a7ace73 | QA-TEST QA-AI-analysis-I 1 | done | 11.0 | - | 21 / 4.5 | - | 3 / 0.3 | 37 / 4.6 | 97 (14) | 0 / 0 | 0 |
| 11-05 17:01 | 4eb8e2f4 | QA-TEST QA-E2E-study-I 1 | done | 21.3 | - | 12 / 2.1 | 3 / 1.0 | 4 / 0.4 | 59 / 11.2 | 173 (9) | 0 / 0 | 0 |
| 11-05 17:15 | 57c42f61 | QA-TEST QA-AI-analysis-I 1 | done | 3.1 | - | - | - | - | 29 / 2.8 | 44 (2) | 0 / 0 | 0 |

## Compared with the first baseline

| Measure | First baseline (<= 0.4.95, 41 runs) | Now (0.4.96-0.4.98, 9 runs) |
|---|---|---|
| All calls refused | 17% | 11% |
| Case: refused share | 11% | 8% |
| Case: wall time | target < 5 min | 12.3 min (cf319cd4, full case with geoscientists, 2 approval cards); 18.8 min (bf3990c4, economics, 12.6 min of it one approval wait) |
| Case: active min per run | 4.7 | 4.3 |
| Case: instances | 0 | 4 (cf319cd4: the geoscientists team runs in parallel, 59 s for the team call) |
| Plant: active min per run | 77.9 | 3.3 (2 runs, both build a known plant for a study, not a fresh design) |
| Plant: refused share | 16% | 12% |
| Runs reaching `optimize` | 1 of 17 | 1 of 2 plant runs (4eb8e2f4, optimize 45 s) |
| Simulate: refused share | 35% | 12% |
| First-try refusal: patch_plant | 40% | 50% (1 of 2) |
| First-try refusal: build_plant | 43% | 33% (1 of 3) |
| First-try refusal: calculate | 52% | 67% (2 of 3) |
| First-try refusal: run_python | 81% | 100% (1 of 1) |
| First-try refusal: read_stored | 9.7% | 6% (10 of 175) |
| First-try refusal: evaluate_module | 52% | not called |

Top-10 causes of the first baseline, per run (count / runs):

| Cause | First baseline per run | Now per run | Now count |
|---|---|---|---|
| T1 missing value on evaluate_module | 6.1 | 0 | 0 |
| T2 evaluate_module inlets | 4.2 | 0 | 0 |
| T3 read_stored / read_result reference | 6.9 | 1.8 | 16 |
| T4 calculate / run_python | 4.7 | 0.8 | 7 |
| T5 patch_plant not_allowed / invalid_value | 3.4 | 0 | 0 |
| T6 unknown name on evaluate_module / patch_plant | 2.1 | 0 | 0 |
| T7 no case / unknown plant reference | 2.2 | 0.3 | 3 |
| T8 patch/build/simulate invalid input | 2.0 | 0.1 | 1 |
| T9 set_case / update_state | 1.7 | 1.0 | 9 |
| T10 nested stopped | 0.7 | 0 | 0 |
| other (new) | - | 3.6 | 32 |

T1, T2, T5, T6 are 0 because no run used evaluate_module or a fresh design (the case for them is
untested here, not proven fixed). The largest group now is "other": `sensitivity` refused 11 of 13
calls (economist passes `design/HackathonPlant`, the project plant's name, as a design reference;
QA-152, fixed after these runs), `read_study` 4, `read_plant` 3 (mutually exclusive arguments).

## Where the time goes now (step timestamps)

- **The model is the time.** 373 model calls, 49 min in total, median 5.2 s, mean 7.9 s. Tool time
  outside the model is small: only 4 calls took more than 4 s (geoscientists team 59 s, optimize
  45 s, sample_uncertainty 26 s, run_study 26 s).
- **Input size per call** (median / max input tokens): case_lead 42 k / 73 k, design_lead 38 k / 51 k,
  explainer 31 k / 52 k, reviewer 31 k / 41 k, analysis_lead 25 k / 53 k, economist 18 k / 27 k.
  The case lead and design lead carry the largest prompts; this is the main lever left (IMPROVEMENTS
  already notes 40-78 k for the case lead).
- **Long final answers**: the slowest calls are final write-ups: analysis_lead 82 s with 9.3 k output
  tokens (4eb8e2f4 step 21, a finish), explainer 47 s / 4.5 k and 37 s / 3.9 k, analysis_lead
  46 s and 41 s at ~4 k. Three agents write about the same result in a row (analysis_lead, reviewer,
  explainer), as QA-179 and QA-187 describe.
- **Wall time vs work**: wall minus model time is mostly waiting for the user (the QA threads
  answer the cards): bf3990c4 18.8 min wall, 3.1 min model, one gap of 12.6 min after a set_case
  approval card; 4eb8e2f4 one gap of 6.2 min after build_plant (a plant approval card). The log
  records these approval-gated calls and `ask_user` with duration 0, so a wait cannot be told
  from work without reading the card (filed, see below).
- **Repeats**: economist calls `list_studies` with no arguments 4 to 6 times in one run (3 of 5
  economist runs); read_case re-read 18 times in all (case_lead `read_case` with the same section
  4 times in two runs, QA-157).
- **Curator** writes 9 lessons in one step (cf319cd4, a 94 s gap), inside the run's wall time
  (QA-199 covers the content).

## New slow spots filed (linked to QA-150)

See `documents/project/quality-assurance/BUGS.md`, reporter speed-analysis-II.

## Second pass

Re-run with the runs on geomind 0.4.100+ (backend 1.1.104+): copy the scripts to a fresh work
dir (`/tmp/sa2`, not the first baseline's `/tmp/sa/data`, which still holds the 41 old runs),
set the start filter in `fetch2.py` to the deploy time, keep only ended runs.

## Second pass (18:04 UTC): runs on geomind 0.4.102 to 0.4.106

Runs that started after 17:21 UTC (backend 1.1.104+) and had ended by 18:04 UTC: only **3**, all
QA-TEST QA-E2E-study-I 1 (52383511 done 7.7 min, 01222f3a done 2.4 min, fd4b7e2c cancelled
0.9 min). The QA threads started few runs in this window; the numbers below are indicative only.

- Calls: 123, refused 12 (10%; first pass 11%, first baseline 17%).
- 52383511 plant stage (design_lead preparing a study): 28 calls, 9 refused: `read_plant` with two
  of design / project_plant / plant_version at once (2), `run_study` with metrics `capex`/`opex`
  that studies do not have and `by = 'heating_coverage'` (2), `calculate` with bare numbers (2),
  `read_result('costs')` (1, QA-209).
- QA-219 (economist `list_studies` repeats): 2 repeats in 3 runs, down from 4-6 per run, but too
  few economist runs to call it fixed.
- Long final write-ups persist: explainer 58 s / 7.0 k output tokens and 42 s / 5.4 k (61 k input);
  analysis_lead median output 1.1 k, project_lead 1.2 k per call.
- No approval waits in these 3 runs (no gap > 60 s between steps).

Next pass: when the QA threads have ended runs on 0.4.106 with a case or a fresh design stage
(T1, T2, T5, T6 are still untested since the first baseline).
