# Messages API

## WebSocket Connection
WebSocket endpoint: ws://domain.com/ws/{user_id}

## REST Endpoints

### GET /api/v1/messages/{user_id}
Get conversation history with specific user.

**Headers:**
Authorization: Bearer {token}

**Response:**
```json
[
    {
        "id": 1,
        "sender_id": 1,
        "receiver_id": 2,
        "content": "Hello!",
        "created_at": "2024-03-20T12:00:00Z",
        "read_at": null
    }
]

POST /api/v1/messages/
Send a new message.
Headers:
Authorization: Bearer {token}
Request Body:
{
    "receiver_id": 2,
    "content": "Hello!"
}
