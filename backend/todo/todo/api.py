from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from todo.database import get_db
from .crud import TodoCrud
from .schemas import Todo, TodoWithId

todos_router = APIRouter(prefix="/todos", tags=["todo"])


@todos_router.get("", response_model=list[TodoWithId])
def get_todos(db: Session = Depends(get_db)):
    return TodoCrud.get_todos(db=db)


@todos_router.post("", response_model=UUID)
def create_todo(todo: Todo, db: Session = Depends(get_db)):
    return TodoCrud.create_todo(todo=todo, db=db)


@todos_router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: UUID, db: Session = Depends(get_db)):
    todo = TodoCrud.get_todo(todo_id=todo_id, db=db)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return todo


@todos_router.put("/{todo_id}")
def update_todo(todo_id: UUID, todo: Todo, db: Session = Depends(get_db)):
    updated = TodoCrud.update_todo(todo_id=todo_id, todo=todo, db=db)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo item not found")


@todos_router.delete("/{todo_id}")
def delete_todo(todo_id: UUID, db: Session = Depends(get_db)):
    deleted = TodoCrud.delete_todo(todo_id=todo_id, db=db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo item not found")
