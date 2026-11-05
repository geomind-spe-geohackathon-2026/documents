# QA-329: Write tools ran without any approval card with Auto-approve off: a follow-up chat request made ~20 patch_plant and 1 build_plant calls (run e3c10ff9) and the user was never asked, while the run before in the same chat asked for every write

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | backend,geomind |
| Reporter | QA-E2E-design-I |
| Found | 2026-11-05 19:31 UTC |
| Versions | backend 1.1.117 (geomind and gemini of that image) |
| Where | project QA-TEST QA-E2E-design-I 3 (d555740a-1054-4642-b905-4919d36702a7); chat 135dd243-9b7a-4c0f-8763-c64729265b80; runs 06fd16f0 (18:51-19:12 UTC) and e3c10ff9-933a-4ab4-abf5-591d4f2d63f8 (19:15:31-19:31:17 UTC) |
| Fixer | |

## Steps

1. In a chat with Auto-approve off, ask for a design (run 06fd16f0): every build_plant, patch_plant and set_ranges showed an approval card (cards at 18:52-19:06 UTC).
2. In the same chat, send a follow-up: "Now compare the kept design with 2 and 3 doublets at 300 m3/h each ..." (run e3c10ff9).

## Expected

Every write (build_plant, patch_plant, set_ranges, a study that writes designs) asks for approval, as in run 06fd16f0, until the user turns Auto-approve on.

## Actual

Run e3c10ff9 made about 20 patch_plant calls, 1 build_plant, 1 set_ranges, 2 size_plant and 2 run_study calls (log 19:16:53-19:25:04) and **never stopped for an approval**: polling GET /assistant/runs/{id} every 15 s from 19:15:41 to 19:31:17 saw no `request`; the chat shows no approval card for the run. GET /assistant/chat/{chat}/auto-approve = `{"auto_approve": false}` after the run, and the chat's Auto-approve button is `aria-pressed="false"`. I never pressed Auto-approve in this chat.

## Evidence

Run log GET /api/v1/assistant/runs/e3c10ff9-933a-4ab4-abf5-591d4f2d63f8/log (design_lead tool calls 19:16:53-19:25:04); the poller log of this session (no request in 62 polls).

## Cause

Unknown. Guesses: `backend/src/api/v1/assistant/runs/adapters/session.py:129` reads `auto_approve_on(redis, chat_id)` when the run starts; a stale or wrongly keyed Redis value (or a resume path that builds `Permissions(mode="auto")`) would allow every write; or the follow-up run inherited the project lead's "auto" mode from QA-086 (engine.py:398, runs in auto mode take their next steps without asking).

## Proposed fix

Log the permission mode on run.started (and in the run log); build Permissions from the chat's stored setting on every start and resume; a test: two runs in one chat with auto-approve off both ask for writes.

## Fix

## Retest
