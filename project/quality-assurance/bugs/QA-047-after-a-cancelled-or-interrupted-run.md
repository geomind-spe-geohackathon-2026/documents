# QA-047: After a cancelled or interrupted run, the next run starts the work over: unsaved engineer work is lost, the stored design is not reused

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | Fatemeh (runs), Claude (write-up) |
| Found | 2026-11-04 21:22 UTC |
| Versions | frontend 1.1.33; backend 1.1.17 to 1.1.40 during these runs |
| Where | (A) chat 33c76f29-064f-4047-9926-ff8937beddf7 (project test hack): run a61cfb19 cancelled, then run f78c671a on "continue"; (B) chat 1b669d3e-ea13-43ce-b2aa-9f3d8ab258da (project QA qa-6): run 55be0d14 interrupted, then run a2dd83e3 |
| Fixer | hotfix-python |

## Steps

(A) After the long run a61cfb19 is cancelled (QA-017), the user sends "continue" in the same chat.
(B) Run 55be0d14 stops with "interrupted: the app was updated or restarted; send your message
again"; the user sends the same message again (run a2dd83e3).

## Expected

The new run goes on from where the last one stopped: it reuses what the chat already holds (the
case, the stored designs, the agents' findings) and redoes only the step that did not finish.

## Actual

(A) The chat holds `design/hhpc_deep_doublet` and `design/hhpc_connected` (run_artifacts, 19:42 and
19:45 UTC) and the problem state's design.modules and owners. The new run (f78c671a): the coordinator
turns "continue" into "design the plant from the attached files ... continue the design on the case
as it stands"; the design lead reads the project plant v1 and calls build_plant again as
`hhpc_start`, then fills the parts again. The reservoir, well and energy systems engineers' work of
the cancelled run (about 15 minutes, QA-016) was never written (patch_plant waited for an approval),
so it is lost and done again.

(B) The interrupted run had read the three files and run the geoscientist (104 s, a full answer of
ground, reservoir and brine values), but no case was set yet (its set_case was refused). The new run
reads the files again and runs the geoscientist again from nothing.

## Evidence

- (A) Postgres, read-only: `run_artifacts` of chat 33c76f29 (design/hhpc_deep_doublet,
  design/hhpc_connected); `run_events` of f78c671a (seq 18 to 145: the coordinator's task, read_plant
  project_plant=hhpc_deep_doublet, build_plant name=hhpc_start).
- (B) [`run-55be0d14...json.gz`](../evidence/QA-047/run-55be0d14272448bca4b70aa2395654c8.json.gz),
  [`run-a2dd83e3...json.gz`](../evidence/QA-047/run-a2dd83e3f69548a9aaa4e84b13003ed3.json.gz)

## Cause

Guess: what an agent finds (the geoscientist's values, an engineer's parameters) is kept only in its
nested run's messages until a write tool runs; the problem state has no "work in progress", and the
brief for a new run does not point at the chat's stored designs. "continue" carries no reference
to the last run, so the coordinator writes a fresh brief.

Note (B, good news): the interrupted run now ends `failed` with the message "The run stopped because
the app was updated or restarted; send your message again" (QA-017's case, handled).

## Fix

- 2026-11-04 21:28 UTC: part fixed in geomind 0.4.45 (commit 5ec7d83, project and design lead prompts: go on from the stored design after a stopped run); backend 1.1.43, waiting for deploy. The engineers' loss in (A) is QA-016 (fixed). Left for development mode: a work-in-progress record of unwritten findings (B: the geoscientist's answer before set_case).
## Retest
