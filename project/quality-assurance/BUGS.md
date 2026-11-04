# Bugs

One line per bug; details in `bugs/`. Never edit this file by hand: use `qa.py` (see
[README.md](README.md)), which takes the next id and claims bugs under a lock. Statuses: open, fixing, fixed, verified, blocked,
wont-fix, duplicate.

| Id | Status | Severity | Area | Title | Reporter | Fixer |
|---|---|---|---|---|---|---|
| [QA-001](bugs/QA-001-read-case-on-a-project-with.md) | fixing | minor | frontend, geomind | read_case on a project with no case shows a red failed with a wrong instruction | Fatemeh | hotfix-front |
| [QA-002](bugs/QA-002-case-lead-writes-the-pump-efficiency.md) | open | minor | geomind | Case lead writes the pump efficiency requirement wrong; set_case refuses it | Fatemeh |  |
| [QA-003](bugs/QA-003-case-page-chart-the-y-axis.md) | fixing | cosmetic | frontend | Case page chart: the y-axis unit overlaps the top tick (reads MW0) | Fatemeh | hotfix-front |
| [QA-004](bugs/QA-004-ask-economics-a-unit-the-key.md) | fixed | major | geomind, data | ask_economics: a unit the key refuses is found only after the user's approve all | Fatemeh | hotfix-python |
| [QA-005](bugs/QA-005-chat-the-economics-question-is-one.md) | fixing | minor | frontend | Chat: the economics question is one unreadable wall of text, labelled "You answered" | Fatemeh | hotfix-front |
| [QA-006](bugs/QA-006-many-economics-keys-stay-open-no.md) | blocked | minor | data | Many economics keys stay open: no catalogue row | Fatemeh | hotfix-back |
| [QA-007](bugs/QA-007-ask-economics-fails-again-and-again.md) | verified | blocker | geomind | ask_economics fails again and again on a different check each time | Fatemeh | hotfix-back |
| [QA-008](bugs/QA-008-runs-and-logs-crashes-while-a.md) | fixing | major | frontend | Runs and logs crashes while a run is active: "n.includes is not a function" | Fatemeh | hotfix-front |
| [QA-009](bugs/QA-009-the-same-ask-user-question-is.md) | fixed | major | geomind | The same ask_user question is asked three times in one run | Fatemeh | hotfix-python |
| [QA-010](bugs/QA-010-a-delegated-answer-leaves-the-case.md) | blocked | major | geomind | The user delegates the open values to the agent; the agent sets nothing and proposes nothing | Fatemeh | hotfix-python |
| [QA-011](bugs/QA-011-an-openrouter-504-kills-the-nested.md) | blocked | major | geomind | An OpenRouter 504 stops the whole nested case-lead run; nothing retries | Fatemeh | hotfix-python |
| [QA-012](bugs/QA-012-deepseek-returns-empty-answers-on-long.md) | open | minor | geomind | DeepSeek returns an empty answer on long contexts; the call is lost | Fatemeh |  |
| [QA-013](bugs/QA-013-ask-economics-answer-hits-the-output.md) | open | minor | geomind | The case lead's ask_economics call hits the 16,000-token output limit and is cut | Fatemeh |  |
| [QA-014](bugs/QA-014-project-lead-calls-read-case-with.md) | open | minor | geomind | Project lead calls read_case with sections the case does not have | Fatemeh |  |
| [QA-015](bugs/QA-015-design-goes-on-while-gemini-reports.md) | fixing | major | geomind | Design goes on while gemini reports a case value the plant needs as missing | Fatemeh | hotfix-python |
| [QA-016](bugs/QA-016-an-approval-inside-fill-parts-never.md) | fixing | major | geomind | An approval inside fill_parts never reaches the user, ignores auto-approve, loses the engineer's work and leaves the run waiting | Fatemeh | hotfix-python |
| [QA-017](bugs/QA-017-a-backend-deploy-kills-an-active.md) | verified | major | backend | A backend deploy kills an active run; it stays waiting forever with no message | Fatemeh | hotfix-back |
| [QA-018](bugs/QA-018-process-engineer-s-first-build-plant.md) | open | minor | geomind | Process engineer's first build_plant sends a type with modules that differ from it; refused | Fatemeh |  |
| [QA-019](bugs/QA-019-runs-and-logs-the-step-list.md) | fixing | cosmetic | frontend | Runs and logs: the step list's token numbers spill out of the card | Fatemeh | hotfix-front |
| [QA-020](bugs/QA-020-engineers-repeat-the-same-read-case.md) | open | minor | geomind | Engineers repeat the same read_case and read_plant calls many times in a row | Fatemeh |  |
| [QA-021](bugs/QA-021-every-llm-call-gets-429-too.md) | fixed | blocker | backend,infra | Every LLM call gets 429 Too Many Requests on the free nemotron model; the chat shows Thinking with no message | Fatemeh | hotfix-back |
| [QA-022](bugs/QA-022-chat-a-cancelled-run-s-messages.md) | fixing | major | frontend,backend | Chat: a cancelled run's messages and steps disappear from the chat | Fatemeh | hotfix-front |
| [QA-023](bugs/QA-023-new-chat-on-a-project-with.md) | open | minor | geomind | New chat on a project with a copied case offers only case-building chips (Build the case by questions, Which files do you need?) | qa-4 |  |
| [QA-024](bugs/QA-024-api-rate-limit-100-requests-a.md) | fixed | major | backend | API rate limit (100 requests a minute per user) blocks normal page loads; the page shows only Rate limit exceeded | qa-8 | hotfix-back |
| [QA-025](bugs/QA-025-chat-shows-internal-error-in-geomind.md) | fixing | minor | frontend | Chat shows 'internal error in geomind' for a run interrupted by an app restart; the run says send your message again | qa-1 | hotfix-front |
| [QA-026](bugs/QA-026-approval-card-for-set-case-shows.md) | fixing | major | geomind | Approval card for set_case shows only 'Allow set_case (write)?': the user cannot see which values, units or sources they approve | qa-1 | hotfix-python |
| [QA-027](bugs/QA-027-run-log-page-does-not-update.md) | fixing | major | frontend | Run log page does not update during a run: status, steps and tokens stay as at page load until a reload | qa-7 | hotfix-front |
| [QA-028](bugs/QA-028-the-first-request-typed-in-new.md) | fixing | minor | frontend | The first request typed in New project is lost when the user leaves the chat before sending it | qa-6 | hotfix-front |
| [QA-029](bugs/QA-029-a-429-replaces-the-whole-page.md) | fixing | major | frontend | A 429 replaces the whole page with 'Rate limit exceeded'; no wait for Retry-After and no retry | hotfix-back | hotfix-front |
| [QA-030](bugs/QA-030-chat-shows-nothing-while-the-model.md) | fixing | minor | frontend | Chat shows nothing while the model provider is retried; show the live retry event | hotfix-back | hotfix-front |
| [QA-031](bugs/QA-031-auto-approve-works-only-while-the.md) | fixing | minor | frontend | Auto-approve works only while the chat tab is open; with the tab closed the run waits for an approval | qa-5 | hotfix-front |
| [QA-032](bugs/QA-032-case-page-the-challenge-demand-csvs.md) | open | major | gemini | Case page: the challenge demand CSVs are refused by hand (first column 'date', expected 'time'); no way to map the column | qa-8 |  |
| [QA-033](bugs/QA-033-case-page-the-box-says-2.md) | fixing | minor | frontend | Case page: the box says '2 problems to fix' but lists 5 lines, one of them twice | qa-8 | hotfix-front |
