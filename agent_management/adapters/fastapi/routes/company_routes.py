"""FastAPI routes for company operations."""
from typing import Callable
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.company_command import (
    CreateCompany,
    UpdateCompany,
    DeleteCompany,
    GetCompany,
    ListCompanies
)
from domain.command_handlers.company_handler import (
    create_company,
    update_company,
    delete_company,
    get_company,
    list_companies
)
from adapters.postgres.repositories.company_repository import CompanyRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/companies", tags=["companies"])


async def get_company_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for company handler functions.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        dict[str, Callable]: Dictionary containing handler functions for companies
    """
    repository = CompanyRepository(session)
    return {
        'create_company': lambda cmd: create_company(repository, cmd),
        'update_company': lambda cmd: update_company(repository, cmd),
        'delete_company': lambda cmd: delete_company(repository, cmd),
        'get_company': lambda cmd: get_company(repository, cmd),
        'list_companies': lambda: list_companies(repository)
    }


@router.post("/", response_model=int)
async def create_company_route(
    command: CreateCompany,
    handler: dict[str, Callable] = Depends(get_company_handler)
):
    """Create a new company."""
    return await handler['create_company'](command)


@router.put("/{company_id}")
async def update_company_route(
    company_id: int,
    command: UpdateCompany,
    handler: dict[str, Callable] = Depends(get_company_handler)
):
    """Update an existing company."""
    command.company_id = company_id
    if not await handler['update_company'](command):
        raise HTTPException(status_code=404, detail="Company not found")
    return {"status": "success"}


@router.delete("/{company_id}")
async def delete_company_route(
    company_id: int,
    handler: dict[str, Callable] = Depends(get_company_handler)
):
    """Delete a company."""
    if not await handler['delete_company'](DeleteCompany(company_id=company_id)):
        raise HTTPException(status_code=404, detail="Company not found")
    return {"status": "success"}


@router.get("/", response_model=ListCompanies)
async def list_companies_route(
    handler: dict[str, Callable] = Depends(get_company_handler)
):
    """List all companies."""
    return await handler['list_companies']()


@router.get("/{company_id}")
async def get_company_route(
    company_id: int,
    handler: dict[str, Callable] = Depends(get_company_handler)
):
    """Get a company by ID."""
    result = await handler['get_company'](GetCompany(company_id=company_id))
    if not result:
        raise HTTPException(status_code=404, detail="Company not found")
    return result
