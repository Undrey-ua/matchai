# Matches API

## Endpoints

### GET /api/v1/matches/potential
Get potential matches.

**Headers:**
Authorization: Bearer {token}

**Response:**
```json
[
    {
        "id": 2,
        "name": "Jane Doe",
        "bio": "About Jane...",
        "location": "New York",
        "interests": ["art", "travel"],
        "compatibility_score": 0.85
    }
]

### POST /api/v1/matches/{user_id}
Like or match with a user.

**Headers:**
Authorization: Bearer {token}

**Response:**
```json
{
    "match_id": 1,
    "status": "liked",
    "created_at": "2024-03-20T12:00:00Z"
}