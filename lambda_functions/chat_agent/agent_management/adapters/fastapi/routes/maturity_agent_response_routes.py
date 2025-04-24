"""FastAPI routes for maturity agent response operations."""
from typing import Optional, Callable
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.maturity_agent_response_command import (
    CreateMaturityAgentResponse,
    UpdateMaturityAgentResponse,
    DeleteMaturityAgentResponse,
    GetMaturityAgentResponse,
    MaturityAgentResponseData,
    ListMaturityAgentResponses
)
from domain.command_handlers import maturity_agent_response_handler
from adapters.postgres.repositories.maturity_agent_response_repository import MaturityAgentResponseRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/maturity-agent-responses", tags=["maturity-agent-responses"])


async def get_maturity_agent_response_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for maturity agent response handler functions.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        dict[str, Callable]: Dictionary containing handler functions for maturity agent responses
    """
    repository = MaturityAgentResponseRepository(session)
    return {
        'create_maturity_response': lambda cmd: maturity_agent_response_handler.create_maturity_response(repository, cmd),
        'update_maturity_response': lambda cmd: maturity_agent_response_handler.update_maturity_response(repository, cmd),
        'delete_maturity_response': lambda cmd: maturity_agent_response_handler.delete_maturity_response(repository, cmd),
        'get_maturity_response': lambda cmd: maturity_agent_response_handler.get_maturity_response(repository, cmd),
        'list_maturity_responses': lambda agent_id=None, maturity_question_id=None: 
            maturity_agent_response_handler.list_maturity_responses(
                repository, agent_id, maturity_question_id
            )
    }


@router.post("/", response_model=int)
async def create_maturity_response_route(
    command: CreateMaturityAgentResponse,
    handler: dict[str, Callable] = Depends(get_maturity_agent_response_handler)
):
    """
    Create a new maturity agent response.
    
    Args:
        command: CreateMaturityAgentResponse command with response details
        handler: Maturity agent response handler functions
        
    Returns:
        int: ID of the created maturity agent response
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        return await handler['create_maturity_response'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{maturity_agent_response_id}", response_model=bool)
async def update_maturity_response_route(
    maturity_agent_response_id: int,
    command: UpdateMaturityAgentResponse,
    handler: dict[str, Callable] = Depends(get_maturity_agent_response_handler)
):
    """
    Update an existing maturity agent response.
    
    Args:
        maturity_agent_response_id: ID of the maturity agent response to update
        command: UpdateMaturityAgentResponse command with updated response details
        handler: Maturity agent response handler functions
        
    Returns:
        bool: True if update was successful
        
    Raises:
        HTTPException: If maturity agent response not found or validation fails
    """
    command.maturity_agent_response_id = maturity_agent_response_id
    try:
        if not await handler['update_maturity_response'](command):
            raise HTTPException(
                status_code=404, detail="Maturity agent response not found")
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{maturity_agent_response_id}", response_model=bool)
async def delete_maturity_response_route(
    maturity_agent_response_id: int,
    handler: dict[str, Callable] = Depends(get_maturity_agent_response_handler)
):
    """
    Delete a maturity agent response.
    
    Args:
        maturity_agent_response_id: ID of the maturity agent response to delete
        handler: Maturity agent response handler functions
        
    Returns:
        bool: True if deletion was successful
        
    Raises:
        HTTPException: If maturity agent response not found
    """
    if not await handler['delete_maturity_response'](
        DeleteMaturityAgentResponse(maturity_agent_response_id=maturity_agent_response_id)
    ):
        raise HTTPException(status_code=404, detail="Maturity agent response not found")
    return True


@router.get("/{maturity_agent_response_id}", response_model=MaturityAgentResponseData)
async def get_maturity_response_route(
    maturity_agent_response_id: int,
    handler: dict[str, Callable] = Depends(get_maturity_agent_response_handler)
):
    """
    Get a maturity agent response by ID.
    
    Args:
        maturity_agent_response_id: ID of the maturity agent response to get
        handler: Maturity agent response handler functions
        
    Returns:
        MaturityAgentResponseData: Maturity agent response data
        
    Raises:
        HTTPException: If maturity agent response not found
    """
    response = await handler['get_maturity_response'](
        GetMaturityAgentResponse(maturity_agent_response_id=maturity_agent_response_id)
    )
    if not response:
        raise HTTPException(status_code=404, detail="Maturity agent response not found")
    return response


@router.get("/", response_model=ListMaturityAgentResponses)
async def list_maturity_responses_route(
    agent_id: Optional[int] = Query(None, description="Filter by agent ID"),
    maturity_question_id: Optional[int] = Query(
        None, description="Filter by maturity question ID"),
    handler: dict[str, Callable] = Depends(get_maturity_agent_response_handler)
):
    """
    List all maturity agent responses with optional filters.
    
    Args:
        agent_id: Optional agent ID filter
        maturity_question_id: Optional maturity question ID filter
        handler: Maturity agent response handler functions
        
    Returns:
        ListMaturityAgentResponses: List of maturity agent responses
    """
    return await handler['list_maturity_responses'](agent_id, maturity_question_id)
