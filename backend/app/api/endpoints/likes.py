from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import Like, Post, User
from app.schemas.like import LikeCreate, Like as LikeSchema

router = APIRouter()

@router.post("/", response_model=LikeSchema)
def create_like(like_in: LikeCreate, user_id: int, db: Session = Depends(get_db)):
    """
    Create new like.
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if post exists
    post = db.query(Post).filter(Post.id == like_in.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Check if like already exists
    existing_like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == like_in.post_id
    ).first()
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already liked"
        )
    
    like = Like(
        user_id=user_id,
        post_id=like_in.post_id
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

@router.get("/user/{user_id}", response_model=List[LikeSchema])
def read_user_likes(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get likes by user ID.
    """
    likes = db.query(Like).filter(Like.user_id == user_id).offset(skip).limit(limit).all()
    return likes

@router.delete("/{like_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_like(like_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Delete like.
    """
    like = db.query(Like).filter(Like.id == like_id, Like.user_id == user_id).first()
    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Like not found"
        )
    
    db.delete(like)
    db.commit()
    return None 