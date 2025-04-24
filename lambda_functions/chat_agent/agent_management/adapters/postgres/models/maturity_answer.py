"""SQLAlchemy model for maturity answers."""
from datetime import datetime
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class MaturityAnswer(Base):
    """Maturity Answer database model."""
    __tablename__ = 'maturity_answers'

    maturity_answer_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey(
        'sessions.session_id', ondelete='CASCADE'), nullable=False)
    maturity_question_id = Column(Integer, ForeignKey(
        'maturity_questions.maturity_question_id', ondelete='CASCADE'), nullable=False)
    answer_text = Column(Text, nullable=False)
    answered_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationships
    # session = relationship("Session", back_populates="maturity_answers")
    # maturity_question = relationship("MaturityQuestion", back_populates="maturity_answers")

    # Constraints and Indexes
    __table_args__ = (
        UniqueConstraint('session_id', 'maturity_question_id',
                         name='uq_session_maturity_question'),
        Index('idx_maturity_answer_session_id', session_id),
        Index('idx_maturity_answer_question_id', maturity_question_id),
        Index('idx_maturity_answer_answered_at', answered_at),
    )
