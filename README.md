# Campaign Chronicler

Dockerized tabletop RPG campaign lore tracking app.

## What was failing and why
Your latest error shows Docker BuildKit tried to clone GitHub and failed with:
`fatal: could not read Username for 'https://github.com': terminal prompts disabled`

That means the repo URL used for `build.context` requires authentication (private repo or restricted access), but no non-interactive credentials were provided.

## Correct Unraid deployment options

### Option A (recommended): pull prebuilt images
Use `docker-compose.unraid.yml` in Unraid Compose Manager.

This file is image-only for app services:
- Backend image: `ghcr.io/sefaction/campaign-chronicler/backend:main`
- Frontend image: `ghcr.io/sefaction/campaign-chronicler/frontend:main`

Expected pull behavior:
- `postgres` pulled
- `backend` pulled
- `frontend` pulled
- **No build step** for backend/frontend

If images are private, run on Unraid host first:
```bash
docker login ghcr.io
```

### Option B: build from GitHub source
Use `docker-compose.unraid.build.yml` only when you intentionally want remote source builds.

For private repos, you must set `GIT_CONTEXT` with embedded non-interactive credentials, e.g.:
```bash
GIT_CONTEXT=https://<github-username>:<github-token>@github.com/sefaction/campaign-chronicler.git#main
```

Without that, BuildKit cannot prompt for credentials and will fail exactly like your error.

## Ports (non-conflicting defaults)
- PostgreSQL: `15432 -> 5432`
- Backend API: `18000 -> 8000`
- Frontend UI: `15173 -> 5173`

## Environment variables
See `.env.example` for defaults:
- `DATABASE_URL`
- `SECRET_KEY`
- `POSTGRES_HOST_PORT`
- `BACKEND_HOST_PORT`
- `FRONTEND_HOST_PORT`
- `VITE_API_BASE_URL`
- `BACKEND_IMAGE`
- `FRONTEND_IMAGE`
- `GIT_CONTEXT` (build-mode only)
