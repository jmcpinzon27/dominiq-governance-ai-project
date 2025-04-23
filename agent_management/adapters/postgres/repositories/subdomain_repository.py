"""Repository implementation for subdomain operations."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.command.subdomain_command import CreateSubdomain, UpdateSubdomain, GetSubdomain, SubdomainResponse
from adapters.postgres.models.subdomain import Subdomain


class SubdomainRepository:
    """Repository for subdomain operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateSubdomain) -> int:
        """Create a new subdomain."""
        subdomain = Subdomain(
            subdomain_name=command.subdomain_name,
            domain_id=command.domain_id
        )
        self.session.add(subdomain)
        try:
            await self.session.commit()
            await self.session.refresh(subdomain)
            return subdomain.subdomain_id
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Subdomain name already exists in this domain")

    async def update(self, command: UpdateSubdomain) -> bool:
        """Update an existing subdomain."""
        stmt = select(Subdomain).where(
            Subdomain.subdomain_id == command.subdomain_id)
        result = await self.session.execute(stmt)
        subdomain = result.scalar_one_or_none()

        if not subdomain:
            return False

        subdomain.subdomain_name = command.subdomain_name
        subdomain.domain_id = command.domain_id

        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Subdomain name already exists in this domain")

    async def delete(self, subdomain_id: int) -> bool:
        """Delete a subdomain."""
        stmt = select(Subdomain).where(Subdomain.subdomain_id == subdomain_id)
        result = await self.session.execute(stmt)
        subdomain = result.scalar_one_or_none()

        if not subdomain:
            return False

        await self.session.delete(subdomain)
        await self.session.commit()
        return True

    async def get(self, command: GetSubdomain) -> Optional[SubdomainResponse]:
        """Get a subdomain by ID, name, or domain_id."""
        stmt = select(Subdomain)
        if command.subdomain_id:
            stmt = stmt.where(Subdomain.subdomain_id == command.subdomain_id)
        elif command.subdomain_name and command.domain_id:
            stmt = stmt.where(
                Subdomain.subdomain_name == command.subdomain_name,
                Subdomain.domain_id == command.domain_id
            )
        else:
            return None

        result = await self.session.execute(stmt)
        subdomain = result.scalar_one_or_none()
        return SubdomainResponse.model_validate(subdomain) if subdomain else None

    async def list_all(self, domain_id: Optional[int] = None) -> List[SubdomainResponse]:
        """List all subdomains, optionally filtered by domain_id."""
        stmt = select(Subdomain)
        if domain_id:
            stmt = stmt.where(Subdomain.domain_id == domain_id)
        result = await self.session.execute(stmt)
        subdomains = result.scalars().all()
        return [SubdomainResponse.model_validate(subdomain) for subdomain in subdomains]
