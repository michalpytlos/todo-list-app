from uuid import UUID

from sqlalchemy.orm import Session

from . import models, schemas


class TodoCrud:
    model: type[models.Todo] = models.Todo

    @classmethod
    def get_todos(cls, db: Session) -> list[models.Todo]:
        return db.query(cls.model).all()

    @classmethod
    def create_todo(cls, todo: schemas.Todo, db: Session) -> UUID:
        todo_db = cls.model(**todo.dict())
        db.add(todo_db)
        db.commit()
        return todo_db.id

    @classmethod
    def get_todo(cls, todo_id: UUID, db: Session) -> models.Todo | None:
        return db.query(cls.model).filter(cls.model.id == todo_id).one_or_none()

    @classmethod
    def update_todo(cls, todo_id: UUID, todo: schemas.Todo, db: Session) -> bool:
        todo_db = db.query(cls.model).filter(cls.model.id == todo_id).one_or_none()
        if not todo_db:
            return False
        todo_db.title = todo.title
        todo_db.description = todo.description
        todo_db.completed = todo.completed
        db.commit()
        return True

    @classmethod
    def delete_todo(cls, todo_id: UUID, db: Session) -> bool:
        deleted = db.query(cls.model).filter(cls.model.id == todo_id).delete()
        db.commit()
        if deleted == 0:
            return False
        else:
            return True
