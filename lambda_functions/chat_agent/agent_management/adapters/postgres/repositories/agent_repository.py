"""Repository implementation for agent operations."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.command.agent_command import CreateAgent, UpdateAgent, GetAgent, AgentResponse
from adapters.postgres.models.agent import Agent


class AgentRepository:
    """Repository for agent operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create(self, command: CreateAgent) -> int:
        """Create a new agent."""
        agent = Agent(
            agent_name=command.agent_name,
            agent_role=command.agent_role,
            agent_type=command.agent_type
        )
        self.session.add(agent)
        try:
            await self.session.commit()
            await self.session.refresh(agent)
            return agent.agent_id
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Agent name already exists")

    async def update(self, command: UpdateAgent) -> bool:
        """Update an existing agent."""
        stmt = select(Agent).where(Agent.agent_id == command.agent_id)
        result = await self.session.execute(stmt)
        agent = result.scalar_one_or_none()

        if not agent:
            return False

        agent.agent_name = command.agent_name
        agent.agent_role = command.agent_role
        agent.agent_type = command.agent_type

        try:
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Agent name already exists")

    async def delete(self, agent_id: int) -> bool:
        """Delete an agent."""
        stmt = select(Agent).where(Agent.agent_id == agent_id)
        result = await self.session.execute(stmt)
        agent = result.scalar_one_or_none()

        if not agent:
            return False

        await self.session.delete(agent)
        await self.session.commit()
        return True

    async def get(self, command: GetAgent) -> Optional[AgentResponse]:
        """Get an agent by ID or name."""
        stmt = select(Agent)
        if command.agent_id:
            stmt = stmt.where(Agent.agent_id == command.agent_id)
        elif command.agent_name:
            stmt = stmt.where(Agent.agent_name == command.agent_name)
        elif command.agent_type:
            stmt = stmt.where(Agent.agent_type == command.agent_type)
        else:
            return None

        result = await self.session.execute(stmt)
        agent = result.scalar_one_or_none()
        return AgentResponse.model_validate(agent) if agent else None

    async def list_all(self) -> List[AgentResponse]:
        """List all agents."""
        stmt = select(Agent)
        result = await self.session.execute(stmt)
        agents = result.scalars().all()
        return [AgentResponse.model_validate(agent) for agent in agents]
