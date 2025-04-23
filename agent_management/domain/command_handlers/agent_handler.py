"""Handler for agent-related commands."""
from typing import Optional, List
from domain.command.agent_command import (
    CreateAgent,
    UpdateAgent,
    DeleteAgent,
    GetAgent,
    AgentResponse,
    ListAgents
)


async def create_agent(repository, command: CreateAgent) -> int:
    """Create a new agent."""
    return await repository.create(command)


async def update_agent(repository, command: UpdateAgent) -> bool:
    """Update an existing agent."""
    return await repository.update(command)


async def delete_agent(repository, command: DeleteAgent) -> bool:
    """Delete an agent."""
    return await repository.delete(command.agent_id)


async def get_agent(repository, command: GetAgent) -> Optional[AgentResponse]:
    """Retrieve an agent by ID or name."""
    return await repository.get(command)


async def list_agents(repository) -> ListAgents:
    """List all agents."""
    agents = await repository.list_all()
    return ListAgents(agents=agents)
