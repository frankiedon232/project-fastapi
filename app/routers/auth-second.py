from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oath2

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    '''
        The form from OAuth2PasswordRequestForm will return from user entry
        Note: the form can return anything, it could email username or id, you deside what it is
        but the name recognise is username and password

        1. username
        2. password

        The we need to get this data in this order and use it accordingly
    '''

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    #  Create a token -  you can add more data if you want to. for this is ust for learning
    access_token = oath2.create_access_token(data={"user_id": user.id})

    #  Return a token - so basically we created a bearer token using JWT, so we can extract the data. Mmmm
    return {"access_token": access_token, "token_type": "bearer"}
