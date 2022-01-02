from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, utils, models, oauth2
from app.database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2PasswordRequestForm returns a dictionary
    {"username": "blahblah", "password": "bleah"}

    """

    search_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not search_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials.")
    # print(f"search user: {search_user.email}")

    # verify if password is the same as is in the databases
    attempt_password = user_credentials.password

    if not utils.verify_psw(attempt_password, search_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials(p).")

    # create token
    # need to install pip install python-jose[cryptography]
    # return token

    access_token = oauth2.create_access_token(
        data={
            "user_id": search_user.id
        }
    )

    return {"access_token": access_token, "token_type": "bearer"}
