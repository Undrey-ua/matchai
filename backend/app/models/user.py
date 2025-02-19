from sqlalchemy import Boolean, Column, Integer, String, DateTime, ARRAY, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    interests = Column(ARRAY(String), default=[])
    age = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    social_links = Column(ARRAY(String), default=[])
    is_active = Column(Boolean, default=True)
    interest_vector = Column(ARRAY(Float), default=[])
    last_update = Column(DateTime, default=datetime.utcnow)

    # Relationships
    posts = relationship("Post", back_populates="user")
    likes = relationship("Like", back_populates="user")
    matches_as_user = relationship("Match", foreign_keys="Match.user_id", back_populates="user")
    matches_as_matched = relationship("Match", foreign_keys="Match.matched_user_id", back_populates="matched_user")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    source = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    matched_user_id = Column(Integer, ForeignKey("users.id"))
    similarity_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id], back_populates="matches_as_user")
    matched_user = relationship("User", foreign_keys=[matched_user_id], back_populates="matches_as_matched")