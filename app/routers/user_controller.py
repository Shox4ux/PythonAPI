
from typing import List
from .. import functions, schemas, models
from fastapi import  Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db


router = APIRouter(prefix="/users",tags=['users'])



@router.get("/", response_model=List[schemas.UserBasicResponse])
async def get_users(user: schemas.CreateUser, db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserBasicResponse)
async def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

# Password hashshing is taking place
    user.password = functions.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserBasicResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM words WHERE id = %s ''', (str(id),))
    # sorted_word = cursor.fetchone()
    sorted_word = db.query(models.User).filter(models.User.id == id).first()
    if not sorted_word:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    return sorted_word
