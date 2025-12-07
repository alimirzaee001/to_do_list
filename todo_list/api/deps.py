"""FastAPI dependencies for database session and services."""

from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..services import ProjectService, TaskService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    return ProjectService(db)


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)
