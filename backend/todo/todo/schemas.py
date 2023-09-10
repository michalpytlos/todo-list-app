from uuid import UUID

from pydantic import BaseModel


class Todo(BaseModel):
    title: str
    description: str
    completed: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Foo",
                "description": "Lorem Ipsum",
                "completed": False,
            }
        }


class TodoWithId(Todo):
    id: UUID

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "7aed0faf-f802-4e3c-83eb-726e87b0ed1b",
                "title": "Foo",
                "description": "Lorem Ipsum",
                "completed": False,
            }
        }
