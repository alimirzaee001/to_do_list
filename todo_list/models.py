"""
ORM models for the ToDo List application using SQLAlchemy.

Includes Project and Task entities with basic validation helpers.
"""

from datetime import datetime, date
from enum import Enum
import uuid
from typing import Optional
from sqlalchemy import (
    Column,
    String,
    Date,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .db import Base


class TaskStatus(str, Enum):
    """Enumeration of possible task statuses."""

    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class Project(Base):
    """Represents a project in the ToDo List system."""

    __tablename__ = "projects"
    __table_args__ = (UniqueConstraint("name", name="uq_projects_name"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def validate(self) -> None:
        """Validate project data."""
        if not self.name or self._count_words(self.name) > 30:
            raise ValueError("Project name must be at most 30 words long")
        if not self.description or self._count_words(self.description) > 150:
            raise ValueError("Project description must be at most 150 words long")

    def update_details(self, name: Optional[str] = None, description: Optional[str] = None) -> None:
        """Update project details with validation."""
        if name is not None:
            if not name or self._count_words(name) > 30:
                raise ValueError("Project name must be at most 30 words long")
            self.name = name

        if description is not None:
            if not description or self._count_words(description) > 150:
                raise ValueError("Project description must be at most 150 words long")
            self.description = description

    def _count_words(self, text: str) -> int:
        return len(text.strip().split())


class Task(Base):
    """Represents a task in the ToDo List system."""

    __tablename__ = "tasks"
    __table_args__ = (
        UniqueConstraint("title", "project_id", name="uq_task_title_per_project"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, name="task_status"), default=TaskStatus.TODO, nullable=False
    )
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    project: Mapped[Project] = relationship("Project", back_populates="tasks")

    def validate(self) -> None:
        """Validate task data."""
        if not self.title or self._count_words(self.title) > 30:
            raise ValueError("Task title must be at most 30 words long")
        if not self.description or self._count_words(self.description) > 150:
            raise ValueError("Task description must be at most 150 words long")
        if self.deadline and self.deadline < date.today():
            raise ValueError("Task deadline cannot be in the past")

    def update_details(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[date] = None,
    ) -> None:
        """Update task details with validation."""
        if title is not None:
            if not title or self._count_words(title) > 30:
                raise ValueError("Task title must be at most 30 words long")
            self.title = title

        if description is not None:
            if not description or self._count_words(description) > 150:
                raise ValueError("Task description must be at most 150 words long")
            self.description = description

        if deadline is not None:
            if deadline < date.today():
                raise ValueError("Task deadline cannot be in the past")
            self.deadline = deadline

    def update_status(self, new_status: TaskStatus) -> None:
        """Update the task status."""
        self.status = new_status

    def _count_words(self, text: str) -> int:
        return len(text.strip().split())
