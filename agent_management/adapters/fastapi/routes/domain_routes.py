"""FastAPI routes for domain operations."""
from typing import Callable
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.domain_command import (
    CreateDomain,
    UpdateDomain,
    DeleteDomain,
    GetDomain,
    DomainResponse,
    ListDomains
)
from domain.command_handlers.domain_handler import (
    create_domain,
    update_domain,
    delete_domain,
    get_domain,
    list_domains
)
from adapters.postgres.repositories.domain_repository import DomainRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/domains", tags=["domains"])


async def get_domain_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for domain handler functions.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        dict[str, Callable]: Dictionary containing handler functions for domains
    """
    repository = DomainRepository(session)
    return {
        'create_domain': lambda cmd: create_domain(repository, cmd),
        'update_domain': lambda cmd: update_domain(repository, cmd),
        'delete_domain': lambda cmd: delete_domain(repository, cmd),
        'get_domain': lambda cmd: get_domain(repository, cmd),
        'list_domains': lambda: list_domains(repository)
    }


@router.post("/", response_model=int)
async def create_domain(
    command: CreateDomain,
    handler: dict[str, Callable] = Depends(get_domain_handler)
):
    """Create a new domain."""
    try:
        return await handler['create_domain'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{domain_id}", response_model=bool)
async def update_domain(
    domain_id: int,
    command: UpdateDomain,
    handler: dict[str, Callable] = Depends(get_domain_handler)
):
    """Update an existing domain."""
    command.domain_id = domain_id
    try:
        if not await handler['update_domain'](command):
            raise HTTPException(status_code=404, detail="Domain not found")
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{domain_id}", response_model=bool)
async def delete_domain(
    domain_id: int,
    handler: dict[str, Callable] = Depends(get_domain_handler)
):
    """Delete a domain."""
    if not await handler['delete_domain'](DeleteDomain(domain_id=domain_id)):
        raise HTTPException(status_code=404, detail="Domain not found")
    return True


@router.get("/{domain_id}", response_model=DomainResponse)
async def get_domain_route(
    domain_id: int,
    handler: dict[str, Callable] = Depends(get_domain_handler)
):
    """Get a domain by ID."""
    domain = await handler['get_domain'](GetDomain(domain_id=domain_id))
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    return domain


@router.get("/", response_model=ListDomains)
async def list_domains_route(
    handler: dict[str, Callable] = Depends(get_domain_handler)
):
    """List all domains."""
    return await handler['list_domains']()
