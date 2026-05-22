# Campaign Chronicler

Dockerized tabletop RPG campaign lore tracking app.

## Fix for the GHCR `denied` error
Your latest failure is specifically GHCR auth/visibility:
- `ghcr.io/sefaction/campaign-chronicler/frontend:main ... denied`

To eliminate GHCR entirely, `docker-compose.unraid.yml` now builds backend/frontend directly from your public GitHub repo:
- `https://github.com/sefaction/campaign.chronicler.git#main`

So:
- `postgres` is pulled (`postgres:16`)
- `backend` is built from GitHub context
- `frontend` is built from GitHub context

## Unraid deployment (recommended)
1. In Unraid Compose Manager, use `docker-compose.unraid.yml` as the stack file.
2. Set (or keep default) environment variables from `.env.example`.
3. Redeploy with rebuild.

Expected logs:
- Pull step: postgres pulled; backend/frontend skipped (they are build services).
- Build step: backend/frontend build from GitHub context.

## If build fails on wrong repo path
If your actual repo slug is different, set `GIT_CONTEXT` explicitly, for example:
- `https://github.com/sefaction/campaign-chronicler.git#main`
- `https://github.com/sefaction/campaign.chronicler.git#main`

## Ports (non-conflicting defaults)
- PostgreSQL: `15432 -> 5432`
- Backend API: `18000 -> 8000`
- Frontend UI: `15173 -> 5173`

## Environment variables
See `.env.example`:
- `DATABASE_URL`
- `SECRET_KEY`
- `POSTGRES_HOST_PORT`
- `BACKEND_HOST_PORT`
- `FRONTEND_HOST_PORT`
- `VITE_API_BASE_URL`
- `GIT_CONTEXT`
