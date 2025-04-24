"""PostgreSQL repository implementation for companies."""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from adapters.postgres.models.company import Company
from domain.command.company_command import (
    CreateCompany,
    UpdateCompany,
    GetCompany,
    CompanyResponse,
    ListCompanies
)


class CompanyRepository:
    """Repository for company operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self._session = session

    async def create(self, command: CreateCompany) -> int:
        """Create a new company."""
        company = Company(
            company_name=command.company_name,
            industry_id=command.industry_id
        )
        self._session.add(company)
        try:
            await self._session.commit()
            await self._session.refresh(company)
            return company.company_id
        except IntegrityError:
            await self._session.rollback()
            raise ValueError("Company name already exists or invalid industry ID")

    async def update(self, command: UpdateCompany) -> bool:
        """Update an existing company."""
        stmt = select(Company).where(Company.company_id == command.company_id)
        result = await self._session.execute(stmt)
        company = result.scalar_one_or_none()

        if not company:
            return False

        if command.company_name is not None:
            company.company_name = command.company_name
        if command.industry_id is not None:
            company.industry_id = command.industry_id

        try:
            await self._session.commit()
            return True
        except IntegrityError:
            await self._session.rollback()
            raise ValueError("Company name already exists or invalid industry ID")

    async def delete(self, company_id: int) -> bool:
        """Delete a company."""
        stmt = select(Company).where(Company.company_id == company_id)
        result = await self._session.execute(stmt)
        company = result.scalar_one_or_none()

        if company:
            await self._session.delete(company)
            await self._session.commit()
            return True
        return False

    async def get(self, command: GetCompany) -> Optional[CompanyResponse]:
        """Get a company by ID or name."""
        stmt = select(Company)
        if command.company_id:
            stmt = stmt.where(Company.company_id == command.company_id)
        elif command.company_name:
            stmt = stmt.where(Company.company_name == command.company_name)
        else:
            return None

        result = await self._session.execute(stmt)
        company = result.scalar_one_or_none()

        if not company:
            return None

        return CompanyResponse(
            company_id=company.company_id,
            company_name=company.company_name,
            industry_id=company.industry_id
        )

    async def list_all(self) -> ListCompanies:
        """List all companies."""
        stmt = select(Company)
        result = await self._session.execute(stmt)
        companies = result.scalars().all()

        return ListCompanies(companies=[
            CompanyResponse(
                company_id=c.company_id,
                company_name=c.company_name,
                industry_id=c.industry_id
            ) for c in companies
        ])
