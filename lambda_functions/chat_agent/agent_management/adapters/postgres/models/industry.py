"""SQLAlchemy model for industries."""
from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class Industry(Base):
    """Industry database model."""
    __tablename__ = 'industries'

    industry_id = Column(Integer, primary_key=True)
    industry_name = Column(String(100), nullable=False, unique=True)

    # Relationships
    # companies = relationship(
    #     "Company", back_populates="industry", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_industry_name', industry_name),
    )
