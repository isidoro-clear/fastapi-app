from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskOut, TaskCreateInternal
from app.models.task import Task
from app.core.auth import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskOut])
def read_tasks(current_user: Annotated[User, Depends(get_current_active_user)], skip: int = 0, limit: int = 10):
    tasks = current_user.tasks
    return tasks

@router.get("/{task_id}", response_model=TaskOut)
def read_task(task_id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    task = Task.find_by(id=task_id, user_id=current_user.id)
    if task is None:
        return {"error": "Task not found"}
    return task

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate, current_user: Annotated[User, Depends(get_current_active_user)]):
    task_with_user = TaskCreateInternal(**task.dict(), user_id=current_user.id)
    print("Task with user:", task_with_user)
    return Task.create(task_with_user)

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: str, task: TaskCreate, current_user: Annotated[User, Depends(get_current_active_user)]):
    updated_task = Task.update(task_id, current_user.id, task)
    if updated_task is None:
        return {"error": "Task not found"}
    return updated_task

@router.delete("/{task_id}", response_model=TaskOut)
def delete_task(task_id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    deleted_task = Task.delete(task_id, current_user.id)
    if deleted_task is None:
        return {"error": "Task not found"}
    return deleted_task