"""Handler for domain agent response-related commands."""
from typing import Optional, List, Callable
from functools import partial
from domain.command.domain_agent_response_command import (
    CreateDomainAgentResponse,
    UpdateDomainAgentResponse,
    DeleteDomainAgentResponse,
    GetDomainAgentResponse,
    DomainAgentResponseData,
    ListDomainAgentResponses
)


async def create_domain_response(repository: Callable, command: CreateDomainAgentResponse) -> int:
    """Create a new domain agent response.
    
    Args:
        repository: DomainAgentResponse repository
        command: CreateDomainAgentResponse command
        
    Returns:
        int: ID of the created domain agent response
    """
    return await repository.create(command)


async def update_domain_response(repository: Callable, command: UpdateDomainAgentResponse) -> bool:
    """Update an existing domain agent response.
    
    Args:
        repository: DomainAgentResponse repository
        command: UpdateDomainAgentResponse command
        
    Returns:
        bool: True if update was successful
    """
    return await repository.update(command)


async def delete_domain_response(repository: Callable, command: DeleteDomainAgentResponse) -> bool:
    """Delete a domain agent response.
    
    Args:
        repository: DomainAgentResponse repository
        command: DeleteDomainAgentResponse command
        
    Returns:
        bool: True if deletion was successful
    """
    return await repository.delete(command.domain_agent_response_id)


async def get_domain_response(repository: Callable, command: GetDomainAgentResponse) -> Optional[DomainAgentResponseData]:
    """Retrieve a domain agent response by ID or filters.
    
    Args:
        repository: DomainAgentResponse repository
        command: GetDomainAgentResponse command
        
    Returns:
        Optional[DomainAgentResponseData]: Domain agent response data if found, None otherwise
    """
    return await repository.get(command)


async def list_domain_responses(
    repository: Callable,
    agent_id: Optional[int] = None,
    domain_question_id: Optional[int] = None
) -> ListDomainAgentResponses:
    """List all domain agent responses, optionally filtered.
    
    Args:
        repository: DomainAgentResponse repository
        agent_id: Optional agent ID filter
        domain_question_id: Optional domain question ID filter
        
    Returns:
        ListDomainAgentResponses: List of domain agent responses
    """
    responses = await repository.list_all(agent_id, domain_question_id)
    return ListDomainAgentResponses(responses=responses)


def create_domain_agent_response_handler(repository: Callable) -> dict:
    """Create a dictionary of domain agent response handler functions.
    
    Args:
        repository: DomainAgentResponse repository
        
    Returns:
        dict: Dictionary of handler functions
    """
    return {
        'create_domain_response': partial(create_domain_response, repository),
        'update_domain_response': partial(update_domain_response, repository),
        'delete_domain_response': partial(delete_domain_response, repository),
        'get_domain_response': partial(get_domain_response, repository),
        'list_domain_responses': partial(list_domain_responses, repository),
    }
