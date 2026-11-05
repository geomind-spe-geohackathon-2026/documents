# QA-358: Rename the RAG tools to Knowledge names everywhere: read_rag -> read_knowledge, search_rag -> search_knowledge (one name per tool, no aliases left in prompts, skills, handbooks, events, UI)

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind,backend,frontend |
| Reporter | Sahand |
| Found | 2026-11-05 21:20 UTC |
| Versions | geomind HEAD 2026-11-05 22:20 Trondheim |
| Where | geomind tools, prompts, skills; Knowledge handbooks; backend events; frontend tool labels |
| Fixer | |

## Steps

1. grep geomind for read_rag / search_rag.

## Expected

Sahand 22:20 Trondheim: the tools are named read_knowledge and search_knowledge only. Rename the tool registrations, every prompt/skill/handbook mention, run-log labels and UI labels; no old names left (one grep must find none). Do it together with QA-351 (outline + section reads).

## Actual

geomind uses both: read_rag 61x and search_rag 61x next to read_knowledge 65x and search_knowledge 18x (grep of geomind/, 22:20).

## Evidence

Grep counts above.

## Cause

Old RAG names kept beside the new Knowledge names (the read_rag -> read_file/read_knowledge rename was never finished). Sahand's request: top. Python team (member on QA-351), backend/frontend labels to their leads; Knowledge handbooks: the handbook threads replace mentions.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
