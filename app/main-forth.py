from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from . database import engine, get_db


# This line is responsible in creating all our ORM models automatically if they do not exists
# If they exists it will not.
models.Base.metadata.create_all(bind=engine)


# This is the FastAPI app
app = FastAPI()


# settings connection to postgres
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi",
                                user="postgres", password="ACCESS", port="5432", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print(f"Connectiong to database failed: Error is:  {error}")
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


# RETRIEVING POSTS USING SQLALCHEMY - ORM
# WHEN NOT RETRIVING A SINGLE POST WITH RESPONSE MODEL, USE List[...]
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts


# CREATING POST USING SQLALCHEMY - ORM
# PYDANTIC and ORM TOGETHER, PYDANTIC TO VALIDATE THE SCHEMA, ORM - TO USE OUR TABLE MODELS
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    # method one is defining the fields one by one
    # # the disadvantage to this this fields may be too long, This is why example twu uses converting it to dict
    '''
    new_post = models.Post(
        title=post.title, content=post.content, published=post.published)
    '''

    # CREATING POST USING SQLALCHEMY - ORM
    # This is example two, converting the fields in the model to dict, to shorten it
    # With this method if you add another field it will automatically unpack
    # **post.dict() is depricated, so i used **post.model_dump(). thew one
    new_post = models.Post(**post.model_dump())

    db.add(new_post)  # to add new row - insert
    db.commit()  # to commit changes

    # This is just like the (RETURNING * ) in postgress. So its Optional
    # This is to retrieve the just inserted data, your use case may determin to have it ot not
    db.refresh(new_post)

    return new_post


# GET LATEST POSTS
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return post


# RETRIEVING INDIVIDUAL POST USING SQLALCHEMY - ORM
@app.get("/posts/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": f"post with the id: {id} was not found"})
    return post


# DELETING POST USING SQLALCHEMY - ORM
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": f"post with the id {id} does not exist"})

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATING POST USING SQLALCHEMY - ORM
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    found_post = post_query.first()

    if found_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": f"post with the id {id} does not exist"})

    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()


# CREATING USERS
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# USER ACCOUNT RETRIEVAL
@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exists")

    return user
