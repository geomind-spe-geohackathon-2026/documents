# QA-229: Design request 'design and check against the requirements' runs reviewer, analysis lead, economist (uncertainty 200 samples, a refused sensitivity, what-if simulates) and explainer after the design is done: 14 of 39 min and 2.5 M of 5.6 M input tokens nobody asked for

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-design-I |
| Found | 2026-11-05 17:36 UTC |
| Versions | backend 1.1.104, geomind 0.4.97, gemini 0.6.16 |
| Where | https://geomind.team/projects/f1704a61-f1b8-4b63-84d3-20bd30beaed7/assistant/chat/cd332dde-7afa-4865-8a75-d8f6d4be6354; run 76d19df6-485f-46ee-a182-6b03ed70ab33 |
| Fixer | hotfix-python-lead |

## Steps

1. Reference case loaded. Chat: "Please design a geothermal heating and cooling plant ... Show me the design and check it against the case requirements."
2. Approve every card; wait for the answer.

## Expected

Design lead designs, sizes, simulates and checks (it did: `check_results` 10 of 10 passed at 17:16:48); the project lead hands that back, perhaps with one reviewer pass. No economics study, no uncertainty, no sensitivity: the user did not ask for them.

## Actual

Per agent (run log `ts`, `llm_calls[].duration`, `input_tokens`):

| Agent | UTC | LLM s | Input tokens | Calls (refused) |
|---|---|---|---|---|
| design_lead | 16:52-17:17 | 373 | 2.13 M | 67 (7) |
| reservoir_engineer | 16:55-17:04 | 698 | 0.43 M | 51 (13) |
| energy_systems_engineer | 16:55-17:14 | 506 | 0.41 M | 40 (4) |
| reviewer | 17:17-17:19 | 86 | 0.22 M | 17 (1) |
| analysis_lead | 17:19-17:26 | 250 | 1.00 M | 54 (11) |
| economist | 17:19-17:25 | 152 | 0.56 M | 35 (3) |
| explainer | 17:26-17:30 | 192 | 0.72 M | 27 (0) |

After the design was finished and checked (17:17), the project lead sent the reviewer (re-ran the checks the design lead had run), then the analysis lead ("give the numbers behind the verified design"): a 200-sample uncertainty study `best_v1_uncertainty`, a sensitivity on `size.doublets`/`d0.nominal_flow` that gemini refused, two what-if simulates (which then became the wrong Results row, QA-223), then the explainer. 17:17-17:31 = 14 of 39 min, 2.50 M of 5.56 M input tokens. The answer is ~2,000 words.

## Evidence

- Run log (GET /api/v1/assistant/runs/76d19df6-.../log): project_lead calls `reviewer` 17:17:14, `analysis_lead` 17:19:01, `explainer` 17:26:24.

## Cause

Guess: the project lead prompt (`geomind/geomind/agents/project/lead`) routes every finished design through review, analysis and explainer as a fixed pipeline, not by what the user's goal asks; its own `/goal` ("design ... and check it against the case requirements") did not include economics or uncertainty.

## Proposed fix

Project lead prompt: after the design lead returns a design whose check passed, compare the goal with what is done; call the analysis lead only when the goal asks for costs, sensitivity or uncertainty; let the design lead's check stand (no second reviewer run of the same `check_results`) unless the check failed or values were assumed; the explainer writes a short answer and offers the next steps as chips (economics, uncertainty) instead of running them.

## Fix

- 2026-11-05 18:32 UTC: deployed by 19:22 CET: backend 1.1.115, geomind 0.4.123, gemini 0.6.21 (hotfix-python team)
## Retest
