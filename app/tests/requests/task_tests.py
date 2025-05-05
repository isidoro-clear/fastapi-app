# app/tests/requests/task_tests.py

import pytest

user_payload = {
    "first_name": "Jhon",
    "last_name": "Doe",
    "email": "jhon.doe@example.com",
    "password": "123456",
}

task_payload = {
    "title": "Test task",
    "description": "Descrição de teste",
    "done": False,
}


@pytest.fixture
def signup_user(client):
    response = client.post("/signup/", json=user_payload)
    assert response.status_code in (200, 201)
    return response.json()


@pytest.fixture
def signin_user(client):
    signin_data = {
        "username": user_payload["email"],
        "password": user_payload["password"],
    }
    response = client.post("/signin", data=signin_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def create_task(client, signup_user, signin_user):
    response = client.post("/tasks/", json=task_payload, headers=signin_user)
    assert response.status_code == 200
    return response.json()


def test_create_task(create_task):
    assert "id" in create_task
    assert create_task["title"] == task_payload["title"]
