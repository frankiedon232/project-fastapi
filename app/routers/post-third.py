from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import asc
from sqlalchemy.orm import Session
from typing import List, Optional
from .. database import get_db
from .. import models, schemas, oath2


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# RETRIEVING POSTS
# WHEN NOT RETRIVING A SINGLE POST WITH RESPONSE MODEL, USE List[...]
# GET POSTS BELONGING TO LOGGED IN USERS
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    '''
     This is every information about get <b>TEST OF BOLD TEXT</b>
    '''

    print(f"The Authenticated user is: {current_user.email}")
    print(f"Limit: {limit}, Skip: {skip}, search: {search} ")

    # WITHOUT LIMITS- NOT USING QUARY PARAMETERS
    # AND ALSO GETTING ONLY CURRENT LOGGED IN USER POSTS
    '''
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    '''

    # WITH QUERY PARAMETERS - LIMITING TOTAL NUMBER OF RETREIVAL
    # AND RETRIEVING ONLY OWNERS POST.
    # THEN FILTER AND SHOW ONLY OWNERS POSTS
    '''
    posts = db.query(models.Post).filter( models.Post.owner_id == current_user.id).limit(limit).all()
    '''

    # WITH QUERY PARAMETERS - LIMITING TOTAL NUMBER OF RETREIVAL
    # AND RETRIEVING ALL POST FOR ALL OWNERS. JUST FOR MORE DATA SAKE TO WORK WITH

    # FILTER AND SHOW ALL OWNERS POSTS - IRRESPECTIVE OF WHO POSTED IT

    '''
    posts = db.query(models.Post).limit(limit).all()
    '''

    # ADDING SKIP WITH OFFSET
    # YOU APPLY TO OTHERS, BUT AFTER THE limit()
    '''
    posts = db.query(models.Post).limit(limit).offset(skip).all()
    '''

    # ADDING SORTING ASC OR DESC
    '''
    posts = db.query(models.Post).order_by(
        asc(models.Post.id)).limit(limit).offset(skip).all()
    '''

    # INCLUSING SEARCH
    posts = db.query(models.Post).filter(models.Post.title.contains(
        search)).order_by(asc(models.Post.id)).limit(limit).offset(skip).all()

    return posts


# ADDED DEPENDENCY (get_current_user) FOR LOGIN/ LOGGED IN BEFORE CREATING POST
# AND IT FORCES USERS TO BE LOOGED IF NOT BEFORE CREATING A POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    print(f"The Authenticated user is: {current_user.email}")
    print(current_user.id)

    # INCLUDING THE CURRENT LOGGED IN USER AS THE OWNER OF THE POST, BY APPENDING IT TO THE POST BODY
    # POSTING BASES ON CURRENT USER
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()

    db.refresh(new_post)

    return new_post


# RETRIEVING INDIVIDUAL POST
# ONLY GET FILTER POSTS THAT BELONG TO THE CURRENT LOGGEDIN OWNER
@router.get("/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    print(f"The Authenticated user is: {current_user.email}")

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": f"post with the id: {id} was not found"})

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"You do not own this post with id: {id} not found"})

    return post


# DELETING POST BASES ON OWNER ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    print(f"The Authenticated user is: {current_user.email}")
    print(current_user.id)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": f"post with the id {id} does not exist"})

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATING POST BASED ON THE CURRENT OWNER
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    print(f"The Authenticated user is: {current_user.email}")

    post_query = db.query(models.Post).filter(models.Post.id == id)
    found_post = post_query.first()

    if found_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "message": f"post with the id {id} does not exist"})

    if found_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
