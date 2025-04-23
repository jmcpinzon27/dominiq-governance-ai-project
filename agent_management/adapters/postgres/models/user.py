"""SQLAlchemy model for users."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class User(Base):
    """User database model."""
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)
    company_id = Column(Integer, ForeignKey(
        'companies.company_id'), nullable=False)
    # created_at = Column(
    #     DateTime(timezone=True),
    #     server_default=func.now(),
    #     nullable=False
    # )
    # updated_at = Column(
    #     DateTime(timezone=True),
    #     onupdate=func.now()
    # )
    # company = relationship("Company", back_populates="projects")

    # Indexes for frequent queries
    __table_args__ = (
        Index('idx_user_email', email),
        Index('idx_user_role', role_id),
        Index('idx_user_company', company_id),
    )
