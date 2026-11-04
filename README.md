# GeoMind: project documents

GeoMind designs geothermal heating and cooling plants with AI agents. A user gives files (a brief,
demand series) and says what they want in chat; the agents set the case, design and size a plant,
check it with the GEMINI digital twin and report. Built for the SPE Europe Energy GeoHackathon on
GEMINI; the product is general, geothermal first.

- App: https://geomind.team
- API: https://api.geomind.team
- GitHub: organisation `geomind-spe-geohackathon-2026`

## Repos in the project root

| Folder | What it is |
|---|---|
| `frontend/` | The web app: React, Vite, Tailwind. |
| `backend/` | The API and the worker: FastAPI, Celery, Postgres, Redis, MinIO, InfluxDB, Chroma. |
| `geomind/` | The agent package (`import geomind as gd`). |
| `gemini/` | The physics and engine package (`import gemini as gm`). |
| `infrastructure/` | The shared services: proxy, tunnel, data stores. |
| `documents/` | These documents, for people (repo `documents`). |
| `.claude/` | Context for agents and Claude Code sessions (repo `.claude`). |

The frontend calls the backend; the backend runs the geomind agents; geomind uses gemini.

## These documents

One folder per repo, the same names as the clones in the project root, and `project/` for what
concerns the whole project. Each repo also has its own `docs/` in its clone. Agent context is in
the `.claude` repo.

| Folder | Holds |
|---|---|
| [project/](project/README.md) | How we work ([development modes](project/ops/development-modes.md), [release and deploy](project/ops/release-and-deploy.md)), **[quality assurance](project/quality-assurance/README.md)** with [BUGS.md](project/quality-assurance/BUGS.md), old bug lists, design notes, plans. |
| [backend/](backend/README.md) | Contracts between the repos. |
| [frontend/](frontend/README.md) | (none yet) |
| [gemini/](gemini/README.md) | (none yet) |
| [geomind/](geomind/README.md) | (none yet) |
| [infrastructure/](infrastructure/README.md) | The services running on the Dell. |
