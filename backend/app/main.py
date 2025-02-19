from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
# from app.api.routes import router
from app.services.chat import handle_chat_connection
from app.core.middleware import LoggingMiddleware, ErrorHandlingMiddleware
from app.api.endpoints import users, posts, likes, matches

description = """
# MatchAI API

API для системи знаходження схожих користувачів на основі їхніх інтересів.

## Функціональність

### Користувачі
* 👤 Реєстрація нових користувачів
* 📋 Отримання списку користувачів
* ✅ Валідація email на унікальність

### Пости
* 📝 Створення постів
* 📚 Отримання постів користувача

### Лайки
* ❤️ Додавання лайків
* 👍 Отримання лайків користувача

### Матчі
* 🤝 Пошук схожих користувачів
* 📊 Розрахунок схожості інтересів
"""

app = FastAPI(
    title="MatchAI API",
    description=description,
    version="1.0.0",
    contact={
        "name": "MatchAI Team",
        "url": "https://github.com/undrey-ua/matchai",
    },
    license_info={
        "name": "MIT",
    }
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

# Routes
# app.include_router(router, prefix=settings.API_V1_STR)

# WebSocket
app.websocket("/ws/{user_id}")(handle_chat_connection)

# Роутери
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(
    users.router,
    prefix="/api/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    posts.router,
    prefix="/api/posts",
    tags=["Posts"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    likes.router,
    prefix="/api/likes",
    tags=["Likes"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    matches.router,
    prefix="/api/matches",
    tags=["Matches"],
    responses={404: {"description": "Not found"}},
)

@app.get("/", tags=["Root"])
def read_root():
    """
    Отримати базову інформацію про API.
    """
    return {
        "name": "MatchAI API",
        "version": "1.0.0",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    } 