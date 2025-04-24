"""Repository implementation for domain operations."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.command.domain_command import CreateDomain, UpdateDomain, GetDomain, DomainResponse
from adapters.postgres.models.domain import Domain


class DomainRepository:
    """Repository for domain operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateDomain) -> int:
        """Create a new domain."""
        domain = Domain(domain_name=command.domain_name)
        self.session.add(domain)
        try:
            await self.session.commit()
            await self.session.refresh(domain)
            return domain.domain_id
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Domain name already exists")

    async def update(self, command: UpdateDomain) -> bool:
        """Update an existing domain."""
        stmt = select(Domain).where(Domain.domain_id == command.domain_id)
        result = await self.session.execute(stmt)
        domain = result.scalar_one_or_none()

        if not domain:
            return False

        domain.domain_name = command.domain_name

        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Domain name already exists")

    async def delete(self, domain_id: int) -> bool:
        """Delete a domain."""
        stmt = select(Domain).where(Domain.domain_id == domain_id)
        result = await self.session.execute(stmt)
        domain = result.scalar_one_or_none()

        if not domain:
            return False

        await self.session.delete(domain)
        await self.session.commit()
        return True

    async def get(self, command: GetDomain) -> Optional[DomainResponse]:
        """Get a domain by ID or name."""
        stmt = select(Domain)
        if command.domain_id:
            stmt = stmt.where(Domain.domain_id == command.domain_id)
        elif command.domain_name:
            stmt = stmt.where(Domain.domain_name == command.domain_name)
        else:
            return None

        result = await self.session.execute(stmt)
        domain = result.scalar_one_or_none()
        return DomainResponse.model_validate(domain) if domain else None

    async def list_all(self) -> List[DomainResponse]:
        """List all domains."""
        stmt = select(Domain)
        result = await self.session.execute(stmt)
        domains = result.scalars().all()
        return [DomainResponse.model_validate(domain) for domain in domains]
