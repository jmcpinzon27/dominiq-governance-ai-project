"""Repository implementation for maturity agent response operations."""
from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.command.maturity_agent_response_command import (
    CreateMaturityAgentResponse,
    UpdateMaturityAgentResponse,
    GetMaturityAgentResponse,
    MaturityAgentResponseData
)
from adapters.postgres.models.maturity_agent_response import MaturityAgentResponse


class MaturityAgentResponseRepository:
    """Repository for maturity agent response operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateMaturityAgentResponse) -> int:
        """Create a new maturity agent response.
        
        Args:
            command: CreateMaturityAgentResponse command
            
        Returns:
            int: ID of the created maturity agent response
            
        Raises:
            ValueError: If invalid agent or maturity question reference
        """
        try:
            response = MaturityAgentResponse(
                agent_id=command.agent_id,
                maturity_question_id=command.maturity_question_id,
                response_text=command.response_text,
                response_date=command.response_date
            )
            self.session.add(response)
            await self.session.commit()
            await self.session.refresh(response)
            return response.maturity_agent_response_id
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Invalid agent or maturity question reference")

    async def update(self, command: UpdateMaturityAgentResponse) -> bool:
        """Update an existing maturity agent response.
        
        Args:
            command: UpdateMaturityAgentResponse command
            
        Returns:
            bool: True if update was successful
            
        Raises:
            ValueError: If invalid agent or maturity question reference
        """
        stmt = select(MaturityAgentResponse).where(
            MaturityAgentResponse.maturity_agent_response_id == command.maturity_agent_response_id
        )
        result = await self.session.execute(stmt)
        response = result.scalar_one_or_none()

        if not response:
            return False

        response.agent_id = command.agent_id
        response.maturity_question_id = command.maturity_question_id
        response.response_text = command.response_text
        response.response_date = command.response_date

        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Invalid agent or maturity question reference")

    async def delete(self, maturity_agent_response_id: int) -> bool:
        """Delete a maturity agent response.
        
        Args:
            maturity_agent_response_id: ID of the maturity agent response to delete
            
        Returns:
            bool: True if deletion was successful
        """
        stmt = select(MaturityAgentResponse).where(
            MaturityAgentResponse.maturity_agent_response_id == maturity_agent_response_id
        )
        result = await self.session.execute(stmt)
        response = result.scalar_one_or_none()

        if not response:
            return False

        await self.session.delete(response)
        await self.session.commit()
        return True

    async def get(self, command: GetMaturityAgentResponse) -> Optional[MaturityAgentResponseData]:
        """Get a maturity agent response by ID or filters.
        
        Args:
            command: GetMaturityAgentResponse command
            
        Returns:
            Optional[MaturityAgentResponseData]: Maturity agent response data if found, None otherwise
        """
        stmt = select(MaturityAgentResponse)

        conditions = []
        if command.maturity_agent_response_id:
            conditions.append(MaturityAgentResponse.maturity_agent_response_id ==
                              command.maturity_agent_response_id)
        if command.agent_id:
            conditions.append(MaturityAgentResponse.agent_id == command.agent_id)
        if command.maturity_question_id:
            conditions.append(MaturityAgentResponse.maturity_question_id ==
                              command.maturity_question_id)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.session.execute(stmt)
        response = result.scalar_one_or_none()
        return MaturityAgentResponseData.model_validate(response) if response else None

    async def list_all(
        self,
        agent_id: Optional[int] = None,
        maturity_question_id: Optional[int] = None
    ) -> List[MaturityAgentResponseData]:
        """List all maturity agent responses, optionally filtered.
        
        Args:
            agent_id: Optional agent ID filter
            maturity_question_id: Optional maturity question ID filter
            
        Returns:
            List[MaturityAgentResponseData]: List of maturity agent responses
        """
        stmt = select(MaturityAgentResponse)

        if agent_id:
            stmt = stmt.where(MaturityAgentResponse.agent_id == agent_id)
        if maturity_question_id:
            stmt = stmt.where(
                MaturityAgentResponse.maturity_question_id == maturity_question_id)

        result = await self.session.execute(stmt)
        responses = result.scalars().all()
        return [MaturityAgentResponseData.model_validate(r) for r in responses]
