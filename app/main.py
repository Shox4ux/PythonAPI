from typing import Optional
from fastapi.params import Body
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


class Word(BaseModel):
    word: str
    transcription: str
    definition: str
    example: str
    level: str


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres',
                                user='postgres', password='shox2005', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Successfully connected to database')
        break
    except Exception as error:
        print('Error:', error)
    time.sleep(3)

app = FastAPI()


@app.get("/sqlalchemy")
def get_alchemy(db: Session = Depends(get_db)):
    words = db.query(models.Word).all()
    return {"data": words}


@app.get("/words")
def get_all_words(db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM words ''')
    # words = cursor.fetchall()
    words = db.query(models.Word).all()
    return {"words": words}


@app.get("/words/{id}")
def get_word_by_id(id: int):
    cursor.execute('''SELECT * FROM words WHERE id = %s ''', (str(id),))
    sorted_word = cursor.fetchone()
    if not sorted_word:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"word with id: {id} was not found")
    return {"word_detail": sorted_word}


@app.post("/words", status_code=status.HTTP_201_CREATED)
def create_word(word_data: Word):
    # cursor.execute( '''INSERT INTO words (word, transcription, definition, example, level) VALUES (%s,%s,%s,%s,%s) RETURNING * ''' ,
    # (word_data.word,word_data.transcription ,word_data.definition,word_data.example,word_data.level))

    # new_word = cursor.fetchone()
    # conn.commit()
    new_word = models.Word(
        word=word_data.word,
        transcription=word_data.transcription, definition=word_data.definition,
        example=word_data.example
    )

    return {"word_data": new_word}


@app.delete("/words/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_word(id: int):
    cursor.execute(
        '''DELETE FROM words WHERE id = %s RETURNING * ''', (str(id),))
    deleted_word = cursor.fetchone()
    if deleted_word == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"word with id:{id} does not exist")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/words/{id}")
def update_word(id: int, word: Word):
    cursor.execute('''UPDATE words SET word = %s, transcription = %s,definition = %s,example = %s,level = %s WHERE id = %s RETURNING * ''',
                   (word.word, word.transcription, word.definition, word.example, word.level, str(id),))
    updated_word = cursor.fetchone()
    conn.commit()

    if updated_word == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"word with id:{id} does not exist")
    return {"data": updated_word}
