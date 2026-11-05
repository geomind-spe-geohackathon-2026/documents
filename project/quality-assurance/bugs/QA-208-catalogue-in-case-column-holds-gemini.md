# QA-208: Catalogue: in_case column holds gemini's hackathon sample values (43 rows, e.g. 1239.1304347826087, 0.3, 60), competition data in a general catalogue, unused by code

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | data |
| Reporter | handbook-econ-report-I |
| Found | 2026-11-05 17:24 UTC |
| Versions | Knowledge data-economics.csv 74a0d44b; geomind data/knowledge/data-economics.csv (main) |
| Where | data-economics.csv column `in_case` (43 rows); data-economics.md |
| Fixer | handbook-econ-report-I |

## Steps

1. `python3 -c "import csv; print(sorted({r['in_case'] for r in csv.DictReader(open('data-economics.csv')) if r['in_case']}))"`

## Expected

A general catalogue holds sourced values only. Competition data lives in its own Knowledge files (Sahand, 2026-11-05: no competition specifics in general material); the hackathon sample values are in `knowledge/hackathon-2026-assumptions.md`.

## Actual

43 rows carry `in_case` = the value gemini's hackathon sample uses for that key: 0.05, 0.1, 0.2, 0.2239, 0.3, 0.5, 0.73786, 1, 1000000.0, 1239.1304347826087, 2, 300, 500, 60 (e.g. every drilling row shows 1239.1304347826087, the absorption chiller rows 0.3, the heat price rows 60). No code reads the column (`grep -rn in_case geomind/geomind`: none). An agent reading a row can take `in_case` for a recommended or case value, and it repeats the 17-digit precision of QA-202.

## Evidence

- The rows quoted above (`geomind/data/knowledge/data-economics.csv`).

## Cause

Fact: a column from gemini's `docs/cost-sources/sources.csv` (v0.5.13) that compared each row with the sample case.

Fix (data): drop the `in_case` column from data-economics.csv (and its mention, if any, in data-economics.md); re-upload. The sample's values stay in the assumptions file.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
