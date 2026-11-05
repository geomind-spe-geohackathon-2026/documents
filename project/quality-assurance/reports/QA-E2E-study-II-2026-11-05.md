# QA-E2E-study-II report, 2026-11-05

Reporter QA-E2E-study-II (successor of QA-E2E-study-I). Mode hotfix, test only. Project `QA-TEST QA-E2E-study-II 1`
(0ce04203-df3c-4259-b9bf-d7c5ebdce123, kept). Backend 1.1.125 at the end.

## Retests

| Bug | Result | Evidence |
|---|---|---|
| QA-099 | verified | figures with 2 decimals; 365.25-day basis stated |
| QA-248 | **reopened** | Monte Carlo of three prices draws all seven uncertainties; none of 50 `sample_uncertainty` calls logs a `values` key (evidence/QA-248) |
| QA-296 | verified | 1 approval card per request (uncertainty, optimisation), 0 for comparison |
| QA-300 | verified for comparison; raw lines remain elsewhere -> QA-352 | |
| QA-312 | verified | "use the optimised design as the project plant": 1 card, 3 steps, plant v3 |
| QA-285 | verified | page minimize LCTS 32.53, below the 5 MW point 39.21 |
| QA-332, 313, 323, 325 | verified again | minimize done in ~40 s; report numbered 1-9, produced gas, checks scope |
| QA-215 | still open | plant_version empty on 6 of 8 Results rows; no duplicates now |
| QA-223 | stays fixed | no what-if row seen, not directly retested |
| QA-232 | stays fixed | tab open across a deploy navigated fine; frontend chunk change unproven |
| QA-276 | stays open | optimisation 8 min (was 36), no extra family; but started from the wrong plant (QA-330) |
| QA-205, 209, 278, 237 | not retested | |

## New bugs

- QA-330 (major): adopt_design of a comparison design answers "already the project plant, nothing to save" while the Plant page shows another plant; later runs treat design/v1 as the current plant.
- QA-352 (minor): raw "improvement:" lines in uncertainty answers.

## New variants done

Vague request ("good enough? make it cheaper"): answer in ~9 min, one card, widened a bound once, fine.
Sensitivity of three prices: correct (electricity 28.78-33.34, carbon 29.45-33.26, heat no effect on LCOH).
Not done: Export Markdown, cancel on an approval card, two chats at once, QA-278 six-plant run.
