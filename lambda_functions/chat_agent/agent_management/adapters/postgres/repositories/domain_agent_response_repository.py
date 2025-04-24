"""Repository implementation for domain agent response operations."""
from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.command.domain_agent_response_command import (
    CreateDomainAgentResponse,
    UpdateDomainAgentResponse,
    GetDomainAgentResponse,
    DomainAgentResponseData
)
from adapters.postgres.models.domain_agent_response import DomainAgentResponse


class DomainAgentResponseRepository:
    """Repository for domain agent response operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateDomainAgentResponse) -> int:
        """Create a new domain agent response.
        
        Args:
            command: CreateDomainAgentResponse command
            
        Returns:
            int: ID of the created domain agent response
            
        Raises:
            ValueError: If invalid agent or domain question reference
        """
        try:
            response = DomainAgentResponse(
                agent_id=command.agent_id,
                domain_question_id=command.domain_question_id,
                response_text=command.response_text,
                response_date=command.response_date
            )
            self.session.add(response)
            await self.session.commit()
            await self.session.refresh(response)
            return response.domain_agent_response_id
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Invalid agent or domain question reference")

    async def update(self, command: UpdateDomainAgentResponse) -> bool:
        """Update an existing domain agent response.
        
        Args:
            command: UpdateDomainAgentResponse command
            
        Returns:
            bool: True if update was successful
            
        Raises:
            ValueError: If invalid agent or domain question reference
        """
        stmt = select(DomainAgentResponse).where(
            DomainAgentResponse.domain_agent_response_id == command.domain_agent_response_id
        )
        result = await self.session.execute(stmt)
        response = result.scalar_one_or_none()

        if not response:
            return False

        response.agent_id = command.agent_id
        response.domain_question_id = command.domain_question_id
        response.response_text = command.response_text
        response.response_date = command.response_date

        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Invalid agent or domain question reference")

    async def delete(self, domain_agent_response_id: int) -> bool:
        """Delete a domain agent response.
        
        Args:
            domain_agent_response_id: ID of the domain agent response to delete
            
        Returns:
            bool: True if deletion was successful
        """
        stmt = select(DomainAgentResponse).where(
            DomainAgentResponse.domain_agent_response_id == domain_agent_response_id
        )
        result = await self.session.execute(stmt)
        response = result.scalar_one_or_none()

        if not response:
            return False

        await self.session.delete(response)
        await self.session.commit()
        return True

    async def get(self, command: GetDomainAgentResponse) -> Optional[DomainAgentResponseData]:
        """Get a domain agent response by ID or filters.
        
        Args:
            command: GetDomainAgentResponse command
            
        Returns:
            Optional[DomainAgentResponseData]: Domain agent response data if found, None otherwise
        """
        stmt = select(DomainAgentResponse)

        conditions = []
        if command.domain_agent_response_id:
            conditions.append(DomainAgentResponse.domain_agent_response_id ==
                              command.domain_agent_response_id)
        if command.agent_id:
            conditions.append(DomainAgentResponse.agent_id == command.agent_id)
        if command.domain_question_id:
            conditions.append(DomainAgentResponse.domain_question_id ==
                              command.domain_question_id)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.session.execute(stmt)
        response = result.scalar_one_or_none()
        return DomainAgentResponseData.model_validate(response) if response else None

    async def list_all(
        self,
        agent_id: Optional[int] = None,
        domain_question_id: Optional[int] = None
    ) -> List[DomainAgentResponseData]:
        """List all domain agent responses, optionally filtered.
        
        Args:
            agent_id: Optional agent ID filter
            domain_question_id: Optional domain question ID filter
            
        Returns:
            List[DomainAgentResponseData]: List of domain agent responses
        """
        stmt = select(DomainAgentResponse)

        if agent_id:
            stmt = stmt.where(DomainAgentResponse.agent_id == agent_id)
        if domain_question_id:
            stmt = stmt.where(
                DomainAgentResponse.domain_question_id == domain_question_id)

        result = await self.session.execute(stmt)
        responses = result.scalars().all()
        return [DomainAgentResponseData.model_validate(r) for r in responses]
