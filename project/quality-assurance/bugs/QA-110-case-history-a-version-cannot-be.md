# QA-110: Case History: a version cannot be opened, compared or restored; the note is always 'Case set by the assistant' and Saved by says Administrator

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | frontend |
| Reporter | Fatemeh (screenshot), Claude (write-up) |
| Found | 2026-11-05 10:45 UTC |
| Versions | backend 1.1.84 |
| Where | https://geomind.team/projects/cf0c3d9c-d925-4ffa-bd29-3ac8205090d3/design/case?chat=27379f2e-0103-4ddf-a020-f0cd4deb20a6, Case > History |
| Fixer | hotfix-front-III |

## Steps

1. A run sets the case three times (v1 11:13, v2 11:14, v3 11:15).
2. Open Case > History.

## Expected

The user can see what each version holds and what changed: open a version, see the differences to the one before (paths, old and new values, with their source), and restore an older one, as the Plant History can (Restore). The note says what changed ("requirements: heating_unmet_share added"), and Saved by names the assistant when the assistant saved it.

## Actual

A read-only list: Version, Note, Saved by, Saved. No row opens; no compare; no restore. Every note is "Case set by the assistant". Saved by says "Administrator" for versions the assistant made. Since every value in the case must carry its source and the user approves it (the no-default rule), the user has no way to see which values changed and why.

## Evidence

- ![Case History](../evidence/QA-110/1.webp)
- `frontend/src/domains/design/case/history-panel.tsx`: the case panel takes no `onRestore` and has no row action; the plant's history panel has Restore.

## Cause

Fact (code): the case history renders a plain table. Guess: the backend stores each version's content (case_versions.content) but no change summary; the note comes from geomind's set_case with a fixed text, and the author is the logged-in user who owns the run. Fix: a row opens the version read-only with a diff to the previous one (paths and values, source), a Restore like the plant's, a note built from the changed paths, and Saved by "Assistant (run <id>)".

## Fix

hotfix-back-II, 2026-11-05 11:05 UTC, backend part (split agreed with hotfix-front-II; frontend
part for hotfix-front-III, `.claude/notes/sessions/hotfix-front-2.md`). The note text came from
the backend (`VersionRecorder`, a fixed "Case set by the assistant"), not geomind; Saved by is the
run's user because the assistant saves as that user. Backend 1.1.87 (49d587b): `GET
/design/case/versions/{number}`; `POST /design/case/versions/{number}/restore` `{project, base}`
(content and files of that version as the next version, note "Restored version N", 409 on a stale
base); assistant case notes name up to six changed paths and files; `Version.by` = `assistant` or
`user` on case and plant versions. Deploy 11:30 UTC. Still owed (frontend): open a version
read-only, diff with the previous one, Restore, Saved by from `by`.
- 2026-11-05 11:05 UTC: backend part done in 1.1.87 (11:30 UTC); frontend part for hotfix-front-III
- 2026-11-05 ~12:40 UTC (live backend 1.1.86, so 1.1.87 not out yet): the Plant History has the same gaps, so the frontend part should cover both panels: a version cannot be opened or compared (only Restore); Saved by "Administrator" on assistant versions; the notes are cut ("Plant energy_r8 changed by the assist...") and say only the design's name, not what changed; a "#" column (1, 2, 3 ...) beside Version repeats the order and means nothing to the user. ![plant history](../evidence/QA-110/2-plant-history.webp)

hotfix-front-III, frontend part: 1.1.97 (f19a7da) and 1.1.98 (464d96d), shared `frontend/src/shared/versions/` (diff and history views) for Case and Plant History: no "#" column beside Version; the full note; Saved by "Assistant" from `Version.by`; Open on every row opens the version read-only with "Changes from version N-1" (path, added/removed/changed, old and new value, source; case files included; plant modules, connections, spec, structure) and "All values". Case: "Restore this version" posts `/design/case/versions/{n}/restore` with the latest number as base (a 409 says the case was saved again; disabled while the form has unsaved changes). Plant: Restore loads the version into the editor as before. Deploy 11:30 UTC.
- 2026-11-05 14:11 UTC: frontend 1.1.99 (e9435c4) deployed 14:10 UTC, bundle index-BlepNtQt.js
## Retest

- 2026-11-05 14:12 UTC: live 1.1.99 with backend 1.1.87: Case and Plant History without # column, Saved by Assistant, Open shows read-only version, case v8 vs v7 diff (reference_depth 2500->3000 m, heating return 60->55 degC), plant v2 vs v1 diff. Restore not pressed live (would write a version)
