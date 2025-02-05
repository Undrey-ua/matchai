from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router
from app.services.chat import handle_chat_connection
from app.core.middleware import LoggingMiddleware, ErrorHandlingMiddleware
from app.api.endpoints import auth, categories
from app.core.oauth import oauth

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
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
app.include_router(router, prefix=settings.API_V1_STR)

# WebSocket
app.websocket("/ws/{user_id}")(handle_chat_connection)

# Ініціалізація OAuth
oauth.init_app(app)

# Роутери
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])

@app.get("/")
async def root():
    return {"message": "Welcome to Dating Service API"} 