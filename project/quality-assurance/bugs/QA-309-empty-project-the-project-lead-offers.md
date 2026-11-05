# QA-309: Empty project: the project lead offers 'Use the GEMINI hackathon example case', but its demand files are nowhere the case lead can read; the case ends with the 30 / 10 MW peaks as constant demand (2.4x the brief's heat, 3.7x its cold)

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 19:00 UTC |
| Versions | geomind 0.4.114 or later (backend 1.1.110+; deploys ran during the run) |
| Where | api.geomind.team; project QA-TEST QA-AI-case-I 10 (40d0f25a-2b9e-4785-b41a-5f3ca414adf4), empty (no files); chat run 55a9cd7b-18ce-43a9-b260-a4982eb07a1c |
| Fixer | |

## Steps

1. New project with no files. Chat: "design me a geothermal plant".
2. The project lead's question (10 s): pick "Use the GEMINI hackathon example case".
3. Answer the next questions as a user who does not know ("Use your own reasonable assumptions"),
   then approve all.

## Expected

An option the agents offer can be carried out: the example case is set as the reference case
(`gemini/examples/hackathon_2026/case.json`), with its two daily demand series; or the option is
not offered without the files (ask the user to upload the competition files instead).

## Actual

- 18:47:34 UTC project lead: "...If you would rather not gather that now, I can build the plant on
  the GEMINI hackathon example case instead." (option "Use the GEMINI hackathon example case").
- The case lead reads `hackathon-2026-assumptions.md`, tries `read_rag("knowledge/GEMINI_Heating_Demand_Daily_2027.csv")`
  and the cooling one (both refused: not in Knowledge), searches, `web_search`es for the files,
  then asks the user (18:49:4x) to upload the two CSVs.
- After "use your own assumptions" it proposes (18:50:57): `demand.heating.power = 30.0 MW constant`,
  `demand.cooling.power = 10.0 MW constant` ("the brief's own peak ... the plant will be oversized
  and the economics pessimistic"), and sets them on approve all (18:52:11).
- So the "example case" has 262.8 GWh/yr of heat instead of 111.67 (x2.35) and 87.6 GWh/yr of cold
  instead of 23.74 (x3.69); the design team then sizes a plant on it (`build_plant` 18:53:59).
  Any result is not comparable with the reference, although the run calls it the example case.
- Also in this run: the first `set_case` refused for `"unit": "mol/mol"` on the dissolved gas (QA-222 family).

Good, for QA-283: the project lead asked first (10 s, not 5.5 min), and never briefed from a
case.json that does not exist.

## Evidence

- `../evidence/QA-309/run-55a9cd7b-case-stage.json` (run log up to the design stage)
- `../evidence/QA-309/answers.json` (all questions and answers)

## Cause

The project lead's option comes from knowing an example case exists in Knowledge
(`hackathon-2026-assumptions.md`, `hackathon-2026-brief.md`), but the demand series (the two CSVs)
are only in `gemini/examples/hackathon_2026/`, never in Knowledge or any place `set_case` can load.

## Proposed fix

- Either: data + backend: put the two competition CSVs (or the reference `data/demand.csv`) in
  global Knowledge, and let `set_case` take a Knowledge data file as a series (`file: "knowledge/..."`);
  then the example case is the reference case exactly.
- Or: geomind `prompts/project/lead.md`: offer the example case only together with "upload the three
  competition files (PDF, two CSVs)"; never as a way without files.
- geomind `prompts/case/lead.md`: a constant at the peak is never proposed for a case that has a
  named series somewhere; ask for the file again, or leave the demand open and stop.

## Speed and accuracy

Accuracy: annual heat x2.35, cold x3.69 vs the competition data. Speed: the question came in
10 s (good); case stage to the economics question 5 min 16 s.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
