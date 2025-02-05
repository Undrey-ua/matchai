from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, services
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.UserService.create_user(db=db, user=user)

@router.get("/users/matches/potential/", response_model=List[schemas.User])
def get_potential_matches(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return services.UserService.get_potential_matches(db=db, user_id=current_user.id)

@router.post("/matches/{user_id}", response_model=schemas.Match)
def create_match(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return services.MatchService.create_match(
        db=db,
        user_id=current_user.id,
        matched_user_id=user_id
    )

@router.post("/messages/", response_model=schemas.Message)
def create_message(
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return services.MessageService.create_message(
        db=db,
        message=message,
        sender_id=current_user.id
    )

@router.get("/messages/{user_id}", response_model=List[schemas.Message])
def get_conversation(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return services.MessageService.get_conversation(
        db=db,
        user1_id=current_user.id,
        user2_id=user_id
    ) 