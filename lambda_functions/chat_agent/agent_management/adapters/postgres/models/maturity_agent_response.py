"""SQLAlchemy model for maturity agent responses."""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class MaturityAgentResponse(Base):
    """Maturity Agent Response database model."""
    __tablename__ = 'maturity_agent_responses'

    maturity_agent_response_id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey(
        'agents.agent_id', ondelete='CASCADE'), nullable=False)
    maturity_question_id = Column(
        Integer,
        ForeignKey('maturity_questions.maturity_question_id', ondelete='CASCADE'),
        nullable=False
    )
    response_text = Column(Text, nullable=False)
    response_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    # agent = relationship("Agent", back_populates="maturity_agent_responses")
    # maturity_question = relationship(
    #     "MaturityQuestion", back_populates="maturity_agent_responses")

    # Indexes
    __table_args__ = (
        Index('idx_maturity_agent_responses_agent_id', agent_id),
        Index('idx_maturity_agent_responses_question_id', maturity_question_id),
        Index('idx_maturity_agent_responses_date', response_date),
    )
