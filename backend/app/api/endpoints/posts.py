from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import Post, User
from app.schemas.post import PostCreate, Post as PostSchema

router = APIRouter()

@router.post("/", response_model=PostSchema)
def create_post(post_in: PostCreate, user_id: int, db: Session = Depends(get_db)):
    """
    Create new post.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    post = Post(
        content=post_in.content,
        source=post_in.source,
        user_id=user_id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/", response_model=List[PostSchema])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve posts.
    """
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

@router.get("/user/{user_id}", response_model=List[PostSchema])
def read_user_posts(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get posts by user ID.
    """
    posts = db.query(Post).filter(Post.user_id == user_id).offset(skip).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=PostSchema)
def read_post(post_id: int, db: Session = Depends(get_db)):
    """
    Get post by ID.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post 