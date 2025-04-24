"""FastAPI routes for role operations."""
from typing import Callable
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.role_command import (
    CreateRole,
    UpdateRole,
    DeleteRole,
    GetRole,
    RoleResponse,
    ListRoles
)
from domain.command_handlers.role_handler import (
    create_role,
    update_role,
    delete_role,
    get_role,
    list_roles
)
from adapters.postgres.repositories.role_repository import RoleRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/roles", tags=["roles"])


async def get_role_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for role handler functions.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        dict[str, Callable]: Dictionary containing handler functions for roles
    """
    repository = RoleRepository(session)
    return {
        'create_role': lambda cmd: create_role(repository, cmd),
        'update_role': lambda cmd: update_role(repository, cmd),
        'delete_role': lambda cmd: delete_role(repository, cmd),
        'get_role': lambda cmd: get_role(repository, cmd),
        'list_roles': lambda: list_roles(repository)
    }


@router.post("/", response_model=int)
async def create_role_route(
    command: CreateRole,
    handler: dict[str, Callable] = Depends(get_role_handler)
):
    """Create a new role."""
    try:
        return await handler['create_role'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{role_id}", response_model=bool)
async def update_role_route(
    role_id: int,
    command: UpdateRole,
    handler: dict[str, Callable] = Depends(get_role_handler)
):
    """Update an existing role."""
    command.role_id = role_id
    try:
        if not await handler['update_role'](command):
            raise HTTPException(status_code=404, detail="Role not found")
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{role_id}", response_model=bool)
async def delete_role_route(
    role_id: int,
    handler: dict[str, Callable] = Depends(get_role_handler)
):
    """Delete a role."""
    command = DeleteRole(role_id=role_id)
    if not await handler['delete_role'](command):
        raise HTTPException(status_code=404, detail="Role not found")
    return True


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role_route(
    role_id: int,
    handler: dict[str, Callable] = Depends(get_role_handler)
):
    """Get a role by ID."""
    command = GetRole(role_id=role_id)
    role = await handler['get_role'](command)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.get("/", response_model=ListRoles)
async def list_roles_route(
    handler: dict[str, Callable] = Depends(get_role_handler)
):
    """List all roles."""
    return await handler['list_roles']()
