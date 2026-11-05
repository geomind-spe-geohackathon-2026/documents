# QA-280: An economics request naming a site (Trondheim) sends a geoscientist to re-survey site ground/air: 66 knowledge searches, open-meteo downloads, a weather-file card, 11 min before the economics question

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 18:21 UTC |
| Versions | backend 1.1.110+ (geomind 0.4.110+); two deploys during the run (celery restarts) |
| Where | https://geomind.team/projects/fa001b0b-183c-4f2e-94b4-1655d0ea56f9/assistant/chat; project "QA-TEST QA-E2E-economics-I 7"; run 5c1cd7b2-5d55-41ab-b8a2-9989c61d292c |
| Fixer | |

## Steps

1. Reference case (competition data), no economics.
2. Chat (18:10:42 UTC): "Our plant will be built in Trondheim, Norway, and will be financed by the
   municipality. Set up the economics with Norwegian prices where they differ."

## Expected

The user asks for the economics. The lead either sets the economics at once, or asks ONE short
question first ("Should I also move the site values (ground, air) to Trondheim? The case's are
from the competition brief.") before any site work. The economics question within 1-3 min.

## Actual

- The coordinator's task: "The user wants the plant sited in Trondheim ... and the economics set
  up with Norwegian prices". The case lead sends ONE geoscientist on "Group II (site.ground,
  site.reservoir, site.air) for a geothermal plant sited in TRONDHEIM" without asking.
- The geoscientist makes 66 `search_knowledge` calls (65 distinct queries, e.g. "Trondheim",
  "NOK Norway SSB Statistics Norway row id", "analysis-period-dea-2019-geothermal-dk Denmark 25 yr",
  economics queries outside its group), 13 `read_knowledge`, 8 `read_mcp` (open-meteo: geocode
  twice, elevation twice, historical 2025 failed "API unavailable", 2024 twice "interrupted by a
  crash" (the deploys), then month, year, ERA5, CMIP6 2027 projection) and 2 `save_mcp_table`.
- 18:21:56: approval card "Saved a connector table to the case: data/open-meteo_trondheim_2027_projection.csv"
  (screenshot 1). I denied it ("Do not change the site ... I only asked for the economics").
- The economics question came at ~18:27 UTC: 16-17 min after the request (11 min of it before
  my denial). It then had its own accuracy problem (QA-279).
- Knowledge holds no Norwegian site data, so all the searching found nothing usable for ground or
  reservoir.

## Evidence

- ![weather-file card](../evidence/QA-280/1.png); text `../evidence/QA-280/chat-weather-card.txt`
- Run JSON: `../evidence/QA-280/run-5c1cd7b2.json.gz` (geoscientist steps 1-12, 18:11-18:21 UTC)

## Cause

Fact: coordinator task and case lead brief (above). Guess: the case lead's skill treats a named
location as a case change that needs site values, and the geoscientist has no search budget or
"stop when the knowledge base has no source for this region" rule.

## Proposed fix

geomind:
1. Case lead skill: when a request is about economics and names a place, ask once whether the
   site values should follow, before any site work; never start a site survey on an economics
   request alone.
2. Geoscientist: a budget of search calls per field group (e.g. 8) and stop with "missing" when
   the knowledge base has no source for the region; never search outside its group (economics
   queries).
3. Coordinator: keep the user's scope in the task ("economics with Norwegian prices; the user
   names the site Trondheim") rather than "the user wants the plant sited in Trondheim".

## Fix

- 2026-11-05 18:55 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest

- 2026-11-05 19:08 UTC, QA-E2E-economics-I: PASSES on backend 1.1.118. Same request, project
  "QA-TEST QA-E2E-economics-I 9", run 746e64e9: no geoscientist, no open-meteo; 26 tool calls
  (was 117), economics question at 19:05:38 (5.6 min incl. three approvals: one set_case of
  `about.site`/`ownership`, two web searches), run done 19:08:20, 742k tokens, 0.020 USD (was
  3.55M, 0.072). The site is only recorded in `about.site`. Run: `../evidence/QA-280/run-746e64e9.json.gz`.
- 2026-11-05 19:08 UTC: QA-E2E-economics-I 19:08 UTC run 746e64e9: no site survey, 26 calls, 8 min, 0.020 USD; see Retest
