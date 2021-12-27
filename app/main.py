from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


# define schema for the post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # optional value
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]


def find_post_by_id(id: int):
    for index, post in enumerate(my_posts):
        # print(post, f"id={id}", f"{post['id']}")
        if post['id'] == id:
            return post, index


@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# validate structure for a new post -  title: str, content: str
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    print(f"payload = {new_post}")
    print(f"payload as dict = {new_post.dict()}")
    # return {"new_post": f"title={payload['title']}, content={payload['content']}"}
    # adaug postul nou la array
    post_as_dict = new_post.dict()
    post_as_dict["id"] = randrange(0, 100_000_000)
    my_posts.append(post_as_dict)
    return {"data": new_post}


# get post from an id
@app.get("/posts/{id}")
def get_post(id: int):
    # return {"data": f"This is the post with id = {id}"}
    search_post = find_post_by_id(id)
    if not search_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found."}
    return {"data": search_post[0]}


@app.delete(path="/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    search_post = find_post_by_id(id)
    if not search_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found.")
    else:
        del my_posts[search_post[1]]
        # return {"data": search_post[0]}
        return {"message": f"The post with id {id} was successful deleted."}


@app.put(path="/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, upd_post: Post):
    search_post = find_post_by_id(id)
    if not search_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found.")
    else:
        original_post = search_post[0]
        upd_post_as_dict = upd_post.dict()
        upd_post_as_dict["id"] = original_post["id"]
        # del my_posts[search_post[1]]
        # my_posts.append(upd_post_as_dict)
        my_posts[search_post[1]] = upd_post_as_dict
        return {"data": upd_post_as_dict}
