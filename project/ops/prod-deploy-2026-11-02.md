# Prod deploy + project import (2026-11-02, prepared by the app thread)

Targets: backend c716849, frontend bc9d45e, gemini 17a9ccda (0.5.3), geomind c9a5c1c (0.4.1). Sibling checkouts clean. No new migration (latest 0009). No sandbox rebuild.

## Deploy (from ~/geomind-spe-hackathon-2026)
```
mkdir deploy-tree && git -C backend worktree add --detach ../deploy-tree/backend c716849 && git -C frontend worktree add --detach ../deploy-tree/frontend bc9d45e && cp -p frontend/.env.production deploy-tree/frontend/
docker tag geomind-backend:latest geomind-backend:prev && docker tag geomind-frontend:latest geomind-frontend:prev
R=$PWD; (cd deploy-tree/backend && docker buildx build --load --build-context gemini=$R/gemini --build-context geomind=$R/geomind -t geomind-backend:latest .) && (cd deploy-tree/frontend && docker buildx build --load -t geomind-frontend:latest .)
(cd backend && docker compose up -d --no-build fastapi celery) && (cd frontend && docker compose up -d --no-build frontend)
```
Adjust to how prod was built before if it differs. Smoke tests without LLM.

## Import (after the owner email is known)
```
docker exec geomind-postgres sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > transfer/prod-before-import.sql   # check var names
docker cp transfer/projects-2026-11-02.tar geomind-fastapi:/tmp/bundle.tar
docker exec geomind-fastapi python -m src.scripts.projects import /tmp/bundle.tar --owner OWNER_EMAIL
```
Bundle: transfer/projects-2026-11-02.tar, sha256 9f3a62930795485e73547e91faa1f5e468b03dcc5a38d99c172d914ea85b1bda

Expected rows: projects 4, case_versions 9, case_files 19, plant_versions 4, studies 7, results 4, chats 8, chat_states 16, messages 12, runs 8, run_events 703, run_artifacts 57, documents 0, activity 39; MinIO objects 10.

Projects: SPE GeoHackathon 2026 46d15d6b-ad9c-4e61-8a3a-c0cea9e20735; Live test b ae542488-...; Live test c 9b6c45d4-...; Live test d 1a25f059-...
