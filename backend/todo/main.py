from fastapi import FastAPI
from todo.routers import todos_router

app = FastAPI()
app.include_router(todos_router)


@app.get("/")
async def root():
    return {"message": "To-do app server."}
