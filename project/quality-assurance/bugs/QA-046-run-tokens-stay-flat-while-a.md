# QA-046: Run tokens stay flat while a nested agent runs, then jump (19,074 for ~7 min, then 527k)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | backend,frontend |
| Reporter | qa-7 |
| Found | 2026-11-04 21:18 UTC |
| Versions | frontend 1.1.46-1.1.50, backend 1.1.40 |
| Where | project "QA qa-7 runs and logs" (b3245cdd-63d3-49d3-91e9-e3ec459cb7c1), chat 51a987be, run d5765e1e, while the geoscientist ran nested under the case lead |
| Fixer | hotfix-back |

## Steps

1. Start a run whose case lead delegates to the geoscientist.
2. Watch the run's token total (chat usage or the run log) while the nested agent works.

## Expected

The total grows with each model call, nested runs included.

## Actual

Seen by qa-7 (not filed by it): the total stayed at 19,074 for about 7 minutes, then jumped to
527k at once.

## Evidence

- ![screenshot](../evidence/QA-046/1.png)
- Run JSON: `../evidence/QA-046/run-<id>.json`

## Cause

Guess: the nested run's usage is added to the root only when the nested run ends, or the live usage event counts only the root's own calls.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-04 21:32 UTC: backend 1.1.44 (40512c9) pushed 21:37 UTC, deploys in the 22:00 UTC window: the run row and a live root usage event (no id, parent null) add the latest totals of running nested runs to the root's last totals. Frontend: if the page sums only root usage events it now grows live; no frontend change expected.
- 2026-11-04 21:33 UTC: deployed in backend 1.1.44 at 21:33 UTC; runs 0cb4b436, 6c5b17e1, f78c671a resumed. Retest: watch a run's total while a nested agent works.
- 2026-11-04 21:34 UTC: correction: the deploy resumed 0cb4b436 and 6c5b17e1; f78c671a had gone to waiting (a question) before the worker restarted, so it was not cut.
## Retest

(Who, when, result.)
