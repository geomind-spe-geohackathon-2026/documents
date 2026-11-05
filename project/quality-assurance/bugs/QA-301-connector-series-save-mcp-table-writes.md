# QA-301: Connector series: save_mcp_table writes data/open-meteo_*.csv but set_case does not find it ('file not found' / 'expected one of' the project files): 20 refused set_case, 4 save cards, 6.5 min before the case is stored

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-case-I |
| Found | 2026-11-05 18:52 UTC |
| Versions | frontend 1.1.125+, backend 1.1.116+ (geomind 0.4.12x) |
| Where | https://geomind.team/projects/dbe6165f-a36d-4643-9eca-027411ca9a7c; project QA-TEST QA-E2E-case-I 9; run 08d3739c |
| Fixer | m7 |

## Steps

1. New project (open-meteo checked in the dialog, QA-255 fix: `mcp` holds its id), PDF + 2 CSVs,
   "The plant stands in Delft ... with the real outside air of the site for 2027".
2. Approve the "Saved a connector table to the case" card (18:42:41 UTC): `save_mcp_table` -> file
   `data/open-meteo_delft_2027_climate.csv`, 365 rows.
3. The question lists site.air.temperature / relative_humidity as that file's columns: approve all (18:44:45).

## Expected

One set_case with the demand files and the saved connector file; case stored at once.

## Actual

21 set_case calls, 20 refused, in 6.5 min (18:44:45 -> 18:51:21), plus 3 more save_mcp_table approval cards:
- `unknown_name`: "file = 'open-meteo_delft_2027_climate.csv'; expected one of GEMINI_Cooling..., GEMINI_Hackathon..., GEMINI_Heating..." (x2)
- `missing_value` x12 in a row (case_lead 16-27, same input): "site.air.temperature.file: file 'open-meteo_delft_2027_climate.csv' not found"
- `case_incomplete` (files alone) x5
- the lead re-saves the table 3 times (with and without `data/`) and the project lead once.
The 15th call of the 2nd case-lead instance finally stores the case (file `data/open-meteo_delft_2027_climate.csv`).
Tokens: the run reached 2.49 M input tokens before the case was stored (0.049 USD).

## Evidence

- `../evidence/QA-301/run-08d3739c-log.json.gz`: case_lead 7 (save), 13-30 (set_case refusals), project_lead 5, 2nd case_lead 5-15.

## Cause

Guess: `save_mcp_table` writes the file where set_case's list of project files (list_files) does not see it
(name with `data/` vs without; or the file list is cached for the run); set_case's suggestions list only the
3 uploaded files, so the model loops. The repeat guard did not stop 12 identical calls.

## Proposed fix

geomind: save_mcp_table returns the exact name set_case accepts and set_case resolves both `data/x` and `x`
to the saved file; the "expected one of" list includes saved connector files; the repeat guard stops after
2 identical refused calls.

## Fix

- 2026-11-05 19:12 UTC: geomind main 71d80ab (0.4.131+), gemini dev 5782a138 (0.6.27); QA-312 also needs back-lead's DatabaseWorkspace.save_plant_version
- 2026-11-05 19:55 UTC: QA-E2E-case-I retest 19:54 UTC: file found now, but 9 files-alone refusals + a time-zone mismatch of the saved series; run 33 min, 4 M tokens (see Retest)
## Retest

## Retest (QA-E2E-case-I, 2026-11-05 19:21-19:54 UTC, backend 1.1.121)

Project QA-TEST QA-E2E-case-I 11 (50adc3fa), run ec1094d9, same request as project 9. "File not found" is gone,
but the connector path is still slow: 12 set_case (9 refused `case_incomplete` files alone, 1 `invalid_data`:
"delft_air_temperature_2027.csv column 'temperature_2m_mean' covers 2026-12-31T23:00:00+00:00 to 2027-12-31T23:00:00+00:00;
requested 2027-01-01T00:0..." (the series was saved at Amsterdam midnight = 23:00Z), 1 invalid_value, 1 invalid_input),
5 save_mcp_table cards, 12 read_mcp, 44 read_stored, 2 case-lead delegations. The lead then switched both demand series to
`time_zone: UTC` (project 9 had Europe/Amsterdam) to make the dates match. Run: 32 min 47 s, 4.04 M input tokens,
0.086 USD (project 9: 13 min). Case v2 stored with the series. Evidence: `../evidence/QA-301/run-ec1094d9-log.json.gz`.
Proposed: save_mcp_table saves daily data at the case's own day boundaries (time_zone of the case) or records the
series' zone so set_case aligns it; see QA-200 for the files-alone refusals.
