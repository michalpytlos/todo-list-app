import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import Column
from todo.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean)
