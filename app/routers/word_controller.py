from typing import List, Optional
from .. import schemas, models, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, get_db


router = APIRouter(prefix="/words", tags=['words'])


@router.get("/", response_model=List[schemas.WordOut])
def get_all_words(db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user_id),
                  word_limit: int = 5, skip: int = 0, search: Optional[str] = ""):

    print(word_limit)
    # cursor.execute('''SELECT * FROM words ''')
    # words = cursor.fetchall()

    words = db.query(models.Word, func.count(models.Vote.word_id).label("votes")).join(
        models.Vote, models.Vote.word_id == models.Word.id, isouter=True).group_by(models.Word.id).filter(models.Word.word.contains(
            search)).limit(limit=word_limit).offset(offset=skip).all()

    return words


@router.get("/{id}", response_model=schemas.WordOut)
def get_word_by_id(id: int, db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user_id)):
    # cursor.execute('''SELECT * FROM words WHERE id = %s ''', (str(id),))
    # sorted_word = cursor.fetchone()
    sorted_word = db.query(models.Word, func.count(models.Vote.word_id).label("votes")).join(
        models.Vote, models.Vote.word_id == models.Word.id, isouter=True).group_by(models.Word.id).filter(models.Word.id == id).first()


   
    if not sorted_word:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"word with id: {id} was not found")

    # if sorted_word.owner_id != user_id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
    return sorted_word


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.WordBasicResponse)
def create_word(word_data: schemas.CreateWord, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user_id)):
    # cursor.execute( '''INSERT INTO words (word, transcription, definition, example, level) VALUES (%s,%s,%s,%s,%s) RETURNING * ''' ,
    # (word_data.word,word_data.transcription ,word_data.definition,word_data.example,word_data.level))
    # new_word = cursor.fetchone()
    # conn.commit()

    print(user.email)
    new_word = models.Word(owner_id=user.id, **word_data.dict())
    db.add(new_word)
    db.commit()
    db.refresh(new_word)

    return new_word


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_word(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user_id)):

    # cursor.execute(
    #     '''DELETE FROM words WHERE id = %s RETURNING * ''', (str(id),))
    # deleted_word = cursor.fetchone()

    word_delete_query = db.query(models.Word).filter(models.Word.id == id)
    word_to_delete = word_delete_query.first()

    if word_to_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"word with id:{id} does not exist")

    if word_to_delete.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    word_delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.WordBasicResponse)
def update_word(id: int, word: schemas.CreateWord, db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user_id)):
    # cursor.execute('''UPDATE words SET word = %s, transcription = %s,definition = %s,example = %s,level = %s WHERE id = %s RETURNING * ''',
    #                (word.word, word.transcription, word.definition, word.example, word.level, str(id),))
    # updated_word = cursor.fetchone()
    # conn.commit()
    updated_word_query = db.query(models.Word).filter(models.Word.id == id)
    word_to_update = updated_word_query.first()

    if word_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"word with id:{id} does not exist")

    if word_to_update.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    updated_word_query.update(word.dict(), synchronize_session=False)
    db.commit()
    return updated_word_query.first()
