"""SQLAlchemy model for projects."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class Project(Base):
    """Project database model."""
    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True)
    project_name = Column(String(100), nullable=False)
    description = Column(Text)
    company_id = Column(
        Integer,
        ForeignKey('companies.company_id', ondelete='CASCADE'),
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
    # company = relationship("Company", back_populates="pprojects")

    # Composite unique constraint
    __table_args__ = (
        Index('idx_project_company_name', company_id, project_name, unique=True),
        Index('idx_project_company', company_id),
    )
