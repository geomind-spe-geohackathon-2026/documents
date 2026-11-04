# Development modes

Every piece of work runs in one of three modes. At the start of every session the agent asks the
user which mode it works in, and changes nothing until the user answers. The session stays in that
mode until the user changes it.

| | Development | Production | Hotfix |
|---|---|---|---|
| When | Normal work on features and bugs. | A change that must be reviewed before it reaches `main`. | A fast fix on production, for example while testing the live site. |
| Branch | The second branch, `dev`. | The second branch, `dev`. | The default branch directly: `main`, except gemini, whose default is `dev`. |
| Tests | Every automated test that needs no LLM: unit, integration, lint, type checks, release profile, end-to-end with fake models. | The same, on `dev` and in CI. | None. No test, lint or check runs. |
| To `main` | The agent fast-forwards `main` to `dev` locally, tags and pushes. | Only a pull request on GitHub that a person approves and merges. The agent never merges locally. | The commit is on the default branch already; tag and push it. |
| Deploy | After `main` is pushed, by the release-and-deploy steps. | After the person merged and the release is tagged. | Right after the push, only the service that changed, with `scripts/hotfix_deploy.sh`; packages as local wheels, no wait for GitHub. |
| After | Report the commit, version and health. | Report the merge and the deploy. | Test the same thing again on the live site, then go on from where the work stopped. Bring `dev` up to `main` at the next development work. |

## One clone, no worktrees

Each repo has one clone in the project root, and work happens in it, on the branch the mode names.
Git worktrees are not used.

## Always commit and push

**Commit before you start and when you finish.** Before you start a piece of work, the clone must
be clean: commit and push anything left (yours), so you start from a known state. When the piece
is done, commit and push at once, before anything else (a deploy, the next bug, a report). The
deploy scripts refuse a clone with uncommitted changes, so one session's half-done work blocks
every deploy of that repo until it is committed.


In every mode, everything left in the working tree is committed and pushed when a piece of work
ends: nothing stays only on the Dell. Stage files by path (the clones are shared by parallel
sessions), and push to the branch of the mode.

## Hotfix, step by step

The fix reaches production as fast as possible.

1. **Find the repo the bug really belongs in** before changing anything: the fix goes in that
   repo. When it could as well be fixed in the frontend or the backend as in a Python package
   (geomind, gemini), fix it in the frontend or the backend. Go to a package only when the bug
   is truly there.
2. Work on that repo's default branch (`main`; for gemini `dev`); pull it first. Change only the
   code the bug needs. Run no tests, no lint, no checks.
3. Raise the version in every project the fix touches, so the number of fixes shows: the patch
   of the package, and the backend's or frontend's patch for every deploy (`CHANGELOG.md` line
   with the bug id).
4. Commit with the bug id and its title in the message (`QA-012: chat question shows as one
   paragraph`), push the default branch.
5. Deploy only what changed, with the repo's script; compose never builds anything:
   - frontend: `frontend/scripts/hotfix_deploy.sh`;
   - backend: `backend/scripts/hotfix_deploy.sh`;
   - a Python package (geomind, gemini): build its wheel locally, do not wait for GitHub:
     `backend/.venv/bin/python -m pip wheel --no-deps -w backend/.tmp/hotfix-wheels geomind/`
     (remove that package's older wheel from `backend/.tmp/hotfix-wheels/` first), raise the
     backend's patch with a CHANGELOG line naming the local wheel, then run
     `backend/scripts/hotfix_deploy.sh`: it builds the image from `main` and installs every wheel
     in `.tmp/hotfix-wheels/` on top (`backend/Dockerfile.hotfix`). The wheels stay there and
     are installed on every hotfix deploy until a development release pins the released version
     in `requirements.txt` and empties the folder. Tag the package's version and push the tag
     too; its CI release may come later.
   The scripts hold one lock, so two sessions never deploy at once.
   During a QA round, deploy only in windows at :00 and :30 UTC, with every fix ready by then;
   a blocker may go at once. A deploy recreates the worker and ends the running agent runs (until
   QA-035), so check the runs table first and name the runs it cut in the bug note.
6. Check the same thing again on the live site, then go on from where the work stopped.
7. Each fix goes in its bug file (`qa.py set ... --status fixed --note ...`). The full tests run
   later, in development mode, and anything they find is fixed there.

## Production, step by step

1. Work on `dev`; run every automated test that needs no LLM; push `dev`.
2. Open a pull request from `dev` to `main` on GitHub with what changed, the tests run and the
   risks. Its description follows the repo's pull request template when there is one.
3. A person reviews, approves and merges it on GitHub. The agent waits; it never merges, rebases or
   pushes `main` itself in this mode.
4. After the merge: tag the release from `main` and deploy by the release-and-deploy steps.

`gh` is not installed on the Dell: open the pull request in the browser from the link GitHub prints
on push, or ask Sahand to.

## Tests that need an LLM

Live runs and end-to-end tests with a real model never run without Sahand's OK, in any mode.

See [release-and-deploy.md](release-and-deploy.md) for versions, backups and checks.
