# QA-295: No-files case: the user approves gradient 25 °C/km, depth 2000 m, pressure 200 barg, GLR 0.5, but set_case stores 30 / 2500 / 250 / 0.8 (the hackathon values); nothing checks the set values against the approved question

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 18:50 UTC |
| Versions | geomind 0.4.114, backend 1.1.110 |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 5 (77e0d7c1-cf15-4931-a74d-71516aafd0a4); chat 2b692128-ea48-473f-8959-828ef6c73b98; run 7ff26b69-e0a2-4407-912c-34266af8a216; case_lead steps 15-17 |
| Fixer | |

## Steps

1. New project, NO files. Chat: "We want geothermal heating for a small town. Can you set it up?"
2. First question (no options): typed "A town of about 5000 homes near Trondheim, Norway. Heating
   only, about 20 MW peak. We have no demand file. Use your own reasonable assumptions for
   anything else."
3. Confirmation question (request-815, 18:01:22 UTC): approve all.

## Expected

The case holds exactly the values of the approved question (prompt : "On approve
all, set them with `set_case`"; handbook-case §8.4).

## Actual

| Path | Approved in the question (18:00:28) | Stored by `set_case` (step 17, 18:01:35) |
|---|---|---|
| site.ground.gradient | 25 °C/km ("a typical gradient for Norwegian bedrock") | **30 °C/km** |
| site.reservoir.reference_depth | 2000 m | **2500 m** |
| site.reservoir.pressure | 200 barg ("hydrostatic at 2000 m") | **250 barg** |
| site.fluid.gas_liquid_ratio | 0.5 Nm3/m3 | **0.8 Nm3/m3** |
| site.ground.surface_temperature | 5 degC | 5 degC (right) |
| demand.heating.* | 20 MW constant, 90/50 degC, 6 bar | right |

The four wrong values are exactly the GEMINI hackathon values (`gemini/examples/hackathon_2026/case.json`,
`knowledge/hackathon-2026-assumptions.md`), which the case lead had seen in Knowledge search results
earlier in the run. The case lead wrote the 4 k-token `set_case` in one 34 s LLM call from memory;
`set_case` and the approval card do not compare it with the question. The approval card (request-843)
shows the JSON, so a careful user could catch it, but the card is cut at 1500 characters.
The design team then built a plant on the wrong reservoir (run cancelled by QA at 18:46 UTC while
waiting on `build_plant`).

Also seen (not separate bugs): the demand is the 20 MW PEAK as a constant for the whole year
(175 GWh/yr instead of a town's ~60-80 GWh/yr); the question says so ("a daily series would be
better"), the user approved. The air pressure is computed by set_case from an assumed elevation of 10 m
(101204.926... Pa), shown with its formula in `about`.

## Evidence

- `../evidence/QA-295/run-7ff26b69.json` (run log; steps 15 `ask_user`, 17 `set_case`)
- `../evidence/QA-295/answers.json` (the questions and answers)
- `../evidence/QA-295/stored-case.json` (`GET /design/case`)

## Cause

Model error (it retyped values from its context, mixing the hackathon document it had read with
its own proposal); no guard. Guess: the hackathon assumptions document comes up in every
`search_rag` for site values, so it sits in the context of a case that is not the hackathon.

## Proposed fix

- geomind `agents/case/lead.py`: after `approve all`, check the next `set_case`: every path the
  question listed with a number must be sent with that number (parse the question's
  `<path> = <value> <unit>` lines, as the prompt writes them); refuse the call with the list of
  differences. Same check for typed answers ("change some").
- Better: build the question from data (a tool `ask_case_values(values=[{path, value, unit, source, reason}])`)
  and let `approve all` set exactly those values (as `ask_economics` does), so the model never retypes them
  (see also QA-163).
- Knowledge/search: `search_rag` should rank `hackathon-2026-assumptions.md` low for a case whose
  brief is not the hackathon (or tag the document with its brief).

## Speed and accuracy

Accuracy: 4 of the 20 approved site values stored wrong (gradient +20 %, depth +25 %, pressure
+25 %, GLR +60 %). Speed: case stage 8 min 34 s (17:55:16 to 18:03:50 economics question), 0.014 USD
until the design stage.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
