# Quality assurance

How we test the app on production (geomind.team) and get every bug fixed. People (Sahand,
Fatemeh) and Claude Code sessions test in parallel and report here; a hotfix session takes the bugs
one by one, fixes them, deploys and reports back here.

## Files

| Path | What it is | Who writes it |
|---|---|---|
| [BUGS.md](BUGS.md) | The index: one line per bug with its id, status, severity, area, title, reporter and fixer. | Only `qa.py`. |
| [qa.py](qa.py) | The tool that reports, claims and updates bugs under a lock. | Everyone runs it. |
| `bugs/QA-<nnn>-<slug>.md` | One file per bug: where, steps, expected, actual, evidence, cause, fix, retest. Made from [TEMPLATE.md](TEMPLATE.md). | The reporter writes the top; the hotfix session writes Fix and Retest. |
| `evidence/QA-<nnn>/` | Screenshots (`1.png`, `2.png` ...), the run JSON (Runs and logs, download), logs. | The reporter. |
| [IMPROVEMENTS.md](IMPROVEMENTS.md) | Ideas to make the app faster, cheaper or make fewer mistakes: one section per `IMP-<nnn>`. | Everyone. |
| [SCENARIOS.md](SCENARIOS.md) | The test scenarios and where each one stands. | Testers. |
| `reports/` | Reports of whole test rounds. | Testers, after a round. |

One file per bug, so parallel sessions never edit the same file at once; `BUGS.md` changes only one
line at a time.

## Always use qa.py

Many sessions read and write here at once. Never edit `BUGS.md` by hand: `qa.py` takes a lock,
pulls, writes, commits and pushes in one step, so no two sessions get the same id and no bug is
claimed twice. Run it from anywhere, with the path:

```sh
QA=~/geomind-spe-hackathon-2026/documents/project/quality-assurance/qa.py
python3 $QA list --status open
python3 $QA new "Title, one line" --severity major --area frontend --reporter qa-3
python3 $QA save QA-021                      # after you filled in the file and the evidence
python3 $QA next --area frontend --fixer hotfix-front    # claim the most severe open bug
python3 $QA claim QA-021 --fixer hotfix-back             # claim one bug by id
python3 $QA set QA-021 --status fixed --note "frontend 1.1.35, commit 4b5c6d7"
python3 $QA set QA-021 --status verified --note "checked again on geomind.team, works"
```

## Report a bug

1. `python3 $QA list`: is it already there? If so, add your evidence to that bug's file and
   `save` it instead of a new one.
2. `python3 $QA new ...`: it gives the id, the file (from `TEMPLATE.md`) and the evidence folder.
3. Fill in the file: where (URL, project, chat, run id), the versions (the API's
   `/api/v1/system/health`, the frontend's bundle), steps, expected, actual, and in Area the repo
   where you think the fix belongs. Put screenshots (`1.png` ...) and the run JSON in
   `evidence/QA-<nnn>/` and link them.
4. `python3 $QA save QA-<nnn>`.
5. Write facts. A guess about the cause goes under Cause, marked as a guess.

## Fix a bug (hotfix session)

1. `python3 $QA next --area <your areas> --fixer <your name>` claims the most severe open bug of
   your areas. Never work on a bug you did not claim.
2. Decide which repo the fix belongs in; if the bug is not in your areas after all, set it back to
   `open` with the right area in a note, and take the next.
3. Fix it in hotfix mode (`documents/project/ops/development-modes.md`): the bug's id in the
   commit message, the version raised, deployed at once.
4. `python3 $QA set QA-<nnn> --status fixed --note "<repo> <version>, commit <sha>, deployed"`.
5. Check it again on geomind.team by the bug's steps, then `--status verified` with a note, or
   `--status open` with what still fails.
6. Tell the coordinator the ids and versions, then take the next bug.

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
