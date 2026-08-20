# Inventory App

A Flask-based microservice that manages a simple catalogue of movies. The service exposes a RESTful API for creating, listing, updating and deleting movie records and provides a health endpoint that verifies the database connection.

This project is part of the Code-Keeper microservices platform and is intended to run as an independent containerized service backed by a PostgreSQL database.

## Overview

- Service exposes movie management endpoints under /api/movies
- Uses SQLAlchemy + Flask-SQLAlchemy with PostgreSQL as the persistent store
- Health endpoint at /health reports database connectivity
- Designed to be containerized and deployed to AWS ECS via the included CI pipeline

## Features

- Full CRUD for Movie resources
- Simple search by title (query param `title`)
- Database connection retry on startup (useful for container orchestration)
- Health check endpoint that verifies DB readiness
- Container image with a built-in healthcheck

## Project Structure

```text
inventory-app/
├── app/
│   ├── __init__.py       # app factory, DB init and retry logic
│   ├── config.py         # configuration and DB URI construction
│   ├── models.py         # SQLAlchemy models
│   └── routes/           # blueprints for movies and health
├── tests/                # unit and integration tests
├── Dockerfile
├── server.py             # WSGI entrypoint (waitress)
├── requirements.txt
├── requirements-dev.txt
├── .gitlab-ci.yml
└── README.md
```

## Prerequisites

- Python 3.12+
- pip
- PostgreSQL (for local development or tests that require DB)
- Docker (optional, recommended for running integration tests and local containers)

## Configuration

The application relies on environment variables. Example `.env`:

```env
INVENTORY_APP_PORT=8000
INVENTORY_DB_USER=inventory
INVENTORY_DB_PASS=inventory_pass
INVENTORY_DB_NAME=inventory_db
INVENTORY_DB_HOST=postgres
```

Required variables:

- `INVENTORY_APP_PORT` — port the app listens on (e.g. 8000)
- `INVENTORY_DB_USER` — Postgres username
- `INVENTORY_DB_PASS` — Postgres password
- `INVENTORY_DB_NAME` — Postgres database name
- `INVENTORY_DB_HOST` — Postgres host (container name or hostname)

The application constructs SQLALCHEMY_DATABASE_URI as:

postgresql://<INVENTORY_DB_USER>:<INVENTORY_DB_PASS>@<INVENTORY_DB_HOST>:5432/<INVENTORY_DB_NAME>

## Local development

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Start a local Postgres instance (example with docker):

```bash
docker run --rm -e POSTGRES_USER=inventory -e POSTGRES_PASSWORD=inventory_pass -e POSTGRES_DB=inventory_db -p 5432:5432 --name inventory-postgres postgres:15
```

Start the app:

```bash
export INVENTORY_APP_PORT=8000
export INVENTORY_DB_USER=inventory
export INVENTORY_DB_PASS=inventory_pass
export INVENTORY_DB_NAME=inventory_db
export INVENTORY_DB_HOST=127.0.0.1
python server.py
```

The app uses a small retry loop during startup to wait for the database; this makes it resilient to ordering issues in orchestration.

## Docker

Build the image:

```bash
docker build -t inventory-app .
```

Run the container (example linking to a Postgres container on the default bridge network):

```bash
docker run --rm -p 8000:8000 \
  -e INVENTORY_APP_PORT=8000 \
  -e INVENTORY_DB_USER=inventory \
  -e INVENTORY_DB_PASS=inventory_pass \
  -e INVENTORY_DB_NAME=inventory_db \
  -e INVENTORY_DB_HOST=postgres \
  --name inventory-app inventory-app
```

The Dockerfile includes a HEALTHCHECK that calls `/health` to verify database readiness.

## API Endpoints

### Health

GET /health/

Response examples:

- Healthy:

```json
{ "status": "ok", "services": { "database": "up" } }
```

- Unhealthy:

```json
{ "status": "error", "services": { "database": "down" }, "error": "..." }
```

### Movies

- GET /api/movies/ — list all movies
  - Optional query param: `title` to search by title (case-insensitive substring)
- POST /api/movies/ — create a new movie
  - JSON body: { "title": "...", "description": "..." }
  - Returns 201 and the created object
- DELETE /api/movies/ — delete all movies (returns 204)
- GET /api/movies/<id> — get a movie by id
- PUT /api/movies/<id> — update a movie by id
  - JSON body must include a non-empty `title`
- DELETE /api/movies/<id> — delete a movie by id (returns 204)

Validation:
- POST/PUT require a `title` field and return 400 on missing/invalid titles

## Testing

Unit tests:

```bash
pytest -v tests/unit --cov=app --cov-report=term
```

Integration tests (uses docker-compose provided in the tests folder):

```bash
docker compose -f tests/integration/docker-compose.yml up -d --wait
pytest -v tests/integration
docker compose -f tests/integration/docker-compose.yml down --rmi local
```

## CI/CD

A GitLab CI pipeline is included in `.gitlab-ci.yml`. It runs the following stages for protected branches:

- build — dependency install and static checks
- test — unit and integration tests
- scan — SonarQube and Trivy scans
- package — Docker image build and push
- deploy — ECS task update (manual protected job)

## Notes

- The app expects a PostgreSQL database; ensure credentials and host are properly configured when deploying.
- The startup retry loop helps when the DB is not immediately available (e.g., on first deployment).
