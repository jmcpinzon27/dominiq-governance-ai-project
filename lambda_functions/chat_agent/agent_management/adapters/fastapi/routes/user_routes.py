"""FastAPI routes for user operations."""
from typing import Callable
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from domain.command.user_command import (
    CreateUser,
    UpdateUser,
    DeleteUser,
    GetUser,
    UserResponse,
    ListUsers
)
from domain.command_handlers.user_handler import (
    create_user,
    update_user,
    delete_user,
    get_user,
    list_users
)
from adapters.postgres.repositories.user_repository import UserRepository
from adapters.postgres.config import get_session

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_handler(
    session: AsyncSession = Depends(get_session)
) -> dict[str, Callable]:
    """
    Dependency injection for user handler functions.
    
    Args:
        session: AsyncSession from dependency injection
        
    Returns:
        dict[str, Callable]: Dictionary containing handler functions for users
    """
    repository = UserRepository(session)
    return {
        'create_user': lambda cmd: create_user(repository, cmd),
        'update_user': lambda cmd: update_user(repository, cmd),
        'delete_user': lambda cmd: delete_user(repository, cmd),
        'get_user': lambda cmd: get_user(repository, cmd),
        'list_users': lambda: list_users(repository)
    }


@router.post("/", response_model=int)
async def route_create_user(
    command: CreateUser,
    handler: dict[str, Callable] = Depends(get_user_handler)
):
    """Create a new user."""
    try:
        return await handler['create_user'](command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}", response_model=bool)
async def route_update_user(
    user_id: int,
    command: UpdateUser,
    handler: dict[str, Callable] = Depends(get_user_handler)
):
    """Update an existing user."""
    command.user_id = user_id
    try:
        if not await handler['update_user'](command):
            raise HTTPException(status_code=404, detail="User not found")
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", response_model=bool)
async def route_delete_user(
    user_id: int,
    handler: dict[str, Callable] = Depends(get_user_handler)
):
    """Delete a user."""
    if not await handler['delete_user'](DeleteUser(user_id=user_id)):
        raise HTTPException(status_code=404, detail="User not found")
    return True


@router.get("/{user_id}", response_model=UserResponse)
async def route_get_user(
    user_id: int,
    handler: dict[str, Callable] = Depends(get_user_handler)
):
    """Get a user by ID."""
    user = await handler['get_user'](GetUser(user_id=user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=ListUsers)
async def route_list_users(
    handler: dict[str, Callable] = Depends(get_user_handler)
):
    """List all users."""
    return await handler['list_users']()
