"""PostgreSQL repository implementation for industries."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from adapters.postgres.models.industry import Industry
from domain.command.industry_command import (
    CreateIndustry,
    UpdateIndustry,
    IndustryResponse
)


class IndustryRepository:
    """Repository for industry operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateIndustry) -> int:
        """Create a new industry.
        
        Args:
            command: CreateIndustry command
            
        Returns:
            int: ID of the created industry
            
        Raises:
            ValueError: If industry name already exists
        """
        industry = Industry(
            industry_name=command.industry_name
        )
        self.session.add(industry)
        try:
            await self.session.commit()
            await self.session.refresh(industry)
            return industry.industry_id
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Industry name already exists")

    async def update(self, command: UpdateIndustry) -> bool:
        """Update an existing industry.
        
        Args:
            command: UpdateIndustry command
            
        Returns:
            bool: True if update was successful
            
        Raises:
            ValueError: If industry name already exists
        """
        stmt = select(Industry).where(Industry.industry_id == command.industry_id)
        result = await self.session.execute(stmt)
        industry = result.scalar_one_or_none()

        if not industry:
            return False

        if command.industry_name is not None:
            industry.industry_name = command.industry_name

        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Industry name already exists")

    async def delete(self, industry_id: int) -> bool:
        """Delete an industry.
        
        Args:
            industry_id: ID of the industry to delete
            
        Returns:
            bool: True if deletion was successful
        """
        stmt = select(Industry).where(Industry.industry_id == industry_id)
        result = await self.session.execute(stmt)
        industry = result.scalar_one_or_none()

        if not industry:
            return False

        await self.session.delete(industry)
        await self.session.commit()
        return True

    async def get_by_id(self, industry_id: int) -> Optional[IndustryResponse]:
        """Get an industry by ID.
        
        Args:
            industry_id: ID of the industry to get
            
        Returns:
            Optional[IndustryResponse]: Industry data if found, None otherwise
        """
        stmt = select(Industry).where(Industry.industry_id == industry_id)
        result = await self.session.execute(stmt)
        industry = result.scalar_one_or_none()
        
        if not industry:
            return None
            
        return IndustryResponse(
            industry_id=industry.industry_id,
            industry_name=industry.industry_name
        )

    async def get_by_name(self, industry_name: str) -> Optional[IndustryResponse]:
        """Get an industry by name.
        
        Args:
            industry_name: Name of the industry to get
            
        Returns:
            Optional[IndustryResponse]: Industry data if found, None otherwise
        """
        stmt = select(Industry).where(Industry.industry_name == industry_name)
        result = await self.session.execute(stmt)
        industry = result.scalar_one_or_none()
        
        if not industry:
            return None
            
        return IndustryResponse(
            industry_id=industry.industry_id,
            industry_name=industry.industry_name
        )

    async def get_all(self) -> List[IndustryResponse]:
        """Get all industries.
        
        Returns:
            List[IndustryResponse]: List of all industries
        """
        stmt = select(Industry)
        result = await self.session.execute(stmt)
        industries = result.scalars().all()
        
        return [
            IndustryResponse(
                industry_id=industry.industry_id,
                industry_name=industry.industry_name
            )
            for industry in industries
        ]
