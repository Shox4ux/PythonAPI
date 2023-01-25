from typing import List
from .. import functions, schemas, models, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=['authendication'])


@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm =  Depends(), db: Session = Depends(get_db)):
    user: models.User = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    if not functions.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    access_token = oauth2.create_auth_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
