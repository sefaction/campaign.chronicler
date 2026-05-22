# Campaign Chronicler

Dockerized tabletop RPG campaign lore tracking app.

## Source of truth deployment
Use `docker-compose.portainer.yml` as the canonical compose file.

### Required env
Set this in Portainer/Unraid stack env:
- `GIT_CONTEXT=https://github.com/sefaction/campaign.chronicler.git#main`

### Default ports
- Frontend: `15173`
- Backend API: `18000`
- Postgres: `15432`

### Deploy
1. Open Portainer/Unraid stack editor.
2. Use `docker-compose.portainer.yml` content.
3. Set `GIT_CONTEXT` env var.
4. Deploy/redeploy.

### Backend access checks
- API docs: `http://<server-ip>:18000/docs`
- Health: `http://<server-ip>:18000/health`

If backend still refuses connection, check container logs for `backend` service first (startup migration/seed failures will stop the API process).


## Persistent data paths (Unraid)
Configured defaults now map directly to your requested appdata paths:
- Backend data: `/mnt/user/appdata/campaign-chronicler/backend`
- Backend uploads: `/mnt/user/appdata/campaign-chronicler/backend/uploads`
- Postgres data: `/mnt/user/appdata/campaign-chronicler/postgres`

These are controlled by:
- `BACKEND_DATA_PATH`
- `BACKEND_UPLOADS_PATH`
- `POSTGRES_DATA_PATH`


## Backend URL requires port
The backend is published on host port `18000` by default.

Use:
- `http://192.168.1.2:18000/health`
- `http://192.168.1.2:18000/docs`

`http://192.168.1.2` (without `:18000`) will fail unless another service is bound to port 80.


### API endpoints
- API root: `http://<server-ip>:18000/`
- Health: `http://<server-ip>:18000/health`
- Swagger docs: `http://<server-ip>:18000/docs`


### Seed login
Use the seeded credentials to sign in from the frontend login page:
- Username: `gm`
- Password: `gm`

Then navigate to `/campaigns`, `/entities`, `/events`, `/sessions`, and related create pages to begin entering data.


### If frontend says "Cannot reach backend" but backend is up
This can be a browser CORS block (shows as fetch failure).
Set `CORS_ORIGINS` to include your frontend URL, e.g.
`http://192.168.1.2:15173`.
