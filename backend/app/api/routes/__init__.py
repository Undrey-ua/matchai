from fastapi import APIRouter
from .user_routes import router as user_router
from .ai_routes import router as ai_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(ai_router, prefix="/ai", tags=["ai"])
