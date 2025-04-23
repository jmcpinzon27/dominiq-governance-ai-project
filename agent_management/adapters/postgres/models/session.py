"""SQLAlchemy model for sessions."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class Session(Base):
    """Session database model."""
    __tablename__ = 'sessions'

    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(
        'users.user_id', ondelete='CASCADE'), nullable=False)
    session_token = Column(String(256), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    session_start = Column(DateTime, nullable=False, default=datetime.utcnow)
    session_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    # user = relationship("User", back_populates="sessions")
    # maturity_answers = relationship(
    #     "MaturityAnswer", back_populates="session", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_session_token', session_token),
        Index('idx_user_id_is_active', user_id, is_active),
    )
