from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.security import verify_password

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    birth_date = Column(Date)
    gender = Column(String)
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    profile_photo = Column(String, nullable=True)
    interests = Column(JSON, nullable=True)
    preferences = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    social_accounts = Column(JSON)  # Зберігаємо токени доступу
    profile_data = Column(JSON)     # Зберігаємо дані профілю

    # Relationships
    sent_messages = relationship("app.models.message.Message", foreign_keys="app.models.message.Message.sender_id", back_populates="sender")
    received_messages = relationship("app.models.message.Message", foreign_keys="app.models.message.Message.receiver_id", back_populates="receiver")

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password) 