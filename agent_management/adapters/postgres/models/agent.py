"""SQLAlchemy model for agents."""
from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class Agent(Base):
    """Agent database model."""
    __tablename__ = 'agents'

    agent_id = Column(Integer, primary_key=True)
    agent_name = Column(String(100), nullable=False, unique=True)
    agent_role = Column(String(200), nullable=True)
    agent_type = Column(String(50), nullable=True)

    # Relationships
    # maturity_agent_responses = relationship(
    #     "MaturityAgentResponse", back_populates="agent", cascade="all, delete-orphan")
    # domain_agent_responses = relationship(
    #     "DomainAgentResponse", back_populates="agent", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_agent_name', agent_name),
        Index('idx_agent_type', agent_type),
    )
