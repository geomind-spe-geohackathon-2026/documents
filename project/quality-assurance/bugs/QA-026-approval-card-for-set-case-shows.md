# QA-026: Approval card for set_case shows only 'Allow set_case (write)?': the user cannot see which values, units or sources they approve

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | qa-1 |
| Found | 2026-11-04 20:21 UTC |
| Versions | frontend bundle assets/index-DnxCbfcj.js, backend 1.1.22; model deepseek/deepseek-v4.1-flash-1017 |
| Where | https://geomind.team/projects/541aa78f-8181-45f4-ac36-e47305e33f37/assistant/chat/062b25d8-1e4a-4b38-aed3-2209baba430a; project "QA qa-1 S1 end to end"; run b894b090-ad7e-4ef6-8c92-412d63bdb989; case lead's first set_case (request-146), 20:20 UTC |
| Fixer | hotfix-python |

## Steps

1. New project, Auto-approve off; attach the challenge PDF and the two demand CSVs; send "Design a
   geothermal heating and cooling plant ... set the case and the economics, design ..., report".
2. The case lead reads the files, asks the geoscientist, then calls set_case.
3. Look at the approval card in the chat.

## Expected

The approval shows what will be written: each key, value, unit and source (file, page), so the user
can check it before approving (project rule: data the user approves comes with its source). At
least a "show details" with the call's arguments.

## Actual

The card reads only "Approval needed / Allow set_case (write)? / Reason (optional) / Approve / Deny"
(screenshot 1). The run's request (`GET /assistant/runs/{id}`) holds only kind, agent, call_id and
the message "Allow set_case (write)?"; no arguments. The steps panel ("Steps so far") does not show
the pending call either, and the run log has no entry for it until the step ends. The user approves
blind. In S1 every case write goes through this card.

## Evidence

- ![screenshot](../evidence/QA-026/1.png)
- Run while waiting: [run-b894b090-waiting.json](../evidence/QA-026/run-b894b090-waiting.json)

## Cause

Fact: `frontend/src/domains/assistant/chat/request-card.tsx` (`Approval`) renders only the
message, a reason field and the two buttons. Guess: geomind's approval request carries no
arguments, so the frontend has nothing to show; both sides need a change (geomind: put the
arguments, or a summary of keys/values/sources, into the request; frontend: show them).

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-04 20:23 UTC: belongs in geomind first: RequestMade.data() (geomind/types/events.py) drops the pending call's input, so the request event and GET /assistant/runs/{id} carry only the message; the frontend cannot show values it never gets. Once geomind puts the call input (or a key/value/unit/source summary) in the request, hotfix-front adds it to the approval card (request-card.tsx).
- 2026-11-04 20:23 UTC: moved to geomind (see the note above): the pending call's input never reaches the frontend
- 2026-11-04 20:29 UTC: fixed in geomind 0.4.32 (commit 97dbbe1): the approval message now holds the call's input as indented JSON (multi-line). Backend 1.1.27 (27adbc4), waiting for deploy. For hotfix-front: request-card.tsx should show the message with its line breaks (whitespace-pre-wrap, perhaps a collapsible details block).
- 2026-11-04 20:31 UTC: shipped in backend 1.1.27 with geomind 0.4.32; prod worker's approval message carries the call input. Live retest (approval card) still to do; the card needs line breaks (hotfix-front).
## Retest

(Who, when, result.)
