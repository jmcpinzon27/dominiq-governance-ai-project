"""SQLAlchemy model for domain questions."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class DomainQuestion(Base):
    """Domain Question database model."""
    __tablename__ = 'domain_questions'

    domain_question_id = Column(Integer, primary_key=True)
    domain_id = Column(Integer, ForeignKey(
        'domains.domain_id', ondelete='CASCADE'), nullable=False)
    industry_id = Column(Integer, ForeignKey(
        'industries.industry_id', ondelete='CASCADE'), nullable=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(20), nullable=False)
    category = Column(String(100), nullable=True)

    # Relationships
    # domain = relationship("Domain", back_populates="domain_questions")
    # industry = relationship("Industry")
    # domain_agent_responses = relationship(
    #     "DomainAgentResponse", back_populates="domain_question", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_domain_question_domain_id', domain_id),
        Index('idx_domain_question_industry_id', industry_id),
        Index('idx_domain_question_type', question_type),
        Index('idx_domain_question_category', category),
    )
