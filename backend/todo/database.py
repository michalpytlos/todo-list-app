from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from todo.config import settings

DATABASE_URL = URL.create(drivername="postgresql", **settings.db.dict())

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
