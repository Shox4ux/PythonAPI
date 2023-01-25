from typing import List
from .. import schemas,models,oauth2
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db


router = APIRouter(prefix="/words", tags=['words'])


@router.get("/", response_model=List[schemas.WordBasicResponse])
def get_all_words(db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM words ''')
    # words = cursor.fetchall()
    words = db.query(models.Word).all()
    return words


@router.get("/{id}", response_model=schemas.WordBasicResponse)
def get_word_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM words WHERE id = %s ''', (str(id),))
    # sorted_word = cursor.fetchone()
    sorted_word = db.query(models.Word).filter(models.Word.id == id).first()
    if not sorted_word:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"word with id: {id} was not found")
    return sorted_word


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.WordBasicResponse)
def create_word(word_data: schemas.CreateWord, db: Session = Depends(get_db), id: int= Depends(oauth2.get_current_user_id)):
    # cursor.execute( '''INSERT INTO words (word, transcription, definition, example, level) VALUES (%s,%s,%s,%s,%s) RETURNING * ''' ,
    # (word_data.word,word_data.transcription ,word_data.definition,word_data.example,word_data.level))
    # new_word = cursor.fetchone()
    # conn.commit()

    new_word = models.Word(**word_data.dict())
    db.add(new_word)
    db.commit()
    db.refresh(new_word)

    return new_word


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_word(id: int, db: Session = Depends(get_db)):

    # cursor.execute(
    #     '''DELETE FROM words WHERE id = %s RETURNING * ''', (str(id),))
    # deleted_word = cursor.fetchone()

    delete_word_query = db.query(models.Word).filter(models.Word.id == id)
    if delete_word_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"word with id:{id} does not exist")
    delete_word_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.WordBasicResponse)
def update_word(id: int, word: schemas.CreateWord, db: Session = Depends(get_db)):
    # cursor.execute('''UPDATE words SET word = %s, transcription = %s,definition = %s,example = %s,level = %s WHERE id = %s RETURNING * ''',
    #                (word.word, word.transcription, word.definition, word.example, word.level, str(id),))
    # updated_word = cursor.fetchone()
    # conn.commit()
    updated_word_query = db.query(models.Word).filter(models.Word.id == id)
    word_sql_alchemy = updated_word_query.first()

    if word_sql_alchemy == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"word with id:{id} does not exist")
    updated_word_query.update(word.dict(), synchronize_session=False)
    db.commit()
    return updated_word_query.first()