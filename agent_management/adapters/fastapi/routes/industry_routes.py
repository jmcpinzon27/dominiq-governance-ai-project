"""FastAPI routes for industry operations."""
from typing import Callable
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.industry_command import (
    CreateIndustry,
    UpdateIndustry,
    DeleteIndustry,
    GetIndustry,
    IndustryResponse,
    ListIndustries
)
from domain.command_handlers.industry_handler import (
    create_industry,
    update_industry,
    delete_industry,
    get_industry,
    list_industries
)
from adapters.postgres.repositories.industry_repository import IndustryRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/industries", tags=["industries"])


async def get_industry_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for industry handler functions.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        dict[str, Callable]: Dictionary containing handler functions for industries
    """
    repository = IndustryRepository(session)
    return {
        'create_industry': lambda cmd: create_industry(repository, cmd),
        'update_industry': lambda cmd: update_industry(repository, cmd),
        'delete_industry': lambda cmd: delete_industry(repository, cmd),
        'get_industry': lambda cmd: get_industry(repository, cmd),
        'list_industries': lambda: list_industries(repository)
    }


@router.post("/", response_model=int, status_code=201)
async def create_industry_endpoint(
    command: CreateIndustry,
    handler: dict[str, Callable] = Depends(get_industry_handler)
):
    """
    Create a new industry.
    
    Args:
        command: CreateIndustry command with industry details
        handler: Industry handler functions
        
    Returns:
        int: ID of the created industry
        
    Raises:
        HTTPException: If industry name already exists
    """
    try:
        return await handler['create_industry'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{industry_id}", response_model=bool)
async def update_industry_endpoint(
    industry_id: int,
    command: UpdateIndustry,
    handler: dict[str, Callable] = Depends(get_industry_handler)
):
    """
    Update an existing industry.
    
    Args:
        industry_id: ID of the industry to update
        command: UpdateIndustry command with updated industry details
        handler: Industry handler functions
        
    Returns:
        bool: True if update was successful
        
    Raises:
        HTTPException: If industry not found or name already exists
    """
    command.industry_id = industry_id
    try:
        result = await handler['update_industry'](command)
        if not result:
            raise HTTPException(status_code=404, detail="Industry not found")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{industry_id}", response_model=bool)
async def delete_industry_endpoint(
    industry_id: int,
    handler: dict[str, Callable] = Depends(get_industry_handler)
):
    """
    Delete an industry.
    
    Args:
        industry_id: ID of the industry to delete
        handler: Industry handler functions
        
    Returns:
        bool: True if deletion was successful
        
    Raises:
        HTTPException: If industry not found
    """
    result = await handler['delete_industry'](DeleteIndustry(industry_id=industry_id))
    if not result:
        raise HTTPException(status_code=404, detail="Industry not found")
    return result


@router.get("/{industry_id}", response_model=IndustryResponse)
async def get_industry_endpoint(
    industry_id: int,
    handler: dict[str, Callable] = Depends(get_industry_handler)
):
    """
    Get an industry by ID.
    
    Args:
        industry_id: ID of the industry to get
        handler: Industry handler functions
        
    Returns:
        IndustryResponse: Industry data
        
    Raises:
        HTTPException: If industry not found
    """
    result = await handler['get_industry'](GetIndustry(industry_id=industry_id))
    if not result:
        raise HTTPException(status_code=404, detail="Industry not found")
    return result


@router.get("/", response_model=ListIndustries)
async def list_industries_endpoint(
    handler: dict[str, Callable] = Depends(get_industry_handler)
):
    """
    List all industries.
    
    Args:
        handler: Industry handler functions
        
    Returns:
        ListIndustries: List of all industries
    """
    return await handler['list_industries']()
