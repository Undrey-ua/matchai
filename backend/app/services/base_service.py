from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from .utils import get_password_hash

class UserService:
    @staticmethod
    def create_user(db: Session, user: schemas.UserCreate) -> models.User:
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            email=user.email,
            hashed_password=hashed_password,
            name=user.name,
            birth_date=user.birth_date,
            gender=user.gender,
            bio=user.bio,
            location=user.location,
            interests=user.interests,
            preferences=user.preferences
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_potential_matches(db: Session, user_id: int, limit: int = 10) -> List[models.User]:
        # Логіка для отримання потенційних матчів
        return db.query(models.User)\
            .filter(models.User.id != user_id)\
            .limit(limit)\
            .all()

class MessageService:
    @staticmethod
    def create_message(db: Session, message: schemas.MessageCreate, sender_id: int) -> models.Message:
        db_message = models.Message(
            content=message.content,
            sender_id=sender_id,
            receiver_id=message.receiver_id
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    @staticmethod
    def get_conversation(db: Session, user1_id: int, user2_id: int) -> List[models.Message]:
        return db.query(models.Message)\
            .filter(
                ((models.Message.sender_id == user1_id) & 
                 (models.Message.receiver_id == user2_id)) |
                ((models.Message.sender_id == user2_id) & 
                 (models.Message.receiver_id == user1_id))
            )\
            .order_by(models.Message.created_at.asc())\
            .all()

class MatchService:
    @staticmethod
    def create_match(db: Session, user_id: int, matched_user_id: int) -> models.Match:
        db_match = models.Match(
            user_id=user_id,
            matched_user_id=matched_user_id,
            status="liked"
        )
        db.add(db_match)
        db.commit()
        db.refresh(db_match)
        
        # Перевірка на взаємний матч
        existing_match = db.query(models.Match)\
            .filter_by(user_id=matched_user_id, matched_user_id=user_id)\
            .first()
            
        if existing_match:
            db_match.status = "matched"
            existing_match.status = "matched"
            db.commit()
            
        return db_match 