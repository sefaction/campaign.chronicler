# Campaign Chronicler

Dockerized tabletop RPG campaign lore tracking app.

## Why backend/frontend pull was being skipped
Your compose previously used `build:` for backend/frontend, not `image:`. `docker compose pull` only pulls services with `image`, so those services were shown as **Skipped No image to be pulled**.

This project now uses pullable images for backend/frontend by default:
- `ghcr.io/sefaction/campaign-chronicler-backend:latest`
- `ghcr.io/sefaction/campaign-chronicler-frontend:latest`

## Run (image-based, good for Unraid updates)
```bash
docker compose pull
docker compose up -d
```

Backend API: http://localhost:18000/docs  
Frontend: http://localhost:15173

## Required image publishing
For pull/update to work, publish both images to GHCR (or change env vars to your registry):
- `BACKEND_IMAGE`
- `FRONTEND_IMAGE`

If your registry is private, authenticate on Unraid host first:
```bash
docker login ghcr.io
```

## Unraid-safe default host ports
Defaults were selected to avoid conflicts with your provided port list:
- PostgreSQL: `15432`
- Backend API: `18000`
- Frontend UI: `15173`

You can override with environment variables:
- `POSTGRES_HOST_PORT`
- `BACKEND_HOST_PORT`
- `FRONTEND_HOST_PORT`

## Environment variables
- `DATABASE_URL`
- `SECRET_KEY`
- `BACKEND_IMAGE`
- `FRONTEND_IMAGE`
- `VITE_API_BASE_URL`

## Features implemented
- Multi-campaign schema with structured entities, relationships, timelines, events, sessions, tags, and calendars.
- Golarion date fields (`year_ar`, `month_number`, `day`, `display_date`, `sort_key`).
- Visibility layers and Foundry prep fields (`foundry_*`, `sync_status`, `last_synced_at`).
- REST CRUD endpoints for required major models.
- Campaign search endpoint and entity detail aggregation endpoint.
- `/foundry` placeholder route group for future sync.
- Alembic migration + seed data.


## Unraid: fix for "Skipped No image to be pulled" + `lstat ... /backend` build errors
Your error proves Unraid is still using an older compose stack definition that contains `build:` entries. If `build:` exists, Compose tries to build locally and will look for `/backend` and `/frontend` paths on Unraid.

Use `docker-compose.unraid.yml` from this repo (image-only, no `build:` keys).

### Exact recovery steps
1. In Unraid Compose Manager, open the `campaign-chronicler` stack editor.
2. Replace stack content with `docker-compose.unraid.yml` from this repo.
3. Confirm there are **no** `build:` lines for backend/frontend.
4. Set env vars (optional overrides):
   - `BACKEND_IMAGE` (default `ghcr.io/sefaction/campaign-chronicler-backend:latest`)
   - `FRONTEND_IMAGE` (default `ghcr.io/sefaction/campaign-chronicler-frontend:latest`)
5. Redeploy using pull + up.

If the registry is private, run `docker login ghcr.io` on the Unraid host first.


## Unraid mode without GHCR (build directly from GitHub)
If GHCR returns `denied`, use `docker-compose.unraid.yml`. It builds backend/frontend directly from GitHub context instead of pulling GHCR app images.

Key behavior:
- `postgres` is still pulled as an image (`postgres:16`).
- `backend` and `frontend` are built from:
  - `context: ${GIT_CONTEXT:-https://github.com/sefaction/campaign-chronicler.git#main}`

Recommended stack file in Unraid Compose Manager:
- `docker-compose.unraid.yml`

Then deploy with rebuild/update so Unraid fetches latest GitHub source for the branch/tag/SHA in `GIT_CONTEXT`.

If you want a pinned release, set for example:
- `GIT_CONTEXT=https://github.com/sefaction/campaign-chronicler.git#v1.0.0`


## Critical fix for `pull access denied for campaign-chronicler-backend:git`
That error happened because Unraid tried to **pull** a local-only tag name (`campaign-chronicler-backend:git`) before build.

`docker-compose.unraid.yml` now avoids custom `image:` tags for build services and sets:
- `pull_policy: never` on `backend` and `frontend`

This forces Unraid to build these services from GitHub context instead of trying to pull nonexistent registries.

### Use this exact stack behavior on Unraid
- Stack file: `docker-compose.unraid.yml`
- `GIT_CONTEXT` should be a valid repo URL, e.g.:
  - `https://github.com/sefaction/campaign-chronicler.git#main`
- Update/rebuild stack (not pull-only) so backend/frontend are built.

Expected pull phase behavior:
- `postgres` pulls normally.
- `backend` and `frontend` are not pulled; they are built from Git context.
