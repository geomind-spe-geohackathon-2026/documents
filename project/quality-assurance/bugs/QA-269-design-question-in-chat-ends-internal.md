# QA-269: Design question in chat ends 'internal error in geomind' after 15 min, no answer: evaluate_module(heat_pump, result, time) refused 7x 'source_in: Stream.fluid: no value', the repeat guard kills the run

| Field | Value |
|---|---|
| Status | verified |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-report-I |
| Found | 2026-11-05 18:22 UTC |
| Versions | backend 1.1.109 (geomind 0.4.110), frontend bundle index-TsXgd_n9.js |
| Where | https://geomind.team/projects/fa329839-43df-48c3-81c3-89af503b92c0/assistant/chat; project QA-TEST QA-E2E-report-I 2; run 7bcc2a22-4ae0-4fb1-ab99-c53dfd54833e (18:05:14-18:19:55 UTC) |
| Fixer | hotfix-python-lead-II |

## Steps

1. After the report of QA-257 (design/v1, result/9b0db55da13a4a5b in this chat), ask:
   "Explain the design to me: how many MW of heat come from the reservoir brine and how many from
   the heat pump's electricity at the January peak? Is a brine cooling of about 35 K consistent
   with 2 x 300 m3/h? And why an absorption chiller instead of a compression chiller here?"

## Expected

An explanation with numbers from the stored result in a few minutes. Hand check from the
result: brine heat per doublet = 300/3600 m3/s x 1030 kg/m3 x ~4.0 kJ/(kg K) x ~35 K ~ 12 MW,
~24 MW for both; heat pump electricity at the peak ~ 15 MW / COP 3.7-4.2 ~ 3.6-4.1 MW.

## Actual

- Routed to the analysis lead only (18 steps; no explainer). 34 read_result, 8 read_stored,
  4 calculate, then `evaluate_module {"name": "heat_pump", "time": "2027-01-28", "result":
  "result/9b0db55da13a4a5b"}` 7 times: 4x `invalid_call: heat_pump: inlet 'source_in':
  Stream.fluid: no value; expected a Fluid or a mapping of its fields`, 3x `failed_before`.
- Run ends `failed`, error `{"code": "error", "message": "evaluate_module: 2 invalid calls in
  a row"}`; the chat shows "The assistant stopped with an internal error in geomind" and no
  answer (screenshot 1). 14 min 41 s, 62 steps (15 retried), 0.81 M input tokens, 0.034 USD.
- The answer needed no evaluate_module: the result's series (hx, heat_pump, d0/d1 flows and
  temperatures) were readable with read_result.

## Evidence

- ![chat after the failed run](../evidence/QA-269/1.png)
- evaluate_module, describe_module, list_modules calls with input and output: `../evidence/QA-269/evaluate-module-calls.json`
- Run steps: `../evidence/QA-269/run-7bcc2a22-steps.txt`

## Cause

Facts: (1) `evaluate_module` with `result` + `time` rebuilds the module's inlets from the stored
result without the stream's fluid (the same family as QA-149 "missing fluid", fixed for other
call forms); (2) the repeat guard turns 2 invalid calls in a row into a run error instead of a
refusal the lead can answer around; (3) the question went to analysis_lead, not the explainer.

## Fix

Proposal (geomind, hotfix-python): (1) `evaluate_module(result=, time=)` takes the inlet fluid
from the plant's fluids (`plant.fluids[...]`) when the stored stream has none; test it on
`heat_pump.source_in` of HackathonPlant; (2) the guard ends the tool, not the run: the agent
gets "stop calling evaluate_module, answer from read_result" and the lead finishes with what it
has; (3) project lead prompt: "explain/why" questions on a stored result go to the explainer.

- Note (QA-E2E-report-I, 2026-11-05 19:00 UTC): the next run in the same chat (8efe3722, a different question after a case change) answered the three questions of this bug without evaluate_module: brine 15.92 MW (hx duty) + 10.23 MW (heat pump source) + heat pump power_in 3.856 MW = 30.0 MW at the 2027-01-28 peak, from read_result series. So read_result alone suffices; the failure is the evaluate_module path plus the guard.
- 2026-11-05 19:11 UTC: geomind main 71d80ab (0.4.131+), gemini dev 5782a138 (0.6.27); QA-312 also needs back-lead's DatabaseWorkspace.save_plant_version
## Retest

QA-E2E-report-I, 2026-11-05 19:52 UTC, backend 1.1.122+, project QA-TEST QA-E2E-report-I 3 (a9ff33c4), run fd996d09 (19:40:45-19:49:34 UTC), the same question: answered in 8 min 49 s, 48 steps (4 retried), 0.88 M input tokens, 0.023 USD, 0 evaluate_module calls. Numbers at the 2027-01-28 peak: brine 23.769 MW (hx 12.364 + heat pump source 11.405), heat pump electricity 3.595 MW (COP 4.173), boiler 2.636 MW = 30.0 MW; brine 599.9955 m3/h, 171.665 kg/s, cooled 85.03 -> 52.20 degC = 32.83 K; year worst 35.52 K (d0) / 34.77 K (d1) <= 40 K. Hand check: 171.665 kg/s x ~4.2 kJ/(kg K) x 32.83 K ~ 23.7 MW, matches. Verified. One wrong claim in the answer filed separately (no compression chiller in gemini: QA-E2E-report-I next bug). Evidence: `../evidence/QA-269/retest.png`, `retest-answer.txt`.
- 2026-11-05 19:51 UTC: retest QA-E2E-report-I run fd996d09: answered in 9 min, numbers check out
