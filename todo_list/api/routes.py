"""API routes for the ToDo List application."""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from ..models import TaskStatus
from ..services import ProjectService, TaskService
from ..schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectOut,
    TaskCreate,
    TaskUpdate,
    TaskOut,
)
from .deps import get_project_service, get_task_service


router = APIRouter(prefix="/api/v1", tags=["ToDo"])


@router.post(
    "/projects",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
)
def create_project(payload: ProjectCreate, service: ProjectService = Depends(get_project_service)):
    try:
        return service.create_project(name=payload.name, description=payload.description)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/projects", response_model=List[ProjectOut], summary="List all projects")
def list_projects(service: ProjectService = Depends(get_project_service)):
    return service.list_projects()


@router.get("/projects/{project_id}", response_model=ProjectOut, summary="Get a project by ID")
def get_project(project_id: UUID, service: ProjectService = Depends(get_project_service)):
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.put("/projects/{project_id}", response_model=ProjectOut, summary="Update a project")
def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
):
    try:
        return service.update_project(project_id, name=payload.name, description=payload.description)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found") from exc


@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
)
def delete_project(project_id: UUID, service: ProjectService = Depends(get_project_service)):
    deleted = service.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task in a project",
)
def create_task(
    project_id: UUID,
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    try:
        status_value = payload.status if payload.status is not None else TaskStatus.TODO
        return service.create_task(
            project_id=project_id,
            title=payload.title,
            description=payload.description,
            deadline=payload.deadline,
            status=status_value,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found") from exc


@router.get(
    "/projects/{project_id}/tasks",
    response_model=List[TaskOut],
    summary="List tasks for a project",
)
def list_project_tasks(project_id: UUID, service: TaskService = Depends(get_task_service)):
    return service.list_tasks_for_project(project_id)


@router.get("/tasks/{task_id}", response_model=TaskOut, summary="Get a task by ID")
def get_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskOut, summary="Update a task")
def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    try:
        return service.update_task(
            task_id=task_id,
            title=payload.title,
            description=payload.description,
            deadline=payload.deadline,
            status=payload.status,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found") from exc


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
