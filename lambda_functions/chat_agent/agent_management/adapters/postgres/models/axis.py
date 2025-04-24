"""SQLAlchemy model for axis."""
from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class Axis(Base):
    """Axis database model."""
    __tablename__ = 'axis'

    axis_id = Column(Integer, primary_key=True)
    axis_name = Column(String(100), nullable=False, unique=True)

    # Relationships
    # maturity_questions = relationship(
    #     "MaturityQuestion", back_populates="axis", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_axis_name', axis_name),
    )
