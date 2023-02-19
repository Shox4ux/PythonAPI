from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from . import schemas, database, models
from sqlalchemy.orm import Session
from .confige import settings

token_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes




def create_auth_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_auth_token(token: str, credential_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credential_exceptions
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exceptions

    return token_data


def get_current_user_id(token: str = Depends(token_schema), db: Session = Depends(database.get_db)):

    credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={'WWW-Autendicate': 'Bearer'})
    token = verify_auth_token(token,credential_exceptions)

    user: models.User = db.query(models.User).filter(models.User.id == token.id).first()
    return user
