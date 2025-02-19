from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
    content: str
    source: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True 