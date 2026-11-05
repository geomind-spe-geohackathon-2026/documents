# QA-E2E-economics-I, 2026-11-05

Scope: chat to economics on https://geomind.team (agent-browser, 1440x1000), from the reference
`gemini/examples/hackathon_2026/case.json` loaded by API without `economics` (plus
`data/demand.csv`). Versions: frontend 1.1.114; backend 1.1.102 -> 1.1.104 (a deploy at ~17:07 UTC,
geomind 0.4.102 c5ed1b1, local wheels). Model deepseek/deepseek-v4.1-flash-1017. Times UTC.

## Runs

| Project | Run | Request | Path | Result |
|---|---|---|---|---|
| QA-TEST QA-E2E-economics-I 1 (e4a51b01) | bf3990c4 | "Please set up the economics ... each with its source." | typed answer: approve all with 3 changes (discount 6 %, carbon 80 EUR/t, drop 4 equipment kinds) | done; values right; sources of the changed keys wrong (QA-186); 3 approval cards |
| QA-TEST QA-E2E-economics-I 2 (8ac1457c) | 2d5ced06 | "Set up the economics of this case." | approve all | FAILED: repeat guard stop, "internal error in geomind" (QA-181); economics stored |
| same | 2d460136 | "discount 7 %, carbon price from the ESMA EU ETS 2025 row; is grid CO2 priced?" | approve 2 cards | done; discount 0.07 right; carbon 51.56 = the 2024 price (QA-202); grid-CO2 answer right |
| QA-TEST QA-E2E-economics-I 3 (72b92b52) | a8bfebc0 | "What does the economics need, and where would each value come from? Then set it up." | stop | done; nothing set; clear summary and a "Set the economics as listed" chip |

## Timing

| Run | Request -> question card | Answer -> run end (agent time) | Whole run | Tokens in / out | Cost USD |
|---|---|---|---|---|---|
| bf3990c4 | 82 s (16:51:05 -> 16:52:27) | ~1 min of agent time; 13 min waiting on my approvals (QA-193) | 18 min 53 s | 383k / 17k (at 17:07) | ~0.010 |
| 2d5ced06 | 71 s | 30 s to the failure | 1 min 50 s | 435k / 9.5k | 0.008 |
| 2d460136 | no question; set_case card at ~85 s | 1.5 min incl. 2 approvals | 2 min 49 s | 694k / 11.5k | 0.0125 |
| a8bfebc0 | ~115 s (15 steps) | 55 s after stop | 2 min 49 s | 316k / 18.6k | 0.011 |

Slowest calls: the case lead's `ask_economics` LLM call (25-33 s, 4.7k-5.7k output tokens) and its
read of the assumptions file before it (12-25 s). Wasted round trips: stale `read_case` after
approve all (QA-181), `set_case` sent with `changes.economics` (refused once), a second `set_case`
just to drop the `about.sources` of removed keys (QA-186).

## Accuracy (approve all vs reference economics.json)

| Key | App | Reference | Note |
|---|---|---|---|
| discount_rate | 0.05 | 0.05 (uncertainty normal 1 %, 2-8 %) | uncertainty missing (QA-191) |
| analysis_period | 25 yr | 25 yr | ok |
| energy.electricity | 105.75 EUR/MWh | 105.75 (uniform 80-140) | uncertainty missing |
| energy.gas | 39.92 EUR/MWh | 39.92 (triangular 25-70) | uncertainty missing |
| carbon.price | 57.03 EUR/t | 57.03 (triangular 30-110) | uncertainty missing; no catalogue row (QA-191) |
| revenue.heat / cold | 60 / 60 EUR/MWh | 60 / 60 | ok |
| capex.heat_pump / boiler / chp | 0.738 / 0.0607 / 0.962 EUR/W | 0.73786 / 0.06073 / 0.96155 | rounded in Knowledge (QA-191) |
| opex.fixed.heat_pump / chp | 0.224 / 1.026 %/yr | 0.2239 / 1.0263 | rounded |
| capex.drilling | 1239.13 EUR/m | 1239.1304 | rounded |
| accounting.gwp.standard | "IPCC AR6 GWP100" (run 1) / open (runs 2, 3) | "IPCC AR6 WG1 table 7.15, GWP100 of fossil methane" | differs |
| every other reference key | equal | | |
| extra keys | circulation_pump, electric_boiler, ice_storage, thermal_storage (catalogue proxies, some with a unit-basis mismatch) | none | QA-192 |
| opex.per_energy, revenue.subsidy | open | absent | ok (no source) |
| Grid CO2 pricing (answer) | not priced, counted in the CO2 metric | QA-128 convention | ok |

