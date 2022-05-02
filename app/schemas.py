from lib2to3.pytree import Base
from pydantic import  BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_date: datetime
    class Config:
            orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Post(PostBase):
    id: int
    created_date: datetime
    owner_id: int
    owner: UserOut
    #Since pydantic only knows how to work with dictionaries, we use this Config class to convert
    #the sqlalchemy model to a pydantic model.
    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):

    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostOUT(BaseModel):
    Post: Post
    votes: int
