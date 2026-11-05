# QA-240: Study 'sample' offers metrics heating_coverage and cooling_coverage in its form but fails with "by = 'heating_coverage'; expected a key of the reports"

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | backend,gemini |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 17:42 UTC |
| Versions | backend 1.1.108 (geomind 0.4.110, gemini 0.6.17) |
| Where | https://geomind.team/projects/4678c5c6-66fc-46dd-9d1e-358c3c5c1d24 (No-agent showcase); sample study on plant version 8 |
| Fixer | hotfix-python-lead |

## Steps

1. New study of kind `sample` with metrics heating_coverage (offered by `/design/study/kinds`).

## Expected

The study runs, or the form does not offer the metric.

## Actual

failed: `by = 'heating_coverage'; expected a key of the reports; did you mean 'heat_delivered'?`. Same for cooling_coverage (offered too).

## Fix

## Retest
