from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. database import get_db
from .. import models, schemas


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# RETRIEVING POSTS USING SQLALCHEMY - ORM
# WHEN NOT RETRIVING A SINGLE POST WITH RESPONSE MODEL, USE List[...]
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts


# CREATING POST USING SQLALCHEMY - ORM
# PYDANTIC and ORM TOGETHER, PYDANTIC TO VALIDATE THE SCHEMA, ORM - TO USE OUR TABLE MODELS
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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


# RETRIEVING INDIVIDUAL POST USING SQLALCHEMY - ORM
@router.get("/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": f"post with the id: {id} was not found"})
    return post


# DELETING POST USING SQLALCHEMY - ORM
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": f"post with the id {id} does not exist"})

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATING POST USING SQLALCHEMY - ORM
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    found_post = post_query.first()

    if found_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": f"post with the id {id} does not exist"})

    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()
