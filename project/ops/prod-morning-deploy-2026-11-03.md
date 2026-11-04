# Morning prod deploy (2026-11-03), waits for Sahand's approval

Blocked tonight by the NTNU Dell permission system (schema migration on prod). Needs Sahand to say go AND allow it in Claude Code settings on the Dell.

Contents (pins come from BACKEND I; take the latest backend main at that time):
- backend with migration 0010 (studies.plant_pinned boolean NOT NULL DEFAULT false, additive; down drops the column)
- geomind 0.4.13 vendored wheel (NEVER 0.4.12: it changed compute_kpis output shape; replaces 0.4.10/0.4.9/0.4.7; leave GEOMIND_GEMINI_THREADS unset; check hash: vendored SHA256SUMS or, since the geomind repo is public (2026-11-03 07:52 UTC), the release URL with sha256 befe3d56…cde55, see /mnt/project-files/geomind/release-0.4.13-for-backend.md)
- MALLOC_ARENA_MAX=2 is set as ENV in the backend Dockerfile (backend dev be46717), so no .env.production change; just verify it in both containers. Keeps long-running workers at about 1.0 to 1.7 GB instead of about 3.5 GB (glibc fragmentation from gemini threads).
- frontend: unchanged unless the app thread sends a pin

Procedure: pg_dump to ~/geomind-backups; back up .env.production; tag geomind-backend:latest -> :prev; clean tree under backend/.tmp/deploy-<hash>/; check alembic head 0010 (down_revision 0009); up fastapi celery; confirm alembic current 0010, existing studies plant_pinned=false, `docker exec geomind-celery printenv MALLOC_ARENA_MAX` = 2; no-LLM smoke (health/site/login 200, 4 projects, versions, DeepSeek-only, relace/fp4, context 128000, no celery tasks, WebSocket replay 101).

Prod right now: backend 8b41338, frontend ffd7673, geomind 0.4.6, gemini 0.5.5, alembic 0009.
