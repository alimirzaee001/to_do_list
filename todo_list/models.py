"""
Core models for the ToDo List application.

This module contains the main data models: Task, Project, and related enums.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import List, Optional
import uuid


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""

    TODO = "todo"
    DOING = "doing"
    DONE = "done"


@dataclass
class Task:
    """Represents a task in the ToDo List system."""

    title: str
    description: str
    status: TaskStatus = TaskStatus.TODO
    deadline: Optional[date] = None
    project_id: Optional[str] = None
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate task data after initialization."""
        if not self.title or len(self.title) < 30:
            raise ValueError("Task title must be at least 30 characters long")

        if not self.description or len(self.description) < 150:
            raise ValueError("Task description must be at least 150 characters long")

        if self.deadline and self.deadline < date.today():
            raise ValueError("Task deadline cannot be in the past")

    def update_status(self, new_status: TaskStatus) -> None:
        """Update the task status."""
        self.status = new_status

    def update_details(self, title: Optional[str] = None,
                      description: Optional[str] = None,
                      deadline: Optional[date] = None) -> None:
        """Update task details with validation."""
        if title is not None:
            if not title or len(title) < 30:
                raise ValueError("Task title must be at least 30 characters long")
            self.title = title

        if description is not None:
            if not description or len(description) < 150:
                raise ValueError("Task description must be at least 150 characters long")
            self.description = description

        if deadline is not None:
            if deadline < date.today():
                raise ValueError("Task deadline cannot be in the past")
            self.deadline = deadline


@dataclass
class Project:
    """Represents a project in the ToDo List system."""

    name: str
    description: str
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    tasks: List[Task] = field(default_factory=list)

    def __post_init__(self):
        """Validate project data after initialization."""
        if not self.name or len(self.name) < 30:
            raise ValueError("Project name must be at least 30 characters long")

        if not self.description or len(self.description) < 150:
            raise ValueError("Project description must be at least 150 characters long")

    def add_task(self, task: Task) -> None:
        """Add a task to the project."""
        task.project_id = self.project_id
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        """Remove a task from the project by ID. Returns True if found and removed."""
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                del self.tasks[i]
                return True
        return False

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID from the project."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def update_details(self, name: Optional[str] = None,
                      description: Optional[str] = None) -> None:
        """Update project details with validation."""
        if name is not None:
            if not name or len(name) < 30:
                raise ValueError("Project name must be at least 30 characters long")
            self.name = name

        if description is not None:
            if not description or len(description) < 150:
                raise ValueError("Project description must be at least 150 characters long")
            self.description = description
