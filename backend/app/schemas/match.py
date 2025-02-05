from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MatchBase(BaseModel):
    user_id: int
    matched_user_id: int
    status: str = "pending"  # pending, accepted, rejected

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
