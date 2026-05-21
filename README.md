# Campaign Chronicler

Dockerized tabletop RPG campaign lore tracking app.

## Run
```bash
docker compose up --build
```
Backend API: http://localhost:8000/docs
Frontend: http://localhost:5173

## Unraid notes
- Use Community Applications Docker Compose Manager.
- Place project on cache/appdata share.
- Keep named volumes `postgres_data` and `media_uploads` for persistent DB and media.
- Map ports as needed if conflicts exist.

## Features implemented
- Multi-campaign schema with structured entities, relationships, timelines, events, sessions, tags, and calendars.
- Golarion date fields (`year_ar`, `month_number`, `day`, `display_date`, `sort_key`).
- Visibility layers and Foundry prep fields (`foundry_*`, `sync_status`, `last_synced_at`).
- REST CRUD endpoints for required major models.
- Campaign search endpoint and entity detail aggregation endpoint.
- `/foundry` placeholder route group for future sync.
- Alembic migration + seed data.
