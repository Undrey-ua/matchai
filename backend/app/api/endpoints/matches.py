from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import Match, User
from app.schemas.match import MatchCreate, Match as MatchSchema

router = APIRouter()

@router.post("/", response_model=MatchSchema)
def create_match(match_in: MatchCreate, user_id: int, db: Session = Depends(get_db)):
    """
    Create new match.
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if matched user exists
    matched_user = db.query(User).filter(User.id == match_in.matched_user_id).first()
    if not matched_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matched user not found"
        )
    
    # Check if match already exists
    existing_match = db.query(Match).filter(
        Match.user_id == user_id,
        Match.matched_user_id == match_in.matched_user_id
    ).first()
    if existing_match:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Match already exists"
        )
    
    match = Match(
        user_id=user_id,
        matched_user_id=match_in.matched_user_id,
        similarity_score=match_in.similarity_score
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

@router.get("/user/{user_id}", response_model=List[MatchSchema])
def read_user_matches(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get matches by user ID.
    """
    matches = db.query(Match).filter(Match.user_id == user_id).offset(skip).limit(limit).all()
    return matches

@router.get("/{match_id}", response_model=MatchSchema)
def read_match(match_id: int, db: Session = Depends(get_db)):
    """
    Get match by ID.
    """
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    return match

@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Delete match.
    """
    match = db.query(Match).filter(Match.id == match_id, Match.user_id == user_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    db.delete(match)
    db.commit()
    return None 