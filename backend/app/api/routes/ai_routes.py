from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.ai_service import AIMatchingService
from app.schemas.interaction import InteractionCreate

router = APIRouter()

@router.get("/matches/recommended/")
async def get_recommended_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ai_service = AIMatchingService()
    matches = ai_service.find_matches(current_user.id, db)
    return matches

@router.post("/interactions/")
async def record_interaction(
    interaction: InteractionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ai_service = AIMatchingService()
    ai_service.update_recommendations(
        current_user.id,
        interaction.type,
        interaction.target_id
    )
    return {"status": "success"}