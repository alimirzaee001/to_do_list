"""
Pydantic schemas for FastAPI endpoints.

Provides request/response models with validation constraints.
"""

from datetime import datetime, date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from .models import TaskStatus


def _word_count(text: str) -> int:
    return len(text.strip().split())


class ProjectBase(BaseModel):
    name: str = Field(..., description="Project name (max 30 words)")
    description: str = Field(..., description="Project description (max 150 words)")

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Project name cannot be empty")
        if _word_count(value) > 30:
            raise ValueError("Project name must be at most 30 words long")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Project description cannot be empty")
        if _word_count(value) > 150:
            raise ValueError("Project description must be at most 150 words long")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Personal productivity",
                "description": "A project to manage personal tasks and goals.",
            }
        }


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, description="New project name (max 30 words)")
    description: Optional[str] = Field(None, description="New project description (max 150 words)")

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if not value.strip():
            raise ValueError("Project name cannot be empty")
        if _word_count(value) > 30:
            raise ValueError("Project name must be at most 30 words long")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if not value.strip():
            raise ValueError("Project description cannot be empty")
        if _word_count(value) > 150:
            raise ValueError("Project description must be at most 150 words long")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated project name",
                "description": "Updated description for the project.",
            }
        }


class ProjectOut(ProjectBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str = Field(..., description="Task title (max 30 words)")
    description: str = Field(..., description="Task description (max 150 words)")
    deadline: Optional[date] = Field(None, description="Deadline in YYYY-MM-DD")
    status: Optional[TaskStatus] = Field(None, description="Task status")

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Task title cannot be empty")
        if _word_count(value) > 30:
            raise ValueError("Task title must be at most 30 words long")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Task description cannot be empty")
        if _word_count(value) > 150:
            raise ValueError("Task description must be at most 150 words long")
        return value

    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, value: Optional[date]) -> Optional[date]:
        if value is not None and value < date.today():
            raise ValueError("Task deadline cannot be in the past")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Write API docs",
                "description": "Draft the API documentation for the ToDo List service.",
                "deadline": "2025-12-31",
                "status": "todo",
            }
        }


class TaskCreate(TaskBase):
    """Schema for creating a task."""


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Task title (max 30 words)")
    description: Optional[str] = Field(None, description="Task description (max 150 words)")
    deadline: Optional[date] = Field(None, description="Deadline in YYYY-MM-DD")
    status: Optional[TaskStatus] = Field(None, description="Task status")

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if not value.strip():
            raise ValueError("Task title cannot be empty")
        if _word_count(value) > 30:
            raise ValueError("Task title must be at most 30 words long")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if not value.strip():
            raise ValueError("Task description cannot be empty")
        if _word_count(value) > 150:
            raise ValueError("Task description must be at most 150 words long")
        return value

    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, value: Optional[date]) -> Optional[date]:
        if value is not None and value < date.today():
            raise ValueError("Task deadline cannot be in the past")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated task title",
                "description": "Adjusted details of the task.",
                "deadline": "2026-01-15",
                "status": "doing",
            }
        }


class TaskOut(TaskBase):
    id: UUID
    project_id: UUID
    status: TaskStatus
    created_at: datetime

    class Config:
        from_attributes = True
