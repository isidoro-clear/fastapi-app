from fastapi import APIRouter, Depends
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from fastapi.responses import JSONResponse
from app.core.auth import get_current_active_user, Token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from app.db import get_db

router = APIRouter(tags=["users"])

@router.get("/me", response_model=UserOut)
def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user is None:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    return current_user

@router.post("/signup", response_model=UserOut)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    return User.create(db, user)

@router.post("/signin")
def signin_user(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    access_token = User.signin(db, data)
    return Token(access_token=access_token, token_type="bearer")
