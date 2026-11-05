# Speed baseline scripts

Read-only analysis of stored agent runs (plan `../speed-case-plant.md`, tasks A1/A2). No secrets:
credentials come from `backend/.env` through `backend/scripts/seed_qa_projects.py`. Work dir is `/tmp/sa`
(`mkdir -p /tmp/sa/scripts /tmp/sa/data`). Run from `backend/` with `.venv/bin/python`, `nice -n 10`.

1. `fetch.py`: list projects and runs, writes `/tmp/sa/data/runs.json`.
2. `fetch2.py`: log and agents of every run started since 2026-11-05 (edit the date); about 540 MB.
3. `analyse.py`: per-stage steps/time/refusals/cards, per-tool first-try refusals, cause clusters.
4. `report.py` (cause groups T1-T11), `write.py` (tables for the baseline document).
`ev.py` reads one run's SSE events (no timestamps in them). Only GET calls are used.
