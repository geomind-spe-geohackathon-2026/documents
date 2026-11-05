# QA-194: Next-step chips on a project whose case has no economics offer 'Design a plant' and nothing for the economics

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | QA-E2E-economics-I |
| Found | 2026-11-05 16:50 UTC |
| Versions | frontend 1.1.114, backend 1.1.102 / 1.1.104 |
| Where | https://geomind.team/projects/e4a51b01-9faf-4bbc-819e-2223ef3d9e7b/assistant/chat (empty chat), and project "QA-TEST QA-E2E-economics-I 2" |
| Fixer | |

## Steps

1. Project whose case is complete (no missing, no problems) but has no `economics`.
2. Open the chat.

## Expected

A chip for the step the project needs next: "Set the economics" (memory rule: suggestions follow
the project state, never generic).

## Actual

Chips: "Design a plant", "Check the case and its sources", "Compare plant options"
(screenshot 1). Nothing names the economics; a cost-based design or study later stops on the
missing economics. After the economics run, the chips did offer "Fill the open economics", so the
state is known at that point.

## Evidence

- ![chips](../evidence/QA-194/1.png)

## Cause

Fact: `geomind/geomind/tools/suggestions.py` `stage_of` / `project_stage` go from "case" to the
plant stage on case state alone; `STAGES["case"] = ("design_plant", "check_case",
"compare_options")` has no economics step, and the `economics` step ("Costs and economics") is
only in the "plant" stage.

## Proposed fix

geomind `suggestions.py`: when the case is ready but `economics` is unset (or has open keys the
case's plants need), put an economics step first in the "case" stage ("Set the economics", message
"Set up the economics of this case.").

## Fix

## Retest
