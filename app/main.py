# run in CMD:  uvicorn.exe app.main:app --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import posts, users, auth, votes
from .config import Settings


# test conection from chrome
# fetch("http://localhost:8000").then(res=>res.json()).then(console.log)

# no need if alembic is implemented
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# allow all domains
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API!!!!"}

