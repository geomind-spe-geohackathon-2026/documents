# QA-033: Case page: the box says '2 problems to fix' but lists 5 lines, one of them twice

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | frontend |
| Reporter | qa-8 |
| Found | 2026-11-04 20:26 UTC |
| Versions | frontend bundle index-DnxCbfcj.js, backend 1.1.22 |
| Where | https://geomind.team/projects/55612f74-441f-4a37-9859-a7ea43ab6600/design/case; project QA qa-8 manual pipeline (case v3); no chat, no run; S8 step: Case by hand, Demand tab |
| Fixer | |

## Steps

1. Case page, Demand: set heating and cooling power to series from a CSV whose first column is not
   `time` (see QA-032).
2. Look at the red box.

## Expected

The count matches the lines, and each problem is listed once, in plain words.

## Actual

The box says "2 problems to fix before saving" and lists 5 lines:
`demand.heating.power enter a valid value`, `demand.cooling.power enter a valid value` (twice), and
the two file problems. "enter a valid value" does not say what is wrong (the real cause is the file
line below it).

## Evidence

- ![problems box](../evidence/QA-033/1.png)

## Cause

(Facts, or a guess marked as one.) Guess: the count is of files/fields, the list of form errors plus check problems; the form errors repeat.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
