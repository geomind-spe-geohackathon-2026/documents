# QA-315: save_mcp_table refuses time_zone 'UTC' because open-meteo names its times 'GMT' (same zone): one refused call per connector series

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 19:00 UTC |
| Versions | geomind 0.4.131 |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 11 (ed373904-e143-412b-b1b5-f4a21fe6f48b); run f4018b98-e445-4c8f-a3f5-4c6eea269d10; case_lead 19:00:17 and 19:00:32 UTC |
| Fixer | |

## Steps

1. As QA-314 (Delft, outside air from a weather service).
2. Read the case lead's `save_mcp_table` calls.

## Expected

UTC and GMT are the same offset (0); a request with `time_zone: "UTC"` for an answer in GMT is saved.

## Actual

- 19:00:17 `save_mcp_table(answer="mcp-f92d7113c077023c", table="structured.daily", file="delft_air_2027.csv", time_zone="UTC")`
  -> `invalid_input`: "time_zone = 'UTC', but the answer names its times in 'GMT'; expected no time_zone, or 'GMT'".
- 19:00:32 the same with "GMT": saved (365 rows). One more approval card and an LLM round trip (~15 s).
- Then the series is set in the case with `"time_zone": "UTC"` anyway.

## Evidence

- `../evidence/QA-314/run-f4018b98.json` (case_lead `save_mcp_table` calls)

## Cause

`save_mcp_table` compares the zone names as strings.

## Proposed fix

geomind `tools/mcp.py` (`save_mcp_table`): compare zones by their offset or IANA canonical name
(UTC, GMT, Etc/UTC, Z, Etc/GMT are equal), and accept them.

## Speed and accuracy

~15 s and one approval card per connector series. No accuracy effect.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
