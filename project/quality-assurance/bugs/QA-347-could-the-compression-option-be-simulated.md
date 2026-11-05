# QA-347: 'Could the compression option be simulated for comparison?': analysis lead asks the design lead through support_lead, which answers 'cannot be routed to any member of this team'; no variant built; the answer also opens with a raw evaluate_module error

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | QA-E2E-report-I |
| Found | 2026-11-05 20:17 UTC |
| Versions | backend 1.1.125+ (geomind 0.4.133+, deploy 55 went live during the run), frontend live |
| Where | https://geomind.team/projects/c60d19cd-b8c1-4c29-8e64-fd168a01ae76/assistant/chat; project QA-TEST QA-E2E-report-I 5; run 4ffa1142-8fb5-42f4-ad58-622c6bd04520 (20:07:58-20:14:27 UTC) |
| Fixer | m3 |

## Steps

1. After a report of design/v1 (HackathonPlant) in the chat, ask: "Why an absorption chiller
   instead of a compression chiller in this design? Could the compression option be simulated
   for comparison?"

## Expected

The project lead sends the "simulate a variant" part to the design lead (who has build_plant /
patch_plant and simulate), gets the variant result, and the analysis lead or explainer compares
it with the absorption baseline (cold, electricity, CAPEX, LCOC, CO2). gemini can model it
(HeatPump in chiller mode, reference plant HeatingHeatPumpCoolingPlant).

## Actual

- Project lead routes only to the analysis lead (steps: analysis_lead 8, support_lead 4,
  analysis_lead 18). The analysis lead sends "Request to the design lead (from the analysis
  lead). Build and simulate a compression-chiller what-if variant ..." to `support_lead`, which
  answers "The design lead's request (from the analysis lead) cannot be routed to any member of
  this team, so it goes back with why." (steps line 33, 45).
- The final answer says "Not in this chat, and I could not produce the comparison numbers ...
  I have no plant-building tool", and lists what a comparison would need.
- The answer opens with a raw tool error: "evaluate_module: this exact call already failed at
  step 24 with invalid_input: inlets = []; HeatPump needs the stream inlets source_in, sink_in
  ..." before the first heading.
- 6 min 29 s, 44 steps (6 retried), 0.95 M input tokens, 0.018 USD.

## Evidence

- Answer text: `../evidence/QA-347/answer.txt`
- Run steps: `../evidence/QA-347/run-4ffa1142-steps.txt`

## Cause

Facts: a sub-team lead has no path to another team: the analysis lead's cross-team request
goes to support_lead, which has no design member. The project lead did not split the question
into an explain part (analysis/explainer) and a build-and-simulate part (design lead). The raw
error text is an earlier tool result copied into the finish answer.

## Fix

Proposal (geomind): (1) project lead prompt: a "could X be simulated / compare with a variant"
question goes to the design lead first, then the analysis lead compares; (2) a sub-team lead's
request for another team returns to the project lead (hand-back "needs design_lead: <task>"),
which routes it, instead of support_lead; (3) finish strips tool error text from the answer.

## Retest

(Who, when, result.)
