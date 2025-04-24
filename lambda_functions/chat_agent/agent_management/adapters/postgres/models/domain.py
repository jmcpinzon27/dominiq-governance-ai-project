"""SQLAlchemy model for domains."""
from sqlalchemy import Column, Integer, String, Index, ForeignKey
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class Domain(Base):
    """Domain database model."""
    __tablename__ = 'domains'

    domain_id = Column(Integer, primary_key=True)
    domain_name = Column(String(100), nullable=False, unique=True)
    company_id = Column(
        Integer,
        ForeignKey('companies.company_id', ondelete='CASCADE'),
        nullable=False
    )

    # Relationships
    # subdomains = relationship(
    #     "Subdomain", back_populates="domain", cascade="all, delete-orphan")
    # domain_questions = relationship(
    #     "DomainQuestion", back_populates="domain", cascade="all, delete-orphan")
    # company = relationship(
    #     "Company", back_populates="companies")
    # Indexes
    __table_args__ = (
        Index('idx_domain_name', domain_name),
    )
