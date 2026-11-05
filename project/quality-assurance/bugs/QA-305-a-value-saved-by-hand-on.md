# QA-305: A value saved by hand on the Case page keeps its old about.sources entry (discount 0.065 saved by hand still says 'user: 6 % in the answer to the economics question')

| Field | Value |
|---|---|
| Status | verified |
| Severity | minor |
| Area | frontend |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 18:57 UTC |
| Versions | backend 1.1.118, frontend live 2026-11-05 18:57 UTC |
| Where | project "QA-TEST QA-E2E-economics-I 6", Design > Case > Economics > Fill in here; case v7 |
| Fixer | |

## Steps

1. Economics set by chat: discount 0.06 with source "user: 6 % in the answer to the economics
   question (the assumptions document gives 0.05)".
2. Case > Economics > Fill in here: Discount rate 0.065; Save version, note "QA: discount 6.5 % by
   hand" (v7).

## Expected

`economics.about.sources.discount_rate` names the hand edit, e.g. "edited by hand, case v7: QA:
discount 6.5 % by hand" (or the user's name and time).

## Actual

v7: `discount_rate.value` 0.065, `about.sources.discount_rate` still "user: 6 % in the answer to
the economics question ..." (API `/design/case`). The agents notice it (a chat answer of 18:56 UTC
said "the note is stale ... say the word and I'll have the case team correct it"), but every
report and explainer reading the sources cites a wrong origin. Split from QA-284 (whose main
part is verified).

## Cause

Fact: the form saves values only; `about.sources` is not touched on a hand save.

## Proposed fix

frontend (schema form save, or backend `save_case` when the diff touches a key that has a source):
for each changed key write `about.sources.<key> = {"source": "edited by hand", "version": <n>,
"note": <note>, "user": <name>}`.

## Fix

Fix: frontend 1.1.131 (commit 9f40897, bundle index-PVHgYO42.js), by front-m2: withHandSources in use-case-editor.ts sets 'user: set by hand on the Case page' on changed keys.
- 2026-11-05 19:14 UTC: frontend 1.1.131
## Retest

- 2026-11-05 19:26 UTC, QA-E2E-economics-I: PASSES on frontend bundle index-PVHgYO42.js. Project 6,
  Fill in here, discount 0.055, Save version (v8): `about.sources.discount_rate` = "user: set by
  hand on the Case page"; the unchanged `carbon.price` keeps its own source. (Version and note are
  not in the source; fine.)
- 2026-11-05 19:24 UTC: QA-E2E-economics-I 19:26 UTC: hand save writes 'user: set by hand on the Case page' for the changed key only (v8)
