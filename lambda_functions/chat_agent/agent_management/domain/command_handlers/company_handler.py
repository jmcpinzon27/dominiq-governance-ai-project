"""Company command handlers."""
from typing import Optional, Callable
from functools import partial
from domain.command.company_command import (
    CreateCompany,
    UpdateCompany,
    DeleteCompany,
    GetCompany,
    ListCompanies
)


async def create_company(repository: Callable, command: CreateCompany) -> int:
    """Create a new company."""
    return await repository.create(command)


async def update_company(repository: Callable, command: UpdateCompany) -> bool:
    """Update an existing company."""
    return await repository.update(command)


async def delete_company(repository: Callable, command: DeleteCompany) -> bool:
    """Delete a company."""
    return await repository.delete(command.company_id)


async def get_company(repository: Callable, command: GetCompany) -> Optional[dict]:
    """Retrieve a company by ID or name."""
    return await repository.get(command)


async def list_companies(repository: Callable) -> ListCompanies:
    """List all companies."""
    return await repository.list_all()


def create_company_handler(repository: Callable) -> dict:
    """Create a dictionary of company-related functions with repository dependency."""
    return {
        'create_company': partial(create_company, repository),
        'update_company': partial(update_company, repository),
        'delete_company': partial(delete_company, repository),
        'get_company': partial(get_company, repository),
        'list_companies': partial(list_companies, repository)
    }
