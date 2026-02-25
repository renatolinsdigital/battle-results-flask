# Docker Guide

This document covers everything about running Battle Results Flask inside Docker: how the project is containerized, all available commands, data persistence, environment variables, and troubleshooting.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Files](#project-files)
   - [Dockerfile](#dockerfile)
   - [docker-compose.yml](#docker-composeyml)
4. [Environment Variables](#environment-variables)
5. [Quick Start (Docker Compose)](#quick-start-docker-compose)
6. [Common Commands](#common-commands)
7. [Running Without Compose](#running-without-compose)
8. [Data Persistence](#data-persistence)
9. [Production Considerations](#production-considerations)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The application ships with a `Dockerfile` and a `docker-compose.yml` so it can be built and run without any local Python installation. The container:

- Is based on `python:3.12-slim`.
- Installs dependencies via Pipenv at build time (no Pipenv needed on the host).
- Runs as a **non-root user** (`appuser`) for security.
- Exposes port **8080**.
- Mounts the `./data` directory from the host so the SQLite database survives container restarts and rebuilds.

---

## Prerequisites

| Tool | Minimum version | Notes |
|---|---|---|
| Docker | 24.0+ | [Install Docker](https://docs.docker.com/get-docker/) |
| Docker Compose | v2 (plugin) | Bundled with Docker Desktop; use `docker compose` (no hyphen) |

Verify your installation:

```bash
docker --version
docker compose version
```

---

## Project Files

### Dockerfile

```
battle-results-flask/
└── Dockerfile
```

The Dockerfile uses a multi-step approach within a single stage:

1. **Base image** – `python:3.13-slim` keeps the image small while providing a compatible Python version.
2. **System dependencies** – `gcc` and `libffi-dev` are installed and then the apt cache is cleaned to minimize the image layer size.
3. **Pipenv install** – `pipenv install --system --deploy` installs all locked dependencies directly into the system Python (no virtualenv inside the container).
4. **Application copy** – The full project is copied after dependencies so that code changes don't invalidate the dependency cache layer.
5. **Non-root user** – A passwordless `appuser` is created and ownership of `/app` is transferred before launching the process.
6. **Startup** – `CMD ["python", "app.py"]` launches the Flask development server (suitable for low-traffic / internal use; see [Production Considerations](#production-considerations) for Gunicorn).

Key `ENV` values set in the image:

| Variable | Value in image |
|---|---|
| `FLASK_APP` | `app.py` |
| `FLASK_RUN_HOST` | `0.0.0.0` |
| `FLASK_RUN_PORT` | `8080` |
| `FLASK_DEBUG` | `False` |
| `PYTHONDONTWRITEBYTECODE` | `1` |
| `PYTHONUNBUFFERED` | `1` |

### docker-compose.yml

```
battle-results-flask/
└── docker-compose.yml
```

The Compose file defines a single service called `web`:

| Field | Value | Purpose |
|---|---|---|
| `build: .` | Current directory | Builds the image from the local Dockerfile |
| `ports: 8080:8080` | host:container | Maps container port 8080 to localhost:8080 |
| `volumes: ./data:/app/data` | host path : container path | Persists the SQLite database on the host |
| `environment` | see below | Passes runtime config as env vars |
| `restart: unless-stopped` | – | Automatically restarts the container on failure or system reboot (unless manually stopped) |

---

## Environment Variables

All runtime configuration is passed via environment variables. `docker-compose.yml` forwards them from the host shell or a `.env` file in the project root.

| Variable | Required | Default (in image) | Description |
|---|---|---|---|
| `FLASK_SECRET_KEY` | **Yes** | none – auto-generated at runtime | Used to sign sessions. Must be set to a stable secret in production, otherwise sessions are invalidated on every restart. |
| `FLASK_DEBUG` | No | `False` | Set to `True` for debug mode (never use in production). |
| `FLASK_RUN_HOST` | No | `0.0.0.0` | Host the server listens on. |
| `FLASK_RUN_PORT` | No | `8080` | Port the server listens on. |
| `LOCAL_DATABASE_PATH` | No | `data` | Subdirectory (relative to `/app`) where the SQLite file is stored. |

### Setting the secret key

**Option A – export in the shell (recommended for local use)**

```bash
# Linux / macOS
export FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Windows PowerShell
$env:FLASK_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"

# Windows CMD
for /f "delims=" %i in ('python -c "import secrets; print(secrets.token_hex(32))"') do set FLASK_SECRET_KEY=%i
```

**Option B – .env file (recommended for persistent local use)**

Create a `.env` file in the project root (it is automatically read by `docker compose`):

```dotenv
FLASK_SECRET_KEY=replace_this_with_a_long_random_string
FLASK_DEBUG=False
LOCAL_DATABASE_PATH=data
```

> **Never commit `.env` to version control.** A `.env.example` template should be committed instead.

---

## Quick Start (Docker Compose)

```bash
# 1. Set the secret key (or create a .env file — see above)
export FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# 2. Build the image and start the container in the foreground
docker compose up --build
```

The application will be available at:

- Web UI: http://localhost:8080
- API docs: http://localhost:8080/api/docs

To stop it press `Ctrl+C`.

---

## Common Commands

### Build

```bash
# Build (or rebuild) the image without starting
docker compose build

# Force a full rebuild (no cache)
docker compose build --no-cache
```

### Start / Stop

```bash
# Start in the foreground (logs visible in terminal)
docker compose up

# Start in the background (detached)
docker compose up -d

# Stop the running container (keeps the container)
docker compose stop

# Stop and remove the container (image is kept)
docker compose down

# Stop, remove the container AND remove the named volumes
docker compose down -v
```

### Rebuild and restart in one step

```bash
docker compose up --build -d
```

### Logs

```bash
# Follow logs of the running container
docker compose logs -f

# Show last 50 lines
docker compose logs --tail=50
```

### Open a shell inside the running container

```bash
docker compose exec web sh
```

### Check container status

```bash
docker compose ps
```

### Remove the built image

```bash
docker rmi battle-results-flask-web
```

---

## Running Without Compose

If you want to use plain `docker` commands instead of Compose:

```bash
# 1. Build the image
docker build -t battle-results-flask .

# 2. Run the container
#    -p  maps host port 8080 to container port 8080
#    -v  mounts the local ./data directory for persistence
#    -e  passes the secret key
#    -d  runs in the background
docker run -d \
  -p 8080:8080 \
  -v "$(pwd)/data:/app/data" \
  -e FLASK_SECRET_KEY=your_secret_key_here \
  -e LOCAL_DATABASE_PATH=data \
  --name battle-results \
  battle-results-flask

# 3. View logs
docker logs -f battle-results

# 4. Open a shell
docker exec -it battle-results sh

# 5. Stop and remove
docker stop battle-results
docker rm battle-results
```

---

## Data Persistence

The SQLite database file is stored inside the container at `/app/data/`. The Compose file mounts `./data` (on the host) to `/app/data` (in the container):

```
Host                  Container
./data/  ←——volume——→  /app/data/
```

This means:

- The database survives `docker compose down` and `docker compose up` cycles.
- Rebuilding the image (`--build`) does **not** wipe the database.
- Only `docker compose down -v` (explicit volume removal) would remove it.

If you want to **reset** the database, delete the file from the host:

```bash
# Linux / macOS
rm data/battle_results.db

# Windows PowerShell
Remove-Item data\battle_results.db
```

---

## Production Considerations

The default `CMD` uses Flask's built-in development server, which is single-threaded and not suitable for real production traffic. For production:

### 1. Use Gunicorn

Add `gunicorn` to `Pipfile`:

```toml
[packages]
gunicorn = "*"
```

Then change the `CMD` in the Dockerfile:

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "app:app"]
```

### 2. Use environment-specific Compose files

```bash
# Development
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 3. HTTPS / reverse proxy

Place an Nginx or Traefik reverse proxy in front of the container to handle TLS termination. The Flask app itself should remain on HTTP internally.

### 4. Secrets management

Avoid plain-text secrets in `.env` for production. Use Docker secrets, a secrets manager (Vault, AWS Secrets Manager), or your orchestration platform's secret store.

---

## Troubleshooting

### Port already in use

```
Error: Bind for 0.0.0.0:8080 failed: port is already allocated
```

Something else is using port 8080. Either stop that process or change the host port in `docker-compose.yml`:

```yaml
ports:
  - "9090:8080"  # map host 9090 → container 8080
```

### Container exits immediately

Check the logs:

```bash
docker compose logs web
```

The most common causes are:
- `FLASK_SECRET_KEY` not set (the app still starts but warns; this alone does not cause an exit).
- A Python syntax error or import error in the application code.
- The `data/` directory is not writable by `appuser` (check host directory permissions).

### Database not persisting

Make sure `./data` exists on the host before starting (Docker creates it automatically, but as `root`, which can cause permission issues on some systems):

```bash
mkdir -p data
```

Then restart:

```bash
docker compose down && docker compose up -d
```

### Rebuilding after dependency changes

If you add or remove packages in `Pipfile`, regenerate `Pipfile.lock` locally first:

```bash
pipenv lock
```

Then rebuild the Docker image:

```bash
docker compose build --no-cache
```
