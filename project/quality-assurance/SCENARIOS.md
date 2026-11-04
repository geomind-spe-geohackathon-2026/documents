# Test scenarios

Each scenario runs end to end on geomind.team. Note where it stands, so a tester (or the hotfix
session after a fix) goes on from there.

| # | Session | Scenario | Status | Stopped at | Bugs |
|---|---|---|---|---|---|
| S1 | qa-1 | Agent-first, end to end: a new project with the challenge PDF and the two demand CSVs (`gemini/examples/hackathon_2026/`); ask in chat to design heating and cooling; follow every question to the case, the economics, the design, the study, the results and the report. | not started | | QA-001 to QA-014 seen before |
| S2 | qa-2 | Chat in depth: a case by questions with no files, the suggestion chips, attachments in the composer, answering and refusing questions, stop, several chats, rename and delete a chat, reload during a run. | not started | | |
| S3 | qa-3 | Case page by hand: every tab (Demand, Site, Utilities, Economics, Requirements, Time), CSV upload and columns, units, validation, save version, history, discard. | not started | | |
| S4 | qa-4 | Plant, Study, Results, Report by hand: templates, flowsheet, parameters and ranges, study kinds, start and cancel, result detail, compare, adopt, report export. | not started | | |
| S5 | qa-5 | Projects and workspace: project list, new project dialog, import and export, overview, library, search, project settings, copy a case from another project, rename and delete (own QA projects only). | not started | | |
| S6 | qa-6 | Knowledge (RAG) and Connectors (MCP): upload and search documents, add and check a connector, use both from chat. | not started | | |
| S7 | qa-7 | Runs and logs: the run list, a run live and finished, steps, per-agent usage, the JSON download, cancel; the usage page. | not started | | QA-008 |
| S8 | qa-8 | Across the app: sign-in and out, account, users (admin), navigation and every route, 404s, narrow and mobile widths, dark mode, keyboard use, console and network errors on every page. | not started | | |
