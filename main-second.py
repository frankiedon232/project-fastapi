from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True          # DEFAULT VALUE
    rating: Optional[int] = None    # OPTIONAL VALUE


# This is just static data in memory. it does not save
# Just for this practice
my_posts = [
    {
        "title": "Hotels In Nigeria",
        "content": "Check out all the hotels we have in nigeria",
        "id": 1,
    },
    {
        "title": "Book Stors",
        "content": "The Book Stores we have here for sure",
        "id": 2,
    }
]


# Function to find posts
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/")
def root():
    return {"message": "Welcome to my API this is changes"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# WITHOUT SCHEMA VALIDATION
# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):  # Retrieving Data
#     # print(payload)
#     return {"new_post": payload}

# PYDANTIC
# WITH SCHEMA VALIDATION - PYDANTIC - USING THE POST MODEL CLASS ABOVE (Post)
# TO VALIDATE THE POST THAT USERS ARE TO SENT IN.

@app.post("/posts")
def create_posts(post: Post):               # Retrieving Data
    post_dict = post.model_dump()  # Convert to dictionary -  post.dict() is deprecated
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# GET LATEST POSTS
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"details": post}


# Rerieving Individual Post
@app.get("/posts/{id}")
def get_posts(id: int):
    post = find_post(id)
    print(post)

    return {"post_details": post}
