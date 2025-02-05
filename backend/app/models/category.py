from sqlalchemy import Column, Integer, String, JSON
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    parent_id = Column(Integer, nullable=True)  # Для ієрархії категорій
    settings = Column(JSON, nullable=True)  # Змінили metadata на settings 