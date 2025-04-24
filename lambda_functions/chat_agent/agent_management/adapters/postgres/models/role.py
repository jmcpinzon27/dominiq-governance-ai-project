"""SQLAlchemy model for roles."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from adapters.postgres.config import Base


class Role(Base):
    """Role database model."""
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(50), nullable=False, unique=True)
    # description = Column(Text)
    # created_at = Column(
    #     DateTime(timezone=True),
    #     server_default=func.now(),
    #     nullable=False
    # )
    # updated_at = Column(
    #     DateTime(timezone=True),
    #     onupdate=func.now()
    # )
