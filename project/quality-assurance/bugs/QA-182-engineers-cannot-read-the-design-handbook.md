# QA-182: Engineers cannot read the design handbook: read_knowledge('handbook-design.md') refused 7 of 7 ('a project file is the lead's to read'); the prompts name it knowledge/handbook-design.md only for the lead

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 17:14 UTC |
| Versions | backend 1.1.104 (geomind 0.4.98, gemini 0.6.17) |
| Where | https://geomind.team/projects/fcc641c0-0119-4182-9a72-adce5a17b3ed; run d4ab496f-4a1f-43fa-b760-0f550fda0714 (hackathon report run) |
| Fixer | |

## Steps

1. Design stage: the design lead asks the team (reservoir, well, energy systems engineers).
2. Each engineer calls `read_knowledge(name="handbook-design.md")`.

## Expected

The handbook text (or the tool takes the bare name of a Knowledge document).

## Actual

7 of 7 calls refused: `read_knowledge: name = 'handbook-design.md'; expected a Knowledge document 'knowledge/<name>'; a project file is the lead's to read`.
The engineers go on without the handbook. The message is also wrong: handbook-design.md is a Knowledge document, not a project file.

## Cause

Fact: `geomind/geomind/tools/knowledge_only.py` refuses a name that does not start with `knowledge/`. Only the design lead's prompt
(`prompts/design/lead.md:52-58`) gives the full name `knowledge/handbook-design.md`; the engineers' prompts and briefs say `handbook-design.md`.
Fix: accept a bare Knowledge name (add the prefix when the document exists) and keep the refusal for real project files only.

## Fix

## Retest
