from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List, Dict

class UserBase(BaseModel):
    email: EmailStr
    name: str
    birth_date: date
    gender: str
    bio: Optional[str] = None
    location: Optional[str] = None
    interests: Optional[List[str]] = None
    preferences: Optional[Dict] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    interests: Optional[List[str]] = None
    preferences: Optional[Dict] = None
    profile_photo: Optional[str] = None

class User(UserBase):
    id: int
    profile_photo: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    receiver_id: int

class Message(MessageBase):
    id: int
    sender_id: int
    receiver_id: int
    read_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True

class MatchBase(BaseModel):
    matched_user_id: int
    status: str

class Match(MatchBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 