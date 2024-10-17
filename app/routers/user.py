from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from .. import models, schemas, utils, oath2


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# CREATING USERS


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    print(f"The Authenticated user is: {current_user.email}")

    # Check if this user exists
    check_user = db.query(models.User).filter(
        models.User.email == user.email).first()

    if check_user != None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"A user with this information already exists")

    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# USER ACCOUNT RETRIEVAL
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    print(f"The Authenticated user is: {current_user.email}")

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exists")

    return user
