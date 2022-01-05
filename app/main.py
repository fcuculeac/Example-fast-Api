# run in CMD:  uvicorn.exe app.main:app --reload
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth, votes
from .config import Settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}

