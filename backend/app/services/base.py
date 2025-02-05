from typing import Any, Optional
from sqlalchemy.orm import Session
from app.core.database import Base

class BaseService:
    def __init__(self, model: Any):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[Any]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: dict) -> Any:
        obj = self.model(**obj_in)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, id: int, obj_in: dict) -> Optional[Any]:
        obj = self.get(db, id)
        if obj:
            for key, value in obj_in.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int) -> bool:
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False 