# Users API

## Endpoints

### GET /api/v1/users/me
Get current user profile.

**Headers:**
Authorization: Bearer {token}

**Response:**
```json
{
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "birth_date": "1990-01-01",
    "gender": "male",
    "bio": "About me...",
    "location": "New York",
    "interests": ["sports", "music"],
    "preferences": {
        "age_range": [25, 35],
        "distance": 50
    }
}

### PUT /api/v1/users/me
Update current user profile.

**Headers:**
Authorization: Bearer {token}

**Request Body:**
{
    "name": "John Doe",
    "bio": "New bio...",
    "location": "New York",
    "interests": ["sports", "music"],
    "preferences": {
        "age_range": [25, 35],
        "distance": 50
    }
}
