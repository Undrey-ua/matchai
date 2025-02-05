# System Design

## Architecture Overview

```plaintext
                     ┌─────────────┐
                     │   Client    │
                     └──────┬──────┘
                            │
                     ┌──────┴──────┐
                     │    Nginx    │
                     └──────┬──────┘
                            │
       ┌────────────────────┴────────────────────┐
       │                                         │
┌──────┴──────┐                           ┌──────┴──────┐
│   Frontend  │                           │   Backend   │
└──────┬──────┘                           └──────┬──────┘
       │                                         │
       │                                  ┌──────┴──────┐
       │                                  │  Database   │
       │                                  └─────────────┘
       │
┌──────┴──────┐
│    Redis    │
└─────────────┘
```

## Components

1. **Frontend**
   - React/TypeScript application
   - Redux for state management
   - WebSocket for real-time chat

2. **Backend**
   - FastAPI application
   - JWT authentication
   - WebSocket support
   - AI matching algorithm

3. **Database**
   - PostgreSQL
   - User profiles
   - Matches
   - Messages

4. **Cache**
   - Redis
   - Session storage
   - Real-time features

