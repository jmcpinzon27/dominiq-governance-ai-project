"""FastAPI routes for domain agent response operations."""
from typing import Optional, Callable
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.domain_agent_response_command import (
    CreateDomainAgentResponse,
    UpdateDomainAgentResponse,
    DeleteDomainAgentResponse,
    GetDomainAgentResponse,
    DomainAgentResponseData,
    ListDomainAgentResponses
)
from domain.command_handlers import domain_agent_response_handler
from adapters.postgres.repositories.domain_agent_response_repository import DomainAgentResponseRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/domain-agent-responses", tags=["domain-agent-responses"])


async def get_domain_agent_response_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for domain agent response handler functions.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        dict[str, Callable]: Dictionary containing handler functions for domain agent responses
    """
    repository = DomainAgentResponseRepository(session)
    return {
        'create_domain_response': lambda cmd: domain_agent_response_handler.create_domain_response(repository, cmd),
        'update_domain_response': lambda cmd: domain_agent_response_handler.update_domain_response(repository, cmd),
        'delete_domain_response': lambda cmd: domain_agent_response_handler.delete_domain_response(repository, cmd),
        'get_domain_response': lambda cmd: domain_agent_response_handler.get_domain_response(repository, cmd),
        'list_domain_responses': lambda agent_id=None, domain_question_id=None: 
            domain_agent_response_handler.list_domain_responses(
                repository, agent_id, domain_question_id
            )
    }


@router.post("/", response_model=int)
async def create_domain_response_route(
    command: CreateDomainAgentResponse,
    handler: dict[str, Callable] = Depends(get_domain_agent_response_handler)
):
    """
    Create a new domain agent response.
    
    Args:
        command: CreateDomainAgentResponse command with response details
        handler: Domain agent response handler functions
        
    Returns:
        int: ID of the created domain agent response
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        return await handler['create_domain_response'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{domain_agent_response_id}", response_model=bool)
async def update_domain_response_route(
    domain_agent_response_id: int,
    command: UpdateDomainAgentResponse,
    handler: dict[str, Callable] = Depends(get_domain_agent_response_handler)
):
    """
    Update an existing domain agent response.
    
    Args:
        domain_agent_response_id: ID of the domain agent response to update
        command: UpdateDomainAgentResponse command with updated response details
        handler: Domain agent response handler functions
        
    Returns:
        bool: True if update was successful
        
    Raises:
        HTTPException: If domain agent response not found or validation fails
    """
    command.domain_agent_response_id = domain_agent_response_id
    try:
        if not await handler['update_domain_response'](command):
            raise HTTPException(
                status_code=404, detail="Domain agent response not found")
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{domain_agent_response_id}", response_model=bool)
async def delete_domain_response_route(
    domain_agent_response_id: int,
    handler: dict[str, Callable] = Depends(get_domain_agent_response_handler)
):
    """
    Delete a domain agent response.
    
    Args:
        domain_agent_response_id: ID of the domain agent response to delete
        handler: Domain agent response handler functions
        
    Returns:
        bool: True if deletion was successful
        
    Raises:
        HTTPException: If domain agent response not found
    """
    if not await handler['delete_domain_response'](
        DeleteDomainAgentResponse(domain_agent_response_id=domain_agent_response_id)
    ):
        raise HTTPException(status_code=404, detail="Domain agent response not found")
    return True


@router.get("/{domain_agent_response_id}", response_model=DomainAgentResponseData)
async def get_domain_response_route(
    domain_agent_response_id: int,
    handler: dict[str, Callable] = Depends(get_domain_agent_response_handler)
):
    """
    Get a domain agent response by ID.
    
    Args:
        domain_agent_response_id: ID of the domain agent response to get
        handler: Domain agent response handler functions
        
    Returns:
        DomainAgentResponseData: Domain agent response data
        
    Raises:
        HTTPException: If domain agent response not found
    """
    response = await handler['get_domain_response'](
        GetDomainAgentResponse(domain_agent_response_id=domain_agent_response_id)
    )
    if not response:
        raise HTTPException(status_code=404, detail="Domain agent response not found")
    return response


@router.get("/", response_model=ListDomainAgentResponses)
async def list_domain_responses_route(
    agent_id: Optional[int] = Query(None, description="Filter by agent ID"),
    domain_question_id: Optional[int] = Query(
        None, description="Filter by domain question ID"),
    handler: dict[str, Callable] = Depends(get_domain_agent_response_handler)
):
    """
    List all domain agent responses with optional filters.
    
    Args:
        agent_id: Optional agent ID filter
        domain_question_id: Optional domain question ID filter
        handler: Domain agent response handler functions
        
    Returns:
        ListDomainAgentResponses: List of domain agent responses
    """
    return await handler['list_domain_responses'](agent_id, domain_question_id)
