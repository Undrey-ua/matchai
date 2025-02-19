from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    interests: List[str] = []
    age: Optional[int] = None
    location: Optional[str] = None
    social_links: List[str] = []

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool = True
    interest_vector: List[float] = []
    last_update: datetime

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str
