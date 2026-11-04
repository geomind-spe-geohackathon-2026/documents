# Test scenarios

Each scenario runs end to end on geomind.team. Note where it stands, so a tester (or the hotfix
session after a fix) goes on from there.

Priority (Fatemeh, 2026-11-04 20:20 UTC): the whole agentic pipeline must work end to end, from chat
through the agents to the case, the economics, the design, the simulation, the results and the
report. Mobile and responsive layout do not matter now.

| # | Session | Scenario | Status | Stopped at | Bugs |
|---|---|---|---|---|---|
| S1 | qa-1 | Agent-first, end to end with the challenge PDF and the two demand CSVs (`gemini/examples/hackathon_2026/`): one chat request for a heating and cooling design; answer every question; reach the case, the economics, the design, the study, the results and the report. | in progress (qa-1, started 2026-11-04 20:12 UTC) | case: case lead asked to approve its first set_case (run b894b090, 20:20 UTC); approved, run going on | QA-024 (evidence), QA-025, QA-026; QA-001 to QA-014 seen before |
| S2 | qa-2 | The same goal, other ways in: no files (the case by questions), a short vague request, a request in steps ("set the case", then "design", then "report"). | in progress (20:40 UTC) | starting: no-files case by questions | |
| S3 | qa-3 | The agents' questions: approve all, change some, a typed answer, "use your own assumptions", refusing; the economics question; values from the files, the knowledge base and the user. | in progress | approve all: runs 1-2 cut by deploys; run 3 next | QA-036 (new); QA-026, QA-024, QA-025 seen |
| S4 | qa-4 | Design and simulation through chat: plant design, sizing, a study (simulation, optimisation, comparison), the results in chat and on the Results page, adopting a result. | in progress | run 2: design lead running (20:20 UTC) | QA-023 |
| S5 | qa-5 | Outputs: the report through chat and on the Report page, export (PDF), the results' numbers and charts, the next-step chips after each answer. | in progress | 20:21 UTC: agent run 9a33db47 (case lead) in project "QA qa-5 outputs report e2e"; first run cut by the 20:20 restart | QA-024 (evidence), QA-031 |
| S6 | qa-6 | Knowledge (RAG) and Connectors (MCP) used by the agents in chat for values the files lack (site, prices, weather). | not started | in progress | start |  
| S7 | qa-7 | Runs and logs during and after agent runs: steps, tool calls, per-agent usage, the JSON download, cancel and resume, a reload during a run. | in progress | run 668fb412 cancelled (20:27 UTC); next: resume with continue | QA-008 (also on ended runs), QA-024, QA-027 |
| S8 | qa-8 | The same pipeline by hand: Case, Plant, Study, Results and Report pages, then ask the agents to continue from what was set by hand. | in progress | start: Case page by hand |  |
