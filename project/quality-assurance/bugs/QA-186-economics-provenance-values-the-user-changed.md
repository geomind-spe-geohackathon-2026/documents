# QA-186: Economics provenance: values the user changed in chat keep the Knowledge source in about.sources; removed keys keep their source until a second set_case

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 17:10 UTC |
| Versions | backend 1.1.102 -> 1.1.104 during the run (geomind 0.4.10x) |
| Where | https://geomind.team/projects/e4a51b01-9faf-4bbc-819e-2223ef3d9e7b/assistant/chat/01f6cabc-e78c-4227-844e-a9f78e4106b1; project "QA-TEST QA-E2E-economics-I 1"; run bf3990c4-303e-462d-9bf2-ca2207d1bbf6; case lead steps 9-12 |
| Fixer | hotfix-python-VIII |

## Steps

1. Project with the reference case (no economics). Chat: "Please set up the economics ... each
   with its source."
2. On the economics question, typed answer: "Approve all, with three changes: discount rate 6 %;
   carbon price 80 EUR/t; and leave the electric boiler, circulation pump, ice storage and thermal
   storage keys open, our plant has none of them."
3. Approve the two `set_case` cards and `accept_case`.

## Expected

`economics.json` holds discount_rate 0.06 and carbon.price 80 EUR/t with source "user, chat
answer of 2026-11-05" (or similar), and the four removed keys have no value and no source. One
`set_case` approval does it.

## Actual

- Values are right (0.06, 80 EUR/t; the four keys gone). QA-120 (8 % sent as 8) does not recur.
- But `about.sources` still says `discount_rate`: "knowledge/hackathon-2026-assumptions.md
  (Economics; Team)" and `carbon.price`: "knowledge/hackathon-2026-assumptions.md (Economics;
  Cited: Instrat, EU ETS 2025 average allowance price ...)" (evidence/QA-186/economics-project1.json).
  The final chat summary says "Carbon price 80 EUR/t. Source: your change", so chat and stored
  file disagree; a report or explainer reading the file cites Instrat for a value the user typed.
- The case lead saw this itself (step 12: "the recorded assumptions still carry the pre-change
  values") but fixed only the removed keys: it needed a SECOND `set_case` approval (17:07 UTC)
  just to null eight `about.sources` entries of the keys removed in the first `set_case`.
- Wasted round trips on the way: step 8 `read_case` served stale (QA-181), step 9 `set_case`
  refused because the patch was sent under `changes.economics` instead of the `economics`
  argument.

Speed: answer 16:53:33 -> run end 17:09:58 UTC, of which ~13 min were waits on my approvals;
agent time after the answer ~1 min (steps 8-13). Three approval cards for one answer.

## Evidence

- Stored economics after the run: `../evidence/QA-186/economics-project1.json` (`about.sources`)
- Question card text: `../evidence/QA-186/economics-question-card.txt`
- Run JSON: `../evidence/QA-186/run-bf3990c4.json.gz`

## Cause

Fact: `set_case` with an `economics` merge patch changes values but leaves
`economics.about.sources` as it was; a key set to `null` keeps its source entry. The case lead's
prompt/skill does not say to update the source of a changed key in the same patch.

## Proposed fix

geomind `tools/gemini/case.py` (`set_case` economics patch): for every economics key the patch
sets, require or derive its source (default for a value taken from the user's answer: "user, chat
answer <date>"), and drop the source entry of every key set to `null`, in the same write. Then the
case lead needs one `set_case` for "approve all with changes". Add one line to the case lead's
economics skill: a changed value carries its new source.

## Fix

- 2026-11-05 17:40 UTC: geomind 0.4.107, deployed: set_case economics patch drops about.sources of each changed or removed key without its own source
## Retest
