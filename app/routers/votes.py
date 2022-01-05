from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, utils, models, oauth2
from app.database import get_db

router = APIRouter(prefix="/votes", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote_new: schemas.Vote,
         db: Session = Depends(get_db),
         current_user: models.User = Depends(oauth2.get_current_user)):
    # verific sa existe acel post_id in posts
    post = db.query(models.Post).filter(models.Post.id == vote_new.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with post id {vote_new.post_id}  not found.")
    search_vote = db.query(models.Vote).filter(models.Vote.user_id == current_user.id,
                                               models.Vote.post_id == vote_new.post_id)
    found_vote = search_vote.first()
    # if direction = 0 => delete, else insert
    direction = vote_new.dir
    if direction == 0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote with post id {vote_new.post_id} and user id {current_user.id} not found.")
        search_vote.delete(syncronize_session=False)
        db.commit()
        return {"message": f"The vote was successful deleted."}
    else:
        #  insert data
        # ins_data = models.Vote(user_id=current_user.id, **new_vote.dict())
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"The user {current_user.id} already vote on this post id {vote_new.post_id}")
        new_vote = models.Vote(post_id=vote_new.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}
