from uuid import UUID

from sqlalchemy.orm import Session
from todo.todo.models import Todo


class TodoTestCrud:
    def __init__(self, db: Session):
        self.db = db

    def insert(self, todo: Todo) -> str:
        self.db.add(todo)
        self.db.commit()
        return str(todo.id)

    def insert_many(self, todos: list[Todo]):
        for todo in todos:
            self.db.add(todo)
        self.db.commit()

    def get_all(self):
        # db.commit() is required to get all the objects from the db
        # otherwise objects already present in the session are not fetched from the db
        # see https://stackoverflow.com/a/18834114 for more details
        self.db.commit()
        return self.db.query(Todo).all()

    def cleanup(self):
        self.db.execute(f"TRUNCATE {Todo.__tablename__}")
        self.db.commit()
        self.db.close()
