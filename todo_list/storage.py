"""
Database-backed storage layer for the ToDo List application.

This module wraps repository calls with session management to keep the
CLI simple while persisting data to PostgreSQL.
"""

from datetime import datetime
from typing import List, Optional

from .models import Project, Task, TaskStatus
from .repositories import ProjectRepository, TaskRepository
from .db import get_session


class DatabaseStorage:
    """Storage implementation backed by PostgreSQL via SQLAlchemy."""

    def __init__(self):
        self.projects_repo = ProjectRepository()
        self.tasks_repo = TaskRepository()

    def create_project(self, name: str, description: str) -> Project:
        with get_session() as session:
            return self.projects_repo.create_project(session, name, description)

    def get_project(self, project_id) -> Optional[Project]:
        with get_session() as session:
            return self.projects_repo.get_project(session, project_id)

    def get_project_by_name(self, name: str) -> Optional[Project]:
        with get_session() as session:
            return self.projects_repo.get_project_by_name(session, name)

    def update_project(self, project_id, name: Optional[str] = None, description: Optional[str] = None) -> Project:
        with get_session() as session:
            return self.projects_repo.update_project(session, project_id, name=name, description=description)

    def delete_project(self, project_id) -> bool:
        with get_session() as session:
            return self.projects_repo.delete_project(session, project_id)

    def list_projects(self) -> List[Project]:
        with get_session() as session:
            return self.projects_repo.list_projects(session)

    def create_task(
        self,
        project_id,
        title: str,
        description: str,
        deadline: Optional[str] = None,
        status: TaskStatus = TaskStatus.TODO,
    ) -> Task:
        parsed_deadline = self._parse_deadline(deadline) if deadline else None
        with get_session() as session:
            return self.tasks_repo.create_task(
                session,
                project_id=project_id,
                title=title,
                description=description,
                deadline=parsed_deadline,
                status=status,
            )

    def get_task(self, task_id) -> Optional[Task]:
        with get_session() as session:
            return self.tasks_repo.get_task(session, task_id)

    def update_task(
        self,
        task_id,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[str] = None,
        status: Optional[TaskStatus] = None,
    ) -> Task:
        parsed_deadline = self._parse_deadline(deadline) if deadline is not None else None
        with get_session() as session:
            return self.tasks_repo.update_task(
                session,
                task_id=task_id,
                title=title,
                description=description,
                deadline=parsed_deadline,
                status=status,
            )

    def delete_task(self, task_id) -> bool:
        with get_session() as session:
            return self.tasks_repo.delete_task(session, task_id)

    def get_project_tasks(self, project_id) -> List[Task]:
        with get_session() as session:
            return self.tasks_repo.get_project_tasks(session, project_id)

    def get_tasks_by_status(self, project_id, status: TaskStatus) -> List[Task]:
        with get_session() as session:
            return self.tasks_repo.get_tasks_by_status(session, project_id, status)

    def close_overdue_tasks(self) -> int:
        """Close tasks that are past deadline and not done. Returns count updated."""
        with get_session() as session:
            return self.tasks_repo.close_overdue_tasks(session)

    def _parse_deadline(self, deadline: Optional[str]):
        if deadline in (None, ""):
            return None
        try:
            return datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Deadline must be in YYYY-MM-DD format")


# Global storage instance
storage = DatabaseStorage()
