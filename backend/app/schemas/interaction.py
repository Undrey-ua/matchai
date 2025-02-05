from pydantic import BaseModel

class InteractionCreate(BaseModel):
    type: str
    target_id: int
