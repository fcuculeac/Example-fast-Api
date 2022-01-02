from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, utils, models
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password : new_user.password
    hashed_password = utils.hash_psw(new_user.password)
    new_user.password = hashed_password
    ins_data = models.User(**new_user.dict())
    db.add(ins_data)
    db.commit()
    db.refresh(ins_data)
    return ins_data  # {"data": ins_data}


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users_data = db.query(models.User).all()
    return users_data   # {"data": posts_data}


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
@router.get("/{id}", response_model=schemas.UserOut)
def get_post(id: int, db: Session = Depends(get_db)):

    search_user = db.query(models.User).filter(models.User.id == id).first()

    if not search_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found.")

    return search_user   # {"data": search_post}
