# Quality assurance

How we test the app on production (geomind.team) and get every bug fixed. People (Sahand,
Fatemeh) and Claude Code sessions test in parallel and report here; a hotfix session takes the bugs
one by one, fixes them, deploys and reports back here.

## Files

| Path | What it is | Who writes it |
|---|---|---|
| [BUGS.md](BUGS.md) | The index: one line per bug with its id, status, severity, area, title, reporter and fixer. | Everyone: add a line when you report, change the status when it changes. |
| `bugs/QA-<nnn>-<slug>.md` | One file per bug: where, steps, expected, actual, evidence, cause, fix, retest. Made from [TEMPLATE.md](TEMPLATE.md). | The reporter writes the top; the hotfix session writes Fix and Retest. |
| `evidence/QA-<nnn>/` | Screenshots (`1.png`, `2.png` ...), the run JSON (Runs and logs, download), logs. | The reporter. |
| [SCENARIOS.md](SCENARIOS.md) | The test scenarios and where each one stands. | Testers. |
| `reports/` | Reports of whole test rounds. | Testers, after a round. |

One file per bug, so parallel sessions never edit the same file at once; `BUGS.md` changes only one
line at a time.

## Report a bug

1. Read `BUGS.md`: is it already there? If so, add your evidence to that bug instead.
2. Take the next free id: the highest `QA-<nnn>` in `BUGS.md` plus one. Add its line to `BUGS.md`
   at once, status `open`, so nobody else takes the id.
3. Copy `TEMPLATE.md` to `bugs/QA-<nnn>-<slug>.md` (slug: a few words, lowercase, dashes) and fill
   in the top: where (URL, project, chat, run id), the versions (the frontend's footer, the API's
   `/api/v1/system/health`), steps, expected, actual.
4. Put the screenshots and the run JSON in `evidence/QA-<nnn>/` and link them from the bug file.
5. Write facts. A guess about the cause goes under Cause, marked as a guess.

## Fix a bug (hotfix session)

1. Take the open bugs from `BUGS.md`, the highest severity first. Set the status to `fixing` and
   the fixer to your session's name before you start, so no other session takes it.
2. Read the bug file and its evidence. Fix in hotfix mode (`docs/ops/development-modes.md`): on
   the default branch (`main`; for gemini `dev`), only the code the bug needs, no tests; tag,
   push, deploy that service.
3. Write Fix in the bug file: the cause, the commit, the version, when it was deployed. Set the
   status to `fixed`.
4. Check it again on geomind.team by the bug's steps. Write Retest. Set the status to `verified`,
   or back to `open` with what still fails.
5. Tell the team in the chat: the ids fixed, the versions deployed, anything that needs a person.

## Statuses

| Status | Means |
|---|---|
| `open` | Reported, nobody works on it. |
| `fixing` | A session works on it (the fixer column says which). |
| `fixed` | Deployed; not checked again yet. |
| `verified` | Checked again on production: it works. |
| `blocked` | Needs a person or a decision (say what in the bug file). |
| `wont-fix` / `duplicate` | Closed, with the reason (or the other id) in the bug file. |

## Severity

| Severity | Means |
|---|---|
| `blocker` | A main flow cannot go on (a run fails, a page crashes, data is lost). |
| `major` | A flow works only with a detour, or gives a wrong result. |
| `minor` | Works, but confusing or noisy. |
| `cosmetic` | Looks wrong only. |

Areas: `frontend`, `backend`, `geomind` (agents and prompts), `gemini`, `data` (catalogue,
knowledge), `infra`.
