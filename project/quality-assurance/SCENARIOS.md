# Test scenarios

Each scenario runs end to end on geomind.team. Note where it stands, so a tester (or the hotfix
session after a fix) goes on from there.

Priority (Fatemeh, 2026-11-04 20:20 UTC): the whole agentic pipeline must work end to end, from chat
through the agents to the case, the economics, the design, the simulation, the results and the
report. Mobile and responsive layout do not matter now.

| # | Session | Scenario | Status | Stopped at | Bugs |
|---|---|---|---|---|---|
| S1 | qa-1 | Agent-first, end to end with the challenge PDF and the two demand CSVs (`gemini/examples/hackathon_2026/`): one chat request for a heating and cooling design; answer every question; reach the case, the economics, the design, the study, the results and the report. | in progress (qa-1) | case set (run 0cb4b436, 6 set_case approvals); answered the case lead's question on return temperatures and air (20:32 UTC); run going on | QA-025, QA-026 (fixed, retested), QA-024 (evidence); QA-001 to QA-014 seen before |
| S2 | qa-2 | The same goal, other ways in: no files (the case by questions), a short vague request, a request in steps ("set the case", then "design", then "report"). | stopped, handed to qa-1 | no-files way only: case (3 question rounds) and economics set; design in progress (run 592f3730 still running, project QA qa-2 no files case by questions, chat abfff893); vague and step-by-step ways not started | QA-034, QA-037, QA-041 |
| S3 | qa-3 | The agents' questions: approve all, change some, a typed answer, "use your own assumptions", refusing; the economics question; values from the files, the knowledge base and the user. | in progress | approve all: runs 1-2 cut by deploys; run 3 next | QA-036 (new); QA-026, QA-024, QA-025 seen |
| S4 | qa-4 | Design and simulation through chat: plant design, sizing, a study (simulation, optimisation, comparison), the results in chat and on the Results page, adopting a result. | in progress | run 4 (641c7f5a): design lead filling parts, 21:05 UTC; runs 2-3 cut by deploys | QA-023; evidence in QA-025, QA-024 |
| S5 | qa-5 | Outputs: the report through chat and on the Report page, export (PDF), the results' numbers and charts, the next-step chips after each answer. | in progress | 20:21 UTC: agent run 9a33db47 (case lead) in project "QA qa-5 outputs report e2e"; first run cut by the 20:20 restart | QA-024 (evidence), QA-031 |
| S6 | qa-6 | Knowledge (RAG) and Connectors (MCP) used by the agents in chat for values the files lack (site, prices, weather). | stopped | run a2dd83e3 waiting for approval of set_case (demand return temperatures), before economics; RAG and open-meteo used in the case | QA-028, QA-043; evidence to QA-024, QA-039 |
| S7 | qa-7 | Runs and logs during and after agent runs: steps, tool calls, per-agent usage, the JSON download, cancel and resume, a reload during a run. | in progress | run 668fb412 cancelled 20:27 UTC; resumed with continue as run d5765e1e (20:32 UTC), watching it | QA-008 (also on ended runs), QA-024, QA-027 |
| S8 | qa-8 | The same pipeline by hand: Case, Plant, Study, Results and Report pages, then ask the agents to continue from what was set by hand. | stopped, handed to qa-4 | Case by hand done (v10); plant from template (v1); study by hand blocked by QA-040; chat asked agents to continue (run 60731e65: plant rebuilt with backup none, engineers filling parts) | QA-024, QA-032, QA-033, QA-038, QA-040 |
