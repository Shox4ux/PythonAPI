from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException ,status
from . import schemas

token_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_auth_token(token:str, credential_exceptions):
    try:
        payload = jwt.encode(token,SECRET_KEY,algorithm=ALGORITHM)

        id : str = payload.get("user_id")

        if id is None:
            raise credential_exceptions 
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exceptions

    return token_data    




def create_auth_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user_id(token:str = Depends(token_schema)):

    credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
     detail=f"Could not validate credentials", headers={'WWW-Autendicate':'Bearer'})
    return verify_auth_token(token,credential_exceptions=credential_exceptions)
        