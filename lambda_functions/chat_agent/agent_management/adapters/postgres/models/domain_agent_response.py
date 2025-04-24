"""SQLAlchemy model for domain agent responses."""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class DomainAgentResponse(Base):
    """Domain Agent Response database model."""
    __tablename__ = 'domain_agent_responses'

    domain_agent_response_id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey(
        'agents.agent_id', ondelete='CASCADE'), nullable=False)
    domain_question_id = Column(
        Integer,
        ForeignKey('domain_questions.domain_question_id', ondelete='CASCADE'),
        nullable=False
    )
    response_text = Column(Text, nullable=False)
    response_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    # agent = relationship("Agent", back_populates="domain_agent_responses")
    # domain_question = relationship(
    #     "DomainQuestion", back_populates="domain_agent_responses")

    # Indexes
    __table_args__ = (
        Index('idx_domain_agent_response_agent_id', agent_id),
        Index('idx_domain_agent_response_question_id', domain_question_id),
        Index('idx_domain_agent_response_date', response_date),
    )
