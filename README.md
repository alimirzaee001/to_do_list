# ToDo List Application (Phase 3)

A layered ToDo List application using Python, PostgreSQL, SQLAlchemy ORM, Alembic migrations, and a FastAPI web service. Phase 3 exposes the domain logic over RESTful endpoints; the legacy CLI is now deprecated.

## Features
- Project and task management with validation (word limits, deadlines not in the past).
- Task statuses: `todo`, `doing`, `done`.
- PostgreSQL persistence with cascaded deletes and unique constraints.
- Repository pattern over SQLAlchemy 2.0.
- Alembic migrations for schema management.
- FastAPI REST API with OpenAPI/Swagger docs.
- Scheduled job to close overdue tasks automatically.

## Requirements
- Python 3.8+
- Docker Desktop (for PostgreSQL)
- `poetry` (recommended) or another way to install dependencies from `pyproject.toml`

## Quickstart
1) Clone and configure environment:
```bash
cp .env.example .env
# adjust DB credentials/ports if needed
```

2) Start PostgreSQL via Docker:
```bash
docker-compose up -d db
```

3) Install dependencies (with Poetry):
```bash
poetry install
```

4) Run migrations:
```bash
poetry run alembic upgrade head
```

5) Run the API (developer mode with reload):
```bash
poetry run todo-api
# or
poetry run uvicorn todo_list.api_app:app --reload
```

6) Open docs:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

> Legacy CLI: The CLI is deprecated in this phase; prefer the HTTP API for all operations.

## Scheduled overdue task closer
- Run once (ad-hoc): `poetry run todo-close-overdue`
- Run continuously with an interval (default 15 minutes, set via `CLOSE_OVERDUE_INTERVAL_MINUTES`):  
  `poetry run todo-scheduler`

## Configuration (`.env`)
- `MAX_NUMBER_OF_PROJECTS` (default 10)
- `MAX_NUMBER_OF_TASKS` (default 100)
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DATABASE_URL`
- `CLOSE_OVERDUE_INTERVAL_MINUTES` (default 15)

## Project structure
```
todo_list/
  api/               # FastAPI routers and dependencies
  api_app.py         # FastAPI application factory
  cli.py             # Legacy CLI (deprecated)
  config.py          # Environment/config loader
  db.py              # SQLAlchemy engine/session setup
  models.py          # ORM models (Project, Task, TaskStatus)
  repositories.py    # Repository layer
  schemas.py         # Pydantic schemas for API I/O
  scheduler.py       # Overdue task closer (once or scheduled)
  services.py        # Service layer over repositories
  storage.py         # Database-backed storage facade (CLI/scheduler)
  server.py          # Convenience runner for the API (uvicorn)
alembic/             # Migration environment
alembic.ini          # Alembic configuration
docker-compose.yml   # PostgreSQL in Docker
pyproject.toml       # Dependencies and scripts
```

## Notes
- Deleting a project cascades to its tasks.
- Task titles are unique per project.
- Deadlines must not be in the past.
- When the scheduler runs, any task with a deadline earlier than today and status not `done` is marked `done`.
