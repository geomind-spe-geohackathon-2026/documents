# QA-364: Results page of projects 0b986dd6 and 8d5d21e0 shows 'Something went wrong' (Cannot read properties of null) instead of the result list

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | frontend |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 22:07 UTC |
| Versions | live build of 2026-11-05 22:10 CET (backend 1.1.134) |
| Where | https://geomind.team/projects/0b986dd6-8f95-4383-9d15-5e589ff122c9/design/results and https://geomind.team/projects/8d5d21e0-ecb0-4894-9cfd-bdd61f670ac7/design/results |
| Fixer | |

## Steps

1. Log in, open either project, open Results.

## Expected

The result list and charts of the project (0b986dd6: agent run 55be302a, LCTS 38.05; 8d5d21e0: no-agent showcase with sensitivity and Monte Carlo).

## Actual

The page shows the error boundary "Something went wrong" with "Cannot read properties of null". Found while recording the demo video; project de2aef71's Results page loads. 0b986dd6's report page also shows an amber "Out of date" banner.

## Evidence

- Seen during the demo recording (Playwright, 22:00-22:12 CET); no screenshot kept.

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
