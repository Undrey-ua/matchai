from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.category import Category
from app.services.base import BaseService

class CategoryService(BaseService):
    def __init__(self):
        super().__init__(Category)

    def create_default_categories(self, db: Session) -> List[Category]:
        """Створює базовий набір категорій"""
        default_categories = [
            {
                "name": "спорт і фітнес",
                "description": "Спорт, фізична активність, здоровий спосіб життя",
                "metadata": {
                    "keywords": ["спорт", "фітнес", "тренування", "змагання"]
                }
            },
            {
                "name": "технології та IT",
                "description": "Програмування, гаджети, інновації",
                "metadata": {
                    "keywords": ["програмування", "комп'ютери", "технології"]
                }
            },
            # Додайте інші категорії...
        ]

        categories = []
        for cat_data in default_categories:
            if not self.get_by_name(db, cat_data["name"]):
                category = self.create(db, cat_data)
                categories.append(category)
        
        return categories

    def get_by_name(self, db: Session, name: str) -> Optional[Category]:
        """Отримує категорію за назвою"""
        return db.query(Category).filter(Category.name == name).first()

    def get_all_active(self, db: Session) -> List[Category]:
        """Отримує всі активні категорії"""
        return db.query(Category).all() 