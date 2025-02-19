from datetime import datetime
from pydantic import BaseModel

class MatchBase(BaseModel):
    matched_user_id: int
    similarity_score: float

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
