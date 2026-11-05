# QA-155: update_state refuses an assumption whose citation is a string, while the error's own shape says 'citation?: string | any | null'

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 16:53 UTC |
| Versions | backend 1.1.102/1.1.103 (geomind 0.4.98), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 1` (4ce816b1-4bd1-48a5-8e77-9414c2b86301); chat fa9cfafb-e39e-4ccd-9dfb-d8427f518c43; run c2b815a8-8c54-4bae-b1c1-769351434fe6 |
| Fixer | |

## Steps

1. Same run as QA-152. The analysis lead records an assumption with
   `citation: "case economics.json (read_case section economics)"`.

## Expected

Either the string is accepted, or the tool description and the error say that `citation` is an
object (`{title, publisher, year, ..., note}`).

## Actual

Analysis lead step 5 (16:53:39): `update_state` -> `invalid_input changes[0] ... citation: Input
should be a valid dictionary; expected '/assumptions/-' to hold Assumption {..., 'citation?': 'string |
any | null'}`. The shape in the error says a string is allowed. One wasted round trip (19 k input
tokens, 9.7 s); the lead retried without the citation 4 minutes later (step 12), so the source of the
assumption was lost.

## Evidence

- `../evidence/QA-152/run-c2b815a8-log.json`, analysis lead steps 5 and 12.

## Cause

`geomind/geomind/context/state.py:41` `citation: dict[str, Any] | None`; `geomind/geomind/tools/state.py`
`shape_of` (around line 74) writes `dict[str, Any]` as `string | any` (it renders the dict's key and
value types, not "object").

## Proposed fix

`tools/state.py`: render a `dict[...]` annotation as `object {title?, publisher?, year?, page?,
link?, note?}` (or `object`). Optionally accept a plain string citation as `{"note": <string>}`.

## More evidence (2026-11-05 17:16 UTC)

Run 57c42f61-2a89-48ba-933c-e87fc348084f, economist steps 11 and 15: the same refusal twice
(`citation: 'user instruction in this chat'`), accepted at step 16 without the citation. Log:
`../evidence/QA-176/run-57c42f61-log.json`.

## Fix

- 2026-11-05 18:59 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)

## Retest

- 2026-11-05 19:15 UTC, QA-AI-analysis-I: geomind 0.4.130 (live since deploy 36, backend 1.1.118+) has
  `Assumption._text_citation` (`geomind/context/state.py:43-46`): a text citation is kept as its `note`. In 5 live
  runs since the deploy (676a19e1, 6c88bb13, edaad491, 1fba1e30, 511a6821) no `update_state` was refused for a citation;
  the agents now send citations as objects. Verified (by the deployed code and no recurrence; the agents did not send a
  text citation in these runs, so the text path itself was not hit live).
