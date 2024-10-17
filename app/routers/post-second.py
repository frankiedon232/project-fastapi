from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. database import get_db
from .. import models, schemas, oath2


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# RETRIEVING POSTS
# WHEN NOT RETRIVING A SINGLE POST WITH RESPONSE MODEL, USE List[...]
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    print(f"The Authenticated user is: {current_user.email}")

    posts = db.query(models.Post).all()
    return posts


# ADDED DEPENDENCY (get_current_user) FOR LOGIN/ LOGGED IN BEFORE CREATING POST
# AND IT FORCES USERS TO BE LOOGED IF NOT BEFORE CREATING A POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    print(f"The Authenticated user is: {current_user.email}")
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()

    db.refresh(new_post)

    return new_post


# RETRIEVING INDIVIDUAL POST
@router.get("/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    print(f"The Authenticated user is: {current_user.email}")

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": f"post with the id: {id} was not found"})
    return post


# DELETING POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    print(f"The Authenticated user is: {current_user.email}")

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": f"post with the id {id} does not exist"})

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATING POST
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    print(f"The Authenticated user is: {current_user.email}")

    post_query = db.query(models.Post).filter(models.Post.id == id)
    found_post = post_query.first()

    if found_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": f"post with the id {id} does not exist"})

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
