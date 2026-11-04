# Prod deploy: gemini 0.5.5 from release wheel (no -e for gemini)

Pins: backend e4c5626, frontend 8a67892, gemini 0.5.5 (release wheel, installed by pip during build), geomind c9a5c1c (0.4.1, still ../geomind build context).
Contract 46 additive, no migration. Numbers identical to 0.5.4 (18,121 values at 1e-9).

Steps (from backend/ and frontend/ at those commits; ../geomind at c9a5c1c):
1. Backup (pg_dump) and tag :prev as usual.
2. docker pull ghcr.io/geomind-spe-geohackathon-2026/gemini-sandbox:0.5.5
3. docker tag ghcr.io/geomind-spe-geohackathon-2026/gemini-sandbox:0.5.5 gemini-sandbox:0.5.5
4. Backend: docker buildx build --load --build-context geomind=../geomind -t geomind-backend:latest .   (or docker compose build; compose.yml passes only the geomind context). Needs github.com access during build. DROP the old --build-context gemini=.
5. Frontend build as before.
6. docker compose up -d --no-build fastapi celery ; frontend up.
7. Smoke without LLM; confirm fastapi/celery report gemini 0.5.5.

GEOMIND_CONTEXT_WINDOW=128000 only needed with geomind 0.4.2.
