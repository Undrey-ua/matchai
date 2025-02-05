import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db
from ..main import app
from ..models import User
from ..schemas import UserCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User",
            "birth_date": "1990-01-01",
            "gender": "male"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"

def test_get_potential_matches(client, test_db):
    # Створюємо тестового користувача
    user = User(
        email="test@example.com",
        hashed_password="hashedpass",
        name="Test User",
        gender="male"
    )
    test_db.add(user)
    test_db.commit()

    # Створюємо токен для аутентифікації
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "password123"}
    )
    token = response.json()["access_token"]

    response = client.get(
        "/users/matches/potential/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200 