from datetime import datetime
from pydantic import BaseModel


# Class PostBase and PostCreate Its the Pydantic Model r Schems Model that handled creating posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# This Class Post handles the resonses. and in the responses we defines what we want users to see
#  we added the orm_mode, to ensure that the pydantic model read the data even if it's not dict but an ORM model
# or any other arbitrary object with attributes.
# orm_mode is depricated use from_attributes instead
class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        from_attributes = True
