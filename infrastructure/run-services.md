# How to bring GeoMind services up and down (2026-11-02)

Repos sit side by side (laptop: ~/geomind-spe-hackathon-2026/; Mac: ~/Desktop/geomind-spe-geohackathon-2026/):
backend, frontend, infrastructure, gemini, geomind. Never commit any `.env` file.

## Where the settings live
- infrastructure/<service>/.env  (one per shared service: traefik, cloudflared, postgres, redis, minio, influxdb, chromadb, pgadmin). Copy from that folder's .env.example. No .env at the infrastructure root.
- backend/.env.production   server deploy (backend/compose.yml reads it). Passwords match the infrastructure services. backend/.env stays for the test suite only.
- backend/.env.dev   local dev only (scripts/stack-up.sh generates it from .env.dev.example).
- frontend/.env.production   committed; VITE_API_URL=https://api.geomind.team/api/v1, read only by `vite build`.

## A) Local development (no domain)
```sh
cd backend
scripts/stack-up.sh            # services (compose project geomind-dev), migrate, seed, API, worker, frontend
scripts/stack-down.sh          # stop, keep data
scripts/stack-down.sh --reset  # stop and delete the data volumes
```
App http://localhost:5173, API http://127.0.0.1:8000/docs.

## B) Server deploy (geomind.team, behind Traefik + Cloudflare Tunnel)
Order up: networks, traefik, cloudflared, data services, backend, frontend. Down: reverse.
```sh
docker network inspect traefik >/dev/null 2>&1 || docker network create traefik
docker network inspect geomind >/dev/null 2>&1 || docker network create geomind

# each shared service, from its own folder
cd infrastructure/traefik     && docker compose up -d
cd ../cloudflared             && docker compose up -d
cd ../postgres                && docker compose up -d   # same for redis, minio, influxdb, chromadb (pgadmin optional)

cd ../../backend  && docker compose up -d --build       # geomind-fastapi (runs migrations first) + geomind-celery
cd ../frontend    && docker compose up -d --build       # geomind-frontend (nginx)
```
Stop one: `docker compose down` in its folder. `docker compose down -v` also DELETES that service's data.
Check before starting: `docker compose config -q`.

Addresses: https://geomind.team (frontend), https://api.geomind.team (API), https://traefik.geomind.team/dashboard/ (Traefik).
Cloudflare Tunnel routes point to https://geomind-traefik:443 (Origin Server Name = the hostname). Certificates: Let's Encrypt via Cloudflare DNS challenge.


## Rules
- Never run `docker compose down -v` without Sahand's OK (it deletes that service's data).
- Add nothing about backend or frontend to infrastructure; each repo runs from its own folder.
- The old infrastructure root compose.yml / .env.example are gone; commands that used them are outdated.
- If docker gives a permission error on the laptop, run it as `sg docker -c "..."`.
- Local dev containers `geomind-dev-*` (backend/compose.services.yml) are separate from the server deploy; do not mix them.
- Only Traefik publishes host ports (80/443); never add host ports to production containers (dev uses 5432/6379/9000-9001/8000/5173 on the laptop).
- To ship a change: commit, then in backend/ or frontend/ run `docker compose up -d --build`. Not while another thread is deploying.
- Do not stop or restart production containers without Sahand's say-so.

## Production deploys (from 2026-11-02 21:25)
- Backend/frontend deploys and data imports: the app thread ("Build frontend and backend with Fatemeh") via its laptop session. Infrastructure (traefik, cloudflared, data services, their .env, Cloudflare): the hosting thread.
- Build only from pushed commits in a clean checkout, with ../gemini and ../geomind at pinned commits; tag running images :prev first; pg_dump the prod DB before a migration or import.
- Smoke tests: site 200, API health 200, login. No LLM calls (no token use for now).
