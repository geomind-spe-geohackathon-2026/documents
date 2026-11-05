# QA-096: Knowledge CSV view: every cell wraps its full text, rows are huge and columns too wide

| Field | Value |
|---|---|
| Status | fixing |
| Severity | minor |
| Area | frontend |
| Reporter | user via coordinator |
| Found | 2026-11-05 09:39 UTC |
| Versions | frontend 1.1.77 |
| Where | https://geomind.team/knowledge, View of cost-sources.csv |
| Fixer | hotfix-front-II |

## Steps

1. Open Knowledge, click View on cost-sources.csv.
2. Look at the table.

## Expected

1. Fixed compact row height: cell text on one line, cut with an ellipsis; a single cell can be expanded (click the cell: popover with the full text).
2. Columns have a capped width; no column grows to fit long text.
3. The header row stays at the top while scrolling down.
4. Horizontal scrolling when there are many columns.

Stock shadcn components.

## Actual

Every cell wraps its full text, so rows are very tall (source, quote, conversion, note) and columns are too wide; few rows fit on screen.

## Evidence

- ![CSV view](../evidence/QA-096/1.png)
- ![Knowledge list](../evidence/QA-096/2.png)

## Scope (user, via Coordinator-III, 09:40 UTC)

Build it as one shared component and use it wherever the app shows tabular data, so the UI is
consistent. Shared component: `frontend/src/shared/ui/data-table.tsx` (DataTable, DataHead,
DataCell). Places, in the order they are switched (small steps, one deploy window each):

| Step | Place | File | State |
|---|---|---|---|
| 1 | CSV/TSV view, Knowledge and project Library | `domains/workspace/documents/csv-table.tsx` | 1.1.82 |
| 2 | Markdown tables (chat answers, .md file view, reports) | `shared/ui/markdown.tsx` | todo |
| 2 | Agent study record | `domains/design/study/record-page.tsx` | todo |
| 2 | Chat design alternatives | `domains/assistant/chat/alternatives-table.tsx` | todo |
| 3 | Results: compare, constraints, findings | `domains/design/results/{compare-table,constraints-card,findings-cards}.tsx` | todo |
| 3 | Evolve structures | `domains/design/study/structures-page.tsx` | todo |
| 4 | Lists with actions: studies, runs, run totals, chat usage, Library, users, case and plant history | `study/{study-table,study-row}.tsx`, `runs/{page,totals-table}.tsx`, `chat/chat-status.tsx`, `documents/page.tsx`, `users/page.tsx`, `{case,plant}/history-panel.tsx` | todo |

## Cause

Every CSV cell wrapped its full text (`whitespace-normal`, max 28rem), so rows grew very tall. The
header was `sticky` but sat inside the shadcn table container (`overflow-x-auto`), so it stuck to
that box, which never scrolls vertically, and scrolled away.

## Fix

Step 1: frontend 1.1.82, commit c88543d (hotfix-front-II): shared DataTable; the table container is the scroll box (both ways) so the header sticks; cells one line with ellipsis, max 15rem wide, click opens the full text in a popover. Checked on a local build with cost-sources.csv: 30 px rows, header stays at the top after scrolling 800 px down and 600 px right, popover shows the full cell.

## Retest

(Who, when, result.)
