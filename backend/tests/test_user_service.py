import pytest
from app.services.user_service import UserService

def test_create_user(db, user_service):
    user_data = {
        "email": "test@example.com",
        "password": "testpass123",
        "name": "Test User"
    }
    user = user_service.create_user(db, user_data)
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert hasattr(user, "hashed_password")

def test_get_user(db, user_service):
    # Створюємо користувача
    user_data = {
        "email": "test@example.com",
        "password": "testpass123",
        "name": "Test User"
    }
    created_user = user_service.create_user(db, user_data)
    
    # Отримуємо користувача
    user = user_service.get(db, created_user.id)
    assert user is not None
    assert user.email == "test@example.com"

def test_authenticate_user(db, user_service):
    # Створюємо користувача
    user_data = {
        "email": "test@example.com",
        "password": "testpass123",
        "name": "Test User"
    }
    user_service.create_user(db, user_data)
    
    # Тестуємо автентифікацію
    authenticated_user = user_service.authenticate(
        db, 
        "test@example.com", 
        "testpass123"
    )
    assert authenticated_user is not None
    
    # Тестуємо неправильний пароль
    wrong_auth = user_service.authenticate(
        db, 
        "test@example.com", 
        "wrongpass"
    )
    assert wrong_auth is None 