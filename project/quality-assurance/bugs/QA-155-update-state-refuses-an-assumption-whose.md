# QA-155: update_state refuses an assumption whose citation is a string, while the error's own shape says 'citation?: string | any | null'

| Field | Value |
|---|---|
| Status | open |
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
