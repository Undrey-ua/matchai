# Authentication API

## Overview
The authentication system uses JWT (JSON Web Tokens) for secure API access.

## Endpoints

### POST /api/v1/auth/register
Register a new user.

**Request Body:**
```json
{
"email": "user@example.com",
"password": "securepassword",
"name": "John Doe",
"birth_date": "1990-01-01",
"gender": "male"
}

**Response:**
```json
{
"id": 1,
"email": "user@example.com",
"name": "John Doe",
"token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

### POST /api/v1/auth/login
Login with existing credentials.

**Request Body:**
```json
{
"email": "user@example.com",
"password": "securepassword"
}
```

**Response:**
```json
{
"access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
"token_type": "bearer"
}
```
