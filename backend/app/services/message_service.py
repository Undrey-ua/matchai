from typing import List, Optional
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.models.message import Message
from datetime import datetime

class MessageService(BaseService):
    def __init__(self):
        super().__init__(Message)

    def send_message(self, db: Session, sender_id: int, receiver_id: int, content: str) -> Message:
        message_data = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "content": content
        }
        return self.create(db, message_data)

    def get_chat_messages(self, db: Session, user1_id: int, user2_id: int, skip: int = 0, limit: int = 50) -> List[Message]:
        return db.query(Message).filter(
            ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
            ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
        ).order_by(Message.id.desc()).offset(skip).limit(limit).all()

    def mark_as_read(self, db: Session, message_id: int, user_id: int) -> Optional[Message]:
        message = self.get(db, message_id)
        if message and message.receiver_id == user_id and not message.read_at:
            message.read_at = datetime.utcnow()
            db.commit()
            db.refresh(message)
        return message

    def get_unread_count(self, db: Session, user_id: int) -> int:
        return db.query(Message).filter(
            Message.receiver_id == user_id,
            Message.read_at.is_(None)
        ).count() 