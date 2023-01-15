from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class Word(Base):
    __tablename__ = 'word_database' 

    id = Column(Integer,primary_key= True,nullable=False)
    word = Column(String,nullable=False)
    transcription = Column(String,nullable=False)
    definition = Column(String,nullable=False)
    example = Column(String,nullable=False)
    level = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))






