# QA-006: Many economics keys stay open: no catalogue row

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | data |
| Reporter | Fatemeh (screenshots), Claude (write-up) |
| Found | 2026-11-04 ~19:00 UTC |
| Versions | frontend 1.1.33, backend 1.1.14 (geomind 0.4.25) |
| Where | https://geomind.team/projects/886404e4-3b22-41bd-8986-1a8bc869e25e/assistant/chat/33c76f29-064f-4047-9926-ff8937beddf7; the question's Open list |
| Fixer | |

## Steps

1. Same run; read the Open list of the economics question.

## Expected

Every key the design needs has a cited row, or the user is asked once for it.

## Actual

Open: opex.fixed.production_pump, opex.fixed.compression_chiller, opex.per_energy.compression_chiller / absorption_chiller / adsorption_chiller, revenue.subsidy.capacity. The design cannot price chillers without them.

## Evidence

- ![screenshot 1](../evidence/QA-006/1.webp)

## Cause

A catalogue gap (partly a known issue of geomind 0.4.24), not a code bug.

## Fix

## Retest
