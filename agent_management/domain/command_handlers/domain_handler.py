"""Handler for domain-related commands."""
from typing import Optional, Callable
from functools import partial
from domain.command.domain_command import (
    CreateDomain,
    UpdateDomain,
    DeleteDomain,
    GetDomain,
    DomainResponse,
    ListDomains
)


async def create_domain(repository: Callable, command: CreateDomain) -> int:
    """Create a new domain."""
    return await repository.create(command)


async def update_domain(repository: Callable, command: UpdateDomain) -> bool:
    """Update an existing domain."""
    return await repository.update(command)


async def delete_domain(repository: Callable, command: DeleteDomain) -> bool:
    """Delete a domain."""
    return await repository.delete(command.domain_id)


async def get_domain(repository: Callable, command: GetDomain) -> Optional[DomainResponse]:
    """Retrieve a domain by ID or name."""
    return await repository.get(command)


async def list_domains(repository: Callable) -> ListDomains:
    """List all domains."""
    domains = await repository.list_all()
    return ListDomains(domains=domains)


def create_domain_handler(repository: Callable) -> dict:
    """Create a dictionary of domain-related functions with bound repository."""
    return {
        'create_domain': partial(create_domain, repository),
        'update_domain': partial(update_domain, repository),
        'delete_domain': partial(delete_domain, repository),
        'get_domain': partial(get_domain, repository),
        'list_domains': partial(list_domains, repository),
    }
