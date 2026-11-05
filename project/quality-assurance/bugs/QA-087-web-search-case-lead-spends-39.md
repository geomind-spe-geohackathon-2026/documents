# QA-087: web_search: case_lead spends 39 searches on one value (compression chiller variable O&M); half refused for >8 words, many empty; no value or source returned

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | functional-qa-3 |
| Found | 2026-11-05 07:23 UTC |
| Versions | backend 1.1.75-1.1.76 (geomind 0.4.71-0.4.72), frontend 1.1.71 |
| Where | project QA2 functional-qa-3 studies (932b318c-f285-4827-aefe-c8fa3327735b), chat 510ab94f-c4f7-4019-9f75-cb40229b374e, run 753645c0, case_lead steps after the 'chiller O&M' question |
| Fixer | hotfix-python |

## Steps

1. Design run asks for `economics.opex.per_energy.compression_chiller` (no catalogue row).
2. Answer: 'I do not know it; look it up on the web with a short English search, one value per query, show value, page and unit conversion; else use heat pump 1.69 EUR/MWh as a labelled assumption'.

## Expected

A few short searches, one value, a source the user can approve, or an early stop and the fallback the user allowed.

## Actual

case_lead made 39 web_search calls in about 30 min (run JSON, tool_calls): about 19 refused with invalid_input (query longer than 8 terms, e.g. 'chiller plant non-fuel variable operating cost per MWh cooling'), about 12 returned empty results (quoted phrases such as '"central compression chiller" VOM'), the rest returned unrelated pages (sciencedirect, uaeexperthub, ashrae). It never read a page with read_web_page, never gave a value, and never fell back to the user-allowed heat pump assumption before the run failed (QA-081, second occurrence). The agent repeats near-identical queries ('"compression chiller" VOM "EUR/MWh" DEA technology data 2020', 3 variants).

## Evidence

- ![screenshot](../evidence/QA-087/1.png)
- Run JSON (gzip): `../evidence/QA-087/run-753645c0.json.gz`

## Cause

Guess: the web-search skill has no search budget or stop rule, and the 8-term limit (QA-071) makes the agent rewrite instead of picking a better source; a cap of about 6 searches then the user's fallback would fit.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 07:31 UTC: geomind 0.4.73 (web_search: six searches per agent and run, searches_left, then a labelled assumption or a gap), backend 1.1.78 (1ed06d8), deployed 07:30 UTC
## Retest

(Who, when, result.)
