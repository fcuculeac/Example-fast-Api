from typing import Optional

from fastapi import FastAPI
# from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


# define schema for the post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # optional value
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}


@app.get("/posts")
def get_posts():
    return {"data": "this is your posts."}


# validate structure for a new post -  title: str, content: str
@app.post("/posts")
def new_posts(new_post: Post):
    print(f"payload = {new_post}")
    print(f"payload as dict = {new_post.dict()}")
    # return {"new_post": f"title={payload['title']}, content={payload['content']}"}
    return {"data": new_post}
