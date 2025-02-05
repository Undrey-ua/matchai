from sqlalchemy.orm import Session
from app.models.user import User

def get_or_create_user(db: Session, email: str, social_accounts: dict, profile_data: dict):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            social_accounts=social_accounts,
            profile_data=profile_data
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user 