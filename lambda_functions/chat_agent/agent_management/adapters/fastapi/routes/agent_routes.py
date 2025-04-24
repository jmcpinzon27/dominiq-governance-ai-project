from typing import Callable, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.agent_command import (
    CreateAgent,
    UpdateAgent,
    DeleteAgent,
    GetAgent,
    AgentResponse,
    ListAgents
)
from domain.command.comon_command import sql, Sources
from domain.command_handlers import agent_handler
from adapters.dynamodb import registration_adapter, message_adapter
from adapters.postgres.repositories.agent_repository import AgentRepository
from adapters.postgres.config import get_session
from adapters.saia_assistant import main as main_asistant

# FIXME: set in the right place to work with
from domain.command_handlers.message_command_handler import get_message, get_generate_diagram_from_cha
from domain.command_handlers.registration_command_handler import get_registration


router = APIRouter(prefix="/agents", tags=["agents"])


async def get_agent_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for agent handler functions.

    Args:
        session: AsyncSession from dependency injection

    Returns:
        dict[str, Callable]: Dictionary containing handler functions for agents
    """
    repository = AgentRepository(session)
    return {
        'create_agent': lambda cmd: agent_handler.create_agent(repository, cmd),
        'update_agent': lambda cmd: agent_handler.update_agent(repository, cmd),
        'delete_agent': lambda cmd: agent_handler.delete_agent(repository, cmd),
        'get_agent': lambda cmd: agent_handler.get_agent(repository, cmd),
        'list_agents': lambda: agent_handler.list_agents(repository)
    }


@router.post("/", response_model=int)
async def create_agent_route(
    command: CreateAgent,
    handler: dict[str, Callable] = Depends(get_agent_handler)
):
    """Create a new agent."""
    try:
        return await handler['create_agent'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{agent_id}", response_model=bool)
async def update_agent_route(
    agent_id: int,
    command: UpdateAgent,
    handler: dict[str, Callable] = Depends(get_agent_handler)
):
    """Update an existing agent."""
    command.agent_id = agent_id
    try:
        if not await handler['update_agent'](command):
            raise HTTPException(status_code=404, detail="Agent not found")
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{agent_id}", response_model=bool)
async def delete_agent_route(
    agent_id: int,
    handler: dict[str, Callable] = Depends(get_agent_handler)
):
    """Delete an agent."""
    if not await handler['delete_agent'](DeleteAgent(agent_id=agent_id)):
        raise HTTPException(status_code=404, detail="Agent not found")
    return True


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    handler: dict[str, Callable] = Depends(get_agent_handler)
):
    """Get an agent by ID."""
    agent = await handler['get_agent'](GetAgent(agent_id=agent_id))
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.get("/", response_model=ListAgents)
async def list_agents_route(
    agent_type: Optional[str] = Query(None, description="Filter by agent type"),
    handler: dict[str, Callable] = Depends(get_agent_handler)
):
    """List all agents, optionally filtered by agent_type."""
    if agent_type:
        return await handler['get_agent'](GetAgent(agent_type=agent_type))
    return await handler['list_agents']()


@router.post('/chat_with_agent')
async def chat_with_agent_route(data): # GetMessages):
    nosql = sql(
        messages=message_adapter,
        registrations=registration_adapter
    )
    sources = Sources(nosql=nosql, asistant=main_asistant, storage=None)
    return await get_message(sources, data)


@router.post('/generate_diagram_from_chat')
async def generate_diagram_from_chat_route(data): # GetMessages):
    nosql = sql(
        messages=message_adapter,
        registrations=registration_adapter
    )
    sources = Sources(
        nosql=nosql, asistant=main_asistant,
        # storage=s3
    )
    return await get_generate_diagram_from_cha(sources, data)
