# Release and deploy

How a change reaches geomind.team. The Deploy thread's live state and exact commands are in
`.claude/notes/deploy-runbook.md` (for agents).

## Branches

`main` stays stable and is what production runs. The mode decides the branch and the way to `main`
([development-modes.md](development-modes.md)): development and production work on `dev`
(development: the agent fast-forwards `main` after every automated test that needs no LLM passes;
production: only a pull request a person approves and merges on GitHub); hotfix works directly
on the default branch (`main`; for gemini `dev`) with no tests. One clone per repo, no worktrees.

## Releases

| Repo | Released from | What a release is |
|---|---|---|
| gemini | `dev` (main = dev) | tag `v<version>`; CI puts the wheel on GitHub Releases |
| geomind | `main` | tag `v<version>`; CI puts the wheel on GitHub Releases |
| backend | `main` | tag `v1.1.<patch>`; pins the gemini and geomind wheels by URL and sha256 |
| frontend | `main` | tag `v1.1.<patch>` |

Consumers install released wheels only, never `-e`. Versions are semver with a `CHANGELOG.md`;
backend and frontend stay on 1.1 and raise only the patch. A geomind release needs Sahand's word.

## Deploys

- Deploy only `main`, from pushed commits in a clean checkout; backend first, then frontend,
  never both at once.
- Tag the running image `:prev` before switching, so a rollback is one tag.
- Back up the database (`pg_dump` to `~/geomind-backups/`) before any migration or import.
- A schema migration needs Sahand's own approval.
- Check after: the site and `https://api.geomind.team/api/v1/system/health` answer 200 with the new
  version, the worker logs say ready, login works.
- Production env edits and production data writes are Sahand's: give him the command.
- Never run `docker compose down -v` or stop production containers without Sahand's OK.
