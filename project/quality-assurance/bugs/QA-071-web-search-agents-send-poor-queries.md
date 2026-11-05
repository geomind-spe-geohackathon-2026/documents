# QA-071: web_search: agents send poor queries; search should be English-only

| Field | Value |
|---|---|
| Status | fixed |
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

Cause (read in prod run_events, hotfix-python-II): queries in Dutch (`Nederland warmtenet ontwerptemperatuur aanvoer 100 °C retour temperatuur`, `KNMI De Bilt langjarig gemiddelde temperatuur 1991-2020 ...`), a search for the project itself (`GEMINI agentic geothermal design hackathon site location Netherlands demand profiles`), searches for values the brief fixes (100 C supply, 20 C chilled water), and long piles of terms for two values (Sahand's sand example, 11 words). The tool sent no language and gave no query rules; the skill had one line on queries.

Fix: `web_search` sends `language=en` to SearXNG and refuses a query longer than 8 words or not in English (non-Latin letters, or common Dutch, German, French or Norwegian words), with an error that says why. The tool description and the `web-search` skill teach: first whether the value is needed at all (a detail the brief never mentions becomes a labelled assumption or a gap, not a long search); never a value the files or the case give, never the project or the chat; one value per query, 3 to 6 English technical terms (quantity, technology, unit, region and year when they matter), with good and bad examples (Sahand's sand query among the bad); 2 or 3 refined queries when results are weak, then ask; primary sources first (IEA, IRENA, EU JRC, TNO, manufacturers, papers). geomind 0.4.65 (commit ea62530, tag v0.4.65), backend 1.1.69 (c330a8d), deployed 2026-11-05 02:00 UTC. Checked in geomind-celery: `geothermal well sand production ppm` gives a GEUS geothermal best-practice PDF among the results; the Dutch KNMI query is refused.

## Retest

(Who, when, result.)
