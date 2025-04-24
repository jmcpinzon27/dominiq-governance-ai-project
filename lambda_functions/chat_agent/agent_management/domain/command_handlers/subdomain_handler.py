"""Handler for subdomain-related commands."""
from typing import Optional, List, Callable
from functools import partial
from domain.command.subdomain_command import (
    CreateSubdomain,
    UpdateSubdomain,
    DeleteSubdomain,
    GetSubdomain,
    SubdomainResponse,
    ListSubdomains
)


async def create_subdomain(repository: Callable, command: CreateSubdomain) -> int:
    """Create a new subdomain."""
    return await repository.create(command)


async def update_subdomain(repository: Callable, command: UpdateSubdomain) -> bool:
    """Update an existing subdomain."""
    return await repository.update(command)


async def delete_subdomain(repository: Callable, command: DeleteSubdomain) -> bool:
    """Delete a subdomain."""
    return await repository.delete(command.subdomain_id)


async def get_subdomain(repository: Callable, command: GetSubdomain) -> Optional[SubdomainResponse]:
    """Retrieve a subdomain by ID, name, or domain_id."""
    return await repository.get(command)


async def list_subdomains(repository: Callable, domain_id: Optional[int] = None) -> ListSubdomains:
    """List all subdomains, optionally filtered by domain_id."""
    subdomains = await repository.list_all(domain_id)
    return ListSubdomains(subdomains=subdomains)


def create_subdomain_handler(repository: Callable) -> dict:
    """Create a dictionary of subdomain-related functions with bound repository."""
    return {
        'create_subdomain': partial(create_subdomain, repository),
        'update_subdomain': partial(update_subdomain, repository),
        'delete_subdomain': partial(delete_subdomain, repository),
        'get_subdomain': partial(get_subdomain, repository),
        'list_subdomains': partial(list_subdomains, repository),
    }
