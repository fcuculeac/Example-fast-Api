from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# define schema for the post
# schema model - pydantic model - schema of the request & response
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # optional value
    # rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
