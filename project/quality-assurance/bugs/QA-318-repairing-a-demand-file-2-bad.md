# QA-318: Repairing a demand file (2 bad days of 365): the case lead retypes the whole series in save_profile and hits the 16000-token output limit again and again (5+ cut calls, ~90 s each); the case is never stored

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-case-I |
| Found | 2026-11-05 19:17 UTC |
| Versions | backend 1.1.118+ (geomind 0.4.13x) |
| Where | https://geomind.team/projects/8858d2c9-1717-42ce-b650-41f11d0b4272; project QA-TEST QA-E2E-case-I 10; run ed83d196 |
| Fixer | m1 |

## Steps

1. Upload the challenge PDF, the cooling CSV and `Heating_Demand_2027_flawed.csv` (the competition heating file in kW,
   column `heating_demand_kWth`, row 2027-03-15 removed, 2027-07-04 = -500; in `../evidence/QA-318/`). Ask for the case.
2. The lead finds both flaws exactly (19:04 UTC, 4 min: "2027-03-15 is missing", "2027-07-04 = -500 kW is negative"
   with neighbours and the summer base). Answer: "For both days use the mean of the two neighbouring days."
3. It computes both repairs with `calculate` (C8f2937 = 17272.5, C4a4b54 = 5289.5), asks the one question; approve all (19:06:10).

## Expected

A repaired copy of the file is stored by a tool (file in, two rows changed, file out), and set_case names it.
The lead never retypes 365 numbers.

## Actual

- case_lead 13: set_case files alone -> refused; 15: set_case on the flawed file -> "no sample on the local date 2027-03-15".
- case_lead 16-20+: `save_profile` with the whole series typed in the arguments: every call ends at the output limit
  ("Your last answer stopped at the output limit of one call (16000 tokens) and was cut, so nothing of it ran").
  The model shortens the name only, and tries again: 5 cut calls by 19:16 (84-110 s each, 16000 output tokens each).
- At 19:16 UTC: 15 min 45 s since sending, 1.47 M tokens, 0.063 USD, no case.
- Also case_lead 9: two `calculate` calls refused "no operand has a source" for the file's own neighbour values.

## Evidence

- `../evidence/QA-318/run-ed83d196-log.json.gz` (case_lead 9-20), the flawed file.

## Cause

Fact: no tool edits rows of a project file; save_profile takes the values in the call. The 16k output cap and
the "answer again, shorter" hint do not stop a repeat.

## Proposed fix

geomind: a tool `repair_series(file, column, rows={date: value|calculation id}) -> new file` (or set_case
`overrides` on a file series) so a fix is a few tokens; after one cut call of the same tool, refuse the repeat and
tell the lead to ask the user for a fixed file. `calculate`: accept a file cell (file, column, date) as a sourced operand.

## Fix

- 2026-11-05 19:34 UTC: geomind main 0df5771, gemini dev e6284347 (0.6.31); pending deploy
- 2026-11-05 20:32 UTC: QA-E2E-case-I retest 20:32 UTC (run 3bc29e97): repair_series cannot add the missing row, cannot re-repair its output, output header 'date' refused by set_case; proposal 500 kW (sign dropped) vs neighbours 5237/5342; no case after 17 min, cancelled
- 2026-11-05 20:36 UTC: geomind 8e1d0b0: gaps inserted, output round-trips into set_case, neighbours shown; pending deploy
## Retest

Update 19:19 UTC: a 6th cut save_profile (output tokens 124774 -> 140774); I cancelled the run at 19:19
(QA-TEST QA-E2E-case-I 10, 19 min, ~1.5 M input tokens, no case).
- 2026-11-05 20:55 UTC: QA-E2E-case-I 20:55 UTC, backend 1.1.130 / geomind 0.4.135: project QA-TEST QA-E2E-case-I 17 run 5c0ad032: repair_series adds 2027-03-15 = 17272.5 and sets 2027-07-04 = 5289.5 (neighbours' mean, user's rule), file data/Heating_Demand_2027.csv has 365 rows and header 'time'; case v3 stored with it (kW, Europe/Amsterdam). Still 4 files-alone set_case refusals (QA-200)
## Retest (QA-E2E-case-I, 2026-11-05 20:15-20:32 UTC, backend 1.1.127, new tool repair_series)

Project QA-TEST QA-E2E-case-I 15 (369b56d4), run 3bc29e97, same flawed heating file. Still no case after 17 min
(2.97 M input tokens, 0.064 USD); I cancelled at 20:32. 3 case-lead delegations, 8 repair_series, 11 set_case:
1. repair_series cannot ADD a missing row: "row '2027-03-15' is no time of the file's 'date' column nor a row index below 364"
   (refused 3x). A gap is the most common flaw; the tool only replaces rows.
2. The repaired file cannot be repaired again: repair_series(file='data/heating_demand_2027.csv') -> "expected one of
   GEMINI_Cooling..., GEMINI_Hackathon..., Heating_Demand_2027_flawed.csv" (2x).
3. The repaired file keeps the header `date`, and set_case refuses it 5x: "data/heating_demand_2027.csv first column = 'date';
   expected 'time'" (the `columns: {date: time}` mapping is not applied to a data/ file); plus 4x files alone.
4. Accuracy of the proposal: this time the case lead proposed its own repairs in the one question (no free question as in
   run ed83d196): "fill 2027-03-15 with 17300 kW (the previous day's value held)" and for 2027-07-04 = -500 kW
   "500 kW (the magnitude as written, sign dropped)" although the neighbours are 5237 and 5342 kW: 500 is 10x too low.
   Evidence: `../evidence/QA-318/project15-question.txt`, `../evidence/QA-318/run-3bc29e97-log.json.gz`.
Proposed: repair_series takes missing rows too (insert by time), accepts its own outputs, writes the time column as
`time` (or set_case applies `columns` to data/ files); the case-lead prompt proposes interpolation from the neighbours
(with `calculate`) for a single bad day, never a sign flip, and asks the user.
