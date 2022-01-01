# run in CMD:  uvicorn.exe app.main:app --reload

from typing import Optional, List

from fastapi import FastAPI, status, HTTPException, Depends
# from fastapi.params import Body
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

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


@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     # return {"status": "success"}
#     posts = db.query(models.Post).all()
#     return {"data": posts}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""
    # SELECT * from posts;
    # """)
    # posts_data = cursor.fetchall()
    # print(posts_data)
    # return {"data": my_posts}
    posts_data = db.query(models.Post).all()
    return posts_data   # {"data": posts_data}


# validate structure for a new post -  title: str, content: str/
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # print(f"payload = {new_post}")
    # print(f"payload as dict = {new_post.dict()}")
    # # return {"new_post": f"title={payload['title']}, content={payload['content']}"}
    # # adaug postul nou la array
    # post_as_dict = new_post.dict()
    # post_as_dict["id"] = randrange(0, 100_000_000)
    # my_posts.append(post_as_dict)
    # return {"data": new_post}

    #  #### default SQL
    # cursor.execute("""
    # insert into posts (title, content, published)
    # values (%s, %s, %s) RETURNING *
    # """, (new_post.title, new_post.content, new_post.published))
    # ins_data = cursor.fetchone()
    #
    # conn.commit()

    # ins_data = models.Post(title=new_post.title,
    #                        content=new_post.content,
    #                        published=new_post.published)

    ins_data = models.Post(**new_post.dict())
    db.add(ins_data)
    db.commit()
    db.refresh(ins_data)
    return ins_data     # {"data": ins_data}


# get post from an id
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # return {"data": f"This is the post with id = {id}"}

    # cursor.execute("""
    # SELECT * from posts where id = %s
    # """, str(id))
    # search_post = cursor.fetchone()

    # search_post = find_post_by_id(id)

    search_post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(search_post)

    if not search_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found."}
    return search_post  # {"data": search_post}


@app.delete(path="/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # search_post = find_post_by_id(id)
    # cursor.execute("""
    # delete from posts where id = %s returning *
    # """, (str(id)))
    # search_post = cursor.fetchone()
    # conn.commit()

    search_post = db.query(models.Post).filter(models.Post.id == id)

    if not search_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found.")
    else:
        # del my_posts[search_post[1]]
        # return {"data": search_post[0]}
        search_post.delete()
        db.commit()
        return {"message": f"The post with id {id} was successful deleted."}


@app.put(path="/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, upd_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # search_post = find_post_by_id(id)

    # cursor.execute("""
    # update posts set title=%s, content=%s, published=%s where id=%s returning *
    # """, (upd_post.title, upd_post.content, upd_post.published, str(id)))
    # search_post = cursor.fetchone()

    search_post = db.query(models.Post).filter(models.Post.id == id)
    post = search_post.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found.")
    else:
        # original_post = search_post[0]
        # upd_post_as_dict = upd_post.dict()
        # upd_post_as_dict["id"] = original_post["id"]
        # # del my_posts[search_post[1]]
        # # my_posts.append(upd_post_as_dict)
        # my_posts[search_post[1]] = upd_post_as_dict
        # return {"data": upd_post_as_dict}
        # conn.commit()

        search_post.update(upd_post.dict())
        db.commit()
        db.refresh(post)

        return post  # {"data": post}


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password : new_user.password
    hashed_password = utils.hash_psw(new_user.password)
    new_user.password = hashed_password
    ins_data = models.User(**new_user.dict())
    db.add(ins_data)
    db.commit()
    db.refresh(ins_data)
    return ins_data  # {"data": ins_data}


@app.get("/users", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users_data = db.query(models.User).all()
    return users_data   # {"data": posts_data}


@app.delete(path="/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):

    search_user = db.query(models.User).filter(models.User.id == id)

    if not search_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found.")
    else:
        search_user.delete()
        db.commit()
        return {"message": f"The user with id {id} was successful deleted."}


# get user from an id
@app.get("/users/{id}", response_model=schemas.UserOut)
def get_post(id: int, db: Session = Depends(get_db)):

    search_user = db.query(models.User).filter(models.User.id == id).first()

    if not search_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found.")

    return search_user  # {"data": search_post}
