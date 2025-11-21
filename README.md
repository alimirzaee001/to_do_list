# ToDo List Application (Phase 2)

A layered ToDo List application using Python, PostgreSQL, SQLAlchemy ORM, and Alembic migrations. Phase 2 moves persistence from in-memory to a relational database, adds a repository layer, and includes a scheduled command to close overdue tasks.

## Features
- Project and task management with validation (word limits, deadlines not in the past).
- Task statuses: `todo`, `doing`, `done`.
- PostgreSQL persistence with cascaded deletes and unique constraints.
- Repository pattern over SQLAlchemy 2.0.
- Alembic migrations for schema management.
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

5) Launch the CLI:
```bash
poetry run todo-cli
```

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
  cli.py             # CLI entrypoint
  config.py          # Environment/config loader
  db.py              # SQLAlchemy engine/session setup
  models.py          # ORM models (Project, Task, TaskStatus)
  repositories.py    # Repository layer
  scheduler.py       # Overdue task closer (once or scheduled)
  storage.py         # Database-backed storage facade
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
