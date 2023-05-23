from typing import Generator

from psycopg2.errors import DuplicateDatabase  # type: ignore
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker
from todo.config import settings
from todo.database import DATABASE_URL

technical_engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")


def get_test_db_url():
    if not settings.test_database:
        raise Exception("Test database is not configured.")
    if settings.test_database == settings.db.database:
        raise Exception("Production database was set as test database.")
    test_db_dict = settings.db.dict()
    test_db_dict["database"] = settings.test_database
    return URL.create(drivername="postgresql", **test_db_dict)


TEST_DATABASE_URL = get_test_db_url()

testing_engine = create_engine(TEST_DATABASE_URL, echo=False)

TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=testing_engine)


def override_get_db() -> Generator:
    try:
        db = TestingSession()
        yield db
    finally:
        db.close()


def create_test_db_if_not_exists():
    with technical_engine.connect() as conn:
        try:
            conn.execute(f"CREATE DATABASE {settings.test_database}")
        except ProgrammingError as e:
            if type(e.orig) is DuplicateDatabase:
                pass
            else:
                raise
