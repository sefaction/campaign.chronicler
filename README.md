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


## Important: correct GitHub repo slug
If Unraid build fails while fetching Git context, verify your slug uses a hyphen, not a dot.

Use:
- `https://github.com/sefaction/campaign-chronicler.git#main`

Not:
- `https://github.com/sefaction/campaign.chronicler.git#main`


## Portainer default compose (recommended first launch sanity check)
Yes — this is the simplest path to get a first successful launch.

Use `docker-compose.portainer.yml` in Portainer with repository checkout enabled (or a local bind that includes this repo).

Why this helps:
- It builds from local repo folders (`./backend`, `./frontend`) instead of remote Git context.
- It avoids GHCR auth and remote BuildKit Git cloning variables.
- It keeps the same non-conflicting host ports:
  - Postgres `15432`
  - Backend `18000`
  - Frontend `15173`

Steps in Portainer:
1. Stacks -> Add stack.
2. Repository method: point to this repo.
3. Compose path: `docker-compose.portainer.yml`.
4. Deploy the stack.


## Portainer fix for `path "/data/compose/.../backend" not found`
That error means Portainer is trying to build from a local relative path (`./backend`) in a stack folder that does not contain this repo tree.

`docker-compose.portainer.yml` now uses GitHub build context per service:
- `context: ${GIT_CONTEXT:-https://github.com/sefaction/campaign-chronicler.git#main}`
- `dockerfile: backend/Dockerfile` and `frontend/Dockerfile`

So Portainer no longer requires `/data/compose/<id>/backend` to exist.

If you still get a fetch error, set `GIT_CONTEXT` explicitly in the stack env to your exact repo URL/branch.


## Portainer fix for `could not read Username for 'https://github.com'`
This specific error usually means the `GIT_CONTEXT` repo URL is not the exact repo slug, so GitHub prompts for credentials and BuildKit cannot answer prompts.

For this project, set `GIT_CONTEXT` explicitly in Portainer stack env to:
- `https://github.com/sefaction/campaign.chronicler.git#main`

Do **not** rely on guessed defaults across different compose files.

Quick verification from your Portainer host shell:
- `git ls-remote https://github.com/sefaction/campaign.chronicler.git`

If that command fails, the URL is wrong for your actual repo slug.
