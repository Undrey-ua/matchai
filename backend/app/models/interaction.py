from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from datetime import datetime
from app.core.database import Base

class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    target_id = Column(Integer, ForeignKey("users.id"))
    interaction_type = Column(String)  # like, view, message
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)  # Додаткові дані про взаємодію