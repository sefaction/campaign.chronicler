# Campaign Chronicler

Dockerized tabletop RPG campaign lore tracking app.

## Run with local source
```bash
GIT_CONTEXT=. docker compose up --build
```

## Run directly from GitHub source context
This lets you deploy/update by changing branch/tag/commit in `GIT_CONTEXT`.

```bash
docker compose up --build
```

By default compose uses:
- `context: ${GIT_CONTEXT:-https://github.com/sefaction/campaign-chronicler#main}`

Examples:
- Latest `main`: `GIT_CONTEXT=https://github.com/sefaction/campaign-chronicler#main`
- A tag: `GIT_CONTEXT=https://github.com/sefaction/campaign-chronicler#v1.0.0`
- A commit SHA: `GIT_CONTEXT=https://github.com/sefaction/campaign-chronicler#<sha>`

Backend API: http://localhost:18000/docs  
Frontend: http://localhost:15173



Default host ports were selected to avoid conflicts with your existing Unraid allocations:
- PostgreSQL: `15432`
- Backend API: `18000`
- Frontend UI: `15173`

You can override with environment variables:
- `POSTGRES_HOST_PORT`
- `BACKEND_HOST_PORT`
- `FRONTEND_HOST_PORT`

## Unraid notes
- Use Community Applications Docker Compose Manager.
- Place project on cache/appdata share.
- Keep named volumes `postgres_data` and `media_uploads` for persistent DB and media.
- For auto-updates from GitHub, set `GIT_CONTEXT` in your Unraid compose env and redeploy.
- Map ports as needed if conflicts exist.

## Features implemented
- Multi-campaign schema with structured entities, relationships, timelines, events, sessions, tags, and calendars.
- Golarion date fields (`year_ar`, `month_number`, `day`, `display_date`, `sort_key`).
- Visibility layers and Foundry prep fields (`foundry_*`, `sync_status`, `last_synced_at`).
- REST CRUD endpoints for required major models.
- Campaign search endpoint and entity detail aggregation endpoint.
- `/foundry` placeholder route group for future sync.
- Alembic migration + seed data.


## Unraid compose-manager fix for missing `.env.example`
If your stack fails with:
`env file .../.env.example not found`
that came from older compose config using `env_file: .env.example`.

This project now sets backend env vars directly in `docker-compose.yml`, so no `env_file` is required.

Optional: if you want to override defaults, define these variables in Unraid Compose Manager:
- `DATABASE_URL`
- `SECRET_KEY`
- `GIT_CONTEXT`
- `POSTGRES_HOST_PORT`
- `BACKEND_HOST_PORT`
- `FRONTEND_HOST_PORT`
- `VITE_API_BASE_URL`
