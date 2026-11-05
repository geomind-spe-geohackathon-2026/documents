# QA-071: web_search: agents send poor queries; search should be English-only

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | Sahand |
| Found | 2026-11-05 01:42 UTC |
| Versions | frontend 1.1.69, backend 1.1.65 (geomind 0.4.64) |
| Where | geomind.team chat, web_search calls of the agents (reported by Sahand; project not given) |
| Fixer | |

## Steps

1. In a chat, let an agent look up a value the files do not give (it calls web_search).
2. Read the query the agent sent in the web_search card.

## Expected

Short, specific English search queries made of the technical terms of the value sought (e.g.
"absorption chiller COP single effect 90 C hot water", "geothermal doublet drilling cost per
km Netherlands 2024"), refined when the first results are poor. Searches in English only.

## Actual

The agents generate poor queries (Sahand, 2026-11-05): results do not answer the question.

## Evidence

- Sahand's report in the coordinator chat; the fixer reads recent web_search calls in prod runs.

## Cause

Guess: the web-search skill and the tool description give no rules for queries; the tool
sends no language to SearXNG.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
