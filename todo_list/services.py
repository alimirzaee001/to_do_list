"""
Service layer wrapping repositories.

Keeps controller logic thin and separates business rules.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from .models import Project, Task, TaskStatus
from .repositories import ProjectRepository, TaskRepository


class ProjectService:
    """Service for project operations."""

    def __init__(self, session: Session):
        self.session = session
        self.repo = ProjectRepository()

    def create_project(self, name: str, description: str) -> Project:
        project = self.repo.create_project(self.session, name, description)
        self.session.commit()
        self.session.refresh(project)
        return project

    def get_project(self, project_id: UUID) -> Optional[Project]:
        return self.repo.get_project(self.session, project_id)

    def list_projects(self) -> List[Project]:
        return self.repo.list_projects(self.session)

    def update_project(self, project_id: UUID, name: Optional[str] = None, description: Optional[str] = None) -> Project:
        project = self.repo.update_project(self.session, project_id, name=name, description=description)
        self.session.commit()
        self.session.refresh(project)
        return project

    def delete_project(self, project_id: UUID) -> bool:
        deleted = self.repo.delete_project(self.session, project_id)
        self.session.commit()
        return deleted


class TaskService:
    """Service for task operations."""

    def __init__(self, session: Session):
        self.session = session
        self.repo = TaskRepository()

    def create_task(
        self,
        project_id: UUID,
        title: str,
        description: str,
        deadline=None,
        status: TaskStatus = TaskStatus.TODO,
    ) -> Task:
        task = self.repo.create_task(
            self.session,
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
            status=status,
        )
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_task(self, task_id: UUID) -> Optional[Task]:
        return self.repo.get_task(self.session, task_id)

    def list_tasks_for_project(self, project_id: UUID) -> List[Task]:
        return self.repo.get_project_tasks(self.session, project_id)

    def update_task(
        self,
        task_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline=None,
        status: Optional[TaskStatus] = None,
    ) -> Task:
        task = self.repo.update_task(
            self.session,
            task_id=task_id,
            title=title,
            description=description,
            deadline=deadline,
            status=status,
        )
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: UUID) -> bool:
        deleted = self.repo.delete_task(self.session, task_id)
        self.session.commit()
        return deleted
