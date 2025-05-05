from pydantic import BaseModel, ConfigDict
from uuid import UUID

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    username: str
    password: str
