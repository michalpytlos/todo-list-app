from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "To-do app server."}
