import pytest
from uuid import UUID
from app.models import Task, User
from app.schemas.task import TaskCreateInternal, TaskUpdate
from app.schemas.user import UserCreate

class TestTaskModel:
    @pytest.fixture
    def user(self, db_session):
        user_data = UserCreate(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123"
        )
        return User.create(db_session, user_data)

    @pytest.fixture
    def task_data(self, user):
        return TaskCreateInternal(
            title="Test Task",
            description="Test Description",
            user_id=user.id
        )

    def test_task_creation(self, db_session, task_data):
        task = Task.create(db_session, task_data)
        
        assert isinstance(task.id, UUID)    
        assert task.title == task_data.title
        assert task.description == task_data.description
        assert task.done is False
        assert task.user_id == task_data.user_id

    def test_task_find_by(self, db_session, task_data):
        created_task = Task.create(db_session, task_data)
        found_task = Task.find_by(db_session, id=created_task.id)
        
        assert found_task is not None
        assert found_task.id == created_task.id
        assert found_task.title == created_task.title

    def test_task_update(self, db_session, task_data):
        created_task = Task.create(db_session, task_data)
        updated_data = TaskUpdate(
            title="Updated Task",
            description="Updated Description",
            done=True
        )
        
        updated_task = Task.update(db_session, str(created_task.id), str(task_data.user_id), updated_data)
        
        assert updated_task is not None
        assert updated_task.title == updated_data.title
        assert updated_task.description == updated_data.description

    def test_task_delete(self, db_session, task_data):
        created_task = Task.create(db_session, task_data)
        deleted_task = Task.delete(db_session, str(created_task.id), str(task_data.user_id))
        
        assert deleted_task is not None
        assert deleted_task.id == created_task.id
        
        # Verify task is actually deleted
        found_task = Task.find_by(db_session, id=created_task.id)
        assert found_task is None

    def test_task_not_found(self, db_session):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        task = Task.find_by(db_session, id=non_existent_id)
        assert task is None

    def test_task_update_not_found(self, db_session, task_data):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        updated_task = Task.update(db_session, non_existent_id, str(task_data.user_id), task_data)
        assert updated_task is None

    def test_task_delete_not_found(self, db_session, task_data):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        deleted_task = Task.delete(db_session, non_existent_id, str(task_data.user_id))
        assert deleted_task is None 