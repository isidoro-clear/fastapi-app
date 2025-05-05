from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskOut, TaskCreateInternal, TaskUpdate
from app.models.task import Task
from app.core.auth import get_current_active_user
from app.models.user import User
from app.db import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskOut])
def read_tasks(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    tasks = current_user.tasks
    return tasks

@router.get("/{task_id}", response_model=TaskOut)
def read_task(
    task_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    task = Task.find_by(db, id=task_id, user_id=current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=TaskOut)
def create_task(
    task: TaskCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    task_with_user = TaskCreateInternal(**task.dict(), user_id=current_user.id)
    return Task.create(db, task_with_user)

@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: str,
    task: TaskUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    updated_task = Task.update(db, task_id, current_user.id, task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}", response_model=TaskOut)
def delete_task(
    task_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    deleted_task = Task.delete(db, task_id, current_user.id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task