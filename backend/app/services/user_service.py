from app.services.base import BaseService
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from typing import Optional

class UserService(BaseService):
    def __init__(self):
        super().__init__(User)

    def create_user(self, db: Session, user_data: dict) -> User:
        hashed_password = get_password_hash(user_data.pop('password'))
        user_data['hashed_password'] = hashed_password
        return self.create(db, user_data)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email)
        if not user or not user.verify_password(password):
            return None
        return user 