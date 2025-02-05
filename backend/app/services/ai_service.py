from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.base import BaseService
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
from transformers import pipeline
from app.services.category_service import CategoryService

class AIMatchingService(BaseService):
    def __init__(self, category_service: CategoryService):
        super().__init__(User)
        self.category_service = category_service
        self.classifier = pipeline(
            "zero-shot-classification",
            model="youscan/ukrainian-bert-base"
        )
        self.categories = []  # Буде заповнено з БД
        self.user_profiles = defaultdict(
            lambda: {
                'posts': [],
                'interests': defaultdict(float),
                'reactions': [],
                'vector': None
            }
        )
        # Розширений список ключових слів українською
        self.keywords = {
            'спорт': ['спорт', 'футбол', 'пробіжка', 'тренування', 'матч'],
            'музика': ['музика', 'концерт', 'пісня', 'гурт'],
            'технології': ['технології', 'python', 'програмування', 'штучний інтелект'],
            'подорожі': ['подорожі', 'похід', 'гори', 'мандрівка'],
            'їжа': ['їжа', 'кухня', 'ресторан', 'готування']
        }

    def initialize_categories(self, db: Session):
        """Ініціалізує категорії з бази даних"""
        categories = self.category_service.get_all_active(db)
        self.categories = [cat.name for cat in categories]
        if not self.categories:
            # Якщо категорій немає, створюємо базові
            created = self.category_service.create_default_categories(db)
            self.categories = [cat.name for cat in created]

    def process_social_content(self, user_id: int, content: Dict[str, Any]) -> None:
        """Обробка контенту з соціальних мереж"""
        profile = self.user_profiles[user_id]
        
        # Обробка постів
        if 'post' in content:
            profile['posts'].append(content['post'])
            # Аналіз тематики поста і додавання інтересів
            interests = self._extract_interests(content['post'])
            profile['interests'].update(interests)
        
        # Обробка реакцій
        if 'reaction' in content:
            profile['reactions'].append(content['reaction'])
            if 'topic' in content['reaction']:
                profile['interests'].add(content['reaction']['topic'])
        
        # Оновлення вектора користувача
        self._update_user_vector(user_id)

    def _extract_interests(self, text: str) -> set:
        """Витягує теми та інтереси з тексту"""
        text = text.lower()
        interests = set()
        
        for category, keywords in self.keywords.items():
            if any(keyword in text for keyword in keywords):
                interests.add(category)
        
        return interests

    def _update_user_vector(self, user_id: int) -> None:
        """Оновлює векторне представлення користувача"""
        profile = self.user_profiles[user_id]
        
        # Об'єднуємо всі текстові дані
        texts = profile['posts'].copy()
        
        # Додаємо інтереси
        texts.extend(list(profile['interests']))
        
        # Додаємо реакції
        for reaction in profile['reactions']:
            if 'topic' in reaction:
                texts.append(reaction['topic'])
        
        if texts:
            # Перетворюємо всі тексти в один документ
            document = ' '.join(texts)
            # Оновлюємо векторайзер на всіх текстах
            self.vectorizer.fit([document])
            # Трансформуємо документ
            profile['vector'] = self.vectorizer.transform([document]).toarray()[0]

    def find_matches(self, user_id: int, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Знаходить найбільш схожих користувачів"""
        user_vector = self.user_profiles[user_id]['vector']
        if user_vector is None:
            return []

        matches = []
        all_users = db.query(User).filter(User.id != user_id).all()

        for other_user in all_users:
            if other_user.id in self.user_profiles and self.user_profiles[other_user.id]['vector'] is not None:
                other_vector = self.user_profiles[other_user.id]['vector']
                # Перевіряємо розмірність векторів
                if user_vector.shape == other_vector.shape:
                    similarity = cosine_similarity([user_vector], [other_vector])[0][0]
                    common_interests = self.user_profiles[user_id]['interests'] & \
                                     self.user_profiles[other_user.id]['interests']
                    
                    matches.append({
                        "user": other_user,
                        "similarity": float(similarity),
                        "common_interests": list(common_interests)
                    })

        # Сортуємо за схожістю
        matches.sort(key=lambda x: x["similarity"], reverse=True)
        return matches[:limit]

    def update_recommendations(self, user_id: int, interaction_type: str, target_id: int) -> None:
        """Оновлює рекомендації на основі взаємодій користувача"""
        interaction_data = {
            "type": interaction_type,
            "target_id": target_id
        }
        self.process_social_content(user_id, interaction_data)