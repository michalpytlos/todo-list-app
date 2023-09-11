from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.database import (
    TestingSession,
    create_test_db_if_not_exists,
    override_get_db,
    testing_engine,
)
from todo.database import Base, get_db
from todo.main import app
from todo.todo.models import Todo


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


@pytest.fixture(autouse=True)
def cleanup_tables(db: Session):
    yield
    db.execute(f"TRUNCATE {Todo.__tablename__}")
    db.commit()
    db.close()
