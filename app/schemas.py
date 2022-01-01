from pydantic import BaseModel, EmailStr
from datetime import datetime


# define schema for the post
# schema model - pydantic model - schema of the request & response
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # optional value
    # rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True
