"""Handler for industry-related commands."""
from typing import Optional, List, Callable
from functools import partial

from domain.command.industry_command import (
    CreateIndustry,
    UpdateIndustry,
    DeleteIndustry,
    GetIndustry,
    IndustryResponse,
    ListIndustries
)


async def create_industry(repository: Callable, command: CreateIndustry) -> int:
    """Create a new industry.
    
    Args:
        repository: Industry repository
        command: CreateIndustry command
        
    Returns:
        int: ID of the created industry
    """
    return await repository.create(command)


async def update_industry(repository: Callable, command: UpdateIndustry) -> bool:
    """Update an existing industry.
    
    Args:
        repository: Industry repository
        command: UpdateIndustry command
        
    Returns:
        bool: True if update was successful
    """
    return await repository.update(command)


async def delete_industry(repository: Callable, command: DeleteIndustry) -> bool:
    """Delete an industry.
    
    Args:
        repository: Industry repository
        command: DeleteIndustry command
        
    Returns:
        bool: True if deletion was successful
    """
    return await repository.delete(command.industry_id)


async def get_industry(repository: Callable, command: GetIndustry) -> Optional[IndustryResponse]:
    """Get an industry by ID.
    
    Args:
        repository: Industry repository
        command: GetIndustry command
        
    Returns:
        Optional[IndustryResponse]: Industry data if found, None otherwise
    """
    return await repository.get_by_id(command.industry_id)


async def list_industries(repository: Callable) -> ListIndustries:
    """List all industries.
    
    Args:
        repository: Industry repository
        
    Returns:
        ListIndustries: List of all industries
    """
    industries = await repository.get_all()
    return ListIndustries(industries=industries)
