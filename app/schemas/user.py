from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: UUID

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str
