from typing import List, Optional

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from sqlalchemy import func

from app import schemas, models, oauth2
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: models.User = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""
    # SELECT * from posts;
    # """)
    # posts_data = cursor.fetchall()
    # print(posts_data)
    # return {"data": my_posts}

    print(f"current user: {current_user.email}")

    # posts_data = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post,
                       func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)

    return results   # {"data": posts_data}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):

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

    ins_data = models.Post(owner_id=current_user.id, **new_post.dict())
    db.add(ins_data)
    db.commit()
    db.refresh(ins_data)
    return ins_data     # {"data": ins_data}


# get post from an id
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,
             db: Session = Depends(get_db),
             current_user: models.User = Depends(oauth2.get_current_user)):
    # return {"data": f"This is the post with id = {id}"}

    # cursor.execute("""
    # SELECT * from posts where id = %s
    # """, str(id))
    # search_post = cursor.fetchone()

    # search_post = find_post_by_id(id)

    # search_post = db.query(models.Post).filter(models.Post.id == id).first()
    search_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    # print(search_post)

    if not search_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found."}
    return search_post  # {"data": search_post}


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # search_post = find_post_by_id(id)
    # cursor.execute("""
    # delete from posts where id = %s returning *
    # """, (str(id)))
    # search_post = cursor.fetchone()
    # conn.commit()

    search_post = db.query(models.Post).filter(models.Post.id == id)
    post = search_post.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found.")
    elif post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized for this action. "
                            + f"Post with id {id} has other owner_id {search_post.first().owner_id}.")
    else:
        # del my_posts[search_post[1]]
        # return {"data": search_post[0]}
        search_post.delete()
        db.commit()
        return {"message": f"The post with id {id} was successful deleted."}


@router.put(path="/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, upd_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
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
    elif post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized for this action. "
                            + f"Post with id {id} has other owner_id {post.owner_id}.")
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
