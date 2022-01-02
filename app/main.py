# run in CMD:  uvicorn.exe app.main:app --reload

from fastapi import FastAPI
# from fastapi.params import Body
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

from . import models
from .database import engine
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

"""
# in case of failure, I will loop till I find a connection
while True:
    try:
        # TODO: the connection need to be dinamic
        conn = psycopg2.connect(host="localhost",
                                database="fastapi",
                                user="postgres",
                                password="123456", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful!")
        break
    except Exception as err:
        print(f"Database failed! Error was {err}")
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]




def find_post_by_id(id: int):
    for index, post in enumerate(my_posts):
        # print(post, f"id={id}", f"{post['id']}")
        if post['id'] == id:
            return post, index

"""

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     # return {"status": "success"}
#     posts = db.query(models.Post).all()
#     return {"data": posts}

