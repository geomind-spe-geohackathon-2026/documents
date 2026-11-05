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

## Exact lines to paste (checked against `tools/sections.py` `section_span` on the uploaded files)

Each agent first gets the Knowledge-only read tool (`read_knowledge`, as the design engineers
have it). Then one bullet under `## Rules` of each prompt:

**prompts/analysis/economist.md**

```
- Method: read `read_knowledge(name="knowledge/handbook-economics.md", section="0")` once before you cost (0.1 rules, 0.5 metrics, 0.7 checklist); for what a metric means, `section="16"`; for a sensitivity or uncertainty, `section="12"` or `section="13"`. Never compute with its formulas: they explain gemini.
```

**prompts/analysis/lead.md**

```
- Method: `read_knowledge(name="knowledge/handbook-economics.md", section="0")` once for costs; to compare or rank designs, `section="14"`; for a sensitivity, `section="12"`.
```

**prompts/project/explainer.md**

```
- Before you write, read `read_knowledge(name="knowledge/handbook-report.md", section="0.2")` (what goes under each heading, from which tool) and `section="0.4"` (checklist), once each. For the economic basis, `read_knowledge(name="knowledge/handbook-economics.md", section="0.5")`. For a competition entry, its brief: `read_knowledge(name="knowledge/hackathon-2026-brief.md", section="4")`.
```

**prompts/project/reviewer.md**

```
- Check the explanation against `read_knowledge(name="knowledge/handbook-report.md", section="15")` and the verdict rules of `section="9"`, read once each.
```

**prompts/project/lead.md**

```
- For a report to a scored brief (a competition or tender), read `read_knowledge(name="knowledge/handbook-report.md", section="16.1")`; for the GEMINI hackathon its criteria and limits are `read_knowledge(name="knowledge/hackathon-2026-brief.md", section="Judging criteria")` and `section="2"`.
```

### Read tool each agent needs

| Agent | File | Tool to add | Scope |
|---|---|---|---|
| economist | `agents/analysis/economist.py` | `read_knowledge` (the Knowledge-only read tool the design engineers have) | global Knowledge only |
| analysis lead | `agents/analysis/lead.py` | `read_knowledge` | global Knowledge only (it already has `read_rag` for project files) |
| explainer | `agents/project/explainer.py` | `read_knowledge` | global Knowledge only |
| reviewer | `agents/project/reviewer.py` | `read_knowledge` | global Knowledge only |

Keep `search_rag` as it is. Every citation below is a `section` number checked with
`section_span`; a bare file name without `knowledge/` is refused (QA-169).

### Skills: one line each

**skills/economics/SKILL.md** (after the first paragraph)

```
The method behind these tools (what each metric means, how gemini computes it, how to read a sensitivity or an uncertainty) is `read_knowledge(name="knowledge/handbook-economics.md", section="16")`, `section="12"` and `section="13"`; this skill holds only the calls.
```

**skills/report/SKILL.md** (end)

```
How a study's table enters the report's `Decisions` (decision record, comparison table): `read_knowledge(name="knowledge/handbook-report.md", section="7")` and `section="6.3"`.
```

**skills/reading-results/SKILL.md** (next to `check_results`)

```
Feasible is `check_results`' `feasible` (gemini's verdict), never the report's `passed`, which tallies only the checks that ran: `read_knowledge(name="knowledge/handbook-report.md", section="9.1")`.
```

Notes: cite numbers, not titles (QA-169), except the brief's first section: its number `1`
resolves to the file's own `#` title, so it is cited by the title "Judging criteria" (checked).

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
