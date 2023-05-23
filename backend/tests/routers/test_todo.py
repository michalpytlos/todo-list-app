from copy import copy
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from tests.utils import TodoTestCrud
from todo import models, schemas
from todo.routers import todos_router


@pytest.fixture
def todo_data() -> dict:
    todo_data = schemas.Todo.Config.schema_extra["example"]
    return copy(todo_data)


@pytest.fixture
def url_prefix() -> str:
    return todos_router.prefix


def test_get_todos(
    client: TestClient,
    url_prefix: str,
    todo_data: dict,
    todo_crud: TodoTestCrud,
):
    # Insert todo
    todos = [models.Todo(**todo_data), models.Todo(**todo_data)]
    todo_crud.insert_many(todos)
    # Send request
    request_url = url_prefix
    response = client.get(request_url)
    # Check if response is correct
    assert response.status_code == 200
    content = response.json()
    assert len(content) == len(todos)


def test_create_todo(
    client: TestClient,
    url_prefix: str,
    todo_data: dict,
    todo_crud: TodoTestCrud,
):
    # Send request
    request_url = url_prefix
    response = client.post(request_url, json=todo_data)
    # Check if response is correct
    assert response.status_code == 200
    content = response.json()
    UUID(content)
    # Check if todo was created
    todos_in_db = todo_crud.get_all()
    assert len(todos_in_db) == 1
    todo_in_db = todos_in_db[0]
    for k, v in todo_data.items():
        assert todo_in_db.__dict__[k] == v


def test_get_todo(
    client: TestClient,
    url_prefix: str,
    todo_data: dict,
    todo_crud: TodoTestCrud,
):
    # Insert todo
    todo = models.Todo(**todo_data)
    todo_id = todo_crud.insert(todo)
    # Send request
    request_url = url_prefix + f"/{todo_id}"
    response = client.get(request_url)
    # Check if response is correct
    assert response.status_code == 200
    content = response.json()
    assert content == todo_data


def test_get_todo_not_found(
    client: TestClient,
    url_prefix: str,
):
    incorrect_todo_id = str(uuid4())
    request_url = url_prefix + f"/{incorrect_todo_id}"
    response = client.get(request_url)
    assert response.status_code == 404


def test_update_todo(
    client: TestClient,
    url_prefix: str,
    todo_data: dict,
    todo_crud: TodoTestCrud,
):
    # Insert todo
    todo = models.Todo(**todo_data)
    todo_id = todo_crud.insert(todo)
    # Todo is modified in the frontend
    updated_todo_data = copy(todo_data)
    new_description = todo_data["description"] + " new text"
    updated_todo_data["description"] = new_description
    # Send request
    request_url = url_prefix + f"/{todo_id}"
    response = client.put(request_url, json=updated_todo_data)
    # Check if response is correct
    assert response.status_code == 200
    # Check if todo was updated
    todo_in_db = todo_crud.get_all()[0]
    assert todo_in_db.description == new_description


def test_update_todo_not_found(
    client: TestClient,
    url_prefix: str,
    todo_data: dict,
):
    incorrect_todo_id = str(uuid4())
    request_url = url_prefix + f"/{incorrect_todo_id}"
    response = client.put(request_url, json=todo_data)
    assert response.status_code == 404


def test_delete_todo(
    client: TestClient,
    url_prefix: str,
    todo_data: dict,
    todo_crud: TodoTestCrud,
):
    # Insert todo
    todo = models.Todo(**todo_data)
    todo_id = todo_crud.insert(todo)
    # Send request
    request_url = url_prefix + f"/{todo_id}"
    response = client.delete(request_url)
    # Check if response is correct
    assert response.status_code == 200
    # Check if todo was deleted
    assert len(todo_crud.get_all()) == 0


def test_delete_todo_not_found(
    client: TestClient,
    url_prefix: str,
):
    incorrect_todo_id = str(uuid4())
    request_url = url_prefix + f"/{incorrect_todo_id}"
    response = client.delete(request_url)
    assert response.status_code == 404
