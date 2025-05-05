from pydantic import BaseModel, ConfigDict
from uuid import UUID

class TaskBase(BaseModel):
    title: str
    description: str | None = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    done: bool

class TaskCreateInternal(TaskCreate):
    user_id: UUID

class TaskOut(TaskBase):
    id: UUID
    done: bool
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)
