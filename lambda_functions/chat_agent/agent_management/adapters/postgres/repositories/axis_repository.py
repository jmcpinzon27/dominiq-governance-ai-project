"""PostgreSQL repository implementation for axis."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from adapters.postgres.models.axis import Axis
from domain.command.axis_command import (
    CreateAxis,
    UpdateAxis,
    AxisResponse
)


class AxisRepository:
    """Repository for axis operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateAxis) -> int:
        """Create a new axis.
        
        Args:
            command: CreateAxis command
            
        Returns:
            int: ID of the created axis
            
        Raises:
            ValueError: If axis name already exists
        """
        axis = Axis(
            axis_name=command.axis_name        )
        self.session.add(axis)
        try:
            await self.session.commit()
            await self.session.refresh(axis)
            return axis.axis_id
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Axis name already exists")

    async def update(self, command: UpdateAxis) -> bool:
        """Update an existing axis.
        
        Args:
            command: UpdateAxis command
            
        Returns:
            bool: True if update was successful
            
        Raises:
            ValueError: If axis name already exists
        """
        stmt = select(Axis).where(Axis.axis_id == command.axis_id)
        result = await self.session.execute(stmt)
        axis = result.scalar_one_or_none()

        if not axis:
            return False

        if command.axis_name is not None:
            axis.axis_name = command.axis_name

        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Axis name already exists")

    async def delete(self, axis_id: int) -> bool:
        """Delete an axis.
        
        Args:
            axis_id: ID of the axis to delete
            
        Returns:
            bool: True if deletion was successful
        """
        stmt = select(Axis).where(Axis.axis_id == axis_id)
        result = await self.session.execute(stmt)
        axis = result.scalar_one_or_none()

        if not axis:
            return False

        await self.session.delete(axis)
        await self.session.commit()
        return True

    async def get_by_id(self, axis_id: int) -> Optional[AxisResponse]:
        """Get an axis by ID.
        
        Args:
            axis_id: ID of the axis to get
            
        Returns:
            Optional[AxisResponse]: Axis data if found, None otherwise
        """
        stmt = select(Axis).where(Axis.axis_id == axis_id)
        result = await self.session.execute(stmt)
        axis = result.scalar_one_or_none()
        
        if not axis:
            return None
            
        return AxisResponse(
            axis_id=axis.axis_id,
            axis_name=axis.axis_name
        )

    async def get_by_name(self, axis_name: str) -> Optional[AxisResponse]:
        """Get an axis by name.
        
        Args:
            axis_name: Name of the axis to get
            
        Returns:
            Optional[AxisResponse]: Axis data if found, None otherwise
        """
        stmt = select(Axis).where(Axis.axis_name == axis_name)
        result = await self.session.execute(stmt)
        axis = result.scalar_one_or_none()
        
        if not axis:
            return None
            
        return AxisResponse(
            axis_id=axis.axis_id,
            axis_name=axis.axis_name
        )

    async def get_all(self) -> List[AxisResponse]:
        """Get all axes.
        
        Returns:
            List[AxisResponse]: List of all axes
        """
        stmt = select(Axis)
        result = await self.session.execute(stmt)
        axes = result.scalars().all()
        
        return [
            AxisResponse(
                axis_id=axis.axis_id,
                axis_name=axis.axis_name
            )
            for axis in axes
        ]
