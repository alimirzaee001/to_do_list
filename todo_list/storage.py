"""
In-memory storage layer for the ToDo List application.

This module provides data access and storage functionality using in-memory collections.
"""

from typing import List, Optional, Dict
from .models import Project, Task, TaskStatus
from .config import config


class InMemoryStorage:
    """In-memory storage implementation for projects and tasks."""

    def __init__(self):
        """Initialize empty storage."""
        self._projects: Dict[str, Project] = {}
        self._tasks: Dict[str, Task] = {}

    @property
    def projects(self) -> Dict[str, Project]:
        """Get all projects."""
        return self._projects.copy()

    @property
    def tasks(self) -> Dict[str, Task]:
        """Get all tasks."""
        return self._tasks.copy()

    def create_project(self, name: str, description: str) -> Project:
        """
        Create a new project.

        Args:
            name: Project name (must be at least 30 characters)
            description: Project description (must be at least 150 characters)

        Returns:
            The created Project instance

        Raises:
            ValueError: If project name already exists or limits exceeded
        """
        # Check project limit
        if len(self._projects) >= config.max_projects:
            raise ValueError(f"Maximum number of projects ({config.max_projects}) exceeded")

        # Check for duplicate names
        for project in self._projects.values():
            if project.name == name:
                raise ValueError(f"Project with name '{name}' already exists")

        project = Project(name=name, description=description)
        self._projects[project.project_id] = project
        return project

    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID."""
        return self._projects.get(project_id)

    def get_project_by_name(self, name: str) -> Optional[Project]:
        """Get a project by name."""
        for project in self._projects.values():
            if project.name == name:
                return project
        return None

    def update_project(self, project_id: str, name: Optional[str] = None,
                      description: Optional[str] = None) -> Project:
        """
        Update an existing project.

        Args:
            project_id: ID of the project to update
            name: New name (optional)
            description: New description (optional)

        Returns:
            The updated Project instance

        Raises:
            ValueError: If project not found or new name conflicts
        """
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found")

        # Check for name conflicts if name is being changed
        if name is not None and name != project.name:
            existing_project = self.get_project_by_name(name)
            if existing_project and existing_project.project_id != project_id:
                raise ValueError(f"Project with name '{name}' already exists")

        project.update_details(name=name, description=description)
        return project

    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project and all its tasks (cascade delete).

        Args:
            project_id: ID of the project to delete

        Returns:
            True if project was found and deleted, False otherwise
        """
        project = self._projects.pop(project_id, None)
        if not project:
            return False

        # Remove all tasks associated with this project
        tasks_to_remove = [task_id for task_id, task in self._tasks.items()
                          if task.project_id == project_id]
        for task_id in tasks_to_remove:
            del self._tasks[task_id]

        return True

    def list_projects(self) -> List[Project]:
        """Get all projects sorted by creation time."""
        return sorted(self._projects.values(), key=lambda p: p.created_at)

    def create_task(self, project_id: str, title: str, description: str,
                   deadline: Optional[str] = None, status: TaskStatus = TaskStatus.TODO) -> Task:
        """
        Create a new task in a project.

        Args:
            project_id: ID of the project
            title: Task title (must be at least 30 characters)
            description: Task description (must be at least 150 characters)
            deadline: Optional deadline date in YYYY-MM-DD format
            status: Task status (defaults to TODO)

        Returns:
            The created Task instance

        Raises:
            ValueError: If project not found, task limit exceeded, or invalid data
        """
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found")

        # Check task limit for this project
        project_task_count = len([t for t in self._tasks.values() if t.project_id == project_id])
        if project_task_count >= config.max_tasks:
            raise ValueError(f"Maximum number of tasks per project ({config.max_tasks}) exceeded")

        # Parse deadline if provided
        parsed_deadline = None
        if deadline:
            try:
                from datetime import datetime
                parsed_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Deadline must be in YYYY-MM-DD format")

        task = Task(
            title=title,
            description=description,
            status=status,
            deadline=parsed_deadline,
            project_id=project_id
        )

        self._tasks[task.task_id] = task
        project.add_task(task)
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self._tasks.get(task_id)

    def update_task(self, task_id: str, title: Optional[str] = None,
                   description: Optional[str] = None, deadline: Optional[str] = None,
                   status: Optional[TaskStatus] = None) -> Task:
        """
        Update an existing task.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            deadline: New deadline in YYYY-MM-DD format (optional)
            status: New status (optional)

        Returns:
            The updated Task instance

        Raises:
            ValueError: If task not found or invalid data
        """
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID '{task_id}' not found")

        # Parse deadline if provided
        parsed_deadline = None
        if deadline is not None:
            if deadline == "":
                parsed_deadline = None
            else:
                try:
                    from datetime import datetime
                    parsed_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Deadline must be in YYYY-MM-DD format or empty")

        task.update_details(title=title, description=description, deadline=parsed_deadline)

        if status is not None:
            task.update_status(status)

        return task

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was found and deleted, False otherwise
        """
        task = self._tasks.pop(task_id, None)
        if not task:
            return False

        # Remove task from project's task list
        project = self.get_project(task.project_id) if task.project_id else None
        if project:
            project.remove_task(task_id)

        return True

    def get_project_tasks(self, project_id: str) -> List[Task]:
        """
        Get all tasks for a specific project.

        Args:
            project_id: ID of the project

        Returns:
            List of tasks in the project
        """
        project = self.get_project(project_id)
        if not project:
            return []

        return [task for task in self._tasks.values() if task.project_id == project_id]

    def get_tasks_by_status(self, project_id: str, status: TaskStatus) -> List[Task]:
        """
        Get all tasks for a project with a specific status.

        Args:
            project_id: ID of the project
            status: Status to filter by

        Returns:
            List of tasks with the specified status
        """
        return [task for task in self.get_project_tasks(project_id) if task.status == status]


# Global storage instance
storage = InMemoryStorage()
