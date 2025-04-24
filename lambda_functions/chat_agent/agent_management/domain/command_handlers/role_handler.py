"""Handler for role-related commands."""
from typing import Optional, List, Callable
from functools import partial
from domain.command.role_command import (
    CreateRole,
    UpdateRole,
    DeleteRole,
    GetRole,
    RoleResponse,
    ListRoles
)


async def create_role(repository: Callable, command: CreateRole) -> int:
    """Create a new role."""
    return await repository.create(command)


async def update_role(repository: Callable, command: UpdateRole) -> bool:
    """Update an existing role."""
    return await repository.update(command)


async def delete_role(repository: Callable, command: DeleteRole) -> bool:
    """Delete a role."""
    return await repository.delete(command.role_id)


async def get_role(repository: Callable, command: GetRole) -> Optional[RoleResponse]:
    """Retrieve a role by ID or name."""
    return await repository.get(command)


async def list_roles(repository: Callable) -> ListRoles:
    """List all roles."""
    roles = await repository.list()
    return ListRoles(roles=roles)


def create_role_handler(repository: Callable) -> dict:
    """Create a dictionary of role handler functions."""
    return {
        'create_role': partial(create_role, repository),
        'update_role': partial(update_role, repository),
        'delete_role': partial(delete_role, repository),
        'get_role': partial(get_role, repository),
        'list_roles': partial(list_roles, repository),
    }
