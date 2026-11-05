# QA-071: web_search: agents send poor queries; search should be English-only

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | Sahand |
| Found | 2026-11-05 01:42 UTC |
| Versions | frontend 1.1.69, backend 1.1.65 (geomind 0.4.64) |
| Where | geomind.team chat, web_search calls of the agents (reported by Sahand; project not given) |
| Fixer | hotfix-python |

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

Example from Sahand (live site, 2026-11-05 ~01:50 UTC): web_search, 0.467 s,
`{"limit": 5, "query": "produced sand concentration geothermal well kg/m3 brine solids removal
cyclone specification"}`. Results: a review of EGS (ResearchGate), a reservoir engineering
textbook (tracer concentration), SIMS 2012 proceedings, a UNESCO geochemistry text, an Epiroc
drilling book. None gives a sand concentration or a desander specification.
Reading: one query mixes three questions (sand rate, solids removal, cyclone spec) and twelve
keywords, so the engine matches generic geothermal pages. Better: one value per query, few
terms, e.g. "geothermal well sand production ppm" then "hydrocyclone desander geothermal brine
specification", and a check first whether the challenge needs that value at all (the PDF gives
no sand data; an approval card for sand concentration also appeared in qa-func-2-II's run).

- Sahand's report in the coordinator chat; the fixer reads recent web_search calls in prod runs.

## Cause

Guess: the web-search skill and the tool description give no rules for queries; the tool
sends no language to SearXNG.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
