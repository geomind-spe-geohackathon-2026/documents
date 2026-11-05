# QA-173: Task: analysis and report agents never point at handbook-economics, handbook-report or hackathon-2026-brief, and explainer, reviewer, economist and analysis lead cannot read a Knowledge section (search_rag only)

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | geomind |
| Reporter | handbook-econ-report-I |
| Found | 2026-11-05 17:12 UTC |
| Versions | geomind main c5ed1b1 (0.4.102) |
| Where | geomind/geomind/prompts/analysis/*.md, prompts/project/{explainer,reviewer,lead}.md, agents/analysis/*.py, agents/project/{explainer,reviewer}.py |
| Fixer | |

## Steps

1. `grep -rn "handbook-economics\|handbook-report\|hackathon-2026" geomind/geomind` (prompts, skills, agents).
2. Look at the tools of `agents/project/explainer.py`, `reviewer.py`, `agents/analysis/economist.py`, `lead.py`.

## Expected

The agents that cost, compare, review and explain a design know where their method lives in
Knowledge and can read one section of it:
- economist and analysis lead: `knowledge/handbook-economics.md` (ch 0: rules, metrics, checklist
  0.7; ch 16 how gemini computes);
- explainer, reviewer, project lead: `knowledge/handbook-report.md` (ch 0: the explainer's eight
  headings with their sources, order of work, checklist 0.4);
- for a competition entry: `knowledge/hackathon-2026-brief.md` (judging, deliverables,
  reference results), next to `knowledge/hackathon-2026-assumptions.md` (case).

## Actual

No analysis or report prompt or skill names any of these files (only the design and case
prompts cite their handbooks). These four agents have `search_rag` only: no `read_knowledge`
(or `read_rag`) to read a cited section, so they see search hits but never a whole section such
as `handbook-report.md` §0.2.

## Evidence

- grep above: no hit in prompts/analysis, prompts/project, skills/economics, skills/report.
- `agents/project/explainer.py:39`, `reviewer.py:38`, `agents/analysis/economist.py:39`,
  `lead.py:46`: `self.search_rag = tools.search_rag`, no knowledge read tool.

## Cause

Fact: the handbooks were added to Knowledge after these prompts were written; only the design
and case prompts were updated (design/lead.md cites `handbook-design.md` chapter 0).

Proposal (hotfix-python, needs Sahand's OK for prompt changes as usual): give these four agents
the Knowledge-only read tool the design engineers have (`read_knowledge`, global Knowledge
only), and add one line to each prompt naming the handbook and its chapter 0, cited the way
QA-169 says resolves (`name="knowledge/handbook-report.md", section="0.2"`, a number, not a bare
title).

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
