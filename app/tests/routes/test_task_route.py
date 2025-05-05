# app/tests/requests/task_tests.py
from __future__ import annotations

import pytest
from uuid import UUID

from app.models import User, Task
from app.schemas.user import UserCreate
from app.schemas.task import TaskCreate


class TestTaskRoute:
    @pytest.fixture
    def valid_user(self, db_session):
        user_data = UserCreate(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="123456",
        )
        return User.create(db_session, user_data)

    @pytest.fixture
    def task_payload(self):
        return {
            "title": "Test Task",
            "description": "Test Description"
        }

    @pytest.fixture
    def signin_user(self, client, valid_user):
        signin_data = {
            "username": valid_user.email,
            "password": "123456",
        }
        response = client.post("/signin", data=signin_data)
        assert response.status_code == 200
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def create_task(self, client, task_payload, signin_user):
        response = client.post("/tasks/", json=task_payload, headers=signin_user)
        assert response.status_code == 200
        return response.json()

    def test_create_task(self, client, task_payload, signin_user):
        response = client.post("/tasks/", json=task_payload, headers=signin_user)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["title"] == task_payload["title"]
        assert response_json["description"] == task_payload["description"]
        assert response_json["done"] is False

    def test_create_task_unauthorized(self, client, task_payload):
        response = client.post("/tasks/", json=task_payload)
        assert response.status_code == 401

    def test_get_task(self, client, create_task, signin_user):
        task_id = create_task["id"]
        response = client.get(f"/tasks/{task_id}", headers=signin_user)
        assert response.status_code == 200
        assert response.json()["id"] == task_id

    def test_get_task_not_found(self, client, signin_user):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/tasks/{non_existent_id}", headers=signin_user)
        assert response.status_code == 404

    def test_get_all_tasks(self, client, create_task, signin_user):
        response = client.get("/tasks/", headers=signin_user)
        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        assert len(tasks) > 0
        assert any(task["id"] == create_task["id"] for task in tasks)

    def test_update_task(self, client, create_task, signin_user):
        task_id = create_task["id"]
        update_data = {
            "title": "Updated task",
            "description": "Updated description",
            "done": True
        }
        response = client.put(f"/tasks/{task_id}", json=update_data, headers=signin_user)
        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["title"] == update_data["title"]
        assert updated_task["description"] == update_data["description"]
        assert updated_task["done"] == update_data["done"]

    def test_update_task_not_found(self, client, signin_user):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        update_data = {
            "title": "Updated task",
            "description": "Updated description",
            "done": True
        }
        response = client.put(f"/tasks/{non_existent_id}", json=update_data, headers=signin_user)
        assert response.status_code == 404

    def test_delete_task(self, client, create_task, signin_user):
        task_id = create_task["id"]
        response = client.delete(f"/tasks/{task_id}", headers=signin_user)
        assert response.status_code == 200
        
        # Verify task is deleted
        get_response = client.get(f"/tasks/{task_id}", headers=signin_user)
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client, signin_user):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        response = client.delete(f"/tasks/{non_existent_id}", headers=signin_user)
        assert response.status_code == 404
