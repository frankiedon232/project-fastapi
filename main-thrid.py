from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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

# Find post index


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
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
def get_posts(id: int, response: Response):
    post = find_post(id)

    if not post:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": f"post with the id {id} was not found"})
    return {"post_details": post}


# Deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # Deleting Post
    # find the inxes in the array that has required ID
    # my_post.pop(index)

    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": f"post with the id {id} does not exist"})

    my_posts.pop(index)
    # return {"message": "post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update Post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": f"post with the id {id} does not exist"})

    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
