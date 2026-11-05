# QA-310: After a cancelled run, the next message is routed as the cancelled request: a Persian LCOH question becomes 'make the heat pump smaller', and the run asks patch_plant 10 MW, which the user had denied three times

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 18:58 UTC |
| Versions | backend 1.1.116+ |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 3 (3ecb4493-3368-4bc2-b2f0-ca0b06670a86); chat 5db7a37c-b2ea-43d6-982f-5ebf2b8ad6a7; run d0098ccc-823c-4c39-9550-3f745612dc9b (after the cancelled run 204b9cd8 of QA-288); request-71 |
| Fixer | |

## Steps

1. QA-288: "Make the heat pump smaller to lower LCOH." Deny set_ranges three times ("Do not change or search the plant ...", "I already said no: no search, no change."), then cancel the run (`POST /assistant/runs/204b9cd8.../cancel`, ended `cancelled`).
2. Next message, in Persian: "هزینه گرمای این پلنت (LCOH) چقدر است و بزرگ‌ترین بخش هزینه کدام است؟" (What is this plant's LCOH and what is the largest cost item?)

## Expected

A question about a result: `loop: tool`, analysis lead, answer from the stored result (LCOH 43.75 EUR/MWh, the cost items), in the user's language or English. The cancelled request stays cancelled.

## Actual

- Coordinator (the conversation it reads: "Make the heat pump smaller to lower LCOH." with no answer and no denial, then the Persian question): `{"kind": "loop", "loop": "project", "task": "The user wants the heat pump made smaller to lower LCOH (the design lead's unconfirmed pick is 10 MW, down from 15 MW in design/v1) - size it and check the plant still meets the case. The user also asks, in Persian, what the plant's LCOH is ... answer that alongside."}`
- The project lead briefs the design lead to resize; 20 s later the user gets (request-71): "Allow patch_plant (write)? Change 1 value(s) of design/v1 and save it as 'hp10': params.heat_pump.capacity." with 10.0 MW, the change the user had refused three times. Cancelled again by me.

## Evidence

- `../evidence/QA-/d0098ccc-823c-4c39-9550-3f745612dc9b.log.json`: coordinator step 1, its messages (the cancelled user message with no reply, no record of the denials or the cancel) and its route; request-71.
- `../evidence/QA-/d0098ccc-823c-4c39-9550-3f745612dc9b.trace.txt`.

## Cause

- A cancelled run leaves its user message in the conversation with no assistant message; nothing says "cancelled by the user" or what the user denied, so the next run's coordinator reads it as still open.
- The cancelled run's assumption `A-hp-pick` (10 MW, unconfirmed) stays in the problem state and reads like a plan.

## Proposed fix

- backend (chat) or geomind (run end): on `cancelled`, store an assistant message (or a system note in the conversation the agents read) such as "Cancelled by the user. Denied: set_ranges heat_pump.capacity 3-15 MW (reason: ...)."
- geomind `prompts/project/coordinator.md`: "Route the newest user message only; an earlier message without an answer was cancelled or failed: never fold it into the task."
- geomind: drop or mark an unconfirmed assumption of a cancelled run, or keep denials in the problem state (`denied: [...]`) for later runs of the chat.

## Fix

## Retest
