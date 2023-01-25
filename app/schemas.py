from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class WordBase(BaseModel):
    word: str
    transcription: str
    definition: str
    example: str
    level: str


class CreateWord(WordBase):
    pass


class WordBasicResponse(WordBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    fullname: str
    email: EmailStr
    password: str


class UserBasicResponse(BaseModel):
    fullname: str
    email: EmailStr
    created_at: datetime

    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id: Optional[str]= None