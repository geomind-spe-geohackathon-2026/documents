# QA-290: Report page gives no warning that its result ran on case v3 after the case changed to v4: header 'Draft from simulation v1', only a small 'From case version 3' under Costs; Export PDF the same

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | frontend |
| Reporter | QA-E2E-report-I |
| Found | 2026-11-05 18:45 UTC |
| Versions | backend 1.1.109+, frontend bundle index-TsXgd_n9.js |
| Where | https://geomind.team/projects/fa329839-43df-48c3-81c3-89af503b92c0/design/report; project QA-TEST QA-E2E-report-I 2 |
| Fixer | |

## Steps

1. Project with result "simulation v1" on case v3.
2. Change the case (here heating return temperature 60 -> 50 degC, saved as case v4 with the
   same call the Case page makes).
3. Open the Report page.

## Expected

A clear note at the top of the report (and in the PDF/Markdown): "This result ran on case
version 3; the case is now version 4. Run the study again before you send this report." The
Study and Results tabs already say "Out of date".

## Actual

Tabs: Study "Out of date", Results "Out of date"; Report "Draft". Report header: "Draft from
simulation v1." Nothing else, except "From case version 3, plant version 1." under Costs.
The PDF/Markdown export carries no warning either (checked the Markdown of the same report
before the change: no case-version note in the header).

## Evidence

- ![Report page after the case change](../evidence/QA-290/1.png)

## Cause

Guess: the Report page does not compare the result's case_version with the project's current one.

## Fix

Proposal (frontend): when result.case_version or plant_version differs from the current
versions, show an "Out of date" banner on the Report page and add the same line to the
exported header (backend export, if the text is built there).

## Retest

(Who, when, result.)
