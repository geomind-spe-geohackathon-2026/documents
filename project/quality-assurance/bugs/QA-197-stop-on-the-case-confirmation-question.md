# QA-197: 'stop' on the case confirmation question does not stop: the project lead sends the case lead again, which makes 7 more set_case calls and asks to store the case

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-case-I |
| Found | 2026-11-05 17:21 UTC |
| Versions | frontend 1.1.113, backend 1.1.103-1.1.104 (geomind 0.4.98-0.4.99) |
| Where | https://geomind.team/projects/92b44928-ff0d-4954-a554-f166477af892/assistant/chat; project QA-TEST QA-E2E-case-I 3; run 6a2d6017 |
| Fixer | |

## Steps

1. New project, upload the challenge PDF and the two CSVs, "Build the complete case ... Stop when the case is complete."
2. The case lead asks the one confirmation question (17 values from the assumptions document); press **stop** (17:11:06 UTC).

## Expected

`stop` ends the case work: the case lead reports what is set and open, the project lead hands that to
the user and the run ends. No further tool call writes the case (handbook-case 8.5: "options approve all,
change some, stop").

## Actual

- case_lead (1st instance) returns "The user answered **stop** ... no case was set".
- project_lead step 2 calls `case_lead` **again** (2nd instance, 17:11 to 17:13:45). It makes 7 more
  `set_case` calls in 2.5 min: 6 refused (files alone; no time_zone x2; power missing x2;
  `requirements[0].case_requirement`, `over` missing) and the 7th is an approval card
  "Allow Set case ... format, kind, name, time ... and 13 more" at 17:13:45, which I denied.
- The run then goes on to the curator (2 Write lesson cards, one of them a wrong lesson, see QA-199) and ends 17:15:50.
- The final answer blames the time zone ("Blocking: both demand series carry dates with no UTC offset")
  for the case not being stored, not the user's stop and denial.
- Cost of the ignored stop: about 4 min, ~600 k input tokens (2nd case_lead), 3 extra cards.

## Evidence

- Run log `../evidence/QA-197/run-6a2d6017-log.json.gz`: steps project_lead 2 (`case_lead` call with the
  1st return text), case_lead 4-12 (set_case calls and errors).
- Chat transcript: "You answered: stop" then "You denied Set case: denied by the user", "You approved Write lesson" x2.

## Cause

Guess: the project lead's prompt does not treat a user's `stop` to a team's question as the end of the
request; it sees "case not set" and re-delegates to finish the brief. The 2nd case lead does not see the
stop either (it asked nothing; it only tried to store file values).

## Proposed fix

geomind `agents/project/lead.py` (prompt) and/or the delegate tool: when a team's return says the user
answered `stop`, the project lead finishes with that report and does not call the team again in this
request (like `earlier_denial` for tools, QA-116: an `ask_user` answer `stop` should hold for the rest of
the request tree). Final summary must name the user's stop as the reason.

## Fix

- 2026-11-05 17:53 UTC: geomind 0.4.111-0.4.114 (HEAD 778970d), deployed in backend 1.1.110 at 18:51 CET
## Retest
