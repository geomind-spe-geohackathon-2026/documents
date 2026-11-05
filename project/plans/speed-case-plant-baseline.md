# Baseline: speed of case and plant (task A1, A2)

Written by speed-analysis-I, 2026-11-05, for Coordinator-IV. Source: the stored logs
(`GET /assistant/runs/{id}/log` and `/agents`) of every agent run that started on production on
2026-11-05 (UTC) up to the time of reading: **41 runs** in 42 projects (21 done, 13 cancelled,
6 failed, 1 running at reading time). Read-only: nothing was started, answered, cancelled or changed. Run again
after every geomind release (the script is described at the end).

## How to read the numbers

- The log has no per-step clock. **Wall min** is `ended - started` of the run and includes every wait for
  an approval or a question card (the user's time is not stored; `ask_user`/`ask_economics` calls last ~0 s in the log).
- **Active min** per stage is the sum of the model call durations plus the tool durations of the
  steps of that stage, without the delegation tools (a call of `case_lead`, `design_lead`, ... lasts as long as the nested run,
  which is counted in its own steps). For parallel instances this adds the instances up, so it is *work*, not elapsed time.
- A step belongs to a stage by its agent and tools: **case** = case_lead and geoscientist steps; **simulate** = steps
  of a plant agent or analysis_lead that call `simulate` or `check_results`; **sizing** = steps that call
  `size_plant`, `set_ranges` or `optimize`; **plant** = the other steps of the design lead and its engineers
  (build, patch, evaluate, read); **other** = coordinator, project lead, analysis, economist, reviewer, report, curator.
- **Refused** = a tool call whose output is `{"error": ...}`. **First-try refusal** = a call whose previous call of the same tool
  by the same agent in the same run was not refused (or there was none): the share of fresh attempts the tool turned down.
- **Cards**: Q = question card (`ask_user` without an approve option); A = approval card (`ask_economics`, or `ask_user` offering "approve").
- **Instances** = distinct `instance` names in `/agents` (parallel sub-agents, IMP-025). Only geomind 0.4.91+ writes them, so the
  older runs show 0.

## Totals per stage (all 41 runs)

| Stage | Runs with it | Steps | Tool calls | Refused | Refused % | Active min total | Active min per run | Q cards | A cards |
|---|---|---|---|---|---|---|---|---|---|
| case | 26 | 718 | 1228 | 131 | 11% | 123 | 4.7 | 22 | 28 |
| plant | 17 | 3199 | 5813 | 958 | 16% | 1324 | 77.9 | 3 | 1 |
| sizing | 11 | 25 | 31 | 8 | 26% | 6 | 0.6 | 0 | 0 |
| simulate | 17 | 264 | 389 | 135 | 35% | 83 | 4.9 | 0 | 0 |
| other | 41 | 744 | 1453 | 293 | 20% | 173 | 4.2 | 5 | 1 |

Whole set: 8914 tool calls, 1525 refused (17%).

What the totals say:

- The plant stage is where the time goes: 3199 of 4950 steps and 1324 of 1709 active minutes. A run that reaches the plant stage
  spends about 78 active minutes in it; the case stage about 5 minutes. Of the 17 runs that reached the plant stage, 1 ended `done` (32a12115, 74 active min, 188 min wall), 5 failed, 10 were cancelled, 1 was still running.
- The refusal rate is 11% in the case stage, 16% in the plant stage and **35% in simulate**; sizing is rarely reached
  (25 steps in 11 runs) and 4 of its 6 `optimize` calls were refused; only run 32a12115 got an `optimize` result (twice; one earlier call refused on a zero-width flow range).
- Stalls (same call with the same input twice or more, per agent): evaluate_module 159, simulate 44, patch_plant 43, check_results 29, list_profiles 28, set_case 16. Re-reads of the same thing with the same
  input (not refused): read_case 533, describe_module 363, read_plant 254, read_result 178, read_stored 156, read_profile 80. The `read_case` count (533 repeats) is the largest single waste of steps.
- Approval and question cards sit almost entirely in the case stage (50 of 60); the plant stage asks the user 4 times in 17 runs.

## Per tool: refusals

Tools with at least 10 calls and one refusal, most refused first.

| Tool | Calls | Refused | Refused % | First tries | First-try refused | First-try refusal % |
|---|---|---|---|---|---|---|
| evaluate_module | 377 | 303 | 80.4% | 101 | 53 | 52.5% |
| patch_plant | 454 | 235 | 51.8% | 241 | 97 | 40.2% |
| read_stored | 1477 | 232 | 15.7% | 1253 | 122 | 9.7% |
| calculate | 180 | 134 | 74.4% | 56 | 29 | 51.8% |
| read_plant | 737 | 118 | 16.0% | 633 | 50 | 7.9% |
| simulate | 201 | 113 | 56.2% | 93 | 15 | 16.1% |
| build_plant | 116 | 66 | 56.9% | 58 | 25 | 43.1% |
| run_python | 79 | 57 | 72.2% | 31 | 25 | 80.6% |
| read_result | 794 | 52 | 6.5% | 744 | 39 | 5.2% |
| web_search | 145 | 39 | 26.9% | 109 | 24 | 22.0% |
| set_case | 97 | 36 | 37.1% | 63 | 20 | 31.7% |
| update_state | 241 | 33 | 13.7% | 210 | 25 | 11.9% |
| read_case | 1093 | 31 | 2.8% | 1075 | 28 | 2.6% |
| energy_systems_engineer | 51 | 12 | 23.5% | 39 | 10 | 25.6% |
| design_lead | 54 | 10 | 18.5% | 50 | 7 | 14.0% |
| case_lead | 41 | 7 | 17.1% | 39 | 6 | 15.4% |
| check_results | 84 | 6 | 7.1% | 79 | 6 | 7.6% |
| describe_module | 887 | 5 | 0.6% | 882 | 5 | 0.6% |
| read_rag | 121 | 4 | 3.3% | 118 | 4 | 3.4% |
| merge_designs | 28 | 4 | 14.3% | 24 | 4 | 16.7% |
| size_plant | 18 | 3 | 16.7% | 15 | 2 | 13.3% |
| read_web_page | 32 | 3 | 9.4% | 29 | 3 | 10.3% |
| process_engineer | 34 | 2 | 5.9% | 33 | 2 | 6.1% |
| compute_kpis | 25 | 1 | 4.0% | 24 | 1 | 4.2% |
| list_plants | 115 | 1 | 0.9% | 115 | 1 | 0.9% |
| describe_case | 80 | 1 | 1.2% | 79 | 1 | 1.3% |
| ask_economics | 15 | 1 | 6.7% | 14 | 1 | 7.1% |

## Per run

Columns "Case / Plant / Sizing / Simulate / Other" are `steps / active minutes`. "Calls (refused)" is the count of tool calls
(refused ones). Runs of 0.1 to 3 min are cancelled or routing-only runs (a question answered by the coordinator).

| Started (UTC) | Run | Project | Status | Wall min | Case steps / min | Plant | Sizing | Simulate | Other | Calls (refused) | Q / A cards | Instances |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 11-05 00:13 | 2d8a6bbf | QA2 qa-func-1 S1 full case | cancelled | 2.7 | - | 10 / 1.5 | - | - | 8 / 0.7 | 32 (2) | 0 / 0 | 0 |
| 11-05 00:16 | 6d47f7c9 | QA2 qa-func-1 S1 full case | failed | 7.5 | 24 / 4.6 | - | - | - | 5 / 0.7 | 40 (3) | 1 / 0 | 0 |
| 11-05 00:28 | 92971ce5 | QA2 qa-func-1 S1 full case | cancelled | 10.4 | 21 / 10.1 | - | - | - | 2 / 0.2 | 32 (18) | 0 / 0 | 0 |
| 11-05 00:40 | d833d5e2 | QA2 qa-func-1 S1 full case | cancelled | 2.8 | 10 / 2.6 | - | - | - | 3 / 0.2 | 20 (6) | 0 / 0 | 0 |
| 11-05 00:43 | 861ef137 | QA2 functional-qa-I full run | failed | 275.6 | 25 / 4.1 | 201 / 86.0 | - | - | 6 / 0.6 | 376 (113) | 1 / 3 | 0 |
| 11-05 01:24 | 7dcfcf93 | sahand test 1 | done | 464.0 | 64 / 15.8 | - | - | - | 15 / 1.6 | 149 (16) | 1 / 2 | 0 |
| 11-05 04:16 | 37950240 | QA2 functional-qa-I full run | cancelled | 62.9 | 30 / 5.3 | 233 / 78.2 | 1 / 0.4 | 4 / 0.8 | 26 / 23.2 | 595 (89) | 1 / 0 | 0 |
| 11-05 04:17 | bd7aa40e | QA2 functional-qa-3 studies | failed | 68.4 | 68 / 8.8 | 180 / 68.5 | 1 / 0.2 | 5 / 1.1 | 11 / 1.4 | 458 (88) | 3 / 3 | 0 |
| 11-05 04:17 | 6921d00e | QA2 functional-qa-2 economics | failed | 29.0 | 34 / 5.6 | 108 / 41.5 | 1 / 0.1 | 2 / 0.4 | 4 / 0.2 | 292 (95) | 1 / 3 | 0 |
| 11-05 04:49 | f59e5d2c | QA2 functional-qa-2 economics | cancelled | 114.8 | 72 / 14.7 | 299 / 131.5 | 1 / 0.3 | 32 / 12.4 | 14 / 1.7 | 837 (95) | 1 / 0 | 0 |
| 11-05 05:20 | b5a578de | QA2 functional-qa-I full run | done | 0.1 | - | - | - | - | 2 / 0.1 | 0 (0) | 0 / 0 | 0 |
| 11-05 05:28 | eb7b95df | QA2 functional-qa-3 studies | cancelled | 37.1 | 14 / 1.8 | 139 / 46.2 | - | 5 / 0.6 | 11 / 1.1 | 289 (44) | 0 / 2 | 0 |
| 11-05 05:31 | c4f00b5c | QA2 functional-qa-I full run | cancelled | 58.5 | 5 / 0.4 | 88 / 31.8 | - | 59 / 17.9 | 10 / 2.4 | 234 (86) | 0 / 1 | 0 |
| 11-05 06:06 | 753645c0 | QA2 functional-qa-3 studies | failed | 75.6 | 40 / 3.6 | 169 / 88.9 | 2 / 1.0 | 11 / 3.7 | 8 / 0.8 | 441 (74) | 3 / 0 | 0 |
| 11-05 06:34 | 004bb7f9 | QA2 functional-qa-I full run | done | 1.9 | - | - | - | - | 5 / 1.9 | 5 (0) | 0 / 0 | 0 |
| 11-05 06:43 | cef908d9 | QA2 functional-qa-2 economics B | cancelled | 168.1 | 78 / 12.7 | 495 / 184.7 | 1 / 0.0 | 32 / 6.0 | 15 / 2.4 | 982 (122) | 8 / 6 | 0 |
| 11-05 07:02 | 3bdd7ebb | QA2 functional-qa-I full run | failed | 268.4 | 24 / 3.3 | 487 / 269.5 | 6 / 1.3 | 51 / 19.3 | 18 / 2.1 | 992 (150) | 1 / 1 | 0 |
| 11-05 07:27 | de266fff | QA2 functional-qa-3 studies | cancelled | 426.8 | 15 / 1.0 | 189 / 75.3 | 1 / 0.0 | 23 / 10.3 | 91 / 31.1 | 717 (101) | 2 / 0 | 0 |
| 11-05 10:10 | 32a12115 | geo mind testing | done | 187.9 | 60 / 10.5 | 176 / 74.1 | 5 / 1.0 | 16 / 2.9 | 103 / 24.1 | 621 (81) | 2 / 3 | 0 |
| 11-05 10:31 | e716040b | QA3 plant | cancelled | 242.9 | - | 65 / 28.4 | - | - | 7 / 0.5 | 138 (10) | 1 / 0 | 0 |
| 11-05 10:31 | bf0da8dd | QA3 case | done | 16.4 | 23 / 4.1 | - | - | - | 9 / 0.9 | 48 (5) | 1 / 2 | 0 |
| 11-05 10:31 | aa3a2f95 | QA3 simulation | done | 0.4 | - | - | - | 1 / 0.0 | 7 / 0.3 | 10 (0) | 0 / 0 | 0 |
| 11-05 10:31 | 80d261c9 | QA3 report | done | 2.8 | - | - | - | 1 / 0.1 | 22 / 2.7 | 31 (3) | 0 / 0 | 0 |
| 11-05 10:31 | f83e7b8b | QA3 study | done | 0.5 | - | - | - | 1 / 0.0 | 8 / 0.5 | 14 (0) | 0 / 0 | 0 |
| 11-05 10:32 | cd6eaba5 | QA3 simulation | done | 37.8 | - | - | - | - | 29 / 8.0 | 52 (12) | 0 / 0 | 0 |
| 11-05 10:33 | 1461ca81 | QA3 study | cancelled | 227.9 | - | 32 / 12.2 | 5 / 1.7 | 10 / 5.9 | 13 / 2.5 | 116 (27) | 0 / 0 | 0 |
| 11-05 10:36 | da7eb467 | QA3 report | done | 7.9 | - | - | - | 1 / 0.2 | 28 / 7.9 | 84 (28) | 0 / 0 | 0 |
| 11-05 10:44 | c4c75dc8 | QA3 report | done | 11.2 | - | - | - | - | 27 / 4.7 | 65 (6) | 0 / 0 | 0 |
| 11-05 10:50 | a5bbf47f | QA3 case | done | 3.6 | 9 / 0.9 | - | - | - | 5 / 0.4 | 18 (0) | 0 / 0 | 0 |
| 11-05 10:55 | bac05d29 | QA3 case | done | 3.1 | 7 / 0.5 | - | - | - | 5 / 0.4 | 21 (0) | 0 / 0 | 0 |
| 11-05 10:55 | 5eb10fa1 | sahand test 1 | cancelled | 137.3 | 3 / 0.2 | 178 / 63.9 | 1 / 0.2 | 10 / 1.2 | 54 / 9.7 | 486 (118) | 2 / 0 | 0 |
| 11-05 10:56 | 0901847a | QA3 report | done | 20.8 | - | - | - | - | 39 / 12.6 | 120 (44) | 0 / 0 | 0 |
| 11-05 10:59 | 1fd21dc2 | QA3 case | done | 1.9 | 3 / 0.2 | - | - | - | 6 / 0.5 | 9 (0) | 1 / 0 | 0 |
| 11-05 11:02 | 9d2e34ca | QA3 case | done | 2.4 | 9 / 1.1 | - | - | - | 3 / 0.3 | 14 (1) | 0 / 0 | 0 |
| 11-05 11:07 | 1a4043da | QA3 case | done | 2.8 | 8 / 0.7 | - | - | - | 5 / 0.5 | 19 (1) | 0 / 0 | 0 |
| 11-05 11:10 | cadc63aa | QA3 simulation | done | 9.8 | - | - | - | - | 30 / 8.9 | 85 (22) | 0 / 0 | 0 |
| 11-05 11:12 | 11597465 | QA3 case | cancelled | 198.0 | 6 / 0.6 | - | - | - | 2 / 0.2 | 10 (3) | 0 / 0 | 0 |
| 11-05 13:54 | 5cd1f2b8 | geo mind testing | done | 12.1 | - | - | - | - | 58 / 12.0 | 67 (28) | 0 / 0 | 0 |
| 11-05 14:29 | cb5a97c2 | sahand test 2 | done | 11.3 | 45 / 6.9 | - | - | - | 21 / 2.2 | 104 (13) | 0 / 2 | 0 |
| 11-05 14:40 | ed03d7ea | sahand test 2 | running | - | - | 150 / 42.2 | - | - | 2 / 0.1 | 247 (15) | 0 / 0 | 3 |
| 11-05 14:52 | 9696f5d4 | QA-TEST manual-qa IMP-025 parallel case timing | done | 3.8 | 21 / 2.9 | - | - | - | 7 / 0.6 | 44 (6) | 0 / 2 | 0 |

Run 9696f5d4 (QA-140, case only, 14:52 UTC) is the only run of this set that ends `done` with a complete case on its own: 3 min 45 s,
28 steps, 41 tool calls, 6 refused, 2 approval and 2 question cards, no parallel split (instance names empty).
It is listed in the table under its start time.

## The top 10 causes of refusals and stalls

Counts are refused calls over the whole set; "runs" is the number of runs the cause occurs in. Each cause lists an example
message as the tool returned it (shortened), the stage, and the fix it calls for, named for hotfix-python.
Fix kinds: **prompt/skill** = words in the agent prompt or a tool's skill; **schema** = the tool's input
schema or its handling in the backend/geomind tool code; **gemini** = a message or behaviour of gemini (request only through Sahand, see rules).

### 1. Reading a stored result with the wrong path (T3): 284 refusals, 24 runs, stage plant and simulate

`read_stored` (232) and `read_result` (52). Example (`design_lead`):
`read_stored: path = d0; 'd0' is no key or index of the result; expected one of d0.esp` and
`Results: module path = 'd0'; expected one of heating_return_pipe, ..., d0.reservoir, d0.well, d0.esp ...`.
The keys of a result are *dotted names* (`d0.esp`), but the agents walk it as a nested path (`d0` then `esp`), or guess a
module name that is not in the plant (`compression_chiller` on a plant that has none; `steps.N`, `summary.summary`).
Only 9.7% of `read_stored` first tries are refused but the agents then retry, 16% overall.
Fix (schema + skill): `read_stored`/`read_result` accept a dotted prefix as one key (try the longest matching key before failing);
the error lists the exact full paths that begin with the given prefix (`d0.esp.fluid_in...`), not only the first level; the skill
`reading-results` states in one line that module ids are dotted names. Add a tool `list_result_paths` or an `outline` argument.

### 2. evaluate_module without its stream inlets (T2): 174 refusals, 14 runs, stage plant

`evaluate_module` called with `inlets = []` or with an inlet the module does not have. Examples (`energy_systems_engineer`):
`evaluate_module: inlets = []; HeatPump needs the stream inlets source_in, sink_in, each with its fluid, T, p and m_dot (or flow), from the case or the plant; or name the module's id with result=result/<id>`,
`pipe: invalid inlet 'air_in'; valid names: fluid_in, air_in: Fluid: 1 validation error for Fluid / A gas fluid needs gas_composition`.
377 calls, **80% refused, 52% on the first try**; the same call is repeated 159 times and 11 nested engineer runs were stopped by
the guard "the same call failed 3 times in a row". This is QA-143 territory.
Fix (schema + prompt/skill): when `inlets` is empty and the plant or the case gives the stream, evaluate_module fills it (from the case: the
reservoir/brine/air values; from the plant: the connected upstream stream) and says what it filled; otherwise the error returns a **complete
ready-to-send inlets JSON** for this module type with the fields to fill (the `suggestions` already do so for some modules: do it for all);
`evaluating-a-module` skill: one worked example per module family (HeatPump, AbsorptionUnit, Pipe with gas, ElectricBoiler, Doublet).
The engineer prompt must say: evaluate a module only after the plant is built, then pass `result=result/<id>`.

### 3. Plant values missing, listed as "no value" (T1): 249 refusals, 17 runs, stage plant and simulate

`read_plant` (79), `simulate` (67), `patch_plant` (35), `build_plant` (22), `evaluate_module` (37 no-value variants). Example:
`d0.drainage_radius: no value [m]: Radius of the drainage area around each well; d0.roughness: no value [m]: ...; d0.reservoir.pressure: no value [Pa]; d0.reservoir.temperature ...`
and, in simulate, `d0.esp.stage_count: no value [-]`, `d0.esp.head_coefficients: no value`. The plant is built and saved with the reservoir, well and pump values
empty, then every read/simulate repeats the same list. The values belong to the reservoir engineer (and the case), see cause 5.
Fix (prompt/skill + schema): `build_plant`/`patch_plant` must refuse *at the write* (not on every later read) with the grouped list by owner
(reservoir engineer: drainage_radius, roughness, reservoir.*; well engineer: ESP curves) so the lead splits them at once (IMP-025 plant stage, plan C1);
the design skill requires the reservoir/well values from the geoscientist's case values (`site.ground.*`) before the first build.
`read_plant` should warn once ("N values empty, owner X"), not refuse. gemini: none needed.

### 4. calculate and run_python misuse (T4): 191 refusals, 18 runs, stage plant, simulate, analysis

`calculate` (134 refused of 180 calls, **74%**) and `run_python` (57 of 79, **72%**; 81% on the first try). Examples:
`calculate: unit = 'h/m3*s' is not a unit gemini knows` (23), `run_python: the code holds data literals; pass each value as a named input instead: line 8: 200` (16),
`calculate: result-cf329e...: d0 does not exist; expected one of d0.esp` (the same dotted-path problem as cause 1),
`calculate: stored = 'result-...heat_pump.power_in.mean' is not a stored result`.
Fix (prompt/skill + schema): the agents compute with these two tools what gemini already returns (checks, KPIs). Point them to `check_results`/`compute_kpis`
in the plant skills; `calculate`: list the accepted unit grammar in the error and in the skill, auto-accept `a*b/c` forms; `run_python`: accept numeric
literals up to a small count (the rule rejects `200`), or return the code rewritten with named inputs. Cap `calculate`/`run_python` per agent
at a few calls per task.

### 5. patch_plant on a value another engineer owns, or on a case value (T5): 139 refusals, 15 runs, stage plant

Examples: `patch_plant: params.d0.drainage_radius and 6 more is the reservoir_engineer engineer's; the reservoir engineer changes only its own part. Hand it back to the design lead` (97 total)
and `params.d0.gradient: gradient is not a design value of the plant; give it in the case, at site.ground.gradient` (49). The process engineer or design lead tries to fill the
empty ground values of cause 3 itself. 454 patch_plant calls, **52% refused** (40% on the first try), the most expensive tool in the set (43 repeats).
Fix (prompt/skill): the design lead's plan hands module groups to their owners *before* any engineer writes (IMP-025 C1); skill `patching-a-plant` opens with the ownership
table (module -> engineer) and the list of values that live in the case (`site.ground.gradient`, `surface_temperature`, ...). Schema: the error should name the tool call to make next
(`set_case` for case values; `reservoir_engineer(task=...)` for owned ones) with the exact paths.

### 6. evaluate_module naming: control vs parameter, module type case, d1 parameters (T6): 88 refusals, 15 runs, stage plant

Examples: `evaluate: parameters.temperature_setpoint is a control, not a parameter; give it in controls` (39 of it in 11 runs),
`modules: unknown module type 'heat_pump'; did you mean 'HeatPump'?` (14), `unknown parameter or control 'd1.nominal_flow'; did you mean 'd0.nominal_flow'?`.
Fix (schema): the tool moves a known control given under `parameters` into `controls` (and says so), and matches module types ignoring case and underscores
(`heat_pump` = `HeatPump`) when there is one match; the suggestion of `describe_module` output lists parameters and controls separately. The skill `evaluating-a-module` shows one call per family (IMP-021).

### 7. Calling a tool before there is a case or a plant (T7): 91 refusals, 21 runs, every stage

`read_case` -> `no_case` (29), `read_plant` / `simulate` -> `project has no plant; expected a design reference` (39 + 23). Example (`project_lead`, first step of 9696f5d4):
`case: the problem state has no case; expected one. Call set_case (source='project' ...) or ask_user for them`. The project lead and the engineers read first and learn the state from the refusal.
Fix (prompt/skill + schema): the first message to every agent carries the state header (case version or "no case", plant version or "no plant", list of stored
designs), so no agent reads what does not exist; `read_case` with no case returns an empty "no_case" *answer*, not a refusal (does not count as a failed call, does not feed the guard). Plan B4.

### 8. build_plant/patch_plant: name collision, unconnected port, internal error (T8): 83 refusals, 14 runs, stage plant

Examples: `design: name = 'surface'; a design with this name is stored with other content; use a new name, such as 'surface_2', and send the same call with it` (29),
`d0.supply_out: unconnected port; connect it to a module or name a plant port` (10), `patch_plant: internal error` (18, runs 753645c0 and eb7b95df; also `build_plant` 753645c0/eb7b95df), `simulate: internal error` (7, three runs).
Fix (schema): a design name that exists with other content gets the next free name automatically (the tool returns the name it used); `unconnected_port` error lists the free ports
of the modules with their types; **`patch_plant: internal error` is a backend defect** (18 calls, no message): hotfix-python/hotfix-back to find the exception in the backend log and return its message.

### 9. set_case and update_state with the wrong form (T9): 68 refusals, 19 runs, stage case and project lead

`set_case` (36 of 97 calls, 37%): `demand.heating.power.file: ... row 1 time = '2027-01-01' has no offset; expected ISO 8601 with an offset or Z, or a time_zone` (9),
`set_case: files = [...] and nothing else; expected changes that name each file as the file of its series` (7), `project has no case: no case.json beside its data` (source='project' on a project without a case).
`update_state: path = '/design/reference'; 'reference' does not exist there` (33 total, 11.9% first-try). These are plan item B4 (the four case refusals of QA-140).
Fix (schema): `set_case` accepts a date without offset when `time_zone` is in the case (default = the case's `site` time zone, or ask once) and a `files`-only call builds the series entries from the file headers and
renames `date` -> `time`; `update_state` creates the missing parent for an `add` and accepts the list form.

### 10. Stalls: same call repeated until the guard stops the run (T10 and repeats): 29 nested runs stopped, 16 runs

`energy_systems_engineer: the nested run stopped with error: evaluate_module: the same call failed 3 times in a row with the same error; the run stops` (11),
`design_lead: the nested run stopped with cancelled` (7), `case_lead ... cancelled` (4; user or coordinator cancelled). Repeated calls per agent: evaluate_module 159, simulate 44, patch_plant 43,
check_results 29, list_profiles 28, set_case 16; the `repeated` flag in the output was set on 56 refusals. Re-reads: read_case 533, describe_module 363, read_plant 254, read_result 178.
Fix (prompt/skill + schema): the guard message is not enough; on the 2nd identical refusal the tool must return a *different, concrete next step* (the corrected call, or "hand back to the design lead
with reason R") and the agent prompt says "never repeat a refused call; change the input or report". A per-run read cache: `read_case`, `describe_module`, `read_plant` return
"unchanged since your read at step N" instead of the full output. Add the budget of plan B5/C4 (steps and minutes per sub-agent).

### Also seen (11th, not in the top 10)

`web_search` 39 refusals in 3 runs: `query has 9 words; expected at most 8 technical terms` (case_lead, economist). Fix (schema + skill): allow 12 words or trim the query in the tool and say so.
Smaller: `simulate` `schedule: params.control.dispatch is missing; expected '...'` (14, one run; the tool should fill the one rule the schedule implements: IMP-019),
`simulate case_incomplete: no requirement on doublet gives a flow range` (8) , `size_plant`/`optimize` refusals (4 of 6 optimize).

## What this says about speed

1. The **case** stage is already near the goal (QA-140: 3 min 45 s) with refusals mainly at `set_case` (cause 9) and `no_case` reads (cause 7). Removing those saves about 6 of 41 calls (a few steps), the split into
   geoscientists (B1/B2) does the rest. The 50 case cards are the other cost: `ask_economics` plus one or two `ask_user` per run (see per run).
2. The **plant** stage never completes quickly. In the 17 runs that reached it: 78 active minutes on average (range 28 to 270), 16% of 5813 calls refused, and
   only one run (32a12115) reached an `optimize` result. The causes 1-6 (reading paths, inlets, empty values, ownership, naming, calculation) are one family:
   the tool errors teach the right call only after the agent has made it, and each refusal costs one model step (about 25 s at the measured pace of 1324 min / 3199 steps).
   Roughly 960 refused plant calls x 25 s = 6.6 h of the 22 h of plant-stage work is spent on refusals alone (an upper estimate: a refusal step also carries the call that follows it). Identical re-reads add about 1,680 more calls (cause 10).
3. **Simulate** is refused 35% of the time (113 of 201 `simulate` calls): empty values (cause 3), the dispatch rule, no plant.

Priorities by effect on speed (steps saved per run): cause 10 re-reads/guard, cause 1+4 paths, cause 2 inlets, cause 3+5 values and ownership, then 6-9.

## Method and reproduction

Scripts (not committed; kept in `/tmp/sa/scripts` of the Dell): `fetch.py` (list projects and runs, `GET /assistant/runs?project=`), `fetch2.py` (log and agents of each run
started since 2026-11-05), `analyse.py` (per step stage, refusals, first-try rate, cause clusters by tool + code + message with ids, quoted names and numbers masked), `write.py`.
A step is not timed; the stage "active min" are model and tool durations. Not measured: user wait, queueing, SSE timing. To get elapsed time per stage, `step.started`/`step.finished`
events would need a timestamp (suggest: add `ts` to events in the backend, hotfix-back).
