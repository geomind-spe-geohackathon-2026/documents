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
| Deploy | After `main` is pushed, by the release-and-deploy steps. | After the person merged and the release is tagged. | Right after the push, only the service that changed. |
| After | Report the commit, version and health. | Report the merge and the deploy. | Test the same thing again on the live site, then go on from where the work stopped. Bring `dev` up to `main` at the next development work. |

## One clone, no worktrees

Each repo has one clone in the project root, and work happens in it, on the branch the mode names.
Git worktrees are not used.

## Always commit and push

In every mode, everything left in the working tree is committed and pushed when a piece of work
ends: nothing stays only on the Dell. Stage files by path (the clones are shared by parallel
sessions), and push to the branch of the mode.

## Hotfix, step by step

1. Work on the default branch of the repo that needs the fix (`main`; for gemini `dev`); pull it
   first. Push only to that branch.
2. Change only the code the problem needs. Run no tests and no checks.
3. Commit, tag a patch version, push the default branch.
4. Deploy only that service at once.
5. Check the same thing again on the live site, then go on from where the work stopped.
6. Each fix goes in the work list with its commit and version. The full tests run later, in
   development mode, and anything they find is fixed there.

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
