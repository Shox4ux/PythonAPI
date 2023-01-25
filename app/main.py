from typing import Optional, List
from fastapi.params import Body
from fastapi import FastAPI, Response, status, HTTPException, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import functions, models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import user_controller,word_controller, auth


models.Base.metadata.create_all(bind=engine)


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


app.include_router(user_controller.router)
app.include_router(word_controller.router)
app.include_router(auth.router)





