from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Session
from app.db import Base
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserCreate
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    tasks = relationship("Task", back_populates="user")

    @classmethod
    def find_by(cls, db: Session, **kwargs):
        return db.query(cls).filter_by(**kwargs).first()

    @classmethod
    def create(cls, db: Session, user_data: UserCreate):
        if db.query(cls).filter(cls.email == user_data.email).first():
            raise ValueError("E-mail já registrado.")

        new_user = cls(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=hash_password(user_data.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @classmethod
    def signin(cls, db: Session, user_data: UserCreate):
        user = db.query(cls).filter(cls.email == user_data.email).first()
        if not user or not verify_password(user_data.password, user.password):
            raise ValueError("E-mail or password is incorrect.")
        token = create_access_token(data={"sub": user.email})
        return token
