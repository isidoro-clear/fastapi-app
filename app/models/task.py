from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from app.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.schemas.task import TaskCreateInternal

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    done = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="tasks")

    @classmethod
    def all(cls, db: Session):
        return db.query(cls).all()
    
    @classmethod
    def find_by(cls, db: Session, **kwargs):
        return db.query(cls).filter_by(**kwargs).first()

    @classmethod
    def create(cls, db: Session, data: TaskCreateInternal):
        new_task = cls(
            title=data.title,
            description=data.description,
            done=False,
            user_id=data.user_id
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    
    @classmethod
    def update(cls, db: Session, task_id: str, user_id: str, data: TaskCreateInternal):
        task = cls.find_by(db, id=task_id, user_id=user_id)
        if not task:
            return None
        task.title = data.title
        task.description = data.description
        task.done = data.done
        db.commit()
        db.refresh(task)
        return task
    
    @classmethod
    def delete(cls, db: Session, task_id: str, user_id: str):
        task = cls.find_by(db, id=task_id, user_id=user_id)
        if not task:
            return None
        db.delete(task)
        db.commit()
        return task
