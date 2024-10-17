from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


# CREATING USER MODEL
# Here we added some extra validation EmailStr
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# CREATING USER RESPONSE MODEL
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# CREATING POST MODEL
# Class PostBase and PostCreate Its the Pydantic Model are Schems Model that handled creating posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# CREATING POST RESPONSE MODEL
# This Class Post handles the resonses. and in the responses we defines what we want users to see
#  we added the orm_mode, to ensure that the pydantic model read the data even if it's not dict but an ORM model
# or any other arbitrary object with attributes.
# orm_mode is depricated use from_attributes instead
# We inheritated some of the other fields from the PostBase
# So here we only put what we want to be added to the response
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


# Addedd this after some time, when we started joining table with SQLAlchemy
# Inherit from BaseModel, because you will be joining schema on this files already like the Post is a class
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


# USER LOGIN
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]


class Vote(BaseModel):
    post_id: int
    dir: Optional[int] = 1
