import pytest
from app.services.ai_service import AIMatchingService
from app.services.user_service import UserService

@pytest.fixture
def ai_service():
    return AIMatchingService()

@pytest.fixture
def users(db, user_service):
    # Створюємо тестових користувачів
    users = []
    for i in range(5):
        user = user_service.create_user(db, {
            "email": f"user{i}@test.com",
            "password": "password123",
            "name": f"User {i}"
        })
        users.append(user)
    return users

def test_initial_features(ai_service, users, db):
    """Тест початкової ініціалізації векторів характеристик"""
    user = users[0]
    limit = 3
    matches = ai_service.find_matches(user.id, db, limit=limit)
    assert len(matches) == min(limit, len(users) - 1)  # або ліміт, або всі користувачі крім себе
    assert all("similarity" in match for match in matches)
    assert all("user" in match for match in matches)

def test_update_user_features(ai_service):
    """Тест оновлення характеристик користувача"""
    user_id = 1
    # Перевіряємо, що вектор створюється при першому оновленні
    ai_service.update_user_features(user_id, {"type": "like", "target_id": 2})
    assert user_id in ai_service.user_features
    
    # Зберігаємо початковий вектор
    initial_vector = ai_service.user_features[user_id].copy()
    
    # Оновлюємо характеристики і перевіряємо, що вектор змінився
    ai_service.update_user_features(user_id, {"type": "like", "target_id": 3})
    assert not (ai_service.user_features[user_id] == initial_vector).all()

def test_find_matches(db, ai_service, users):
    """Тест пошуку збігів"""
    main_user = users[0]
    
    # Оновлюємо характеристики для всіх користувачів
    for user in users:
        ai_service.update_user_features(user.id, {"type": "like", "target_id": main_user.id})
    
    # Шукаємо збіги
    matches = ai_service.find_matches(main_user.id, db, limit=3)
    
    # Перевіряємо результати
    assert len(matches) == min(3, len(users) - 1)  # -1 бо виключаємо самого користувача
    assert all("similarity" in match for match in matches)
    assert all("user" in match for match in matches)
    
    # Перевіряємо сортування за схожістю
    similarities = [match["similarity"] for match in matches]
    assert similarities == sorted(similarities, reverse=True)

def test_update_recommendations(ai_service, users):
    """Тест оновлення рекомендацій"""
    user = users[0]
    target = users[1]
    
    # Зберігаємо початковий стан
    ai_service.update_user_features(user.id, {"type": "view", "target_id": target.id})
    initial_vector = ai_service.user_features[user.id].copy()
    
    # Оновлюємо рекомендації
    ai_service.update_recommendations(user.id, "like", target.id)
    
    # Перевіряємо, що вектор змінився
    assert not (ai_service.user_features[user.id] == initial_vector).all() 