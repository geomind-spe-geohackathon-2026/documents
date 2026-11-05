# QA-296: Optimisation summary asks the user 18 approval cards: 15 run_python (6 then refused for 'data literals' such as a [:300] slice or a print width) and 3 read_web_page for https://example.invalid (refused: not a public address)

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-study-I |
| Found | 2026-11-05 18:47 UTC |
| Versions | backend 1.1.115+ (geomind 0.4.123, gemini 0.6.21) |
| Where | project `QA-TEST QA-E2E-study-I 3` (ac687987-8bfe-452f-8013-7a4b577a3655); chat 00be49e5-9d56-4c05-8dc3-40f2a0a1d919; run 4885075b-6ee6-42bc-b8bb-92ba6fd0a69d |
| Fixer | hotfix-python-lead-II |

## Steps

Fresh seeded project. Chat: "Optimise the current plant for the lowest cost of thermal supply:
search the number of doublets (1 to 3), the flow per doublet (50 to 300 m3/h) and the absorption
chiller capacity within the competition limits. Tell me how many trials were feasible and how the
cost spreads over the feasible ones." Approve every card.

## Expected

One or two cards (set_ranges); the history summary from one tool call (QA-205's fix).

## Actual

- The answer is right now (QA-205 retest passes: "240 trials, 3 feasible", table of the 3 with
  rounded LCTS 49.34 / 49.72 / 53.32). But it takes 14 min 11 s, 70 steps, 107 calls, 1.96 M input
  tokens, 0.037 USD, and the user must click 20 cards:
  - 2 set_ranges (expected);
  - 15 run_python (analysis_lead, 18:37-18:45) "Inspect the shape of the stored optimisation
    history" x3, "List the feasible trials ..." x7, "Inspect the study object ..." x3, ...; 6 of them
    are refused after the user approved: "the code holds data literals; pass each value as a named
    input instead: line 3: 300" (for `repr(h)[:300]`), "line 8: 20", "line 6: 400"; two refused
    for the input shape ("expected one key of case, assumption, ...");
  - 3 read_web_page {"url": "https://example.invalid"} by design_lead at 18:32:42, 18:33:06,
    18:33:16, each refused after approval "the host is not a public address".
- The run_python cards show the code; a user cannot judge them.

## Evidence

Run log: `../evidence/QA-296/run-4885075b-log.json`.

## Cause

Facts: run_python asks approval before its own input/literal checks; its literal check counts slice
bounds and print widths as data. read_web_page asks approval before checking the host. Guess: the
design lead probes read_web_page with a placeholder URL to load the web-search skill.

## Proposed fix

geomind: validate every tool call (inputs, literals, URL host) before asking for approval, so a
refused call never shows a card; allow integer literals used as slice bounds / formatting; give the
analysis lead a history-summary tool (QA-205) so run_python is not needed for it; the design lead
loads skills with read_skill, never with a dummy URL.

## Fix

- 2026-11-05 19:11 UTC: geomind main 71d80ab (0.4.131+), gemini dev 5782a138 (0.6.27); QA-312 also needs back-lead's DatabaseWorkspace.save_plant_version
## Retest
