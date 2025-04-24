"""Handler for maturity agent response-related commands."""
from typing import Optional, List, Callable
from functools import partial
from domain.command.maturity_agent_response_command import (
    CreateMaturityAgentResponse,
    UpdateMaturityAgentResponse,
    DeleteMaturityAgentResponse,
    GetMaturityAgentResponse,
    MaturityAgentResponseData,
    ListMaturityAgentResponses
)


async def create_maturity_response(repository: Callable, command: CreateMaturityAgentResponse) -> int:
    """Create a new maturity agent response.
    
    Args:
        repository: MaturityAgentResponse repository
        command: CreateMaturityAgentResponse command
        
    Returns:
        int: ID of the created maturity agent response
    """
    return await repository.create(command)


async def update_maturity_response(repository: Callable, command: UpdateMaturityAgentResponse) -> bool:
    """Update an existing maturity agent response.
    
    Args:
        repository: MaturityAgentResponse repository
        command: UpdateMaturityAgentResponse command
        
    Returns:
        bool: True if update was successful
    """
    return await repository.update(command)


async def delete_maturity_response(repository: Callable, command: DeleteMaturityAgentResponse) -> bool:
    """Delete a maturity agent response.
    
    Args:
        repository: MaturityAgentResponse repository
        command: DeleteMaturityAgentResponse command
        
    Returns:
        bool: True if deletion was successful
    """
    return await repository.delete(command.maturity_agent_response_id)


async def get_maturity_response(repository: Callable, command: GetMaturityAgentResponse) -> Optional[MaturityAgentResponseData]:
    """Retrieve a maturity agent response by ID or filters.
    
    Args:
        repository: MaturityAgentResponse repository
        command: GetMaturityAgentResponse command
        
    Returns:
        Optional[MaturityAgentResponseData]: Maturity agent response data if found, None otherwise
    """
    return await repository.get(command)


async def list_maturity_responses(
    repository: Callable,
    agent_id: Optional[int] = None,
    maturity_question_id: Optional[int] = None
) -> ListMaturityAgentResponses:
    """List all maturity agent responses, optionally filtered.
    
    Args:
        repository: MaturityAgentResponse repository
        agent_id: Optional agent ID filter
        maturity_question_id: Optional maturity question ID filter
        
    Returns:
        ListMaturityAgentResponses: List of maturity agent responses
    """
    responses = await repository.list_all(agent_id, maturity_question_id)
    return ListMaturityAgentResponses(responses=responses)


def create_maturity_agent_response_handler(repository: Callable) -> dict:
    """Create a dictionary of maturity agent response handler functions.
    
    Args:
        repository: MaturityAgentResponse repository
        
    Returns:
        dict: Dictionary of handler functions
    """
    return {
        'create_maturity_response': partial(create_maturity_response, repository),
        'update_maturity_response': partial(update_maturity_response, repository),
        'delete_maturity_response': partial(delete_maturity_response, repository),
        'get_maturity_response': partial(get_maturity_response, repository),
        'list_maturity_responses': partial(list_maturity_responses, repository),
    }
