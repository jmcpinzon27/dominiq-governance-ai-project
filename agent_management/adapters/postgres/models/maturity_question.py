"""SQLAlchemy model for maturity questions."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class MaturityQuestion(Base):
    """Maturity Question database model."""
    __tablename__ = 'maturity_questions'

    maturity_question_id = Column(Integer, primary_key=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(20), nullable=False)
    question_order = Column(Integer, nullable=True)
    category = Column(String(100), nullable=True)
    axis_id = Column(Integer, ForeignKey('axis.axis_id', ondelete='CASCADE'), nullable=True)
    industry_id = Column(Integer, ForeignKey('industries.industry_id', ondelete='CASCADE'), nullable=True)

    # Relationships
    # axis = relationship("Axis", back_populates="maturity_questions")
    # industry = relationship("Industry")
    # maturity_answers = relationship(
    #     "MaturityAnswer", back_populates="maturity_question")
    # maturity_agent_responses = relationship(
    #     "MaturityAgentResponse", back_populates="maturity_question", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_maturity_question_type', question_type),
        Index('idx_maturity_category', category),
        Index('idx_maturity_question_order', question_order),
        Index('idx_maturity_question_axis_id', axis_id),
        Index('idx_maturity_question_industry_id', industry_id),
    )
