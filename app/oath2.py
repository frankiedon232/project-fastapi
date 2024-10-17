from jose import JWSError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#  SECRET_KEY
SECRET_KEY = settings.secrete_key
#  Algorithm
ALGORITHM = settings.algorithms
#  Expiration Time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# CREATING JWT TOKEN AND ENCODING IT
def create_access_token(data: dict):
    to_encode = data.copy()

    # utcnow is deprecated so i used (.now(datetime.timezone.utc))
    '''
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    '''
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# DECODING JWT TOKEN AND VERFYING IT
def very_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except Exception as e:
        print(f"The error is: {e}")
        raise credentials_exception

    return token_data


# GET THE CURRENT LOGGED IN USER BASED ON THE VERIFIED TOKEN
# INCLUDING DATABASE DEPENDENCY AGAIN AGAIN IN CASE WE NEED IT
def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # YOU CAN FURTHER USER THE JWT DATA TO QUERY YOUR DATABASE IF YOU WANT TO LIKE SO:
    token = very_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
