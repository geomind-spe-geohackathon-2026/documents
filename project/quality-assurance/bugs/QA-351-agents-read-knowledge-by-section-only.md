# QA-351: Agents read Knowledge by section only: a table-of-contents call, then read_knowledge(file, section) returns just that section; no agent reads a whole handbook

| Field | Value |
|---|---|
| Status | fixing |
| Severity | blocker |
| Area | geomind,backend |
| Reporter | Sahand |
| Found | 2026-11-05 20:41 UTC |
| Versions | live 2026-11-05 21:40 Trondheim |
| Where | geomind Knowledge tools (read_knowledge, search_rag/search_knowledge), backend Knowledge API, all agent prompts |
| Fixer | m2 |

## Steps

1. Any run that needs a handbook: watch the Knowledge calls in the run log.

## Expected

Sahand (21:40 Trondheim), highest priority:
1. A cheap table-of-contents call: `knowledge_outline(file)` returns the numbered section titles
   (and sizes) of a Knowledge file; the handbooks keep stable numbered headings.
2. `read_knowledge(file, section)` returns ONLY the requested section (by number or exact title,
   with its subsections if asked), never the whole file; asking for a whole handbook is refused with
   the outline. Search results return the section id, so a hit can be read precisely.
3. Every agent prompt and skill says: first the outline or a search, then read only the sections
   you need ('give us section 3.2 of handbook-design'); never read whole files.
4. Backend: serves sections from the stored Knowledge document (split by headings at upload), so
   the tool does not page through the whole text.
5. Check: a run log shows only outline + section reads, total Knowledge characters per agent far
   below today's (measure before/after).

## Actual

Agents read whole handbooks or many search chunks (e.g. QA-218: 26 search_rag for sections it could not open; QA-169/182 refused reads; QA-272 whole Knowledge pasted into context).

## Evidence

Sahand, 2026-11-05 21:40 Trondheim; related QA-169, QA-182, QA-218, QA-272, QA-173.

## Cause

No section-level read and no outline call; prompts allow whole-file reads. Fix: geomind tools + prompts (python team), section store/API (backend team).

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
