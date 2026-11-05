# QA-113: Drop zone 'Drag and drop files here, or browse' is too thin; no clear highlight while dragging

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | frontend |
| Reporter | user via coordinator |
| Found | 2026-11-05 10:51 UTC |
| Versions | frontend 1.1.86 |
| Where | https://geomind.team/knowledge (and the project Library, New project) |
| Fixer | hotfix-front-II |

## Steps

1. Open Knowledge.
2. Look at the drop zone under the list; drag a file over it.

## Expected

About 3x taller, icon and text centred, a clear highlight while a file is dragged over it; one shared drop-zone component for every upload area.

## Actual

A thin one-line box (about 44 px); the drag highlight is faint.

## Evidence

- ![drop zone](../evidence/QA-113/1.png)

## Cause

The slim variant of the shared DropZone was a single row (py-3); the over state was only a 5 % accent tint.

## Fix

frontend 1.1.91, commit 7169bbe (hotfix-front-II): `shared/attach/drop-zone.tsx` min-height 128 px slim / 192 px full, column layout; while dragging: solid accent border, accent-soft fill, ring, text 'Drop to add the files', no dragleave flicker. Already the one component for Knowledge, Library and New project. The chat composer takes drops on the whole box (no zone) and the case form's per-field file input stays inline. Checked locally on Knowledge: 128 px, drag over shows the highlight. Deploy: 11:00 UTC window.

## Retest

(Who, when, result.)
