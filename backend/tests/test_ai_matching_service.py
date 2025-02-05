import pytest
from app.services.ai_service import AIMatchingService
import numpy as np

@pytest.fixture
def ai_service():
    return AIMatchingService()

@pytest.fixture
def user_service():
    from app.services.user_service import UserService
    return UserService()

@pytest.fixture
def users(db, user_service):
    # Створюємо тестових користувачів з різними інтересами
    users_data = [
        {
            "email": "sport@test.com",
            "password": "password123",
            "name": "Sport Fan",
            "posts": ["Вчора був на футбольному матчі. Неймовірна гра!",
                     "Ранкова пробіжка - найкращий початок дня."],
            "reactions": [
                {"type": "like", "topic": "спорт", "sentiment": "positive"},
                {"type": "comment", "topic": "футбол", "sentiment": "positive"}
            ]
        },
        {
            "email": "tech@test.com",
            "password": "password123",
            "name": "Tech Geek",
            "posts": ["Нова версія Python просто вражає своїми можливостями.",
                     "Штучний інтелект змінює наше життя."],
            "reactions": [
                {"type": "like", "topic": "технології", "sentiment": "positive"},
                {"type": "comment", "topic": "програмування", "sentiment": "positive"}
            ]
        },
        {
            "email": "music@test.com",
            "password": "password123",
            "name": "Music Lover",
            "posts": ["Вчора був на неймовірному концерті!",
                     "Нова пісня улюбленого гурту просто космос."],
            "reactions": [
                {"type": "like", "topic": "музика", "sentiment": "positive"},
                {"type": "comment", "topic": "концерти", "sentiment": "positive"}
            ]
        }
    ]
    
    created_users = []
    for data in users_data:
        user = user_service.create_user(db, {
            "email": data["email"],
            "password": data["password"],
            "name": data["name"]
        })
        created_users.append((user, data))
    
    return created_users

def test_process_social_content(ai_service, users):
    """Тест обробки соціального контенту"""
    user, data = users[0]
    
    # Обробляємо пости
    for post in data["posts"]:
        ai_service.process_social_content(user.id, {"post": post})
    
    # Обробляємо реакції
    for reaction in data["reactions"]:
        ai_service.process_social_content(user.id, {"reaction": reaction})
    
    # Перевіряємо профіль
    profile = ai_service.user_profiles[user.id]
    assert len(profile["posts"]) == len(data["posts"])
    assert len(profile["reactions"]) == len(data["reactions"])
    assert "спорт" in profile["interests"]
    assert profile["vector"] is not None

def test_find_matches(db, ai_service, user_service):
    """Тест пошуку схожих користувачів"""
    # Створюємо тестових користувачів з різними інтересами
    users_data = [
        {
            "email": "sport@test.com",
            "password": "password123",
            "name": "Sport Fan",
            "posts": ["Вчора був на футбольному матчі. Неймовірна гра!",
                     "Ранкова пробіжка - найкращий початок дня."],
            "reactions": [
                {"type": "like", "topic": "спорт", "sentiment": "positive"},
                {"type": "comment", "topic": "футбол", "sentiment": "positive"}
            ]
        },
        {
            "email": "tech@test.com",
            "password": "password123",
            "name": "Tech Geek",
            "posts": ["Нова версія Python просто вражає своїми можливостями.",
                     "Штучний інтелект змінює наше життя."],
            "reactions": [
                {"type": "like", "topic": "технології", "sentiment": "positive"},
                {"type": "comment", "topic": "програмування", "sentiment": "positive"}
            ]
        },
        {
            "email": "music@test.com",
            "password": "password123",
            "name": "Music Lover",
            "posts": ["Вчора був на неймовірному концерті!",
                     "Нова пісня улюбленого гурту просто космос."],
            "reactions": [
                {"type": "like", "topic": "музика", "sentiment": "positive"},
                {"type": "comment", "topic": "концерти", "sentiment": "positive"}
            ]
        }
    ]
    
    created_users = []
    for data in users_data:
        user = user_service.create_user(db, {
            "email": data["email"],
            "password": data["password"],
            "name": data["name"]
        })
        # Обробляємо пости та реакції для кожного користувача
        for post in data["posts"]:
            ai_service.process_social_content(user.id, {"post": post})
        for reaction in data["reactions"]:
            ai_service.process_social_content(user.id, {"reaction": reaction})
        created_users.append(user)
    
    # Шукаємо матчі для першого користувача (Sport Fan)
    matches = ai_service.find_matches(created_users[0].id, db, limit=2)
    
    # Перевіряємо, що є хоча б один матч
    assert len(matches) > 0
    assert all("similarity" in match for match in matches)
    assert all("common_interests" in match for match in matches)
    
    # Перевіряємо сортування за схожістю
    similarities = [match["similarity"] for match in matches]
    assert similarities == sorted(similarities, reverse=True)

def test_extract_interests(ai_service):
    """Тест виявлення інтересів з тексту"""
    text = "Люблю спорт та подорожі, особливо походи в гори."
    interests = ai_service._extract_interests(text)
    assert "спорт" in interests
    assert "подорожі" in interests

def test_update_user_vector(ai_service, users):
    """Тест оновлення векторного представлення користувача"""
    user, data = users[0]
    
    # Спочатку вектор відсутній
    assert ai_service.user_profiles[user.id]["vector"] is None
    
    # Додаємо контент
    ai_service.process_social_content(user.id, {"post": data["posts"][0]})
    
    # Перевіряємо, що вектор створено
    assert ai_service.user_profiles[user.id]["vector"] is not None
    assert isinstance(ai_service.user_profiles[user.id]["vector"], np.ndarray) 