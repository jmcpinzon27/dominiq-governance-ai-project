"""Handler for user-related commands."""
from typing import Optional, List, Callable
from functools import partial
from domain.command.user_command import (
    CreateUser,
    UpdateUser,
    DeleteUser,
    GetUser,
    UserResponse,
    ListUsers
)


async def create_user(repository: Callable, command: CreateUser) -> int:
    """Create a new user."""
    return await repository.create(command)


async def update_user(repository: Callable, command: UpdateUser) -> bool:
    """Update an existing user."""
    return await repository.update(command)


async def delete_user(repository: Callable, command: DeleteUser) -> bool:
    """Delete a user."""
    return await repository.delete(command.user_id)


async def get_user(repository: Callable, command: GetUser) -> Optional[UserResponse]:
    """Retrieve a user by ID or email."""
    return await repository.get(command)


async def list_users(repository: Callable) -> ListUsers:
    """List all users."""
    users = await repository.list()
    return ListUsers(users=users)


def create_user_handler(repository: Callable) -> dict:
    """Create a dictionary of user handler functions."""
    return {
        'create_user': partial(create_user, repository),
        'update_user': partial(update_user, repository),
        'delete_user': partial(delete_user, repository),
        'get_user': partial(get_user, repository),
        'list_users': partial(list_users, repository),
    }
