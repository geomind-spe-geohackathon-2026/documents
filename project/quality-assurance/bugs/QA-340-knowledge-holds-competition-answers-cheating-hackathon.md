# QA-340: Knowledge holds competition answers (cheating): hackathon-2026-brief.md gives reference results and the ranking; hackathon-2026-assumptions.md pre-extracts the competition files and pre-solves the design

| Field | Value |
|---|---|
| Status | fixing |
| Severity | blocker |
| Area | data,geomind |
| Reporter | Sahand (Coordinator-V write-up) |
| Found | 2026-11-05 20:02 UTC |
| Versions | Knowledge on geomind.team, 2026-11-05 21:01 Trondheim |
| Where | Global Knowledge: knowledge/hackathon-2026-brief.md, knowledge/hackathon-2026-assumptions.md (sources in documents/project/quality-assurance/inputs/) |
| Fixer | m4 |

## Steps

1. Read the two files.

## Expected

Sahand (21:01 Trondheim): no cheating. The agents must solve the competition the way they would
solve any similar problem: read the user's files, propose and ask for what is missing, design,
simulate and compare by themselves. Global Knowledge holds only general, source-backed knowledge
(handbooks, general data catalogues), never answers to this competition.

Fix plan:
1. DELETE hackathon-2026-brief.md from Knowledge now (keep it in git for the team's own report).
   §5 is an answer key (precomputed results of six plants, which ranks first, LCTS levers); §1-2
   (judging, deliverables) are organisers' information the user can upload as a project file if
   wanted, not built-in knowledge.
2. Rework hackathon-2026-assumptions.md and remove it from global Knowledge:
   - REMOVE 'What the limits mean for the design' (pre-solved design: heat-pump share 9.75 MW,
     'sample study ranked heat pump + boiler + compression chiller first', gas use) and
     'Competition: Values for checking' / 'Values from the files' (pre-extracted PDF/CSV values):
     the agents must read the PDF and CSVs themselves.
   - MOVE the general equipment parameters ('Plant design values': roughness, Carnot fraction,
     COPs, efficiencies, with their citations) into a general catalogue (e.g.
     knowledge/data-equipment.csv/.md, like data-economics), written for any plant, no
     'hackathon' label; Team-only placeholders are marked as such.
   - The organisers' Discord answers and the team's own assumptions for this case become a
     PROJECT file the user uploads with the case files (user input, shown and approved), not
     global Knowledge.
3. Prompts, skills and handbooks: remove every reference to knowledge/hackathon-2026-* ; the case
   lead proposes missing values from general catalogues (with sources) and asks the user once.
4. QA: rerun the competition case from the three files + the uploaded team-assumptions file and
   check the agents still reach a sound design.

## Actual

The agents read both files from global Knowledge in every project; they contain the competition's extracted inputs, pre-solved design reasoning and reference results.

## Evidence

The two files themselves (sections named above).

## Cause

The files were built to speed up the competition case. Sahand's decision: blocker, fix now. Data/Knowledge part: back-lead; prompt/skill references: python-lead; the general equipment catalogue: a python member (it knows the design values).

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
