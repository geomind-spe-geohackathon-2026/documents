# QA-294: New chat, 'what moved against the last result': the project's Results (3 results, case v3-v5) are invisible to the agents; the analysis lead searches 14 steps (read_study refused, search_rag for a result id) and asks the user to type a result reference

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 18:42 UTC |
| Versions | backend 1.1.116 |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 1 (35a70dbe-5e24-4f51-9c6f-50e06d47fe82); new chat (chat id in the run); run 569e8c99-f26f-43c6-800b-10ac3f61629b; analysis_lead (parent step 8), request-395 |
| Fixer | |

## Steps

1. Project 1 has three results on its Results page (`GET /design/results`): e151aee7 (case v3, LCOH 43.7528), 9686abba (case v4, 44.6406), 056533ec (case v5, 44.1336), made in two other chats.
2. Save the case by hand: permeability 175 -> 160 mD (case v6). Open a new chat.
3. Message: "I changed the reservoir permeability in the case form (site.reservoir.permeability). Re-check the plant on the new case, have it reviewed, and tell me what moved in the requirements and in LCOH against the last result."

## Expected

The re-check runs (it did: design lead, reviewer). For "against the last result" the analysis lead lists the project's results, takes the newest one of the same plant (056533ec, case v5) and compares with `compare`.

## Actual

The analysis lead has no tool that lists the project's results; it sees only the result of this chat. It spends 14 steps (18:39 to 18:42 UTC): `read_study` on the project's studies (refused, `unknown_name`), `search_rag` "permeability previous value design/v2 result" and "result/ design/v2 simulation stored result reference" (Knowledge cannot hold a result), `read_stored` of `project_versions`, then asks (request-395): "The earlier design/v2 result - the run on the case with the previous permeability - is not stored anywhere I can reach ... Do you have the reference of that earlier run, or should I report the current values only?". A user does not know result references.

## Evidence

- `../evidence/QA-294/569e8c99-f26f-43c6-800b-10ac3f61629b.log.json`, `../evidence/QA-294/569e8c99-f26f-43c6-800b-10ac3f61629b.trace.txt`: analysis_lead steps 1-14 and request-395.
- `GET /design/results?project=35a70dbe...`: the three results above.

## Cause

QA-122 gave the agents the project's plant versions and studies (`list_studies`, `project_versions`), not its results. `list_studies` shows the project's studies, but `read_study` refuses them by name (`study/hackathon_sens_150mD`: "expected a reference of the form study/..."), so a study made in another chat cannot be read either.

## Proposed fix

geomind (with the backend Workspace, which already serves `/design/results`):
- A `list_results` tool (or `list_studies` extended) giving the project's results with id, plant version, case version, created and the KPI summary, and `read_result`/`compare` accepting such a project result id.
- `read_study` accepting the project studies that `list_studies` lists (the name it shows).
- `prompts/analysis/lead.md`: "the last result" of a project = the newest project result of the same plant; never ask the user for a reference.

## Fix

## Retest
