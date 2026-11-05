# QA-227: Case changed by hand: the project lead briefs the case lead with the permeability it read before loading the new case (200 mD); the user is asked for the 150 mD they already saved

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 17:40 UTC |
| Versions | backend 1.1.107 (geomind 0.4.98+, gemini 0.6.17) |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 1 (35a70dbe-5e24-4f51-9c6f-50e06d47fe82); chat 134dae07-2e37-4a3a-ae0b-83b5e812017e; run 194c3879-076e-4e3a-b6bf-8f54da25a7ae; project_lead steps 2-5, case_lead step 2, request-90 |
| Fixer | hotfix-python-lead |

## Steps

As QA-224: case saved by hand with `site.reservoir.permeability` 200 -> 150 mD (case version 4), then the chat message "I saved the case form with a new reservoir permeability (site.reservoir.permeability). Does the plant still meet the requirements, and what does it do to LCOH?". Approve the `set_case` card.

## Expected

After `set_case(source: project)` the state holds 150 mD (its output says so). The project lead sends the design team to simulate and check `design/hackathon` on the new case, then the review and the costs. No question to the user: the value is the user's own.

## Actual

1. Step 2 (before loading): `read_case(section: site)` -> permeability 200 mD (the chat's old case).
2. Step 3: `set_case({"source": "project"})` -> output case with `permeability` 150 mD.
3. Step 4: `case_changes` -> `[]` (the loaded case is now the reference, so nothing differs).
4. Step 5: brief to the `case_lead` (quoted): "`read_case(section="site")` gives site.reservoir.permeability = 200 mD ... So the case still holds the value the plant was verified on. What to do: ask the user for the value they saved".
5. The case lead reads the site (150 mD) and still asks (request-90, 17:37:06 UTC): "The case's site.reservoir.permeability still holds the value the plant was verified on (150 mD ...), so the new permeability you saved is not in the case. What value did you save?". The plant was verified on 200 mD, not 150; the sentence is wrong and the question needless.

Time to the needless question: 3 min 13 s (17:33:53 to 17:37:06), with the approval wait.

## Evidence

- `../evidence/QA-227/194c3879-076e-4e3a-b6bf-8f54da25a7ae.log.json`: project_lead steps 2-5 (tool outputs), case_lead steps 1-2 and its user message (the brief), the run's request-90.

## Cause

- The project lead plans from a tool result it read before the case was loaded; nothing tells it the earlier `read_case` is stale after `set_case`.
- `case_changes` after `set_case(source: project)` compares with the case just loaded, so it cannot show what the user changed; the `set_case` output does not list what differs from the state's previous case.
- The case lead follows the brief's claim instead of the case it just read (it says 150 mD and "not in the case" in one sentence).

## Proposed fix

- geomind `tools/gemini` `set_case` with `source: "project"`: add to the output `changed: [{path, before, after}]` against the state's previous case (here permeability 200 -> 150 mD) and a note "earlier read_case results are stale".
- `prompts/project/lead.md`: "A case the user saved by hand (an app event, or the project case newer than the state's) is approved: load it, then brief the design team to simulate and check the current design on it; no `case_lead` step unless gemini names a missing value."
- `prompts/case/lead.md` (or the case skill): "Trust `read_case` over the brief; when the brief's claim differs from the case, report it back instead of asking the user."
- Together with QA-224 (load a newer project case by rule).

## Fix

- 2026-11-05 17:53 UTC: geomind 0.4.111-0.4.114 (HEAD 778970d), deployed in backend 1.1.110 at 18:51 CET
- 2026-11-05 18:16 UTC: QA-AI-project-I 18:16 UTC: retest not reached: the repeated case-edit message was routed to the tool loop and never loaded the case, see QA-266
## Retest

- 2026-11-05 18:23 UTC: QA-AI-project-I 18:23 UTC, backend 1.1.114, new chat, run a4203016: case 150 -> 175 mD by hand; no question to the user, design lead re-simulated design/v2 on 175 mD, reviewer passed 15/15, LCOH 44.134 EUR/MWh (between 43.753 at 200 and 44.641 at 150 mD); 6 min, 0.0126 USD, one card. Trace evidence/QA-227/retest-a4203016.trace.txt
## More evidence (QA-AI-project-I, 17:38 UTC)

After the user's answer "150 mD. It is already in the case I saved (version 4).", the case lead asks a third card (request-118): "Allow set_case (write)? Change the case: site.reservoir.permeability." with the same value 150 mD the case already holds (a no-op write). One user edit of one value cost three stops: load card, question, no-op change card.
