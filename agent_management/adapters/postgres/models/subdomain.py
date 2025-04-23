"""SQLAlchemy model for subdomains."""
from sqlalchemy import Column, Integer, String, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship

from adapters.postgres.config import Base


class Subdomain(Base):
    """Subdomain database model."""
    __tablename__ = 'subdomains'

    subdomain_id = Column(Integer, primary_key=True)
    subdomain_name = Column(String(100), nullable=False)
    domain_id = Column(Integer, ForeignKey(
        'domains.domain_id', ondelete='CASCADE'), nullable=False)

    # Relationships
    # domain = relationship("Domain", back_populates="subdomains")
    # domain_questions = relationship(
    #     "DomainQuestion", back_populates="subdomain", cascade="all, delete-orphan")

    # Indexes and Constraints
    __table_args__ = (
        UniqueConstraint('domain_id', 'subdomain_name',
                         name='uq_domain_subdomain_name'),
        Index('idx_subdomain_domain_id', domain_id),
        Index('idx_subdomain_name', subdomain_name)
    )
