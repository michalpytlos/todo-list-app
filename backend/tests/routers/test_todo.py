from copy import copy
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from todo.todo import schemas
from todo.todo.api import todos_router

TODO_URL_PREFIX = todos_router.prefix


@pytest.fixture
def todo_data() -> dict:
    todo_data = schemas.Todo.Config.schema_extra["example"]
    return copy(todo_data)


def test_create_then_get_todos(
    client: TestClient,
    todo_data: dict,
):
    # Create todos
    todo_count = 2
    todos = {}
    for _ in range(todo_count):
        response = client.post(url=TODO_URL_PREFIX, json=todo_data)
        assert response.status_code == 200
        id = response.json()
        todos[id] = {"id": id} | todo_data
    # Get todos
    response = client.get(url=TODO_URL_PREFIX)
    assert response.status_code == 200
    content = response.json()
    # All todos were returned
    assert len(content) == todo_count
    # Returned todos have all the data
    for todo in content:
        assert todo == todos[todo["id"]]


def test_create_then_get_todo(
    client: TestClient,
    todo_data: dict,
):
    # Create todo
    response = client.post(url=TODO_URL_PREFIX, json=todo_data)
    assert response.status_code == 200
    id = response.json()
    # Get todo
    url = f"{TODO_URL_PREFIX}/{id}"
    response = client.get(url)
    # Check if response is correct
    assert response.status_code == 200
    content = response.json()
    assert content == todo_data


def test_update_todo(
    client: TestClient,
    todo_data: dict,
):
    # Create todo
    response = client.post(url=TODO_URL_PREFIX, json=todo_data)
    assert response.status_code == 200
    id = response.json()
    # Update todo
    updated_todo_data = copy(todo_data)
    new_description = todo_data["description"] + " new text"
    updated_todo_data["description"] = new_description
    url = f"{TODO_URL_PREFIX}/{id}"
    response = client.put(url, json=updated_todo_data)
    assert response.status_code == 200
    # Check if todo was updated
    response = client.get(url)
    assert response.status_code == 200
    todo = response.json()
    assert todo["description"] == new_description


def test_delete_todo(
    client: TestClient,
    todo_data: dict,
):
    # Create todo
    response = client.post(url=TODO_URL_PREFIX, json=todo_data)
    assert response.status_code == 200
    id = response.json()
    # Delete todo
    url = f"{TODO_URL_PREFIX}/{id}"
    response = client.delete(url)
    assert response.status_code == 200
    # Check if todo was deleted
    response = client.get(url)
    assert response.status_code == 404


def test_update_todo_not_found(
    client: TestClient,
    todo_data: dict,
):
    url = f"{TODO_URL_PREFIX}/{str(uuid4())}"
    response = client.put(url=url, json=todo_data)
    assert response.status_code == 404


@pytest.mark.parametrize(
    "method",
    [pytest.param("GET", id="get todo"), pytest.param("DELETE", id="delete todo")],
)
def test_todo_not_found(
    client: TestClient,
    method: str,
):
    url = f"{TODO_URL_PREFIX}/{str(uuid4())}"
    response = client.request(method=method, url=url)
    assert response.status_code == 404
