import pytest
from app.services.message_service import MessageService
from app.services.user_service import UserService

@pytest.fixture
def message_service():
    return MessageService()

@pytest.fixture
def users(db, user_service):
    # Створюємо двох тестових користувачів
    user1 = user_service.create_user(db, {
        "email": "user1@test.com",
        "password": "password123",
        "name": "User One"
    })
    user2 = user_service.create_user(db, {
        "email": "user2@test.com",
        "password": "password123",
        "name": "User Two"
    })
    return user1, user2

def test_send_message(db, message_service, users):
    user1, user2 = users
    message = message_service.send_message(
        db, 
        sender_id=user1.id, 
        receiver_id=user2.id, 
        content="Hello!"
    )
    assert message.content == "Hello!"
    assert message.sender_id == user1.id
    assert message.receiver_id == user2.id
    assert message.read_at is None

def test_get_chat_messages(db, message_service, users):
    user1, user2 = users
    # Відправляємо кілька повідомлень
    message_service.send_message(db, user1.id, user2.id, "Hi!")
    message_service.send_message(db, user2.id, user1.id, "Hello!")
    message_service.send_message(db, user1.id, user2.id, "How are you?")
    
    # Отримуємо історію чату
    messages = message_service.get_chat_messages(db, user1.id, user2.id)
    assert len(messages) == 3
    assert messages[0].content == "How are you?"  # останнє повідомлення перше (desc order)

def test_mark_as_read(db, message_service, users):
    user1, user2 = users
    # Відправляємо повідомлення
    message = message_service.send_message(db, user1.id, user2.id, "Test message")
    assert message.read_at is None
    
    # Позначаємо як прочитане
    updated_message = message_service.mark_as_read(db, message.id, user2.id)
    assert updated_message.read_at is not None

def test_get_unread_count(db, message_service, users):
    user1, user2 = users
    # Відправляємо кілька повідомлень
    message_service.send_message(db, user1.id, user2.id, "Message 1")
    message_service.send_message(db, user1.id, user2.id, "Message 2")
    message_service.send_message(db, user2.id, user1.id, "Message 3")
    
    # Перевіряємо кількість непрочитаних
    assert message_service.get_unread_count(db, user2.id) == 2
    assert message_service.get_unread_count(db, user1.id) == 1 