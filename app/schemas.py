from pydantic import BaseModel, EmailStr, conint
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


class UserBasicResponse(BaseModel):
    fullname: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class WordBasicResponse(WordBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserBasicResponse

    class Config:
        orm_mode = True


class WordOut(BaseModel):
    Word: WordBasicResponse
    votes: int


class CreateUser(BaseModel):
    fullname: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    word_id: int
    dir: conint(le=1)
