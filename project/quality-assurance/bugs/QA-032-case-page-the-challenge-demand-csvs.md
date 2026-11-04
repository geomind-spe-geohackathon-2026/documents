# QA-032: Case page: the challenge demand CSVs are refused by hand (first column 'date', expected 'time'); no way to map the column

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | backend |
| Reporter | qa-8 |
| Found | 2026-11-04 20:26 UTC |
| Versions | frontend bundle index-DnxCbfcj.js, backend 1.1.22 |
| Where | https://geomind.team/projects/55612f74-441f-4a37-9859-a7ea43ab6600/design/case; project QA qa-8 manual pipeline (case v3); no chat, no run; S8 step: Case by hand, Demand tab |
| Fixer | hotfix-back |

## Steps

1. New project, Case page, Start the case (empty).
2. Demand > Heating > Power: click "series", Upload CSV `gemini/examples/hackathon_2026/GEMINI_Heating_Demand_Daily_2027.csv`
   (the competition's file: header `date,heating_demand_MWth`, rows `2027-01-01,24.313`). The same for
   Cooling with `GEMINI_Cooling_Demand_Daily_2027.csv`.
3. Choose the file, the column (`heating_demand_MWth`, `cooling_demand_MWcool`) and the unit MW for each.
4. Time: 2027-01-01 to 2028-01-01, step 1 d.

## Expected

The challenge's own demand files work as given, or the page offers to choose which column is the
time (or converts `date` to `time`).

## Actual

"Save version" stays disabled; the problems box says
`demand.heating.power.file: data/GEMINI_Heating_Demand_Daily_2027.csv first column = 'date'; expected 'time'`
(and the same for cooling). The page gives no way to tell it that `date` is the time column. A user
working by hand must edit the CSV outside the app. The example case in gemini
(`examples/hackathon_2026/data/demand.csv`) uses `time` with ISO timestamps, so it differs from the
files the competition hands out.

## Evidence

- ![demand tab with the problems](../evidence/QA-032/1.png)
- ![time tab, Save version disabled](../evidence/QA-032/2.png)

## Cause

Fact: the message comes from the case check (the series reader wants the first column named
`time`). Guess: accept a first column named `date`/`datetime` (or any parseable first column) in
gemini's series reader, or let the backend's file upload rename it. The agents may convert the file
themselves, which would explain why the chat path works and the hand path does not.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-04 20:30 UTC: for hotfix-back/front: gemini's series reader wants a first column named time and the case has no column-rename field (changing gemini needs Sahand's OK). The backend's case-file upload can rename a first column date/datetime to time (or the Case page can offer it), as the agents already rewrite the file in the chat path. Area moved to backend.
- 2026-11-04 20:32 UTC: hint from hotfix-python: geomind's set_case renames a CSV's first column to time itself (argument columns, geomind/tools/gemini/case.py columns_schema/first_columns); the Case page's upload path does not, so the backend can do the same rename on a by-hand series upload.
- 2026-11-04 20:39 UTC: backend 1.1.35 (355f631) pushed 20:39 UTC, not deployed: 21:00 UTC window. POST /design/case/files saves a CSV whose first column is date/datetime/timestamp with it named time. Date-only values need the case's time zone (gemini reads a time without offset as local in it).
- 2026-11-04 21:03 UTC: deployed in backend 1.1.40 at 21:02 UTC.
## Retest

(Who, when, result.)
- 2026-11-04 21:04 UTC: checked in the production API container (1.1.40): with_time_column turns the header 'date,heating_demand_MWth' into 'time,heating_demand_MWth'. Not uploaded through the page.
