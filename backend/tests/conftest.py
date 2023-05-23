from typing import Generator

import pytest
from fastapi.testclient import TestClient
from tests.database import (
    TestingSession,
    create_test_db_if_not_exists,
    override_get_db,
    testing_engine,
)
from tests.utils import TodoTestCrud
from todo.database import Base, Session, get_db
from todo.main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def db() -> Generator:
    create_test_db_if_not_exists()
    Base.metadata.drop_all(bind=testing_engine)
    Base.metadata.create_all(bind=testing_engine)
    yield TestingSession()


@pytest.fixture
def todo_crud(db: Session) -> Generator:
    todo_crud = TodoTestCrud(db=db)
    yield todo_crud
    todo_crud.cleanup()
