# QA-256: One carbon-price change by chat takes 6 set_case calls, 5 approvals and a full economics re-ask: set_case accepts changes.about (stray top-level about.sources.carbon.price) and the case lead cannot confirm the source it wrote

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 18:02 UTC |
| Versions | backend 1.1.110 (geomind 0.4.110 or later; deploys during the run), frontend live 2026-11-05 |
| Where | https://geomind.team/projects/8ed137a6-e07a-4a05-ae98-2ddd9a86f498/assistant/chat; project "QA-TEST QA-E2E-economics-I 5"; run f7097fbc-c8c4-4140-b531-cf8e190a3359 |
| Fixer | hotfix-python-lead |

## Steps

1. Project with the economics set by approve all (run 4aa5be35; carbon 57.03 EUR/t, Instrat).
2. Chat (17:53:39 UTC): "Use the EU ETS average spot price of 2025 from ESMA in the cost catalogue
   as the carbon price."
3. Approve each card as a user would; deny the 4th (the same source again) with a reason.

## Expected

One `set_case` card (value 57.4757 EUR/t and its source in `economics.about.sources`), then
"Accept case", then a summary. About 1-2 minutes.

## Actual

8 min 40 s (17:53:40 -> 18:02:19), 1.44 M input tokens, 0.023 USD, 46 tool calls, 6 `set_case`
calls, 6 approval cards plus a whole economics question again:

1. step 4: `set_case {"changes": {"about": ...}, "economics": ...}` refused (economics under
   changes).
2. step 5: `set_case changes.about.sources["carbon.price"] + economics.carbon.price` ACCEPTED: the
   value went into `economics.json`, but the source went into the CASE's top-level
   `about.sources["carbon.price"]` (case version 4 "about added"), a stray entry with an
   economics key path at the wrong level. (card 1)
3. step 7: `set_case economics.about.sources["carbon.price"]` (card 2): right place.
4. step 11: the same again with other `basis` text (card 3) -> I denied: "already stored ...
   remove the stray top-level entry".
5. step 15: `set_case changes.about.sources["carbon.price"] = null` (card 4): removes the stray.
6. step 19ish: the same economics source a third time (card 5).
7. Then a FULL `ask_economics` question again (60+ keys, card 6, "Only one value changes ...
   approving changes nothing else") and "Accept case" (card 7).

Why it loops (from the log): `read_case {"section":"economics"}` returns the economics but the
lead keeps checking `about.sources` with `read_stored` on older references (step 12 error:
"'carbon' is no key or index of about.sources" on a result taken before the write) and
`read_case {"section":"economics.about"}` is refused (step 16, sections are top-level only), so
it never confirms the source and writes it again.

Good: the right row now (`carbon-price-eu-ets-esma-price-2025`, 57.4757 EUR/t, 6 digits; QA-202
data fix works), and the final summary is correct.

## Evidence

- Run JSON: `../evidence/QA-256/run-f7097fbc.json.gz` (case lead steps 4-20)
- First set_case card: `../evidence/QA-256/card-set-case-1.txt`
- Economics re-ask card: `../evidence/QA-256/card-economics-reask.txt`
- Chat after the run: `../evidence/QA-256/chat.txt`

## Cause

Facts: `set_case` (geomind `tools/gemini/case.py`) takes `changes.about.sources` with a key such as
`carbon.price` that only exists in economics, and writes it to the case's own `about`;
`read_case` has no way to read `economics.about` directly; the case lead's skill has no rule
"one change = one set_case with value and source, then stop".

## Proposed fix

geomind:
1. `set_case`: refuse `changes.about.sources.<key>` when `<key>` is an economics path (or move it
   to `economics.about.sources`) with an error that names the right argument.
2. `set_case`: return the written `about.sources` entries of the keys it changed in its result,
   so the lead sees the source is stored without another read; allow `read_case` section
   `economics.about` (or a path).
3. Case lead skill / economics recipe: a single value change from the catalogue is one `set_case`
   with value and source in the `economics` argument; never re-ask the whole economics question
   for one key (use `ask_user` with the one value if a confirmation is wanted).

## Fix

## Retest
