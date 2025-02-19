from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
# from app.api.routes import router
from app.services.chat import handle_chat_connection
from app.core.middleware import LoggingMiddleware, ErrorHandlingMiddleware
from app.api.endpoints import users, posts, likes, matches

app = FastAPI(
    title="MatchAI API",
    description="""
    MatchAI API - система для знаходження схожих користувачів на основі їхніх інтересів.
    
    ## Користувачі
    * Створення нового користувача
    * Отримання списку користувачів
    * Перевірка на дублікати email
    
    ## Функціональність
    * Реєстрація користувачів з інтересами
    * Автоматичне створення векторів інтересів
    * Пошук схожих користувачів
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
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
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(likes.router, prefix="/api/likes", tags=["likes"])
app.include_router(matches.router, prefix="/api/matches", tags=["matches"])

@app.get("/")
def read_root():
    return {
        "app": "MatchAI API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    } 