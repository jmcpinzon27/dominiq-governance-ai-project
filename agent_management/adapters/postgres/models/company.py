"""SQLAlchemy models for companies."""
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from adapters.postgres.config import Base


class Company(Base):
    """Company database model."""
    __tablename__ = 'companies'

    company_id = Column(Integer, primary_key=True)
    company_name = Column(String(100), nullable=False, unique=True)
    industry_id = Column(Integer, ForeignKey(
        'industries.industry_id', ondelete='CASCADE'), nullable=True)

    # Relationships
    # industry = relationship("Industry", back_populates="companies")
    # domains = relationship(
    #     "Domain", back_populates="company", cascade="all, delete-orphan")
    # projects = relationship(
    #     "Project", back_populates="company", cascade="all, delete-orphan")
    # users = relationship(
    #     "User", back_populates="company", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_company_name', company_name),
        Index('idx_company_industry_id', industry_id),
    )
