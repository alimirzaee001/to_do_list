"""
Repository layer for database access.

Separates persistence concerns from CLI/business logic.
"""

from datetime import date
from typing import List, Optional
from sqlalchemy import select, func, and_, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .config import config
from .models import Project, Task, TaskStatus


class ProjectRepository:
    """Repository for project entity operations."""

    def create_project(self, session: Session, name: str, description: str) -> Project:
        # Enforce max projects limit
        project_count = session.scalar(select(func.count()).select_from(Project))
        if project_count >= config.max_projects:
            raise ValueError(f"Maximum number of projects ({config.max_projects}) exceeded")

        # Check duplicate name early for better UX
        existing = session.scalar(select(Project).where(Project.name == name))
        if existing:
            raise ValueError(f"Project with name '{name}' already exists")

        project = Project(name=name, description=description)
        project.validate()
        session.add(project)
        session.flush()
        return project

    def get_project(self, session: Session, project_id) -> Optional[Project]:
        return session.get(Project, project_id)

    def get_project_by_name(self, session: Session, name: str) -> Optional[Project]:
        return session.scalar(select(Project).where(Project.name == name))

    def update_project(
        self,
        session: Session,
        project_id,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Project:
        project = self.get_project(session, project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found")

        if name is not None and name != project.name:
            existing = self.get_project_by_name(session, name)
            if existing and existing.id != project_id:
                raise ValueError(f"Project with name '{name}' already exists")

        project.update_details(name=name, description=description)
        try:
            session.flush()
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("Project update failed due to integrity constraint") from exc
        return project

    def delete_project(self, session: Session, project_id) -> bool:
        project = self.get_project(session, project_id)
        if not project:
            return False
        session.delete(project)
        session.flush()
        return True

    def list_projects(self, session: Session) -> List[Project]:
        return list(session.scalars(select(Project).order_by(Project.created_at)).all())


class TaskRepository:
    """Repository for task entity operations."""

    def create_task(
        self,
        session: Session,
        project_id,
        title: str,
        description: str,
        deadline: Optional[date] = None,
        status: TaskStatus = TaskStatus.TODO,
    ) -> Task:
        project = session.get(Project, project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found")

        task_count = session.scalar(
            select(func.count()).select_from(Task).where(Task.project_id == project_id)
        )
        if task_count >= config.max_tasks:
            raise ValueError(f"Maximum number of tasks per project ({config.max_tasks}) exceeded")

        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
            status=status,
        )
        task.validate()
        session.add(task)
        session.flush()
        return task

    def get_task(self, session: Session, task_id) -> Optional[Task]:
        return session.get(Task, task_id)

    def update_task(
        self,
        session: Session,
        task_id,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[date] = None,
        status: Optional[TaskStatus] = None,
    ) -> Task:
        task = self.get_task(session, task_id)
        if not task:
            raise ValueError(f"Task with ID '{task_id}' not found")

        task.update_details(title=title, description=description, deadline=deadline)
        if status is not None:
            task.update_status(status)

        try:
            session.flush()
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("Task update failed due to integrity constraint") from exc

        return task

    def delete_task(self, session: Session, task_id) -> bool:
        task = self.get_task(session, task_id)
        if not task:
            return False
        session.delete(task)
        session.flush()
        return True

    def get_project_tasks(self, session: Session, project_id) -> List[Task]:
        return list(
            session.scalars(
                select(Task).where(Task.project_id == project_id).order_by(Task.created_at)
            ).all()
        )

    def get_tasks_by_status(self, session: Session, project_id, status: TaskStatus) -> List[Task]:
        return list(
            session.scalars(
                select(Task).where(Task.project_id == project_id, Task.status == status)
            ).all()
        )

    def close_overdue_tasks(self, session: Session) -> int:
        """Set status to DONE for tasks past deadline that are not done."""
        today = date.today()
        stmt = (
            update(Task)
            .where(Task.deadline.isnot(None))
            .where(Task.deadline < today)
            .where(Task.status != TaskStatus.DONE)
            .values(status=TaskStatus.DONE)
            .execution_options(synchronize_session="fetch")
        )
        result = session.execute(stmt)
        session.flush()
        return result.rowcount or 0
