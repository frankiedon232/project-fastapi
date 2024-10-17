from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True          # DEFAULT VALUE
    rating: Optional[int] = None    # OPTIONAL VALUE


@app.get("/")
def root():
    return {"message": "Welcome to my API this is changes"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your post for sure yes"}


# WITHOUT SCHEMA VALIDATION
# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):  # Retrieving Data
#     # print(payload)
#     return {"new_post": payload}

# PYDANTIC
# WITH SCHEMA VALIDATION - PYDANTIC - USING THE POST MODEL CLASS ABOVE (Post)
# TO VALIDATE THE POST THAT USERS ARE TO SENT IN.
@app.post("/posts")
def create_posts(post: Post):  # Retrieving Data

    print(post)
    print(post.model_dump)  # convert pydantic model to a dictionary
    print(post.title)
    print(post.content)
    print(post.published)
    print(post.rating)

    return {"data": post}
