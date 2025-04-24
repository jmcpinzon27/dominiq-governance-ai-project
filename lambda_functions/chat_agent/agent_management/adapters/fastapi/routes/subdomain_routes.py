"""FastAPI routes for subdomain operations."""
from typing import Callable, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.subdomain_command import (
    CreateSubdomain,
    UpdateSubdomain,
    DeleteSubdomain,
    GetSubdomain,
    SubdomainResponse,
    ListSubdomains
)
from domain.command_handlers.subdomain_handler import (
    create_subdomain,
    update_subdomain,
    delete_subdomain,
    get_subdomain,
    list_subdomains
)
from adapters.postgres.repositories.subdomain_repository import SubdomainRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/subdomains", tags=["subdomains"])


async def get_subdomain_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for subdomain handler functions.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        dict[str, Callable]: Dictionary containing handler functions for subdomains
    """
    repository = SubdomainRepository(session)
    return {
        'create_subdomain': lambda cmd: create_subdomain(repository, cmd),
        'update_subdomain': lambda cmd: update_subdomain(repository, cmd),
        'delete_subdomain': lambda cmd: delete_subdomain(repository, cmd),
        'get_subdomain': lambda cmd: get_subdomain(repository, cmd),
        'list_subdomains': lambda domain_id: list_subdomains(repository, domain_id)
    }


@router.post("/", response_model=int)
async def create_subdomain_route(
    command: CreateSubdomain,
    handler: dict[str, Callable] = Depends(get_subdomain_handler)
):
    """Create a new subdomain."""
    try:
        return await handler['create_subdomain'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{subdomain_id}", response_model=bool)
async def update_subdomain_route(
    subdomain_id: int,
    command: UpdateSubdomain,
    handler: dict[str, Callable] = Depends(get_subdomain_handler)
):
    """Update an existing subdomain."""
    command.subdomain_id = subdomain_id
    try:
        if not await handler['update_subdomain'](command):
            raise HTTPException(status_code=404, detail="Subdomain not found")
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{subdomain_id}", response_model=bool)
async def delete_subdomain_route(
    subdomain_id: int,
    handler: dict[str, Callable] = Depends(get_subdomain_handler)
):
    """Delete a subdomain."""
    command = DeleteSubdomain(subdomain_id=subdomain_id)
    if not await handler['delete_subdomain'](command):
        raise HTTPException(status_code=404, detail="Subdomain not found")
    return True


@router.get("/{subdomain_id}", response_model=SubdomainResponse)
async def get_subdomain_route(
    subdomain_id: int,
    handler: dict[str, Callable] = Depends(get_subdomain_handler)
):
    """Get a subdomain by ID."""
    command = GetSubdomain(subdomain_id=subdomain_id)
    subdomain = await handler['get_subdomain'](command)
    if not subdomain:
        raise HTTPException(status_code=404, detail="Subdomain not found")
    return subdomain


@router.get("/", response_model=ListSubdomains)
async def list_subdomains_route(
    domain_id: Optional[int] = Query(None, gt=0),
    handler: dict[str, Callable] = Depends(get_subdomain_handler)
):
    """List all subdomains, optionally filtered by domain_id."""
    return await handler['list_subdomains'](domain_id)