User changes: 6 % -> 0.06, 7 % -> 0.07, 80 EUR/t stored right (QA-120 does not recur).

## Bugs

- QA-181 blocker geomind: approve all on the economics question fails the run (ask_economics is
  effect read; repeat guard serves stale results).
- QA-185 major frontend: Economics tab shows the economics file only as raw JSON; "Fill in here"
  starts an empty form with unsaved changes (Save would wipe the economics).
- QA-186 major geomind: changed values keep the Knowledge source in about.sources; removed keys
  need a second set_case.
- QA-191 minor data: rounding, no uncertainty ranges, gwp.standard, no rows for the cited prices.
- QA-192 minor geomind: approve all includes catalogue proxies with a unit-basis mismatch.
- QA-193 minor frontend: Approve/Deny hidden under the JSON in the card's scroll box; empty
  "Accept case" card.
- QA-194 minor geomind: chips on a case without economics offer design, not economics.
- QA-202 minor data: carbon row ids name the report year; "ESMA 2025" gave the 2024 price;
  16-digit values.

## What worked

The case lead finds `hackathon-2026-assumptions.md` at once and prefers it to the catalogue; one
economics question with a source per key; stop leaves the case untouched with a clear summary;
the grid-CO2 explanation is right and cited; chips after the run fit the state.

## Round 2 (17:27-18:35 UTC): retests and new scenarios

Versions moved during the round: backend 1.1.106 -> 1.1.110+, geomind 0.4.106 -> 0.4.110+, several
deploys (runs survived; some "interrupted by a crash" tool calls during restarts).

Retests: QA-181 failed on 0.4.106 (reopened with the code cause: answered calls not in
`succeeded`), verified on 0.4.110; QA-185, QA-186, QA-191, QA-193, QA-202 verified. QA-216
(uncertainty) observed working. Open: QA-192 (fixing), QA-194.

| Project | Run | Scenario | Time | Tokens in | Cost USD | Result |
|---|---|---|---|---|---|---|
| 4 (7d1d7b7c) | 92e9d156 | approve all (QA-181 retest) | 2.5 min | 428k | 0.0096 | failed (guard) |
| 4 | 236f17d4 | "electricity 95 EUR/MWh in 2026 prices" | 13 min incl. my waits | | | good question on price year; 95 -> 73.79 EUR2015 (HICP 2025 proxy) with source |
| 5 (8ed137a6) | 4aa5be35 | approve all (QA-181 retest) | 3 min 7 s | | | done; every reference value exact |
| 5 | f7097fbc | "ESMA EU ETS 2025 price" | 8 min 40 s | 1.44M | 0.023 | right row 57.4757 (QA-202 ok); 6 set_case, re-ask (QA-256) |
| 6 (in list) | 74ef2d84 | approve all with 3 changes (QA-186 retest) | 4 min 33 s | 741k | 0.0137 | one set_case, user sources |
| 6 | d66897ee | question after a hand edit to 0.07 | 8 s | 48k | 0.001 | answers 0.06 (QA-284) |
| 7 (fa001b0b) | 5c1cd7b2 | "Trondheim, Norwegian prices where they differ" | 19 min | 3.55M | 0.072 | unasked site survey (QA-280); catalogue rows replace the assumptions (QA-279); fixed after a typed answer |

New bugs: QA-256, QA-279, QA-280, QA-284 (all major, geomind).
