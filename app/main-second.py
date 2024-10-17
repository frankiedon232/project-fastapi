from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from . database import engine, SessionLocal


# This line is responsible in creating all our ORM models automatically if they do not exists
# If they exists it will not.
models.Base.metadata.create_all(bind=engine)


# This is the FastAPI app
app = FastAPI()


# The dependency. Not: The is what talks to the databases SessionLocal(), referance database.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True          # DEFAULT VALUE


# settings connection to postgres
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi",
                                user="postgres", password="ACCESS", port="5432", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print(f"Connectiong to database failed: Error is {error}")
        time.sleep(3)


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


# TESTING SQLSLCHEMY SETUP
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    return {"status": "success"}


# RETRIEVING POSTS FROM DATABASE
@app.get("/posts")
def get_posts():

    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()

    return {"data": posts}


# PYDANTIC
# WITH SCHEMA VALIDATION - PYDANTIC - USING THE POST MODEL CLASS ABOVE (Post)
# TO VALIDATE THE POST THAT USERS ARE TO SENT IN.
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):               # Retrieving Data

    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (
            post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()

    return {"data": new_post}


# GET LATEST POSTS
@ app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"details": post}


# Rerieving Individual Post
@ app.get("/posts/{id}")
def get_posts(id: int):

    cursor.execute("""SELECT * FROM posts WHERE id = %s """, ([id]))
    post = cursor.fetchone()

    if not post:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": f"post with the id {id} was not found"})
    return {"post_details": post}


# Deleting a post
@ app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": f"post with the id {id} does not exist"})

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update Post
@ app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (
            post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": f"post with the id {id} does not exist"})

    return {"data": updated_post}
